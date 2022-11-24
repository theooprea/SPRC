#include <stdio.h>
#include <time.h>
#include <rpc/rpc.h>

#include <iostream>
#include <algorithm>
#include <vector>
#include <string>

#include "oauth.h"
#include "oauth_svc.h"
#include "helpers.h"
#include "token.h"

/* the user DB, the resources DB, the approvals file from which the end-user
 * will approve/deny requests, and the availability of a newly generated token
 */
std::vector<user> user_db;
std::vector<std::string> resources;
FILE *approvals_file;
int token_availability;

/**
 * @brief Server function that handles the authorisation request
 *
 * @param request The body of the request, containing the username and whether the
 * token has to be automatically generated
 * @param cl The client
 * @return request_auth_response* The response of the server, containing the auth
 * token and the return code
 */
request_auth_response *request_auth_1_svc(request_auth_request *request, struct svc_req *cl) {
    static request_auth_response response;
	user *user_found = NULL;

	printf("BEGIN %s AUTHZ\n", request->user_id);

	/* try to find the username in the database */
	for (auto &it : user_db) {
		if (!strcmp(it.username, request->user_id)) {
			user_found = &it;
			break;
		}
	}

	/* if the user was found */
	if (user_found != NULL) {
		/* set the response code, generate a token based on the user id, and set
		 * a flag in the DB for token auto renewal
		 */
		response.response_code = USER_FOUND;
    	response.auth_token = generate_access_token(request->user_id);
		user_found->auth_token = (char *)malloc((strlen(response.auth_token) + 1) * sizeof(char));
		user_found->auto_renew = request->auto_renew == 1 ? true : false;

		if (!user_found->auto_renew) {
			user_found->renew_token = NULL;
		}

		/* save the token in the database */
		strcpy(user_found->auth_token, response.auth_token);

		printf("  RequestToken = %s\n", response.auth_token);
	}
	/* if the user was not found */
	else {
		/* set response code and an empty token */
		response.response_code = USER_NOT_FOUND;
    	response.auth_token = generate_empty_string();
	}

	return &response;
}

/**
 * @brief Server function that generates the access token for a user, if the request
 * has been approved
 *
 * @param request The body of the request, containing the auth token
 * @param cl The client
 * @return request_access_response* The response of the server, containing the access token,
 * and if the user has opted for token auto renewal, a refresh token
 */
request_access_response *request_access_1_svc(request_access_request *request, struct svc_req *cl) {
    static request_access_response response;
	user *user_found = NULL;

	/* try to find the user whose auth token matches the auth token in the request,
	 * and check if the auth token has been marked as approved
	 */
	for (auto &it : user_db) {
		if (it.auth_token && it.permissions.size() != 0 && !strcmp(it.auth_token, request->auth_token)) {
			user_found = &it;
			break;
		}
	}

	/* if the user was not found */
	if (!user_found) {
		/* return the token as it is and deny the request */
		response.access_token = (char *)malloc((strlen(request->auth_token) + 1) * sizeof(char));

		strcpy(response.access_token, request->auth_token);
		response.response_code = REQUEST_DENIED;
	}
	/* if the user was found */
	else {
		/* generate an access token and save it in the DB*/
		response.access_token = generate_access_token(request->auth_token);
		user_found->access_token = (char *)malloc((strlen(response.access_token) + 1) * sizeof(char));
		strcpy(user_found->access_token, response.access_token);
		user_found->available_actions = token_availability;
		response.response_code = REQUEST_APPROVED;

		printf("  AccessToken = %s\n", response.access_token);

		/* if the user opted for auto renewal, generate a refresh token */
		if (user_found->auto_renew) {
			response.renew_token = generate_access_token(response.access_token);
			user_found->renew_token = (char *)malloc((strlen(response.renew_token) + 1) * sizeof(char));
			strcpy(user_found->renew_token, response.renew_token);

			printf("  RefreshToken = %s\n", response.renew_token);
		}
		else {
			response.renew_token = (char *)malloc(sizeof(char));
			response.renew_token[0] = '\0';
		}
	}

	return &response;
}

/**
 * @brief Server function that marks a request as approved or denied
 *
 * @param request The body of the request, containing the auth token
 * @param cl The client
 * @return approve_request_token_response* The response of the server, containing the auth_token,
 * and the response code
 */
approve_request_token_response *approve_request_token_1_svc(approve_request_token_request *request, struct svc_req *cl) {
	static approve_request_token_response response;
	user *user_found = NULL;
	char buffer[1024], *p, *r;
	permission permission_aux;

	/* try to find the user */
	for (auto &it : user_db) {
		if (it.auth_token != NULL && !strcmp(it.auth_token, request->auth_token)) {
			user_found = &it;
			break;
		}
	}

	/* clear the permisions of the "possibly" already existing token*/
	user_found->permissions.clear();

	r = fgets(buffer, 1024, approvals_file);
	if (buffer[strlen(buffer) - 1] == '\n') {
		buffer[strlen(buffer) - 1] = '\0';
	}

	if (!strcmp(buffer, "*,-") || !r) {
		response.auth_token = (char *)malloc((strlen(request->auth_token) + 1) * sizeof(char));
		strcpy(response.auth_token, request->auth_token);
		response.response_code = DENIED;
	}
	else {
		p = strtok(buffer, ",");

		while (p != NULL) {
			permission_aux.resource = (char *)malloc((strlen(p) + 1) * sizeof(char));
			strcpy(permission_aux.resource, p);
			p = strtok(NULL, ",");
			strcpy(permission_aux.permissions, p);

			user_found->permissions.push_back(permission_aux);

			p = strtok(NULL, ",");
		}

		response.auth_token = (char *)malloc((strlen(request->auth_token) + 1) * sizeof(char));
		strcpy(response.auth_token, request->auth_token);
		response.response_code = APPROVED;
	}

	return &response;
}

bool check_permission(char *permissions, char *op_type) {
	char search;

	if (strcmp(op_type, "READ") && strcmp(op_type, "INSERT") &&
		strcmp(op_type, "MODIFY") && strcmp(op_type, "DELETE") &&
		strcmp(op_type, "EXECUTE")) {
		return false;
	}
	
	switch (op_type[0])
	{
	case 'R':
		search = 'R';
		break;
	case 'I':
		search = 'I';
		break;
	case 'M':
		search = 'M';
		break;
	case 'D':
		search = 'D';
		break;
	case 'E':
		search = 'X';
		break;
	default:
		break;
	}

	return strchr(permissions, search);
}

validate_delegated_action_response *validate_delegated_action_1_svc(validate_delegated_action_request *request, struct svc_req *cl) {
	static validate_delegated_action_response response;
	user *user_found = NULL;

	for (auto &it : user_db) {
		if (it.access_token != NULL && !strcmp(it.access_token, request->access_token)) {
			user_found = &it;
			break;
		}
	}

	if (!user_found) {
		response.response_code = PERMISSION_DENIED;
		printf("DENY (%s,%s,,0)\n", request->op_type, request->resource);
	}
	else {
		if (user_found->available_actions == 0) {
			response.response_code = TOKEN_EXPIRED;
			if (!user_found->auto_renew) {
				printf("DENY (%s,%s,,0)\n", request->op_type, request->resource);
			}
		}
		else {
			if (std::find(resources.begin(), resources.end(), request->resource) == resources.end()) {
				user_found->available_actions--;
				response.response_code = RESOURCE_NOT_FOUND;
				printf("DENY (%s,%s,%s,%d)\n", request->op_type, request->resource, user_found->access_token, user_found->available_actions);
			}
			else {
				permission *permission_found = NULL;

				for (auto &it : user_found->permissions) {
					if (!strcmp(it.resource, request->resource)) {
						permission_found = &it;
					}
				}

				user_found->available_actions--;

				if (!permission_found || !check_permission(permission_found->permissions, request->op_type)) {
					response.response_code = OPERATION_NOT_PERMITTED;
					printf("DENY (%s,%s,%s,%d)\n", request->op_type, request->resource, user_found->access_token, user_found->available_actions);
				}
				else {
					response.response_code = PERMISSION_GRANTED;
					printf("PERMIT (%s,%s,%s,%d)\n", request->op_type, request->resource, user_found->access_token, user_found->available_actions);
				}				
			}
		}
	}

	return &response;
}

renew_token_response *renew_token_1_svc(renew_token_request *request,  struct svc_req *cl) {
	static renew_token_response response;
	user *user_found = NULL;

	for (auto &it : user_db) {
		if (it.renew_token != NULL && !strcmp(it.renew_token, request->renew_token)) {
			user_found = &it;
			break;
		}
	}

	printf("BEGIN %s AUTHZ REFRESH\n", user_found->username);

	response.access_token = generate_access_token(request->renew_token);
	user_found->access_token = (char *)malloc((strlen(response.access_token) + 1) * sizeof(char));
	strcpy(user_found->access_token, response.access_token);

	user_found->available_actions = token_availability;
	printf("  AccessToken = %s\n", response.access_token);

	response.renew_token = generate_access_token(response.access_token);
	user_found->renew_token = (char *)malloc((strlen(response.renew_token) + 1) * sizeof(char));
	strcpy(user_found->renew_token, response.renew_token);

	printf("  RefreshToken = %s\n", response.renew_token);

	return &response;
}

int main (int argc, char **argv)
{
	register SVCXPRT *transp;
	int i, nr_clients, nr_resources;
	FILE *clients_file, *resources_file;
	char buffer[256];

	pmap_unset (SERVER, SERVERVERSION);

	transp = svcudp_create(RPC_ANYSOCK);
	if (transp == NULL) {
		fprintf (stderr, "%s", "cannot create udp service.");
		exit(1);
	}
	if (!svc_register(transp, SERVER, SERVERVERSION, server_1, IPPROTO_UDP)) {
		fprintf (stderr, "%s", "unable to register (SERVER, SERVERVERSION, udp).");
		exit(1);
	}

	transp = svctcp_create(RPC_ANYSOCK, 0, 0);
	if (transp == NULL) {
		fprintf (stderr, "%s", "cannot create tcp service.");
		exit(1);
	}
	if (!svc_register(transp, SERVER, SERVERVERSION, server_1, IPPROTO_TCP)) {
		fprintf (stderr, "%s", "unable to register (SERVER, SERVERVERSION, tcp).");
		exit(1);
	}

	/* verify the number of arguments */
	if (argc != 5) {
		fprintf (stderr, "%s", "Wrong number of arguments. Usage: ");
		fprintf (stderr, "%s", "./server <clients_file> <resource_file> <approvals_file> <token availability>\n");
		exit(1);
	}

	/* populate the user DB */
	clients_file = fopen(argv[1], "r");

	/* if the provided file does not exist */
	if (!clients_file) {
		printf("No clients file found: %s\n", argv[2]);
		exit(1);
	}

	/* get the number of clients from the first line of the file, then populate the DB*/
	fscanf(clients_file, "%d\n", &nr_clients);
	for (i = 0; i < nr_clients; i++) {
		fgets(buffer, 256, clients_file);
		if (buffer[strlen(buffer) - 1] == '\n') {
			buffer[strlen(buffer) - 1] = '\0';
		}

		/* add a new user */
		user_db.push_back(user());

		/* save it's username */
		user_db[i].username = (char *)malloc((strlen(buffer) + 1) * sizeof(char));
		strcpy(user_db[i].username, buffer);

		/* initialise all other data */
		user_db[i].auth_token = NULL;
		user_db[i].access_token = NULL;
		user_db[i].renew_token = NULL;
		user_db[i].available_actions = 0;
		user_db[i].auto_renew = false;

		user_db[i].permissions.clear();
	}

	/* read available resources */
	resources_file = fopen(argv[2], "r");

	/* if the provided file does not exist */
	if (!resources_file) {
		printf("No resource file found: %s\n", argv[2]);
		exit(1);
	}

	/* get the number of resources from the first line of the file, then populate the resources DB*/
	fscanf(resources_file, "%d\n", &nr_resources);
	for (i = 0; i < nr_resources; i++) {
		fgets(buffer, 256, resources_file);
		if (buffer[strlen(buffer) - 1] == '\n') {
			buffer[strlen(buffer) - 1] = '\0';
		}

		resources.push_back(std::string(buffer));
	}

	/* open approvals file */
	approvals_file = fopen(argv[3], "r");

	/* if the provided file does not exist */
	if (!approvals_file) {
		printf("No approvals file found: %s\n", argv[3]);
		exit(1);
	}

	/* token availability */
	token_availability = atoi(argv[4]);

	svc_run ();
	fprintf (stderr, "%s", "svc_run returned");
	exit (1);
	/* NOTREACHED */
}

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

std::vector<user> user_db;
std::vector<std::string> resources;
FILE *approvals_file;
int token_availability;

request_auth_response *request_auth_1_svc(request_auth_request *request, struct svc_req *cl) {
    static request_auth_response response;
	user *user_found = NULL;

	printf("BEGIN %s AUTHZ\n", request->user_id);

	for (auto &it : user_db) {
		if (!strcmp(it.username, request->user_id)) {
			user_found = &it;
		}
	}

	if (user_found != NULL) {
		response.response_code = USER_FOUND;
    	response.auth_token = generate_access_token(request->user_id);
		user_found->auth_token = (char *)malloc((strlen(response.auth_token) + 1) * sizeof(char));
		user_found->auto_renew = request->auto_renew == 1 ? true : false;
		strcpy(user_found->auth_token, response.auth_token);
		printf("  RequestToken = %s\n", response.auth_token);
	}
	else {
		response.response_code = USER_NOT_FOUND;
    	response.auth_token = generate_empty_string();
	}

	return &response;
}

request_access_response *request_access_1_svc(request_access_request *request, struct svc_req *cl) {
    static request_access_response response;
	user *user_found = NULL;

	for (auto &it : user_db) {
		if (it.auth_token && it.permissions.size() != 0 && !strcmp(it.auth_token, request->auth_token)) {
			user_found = &it;
		}
	}

	if (!user_found) {
		response.access_token = (char *)malloc((strlen(request->auth_token) + 1) * sizeof(char));

		strcpy(response.access_token, request->auth_token);
		response.response_code = REQUEST_DENIED;
	}
	else {
		response.access_token = generate_access_token(request->auth_token);
		user_found->access_token = (char *)malloc((strlen(response.access_token) + 1) * sizeof(char));
		strcpy(user_found->access_token, response.access_token);
		user_found->available_actions = token_availability;
		response.response_code = REQUEST_APPROVED;

		if (user_found->auto_renew) {
			response.renew_token = generate_access_token(response.access_token);
		}
		else {
			response.renew_token = (char *)malloc(sizeof(char));
			response.renew_token[0] = '\0';
		}

		printf("  AccessToken = %s\n", response.access_token);
	}

	return &response;
}

approve_request_token_response *approve_request_token_1_svc(approve_request_token_request *request, struct svc_req *cl) {
	static approve_request_token_response response;
	user *user_found = NULL;
	char buffer[1024], *p, *r;
	permission permission_aux;

	for (auto &it : user_db) {
		if (it.auth_token != NULL && !strcmp(it.auth_token, request->auth_token)) {
			user_found = &it;
		}
	}

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
		}
	}

	if (!user_found) {
		response.response_code = PERMISSION_DENIED;
	}
	else {
		if (user_found->available_actions == 0) {
			response.response_code = TOKEN_EXPIRED;
		}
		else {
			if (std::find(resources.begin(), resources.end(), request->resource) == resources.end()) {
				response.response_code = RESOURCE_NOT_FOUND;
			}
			else {
				permission *permission_found = NULL;

				for (auto &it : user_found->permissions) {
					if (!strcmp(it.resource, request->resource)) {
						permission_found = &it;
					}
				}

				if (!permission_found || !check_permission(permission_found->permissions, request->op_type)) {
					response.response_code = OPERATION_NOT_PERMITTED;
				}
				else {
					response.response_code = PERMISSION_GRANTED;
				}
				
				user_found->available_actions = user_found->available_actions - 1;
			}
		}
	}

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

	/* verify arguments */
	if (argc != 5) {
		fprintf (stderr, "%s", "Wrong number of arguments. Usage: ");
		fprintf (stderr, "%s", "./server <clients_file> <resource_file> <approvals_file> <token availability>\n");
		exit(1);
	}

	/* populate user DB */
	clients_file = fopen(argv[1], "r");
	
	if (!clients_file) {
		printf("No clients file found: %s\n", argv[2]);
		exit(1);
	}

	fscanf(clients_file, "%d\n", &nr_clients);
	for (i = 0; i < nr_clients; i++) {
		fgets(buffer, 256, clients_file);
		if (buffer[strlen(buffer) - 1] == '\n') {
			buffer[strlen(buffer) - 1] = '\0';
		}

		user_db.push_back(user());

		user_db[i].username = (char *)malloc((strlen(buffer) + 1) * sizeof(char));
		strcpy(user_db[i].username, buffer);

		user_db[i].auth_token = NULL;
		user_db[i].access_token = NULL;
		user_db[i].renew_token = NULL;
		user_db[i].available_actions = 0;
		user_db[i].auto_renew = false;

		user_db[i].permissions.clear();
	}

	/* read available resources */
	resources_file = fopen(argv[2], "r");

	if (!resources_file) {
		printf("No resource file found: %s\n", argv[2]);
		exit(1);
	}

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

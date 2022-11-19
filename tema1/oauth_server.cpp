#include <stdio.h>
#include <time.h>
#include <rpc/rpc.h>

#include <iostream>
#include <vector>

#include "oauth.h"
#include "oauth_svc.h"
#include "helpers.h"
#include "token.h"

std::vector<user> user_db;
FILE *approvals;

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

	printf("SERVER:\n");

	for (auto &it : user_db) {
		printf("%s %ld\n", it.username, it.permissions.size());
	}

	for (auto &it : user_db) {
		if (!strcmp(it.auth_token, request->auth_token)) {
			user_found = &it;
		}
	}

	response.access_token = (char *)malloc((strlen("salut") + 1) * sizeof(char));

	strcpy(response.access_token, "salut");
	response.response_code = REQUEST_DENIED;

	return &response;
}

approve_request_token_response *approve_request_token_1_svc(approve_request_token_request *request, struct svc_req *cl) {
	static approve_request_token_response response;
	user *user_found = NULL;
	char buffer[1024], *p;
	permission permission_aux;

	for (auto &it : user_db) {
		if (it.auth_token != NULL && !strcmp(it.auth_token, request->auth_token)) {
			user_found = &it;
		}
	}

	user_found->permissions.clear();

	fgets(buffer, 1024, approvals);
	if (buffer[strlen(buffer) - 1] == '\n') {
		buffer[strlen(buffer) - 1] = '\0';
	}

	if (!strcmp(buffer, "*,-")) {
		response.auth_token = (char *)malloc((strlen(request->auth_token) + 1) * sizeof(char));
		strcpy(response.auth_token, request->auth_token);
		response.approved = DENIED;
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
		response.approved = APPROVED;
	}

	return &response;
}

int main (int argc, char **argv)
{
	register SVCXPRT *transp;
	int i, nr_clients;
	FILE *clients_file;
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
	if (argc != 4) {
		fprintf (stderr, "%s", "Wrong number of arguments. Usage: ");
		fprintf (stderr, "%s", "./server <clients_file> <resource_file> <approvals_file> <token availability>\n");
		exit(1);
	}

	/* populate user DB */
	clients_file = fopen(argv[1], "r");
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
	}

	for (auto &it : user_db) {
		it.permissions.clear();
	}

	/* open approvals file */
	approvals = fopen(argv[3], "r");

	svc_run ();
	fprintf (stderr, "%s", "svc_run returned");
	exit (1);
	/* NOTREACHED */
}

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

request_auth_response *request_auth_1_svc(char **user_id, struct svc_req *cl) {
    static request_auth_response response;
	user *user_found = NULL;

	for (auto &it : user_db) {
		if (!strcmp(it.username, *user_id)) {
			user_found = &it;
		}
	}

	if (user_found != NULL) {
		response.response_code = USER_FOUND;
    	response.auth_token = generate_access_token(*user_id);
	}
	else {
		response.response_code = USER_NOT_FOUND;
    	response.auth_token = NULL;
	}

	return &response;
}

request_access_response *request_access_1_svc(request_access_request *request, struct svc_req *cl) {
    static request_access_response response;

	return &response;
}

int main (int argc, char **argv)
{
	register SVCXPRT *transp;
	int i, nr_clients;
	FILE *clients_file;
	char buffer[256];
	user user_aux;

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
	if (argc != 2) {
		fprintf (stderr, "%s", "Wrong number of arguments. Usage: ");
		fprintf (stderr, "%s", "./server <clients_file> <resource_file> <approvals_file> <token availability>\n");
		exit(1);
	}

	/* populate user DB */
	clients_file = fopen(argv[1], "r");
	fscanf(clients_file, "%d\n", &nr_clients);
	for (i = 0; i < nr_clients; i++) {
		fgets(buffer, 256, clients_file);
		buffer[strlen(buffer) - 1] = '\0';

		user_aux.username = (char *)malloc((strlen(buffer) + 1) * sizeof(char));
		strcpy(user_aux.username, buffer);
		user_aux.auth_token = NULL;

		user_db.push_back(user_aux);
	}

	for (auto &it : user_db) {
		printf("SERVER %s\n", it.username);
	}

	svc_run ();
	fprintf (stderr, "%s", "svc_run returned");
	exit (1);
	/* NOTREACHED */
}

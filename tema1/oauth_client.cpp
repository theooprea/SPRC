#include <stdio.h>
#include <time.h>
#include <rpc/rpc.h>

#include <iostream>

#include "oauth.h"
#include "helpers.h"

#define RMACHINE "localhost"

int main(int argc, char **argv) {
    /* variabila clientului */
	CLIENT *handle;
	char buffer[256], *user_id, *action_type, *action_value;
	request_auth_response *request_auth_resp;
	request_auth_request request_auth_req;
	approve_request_token_response *approve_request_token_resp;
	approve_request_token_request approve_request_token_req;
	request_access_response *request_access_resp;
	request_access_request request_access_req;
	FILE *client_actions;

	handle=clnt_create(
		RMACHINE,		/* numele masinii unde se afla server-ul */
		SERVER,		    /* numele programului disponibil pe server */
	    SERVERVERSION,	/* versiunea programului */
		"tcp");			/* tipul conexiunii client-server */
	
	if(handle == NULL) {
		perror("");
		return -1;
	}

	if (argc != 2) {
		fprintf (stderr, "%s", "Wrong number of arguments. Usage: ");
		fprintf (stderr, "%s", "./client <ops_file>\n");
		exit(1);
	}

    client_actions = fopen(argv[1], "r");

	while (fgets(buffer, 256, client_actions)) {
		if (buffer[strlen(buffer) - 1] == '\n') {
			buffer[strlen(buffer) - 1] = '\0';
		}

		user_id = strtok(buffer, ",");
		action_type = strtok(NULL, ",");
		action_value = strtok(NULL, ",");

		printf("%s %s %s\n", user_id, action_type, action_value);

		if (!strcmp(action_type, "REQUEST")) {
			request_auth_req.user_id = NULL;
			request_auth_req.auto_renew = AUTO_RENEW_OFF;

			request_auth_req.user_id = (char *)malloc((strlen(user_id) + 1) * sizeof(char));
			strcpy(request_auth_req.user_id, user_id);
			request_auth_req.auto_renew = atoi(action_value);

			request_auth_resp = request_auth_1(&request_auth_req, handle);

			if (request_auth_resp->response_code == USER_NOT_FOUND) {
				printf("USER_NOT_FOUND\n");
			}
			else {
				printf("%s %s %d\n", request_auth_req.user_id, request_auth_resp->auth_token, request_auth_resp->response_code);

				approve_request_token_req.auth_token = NULL;
				approve_request_token_req.auth_token = (char *)malloc((strlen(request_auth_resp->auth_token) + 1) * sizeof(char));
				strcpy(approve_request_token_req.auth_token, request_auth_resp->auth_token);

				approve_request_token_resp = approve_request_token_1(&approve_request_token_req, handle);

				printf("%s %d\n", approve_request_token_resp->auth_token, approve_request_token_resp->approved);
			}
		}
	}

	request_access_req.auth_token = (char *)malloc((strlen("ceva") + 1) * sizeof(char));
	strcpy(request_access_req.auth_token, "ceva");

	request_access_resp = request_access_1(&request_access_req, handle);
	printf("Received: %s, %d\n", request_access_resp->access_token, request_access_resp->response_code);

    return 0;
}

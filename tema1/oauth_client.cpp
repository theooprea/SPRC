#include <stdio.h>
#include <time.h>
#include <rpc/rpc.h>

#include <iostream>

#include "oauth.h"
#include "helpers.h"

std::vector<user> user_db;

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
	validate_delegated_action_response *validate_delegated_action_resp;
	validate_delegated_action_request validate_delegated_action_req;

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

		user *current_user = NULL;
		for (auto &it : user_db) {
			if (!strcmp(it.username, user_id)) {
				current_user = &it;
			}
		}
		if (current_user == NULL) {
			user_db.push_back(user());

			current_user = &(user_db.back());

			current_user->username = (char *)malloc((strlen(user_id) + 1) * sizeof(char));
			strcpy(current_user->username, user_id);

			current_user->auth_token = (char *)malloc(sizeof(char));
			current_user->auth_token[0] = '\0';
			current_user->access_token = (char *)malloc(sizeof(char));
			current_user->access_token[0] = '\0';
			current_user->renew_token = (char *)malloc(sizeof(char));
			current_user->renew_token[0] = '\0';
			current_user->auto_renew = false;
			
			current_user->available_actions = 0;
		}

		if (!strcmp(action_type, "REQUEST")) {
			request_auth_req.user_id = NULL;
			request_auth_req.auto_renew = AUTO_RENEW_OFF;

			request_auth_req.user_id = (char *)malloc((strlen(user_id) + 1) * sizeof(char));
			strcpy(request_auth_req.user_id, user_id);
			request_auth_req.auto_renew = atoi(action_value);

			if (atoi(action_value) == 1) {
				current_user->auto_renew = true;
			}
			else {
				current_user->auto_renew = false;
			}

			request_auth_resp = request_auth_1(&request_auth_req, handle);

			if (request_auth_resp->response_code == USER_NOT_FOUND) {
				printf("USER_NOT_FOUND\n");
			}
			else {
				/* save resp data into database */
				current_user->auth_token = (char *)malloc((strlen(request_auth_resp->auth_token) + 1) * sizeof(char));
				strcpy(current_user->auth_token, request_auth_resp->auth_token);

				/* approve client request */
				approve_request_token_req.auth_token = NULL;
				approve_request_token_req.auth_token = (char *)malloc((strlen(current_user->auth_token) + 1) * sizeof(char));
				strcpy(approve_request_token_req.auth_token, current_user->auth_token);

				approve_request_token_resp = approve_request_token_1(&approve_request_token_req, handle);

				/* access request */
				request_access_req.auth_token = (char *)malloc((strlen(current_user->auth_token) + 1) * sizeof(char));
				strcpy(request_access_req.auth_token, current_user->auth_token);

				request_access_resp = request_access_1(&request_access_req, handle);

				if (request_access_resp->response_code == REQUEST_DENIED) {
					printf("REQUEST_DENIED\n");
				}
				else {
					current_user->access_token = (char *)malloc((strlen(request_access_resp->access_token) + 1) * sizeof(char));
					strcpy(current_user->access_token, request_access_resp->access_token);

					current_user->renew_token = (char *)malloc((strlen(request_access_resp->renew_token) + 1) * sizeof(char));
					strcpy(current_user->renew_token, request_access_resp->renew_token);

					if (current_user->auto_renew) {
						printf("%s -> %s,%s\n", request_auth_resp->auth_token, request_access_resp->access_token, request_access_resp->renew_token);
					}
					else {
						printf("%s -> %s\n", request_auth_resp->auth_token, request_access_resp->access_token);
					}
				}
			}
		}
		else if (!strcmp(action_type, "READ") || !strcmp(action_type, "INSERT") ||
				 !strcmp(action_type, "MODIFY") || !strcmp(action_type, "DELETE") ||
				 !strcmp(action_type, "EXECUTE")) {

			validate_delegated_action_req.access_token = (char *)malloc((strlen(current_user->access_token) + 1) * sizeof(char));
			strcpy(validate_delegated_action_req.access_token, current_user->access_token);
			
			validate_delegated_action_req.op_type = (char *)malloc((strlen(action_type) + 1) * sizeof(char));
			strcpy(validate_delegated_action_req.op_type, action_type);
			
			validate_delegated_action_req.resource = (char *)malloc((strlen(action_value) + 1) * sizeof(char));
			strcpy(validate_delegated_action_req.resource, action_value);

			validate_delegated_action_resp = validate_delegated_action_1(&validate_delegated_action_req, handle);

			switch (validate_delegated_action_resp->response_code)
			{
			case PERMISSION_DENIED:
				printf("PERMISSION_DENIED\n");
				break;
			case TOKEN_EXPIRED:
				printf("TOKEN_EXPIRED\n");
				break;
			case RESOURCE_NOT_FOUND:
				printf("RESOURCE_NOT_FOUND\n");
				break;
			case OPERATION_NOT_PERMITTED:
				printf("OPERATION_NOT_PERMITTED\n");
				break;
			case PERMISSION_GRANTED:
				printf("PERMISSION_GRANTED\n");
				break;
			default:
				break;
			}
		}
	}

    return 0;
}

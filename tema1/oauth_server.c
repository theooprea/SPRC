#include <stdio.h> 
#include <time.h> 
#include <rpc/rpc.h> 

#include "oauth.h"
#include "helpers.h"

request_auth_response *request_auth_1_svc(char **user_id, struct svc_req *cl) {
    static request_auth_response response;

    response.response_code = USER_FOUND;
    response.token = malloc((strlen(*user_id) + 1) * sizeof(char));
    strcpy(response.token, *user_id);

    return &response;
}

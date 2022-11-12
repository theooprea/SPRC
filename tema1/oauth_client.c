#include <stdio.h> 
#include <time.h> 
#include <rpc/rpc.h> 

#include "oauth.h"
#include "helpers.h"

#define RMACHINE "localhost"

int main() {
    /* variabila clientului */
	CLIENT *handle;
	char *user_id = malloc(10);
	request_auth_response *response;

	handle=clnt_create(
		RMACHINE,		/* numele masinii unde se afla server-ul */
		SERVER,		    /* numele programului disponibil pe server */
	    SERVERVERSION,	/* versiunea programului */
		"tcp");			/* tipul conexiunii client-server */
	
	if(handle == NULL) {
		perror("");
		return -1;
	}

    strcpy(user_id, "toprea");

	response = request_auth_1(&user_id, handle); 
	printf( "The result is: %d %s\n", response->response_code, response->token);

    return 0;
}

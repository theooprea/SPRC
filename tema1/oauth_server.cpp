#include <stdio.h>
#include <time.h>
#include <rpc/rpc.h>
#include <map>

#include "oauth.h"
#include "oauth_svc.h"
#include "helpers.h"

request_auth_response *request_auth_1_svc(char **user_id, struct svc_req *cl) {
    static request_auth_response response;

    response.response_code = USER_FOUND;
    response.token = (char *)malloc((strlen(*user_id) + 1) * sizeof(char));
    strcpy(response.token, *user_id);

    return &response;
}

int main (int argc, char **argv)
{
	register SVCXPRT *transp;

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

	svc_run ();
	fprintf (stderr, "%s", "svc_run returned");
	exit (1);
	/* NOTREACHED */
}

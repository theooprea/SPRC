struct request_auth_response {
	int response_code;
	string auth_token<>;
};

struct request_auth_request {
	int auto_renew;
	string user_id<>;
};

struct request_access_response {
	int response_code;
	string access_token<>;
};

struct request_access_request {
	string user_id<>;
	string auth_token<>;
};

struct approve_request_token_request {
	string auth_token<>;
};

struct approve_request_token_response {
	string auth_token<>;
	int approved;
};

program SERVER {
	version SERVERVERSION {
		request_auth_response REQUEST_AUTH(request_auth_request) = 1;
		request_access_response REQUEST_ACCESS(request_access_request) = 2;
		approve_request_token_response APPROVE_REQUEST_TOKEN(approve_request_token_request) = 3;
	} = 1;
} = 0x31234560;

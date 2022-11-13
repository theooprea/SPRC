struct request_auth_response {
	int response_code;
	string auth_token<>;
};

struct request_access_response {
	int response_code;
	string access_token<>;
};

struct request_access_request {
	string user_id<>;
	string auth_token<>;
};

program SERVER {
	version SERVERVERSION {
		request_auth_response REQUEST_AUTH(string) = 1;
		request_access_response REQUEST_ACCESS(request_access_request) = 2;
	} = 1;
} = 0x31234560;

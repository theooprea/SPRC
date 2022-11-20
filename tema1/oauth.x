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
	string renew_token<>;
};

struct request_access_request {
	string auth_token<>;
};

struct approve_request_token_request {
	string auth_token<>;
};

struct approve_request_token_response {
	string auth_token<>;
	int response_code;
};

struct validate_delegated_action_request {
	string op_type<>;
	string resource<>;
	string access_token<>;
};

struct validate_delegated_action_response {
	int response_code;
};

struct renew_token_request {
	string renew_token<>;
};

struct renew_token_response {
	string access_token<>;
	string renew_token<>;
};

program SERVER {
	version SERVERVERSION {
		request_auth_response REQUEST_AUTH(request_auth_request) = 1;
		request_access_response REQUEST_ACCESS(request_access_request) = 2;
		approve_request_token_response APPROVE_REQUEST_TOKEN(approve_request_token_request) = 3;
		validate_delegated_action_response VALIDATE_DELEGATED_ACTION(validate_delegated_action_request) = 4;
		renew_token_response RENEW_TOKEN(renew_token_request) = 5;
	} = 1;
} = 0x31234560;

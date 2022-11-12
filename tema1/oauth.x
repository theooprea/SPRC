struct request_auth_response {
	int response_code;
	string token<>;
};

program SERVER {
	version SERVERVERSION {
		request_auth_response REQUEST_AUTH(string) = 1;
	} = 1;
} = 0x31234560;

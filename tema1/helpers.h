#ifndef HELPERS_H
#define HELPERS_H

#include <stdlib.h>
#include <iostream>
#include <vector>

#define USER_FOUND 1
#define USER_NOT_FOUND 0

#define APPROVED 1
#define DENIED 0

#define AUTO_RENEW_ON 1
#define AUTO_RENEW_OFF 0

#define REQUEST_APPROVED 1
#define REQUEST_DENIED 0

#define PERMISSION_DENIED 0
#define TOKEN_EXPIRED 1
#define RESOURCE_NOT_FOUND 2
#define OPERATION_NOT_PERMITTED 3
#define PERMISSION_GRANTED 4

#define TOKEN_MAX_LENGTH 256
#define TOKEN_RANDOM_CHARS 10

struct permission {
    char *resource;
    char permissions[6];
};

struct user {
    char *username;
    char *auth_token;
    char *access_token;
    int available_actions;
    char *renew_token;
    std::vector<permission> permissions;
};

char *generate_empty_string() {
    char *empty_string = (char *)malloc(1 * sizeof(char));
    empty_string[0] = '\0';
    return empty_string;
}

#endif

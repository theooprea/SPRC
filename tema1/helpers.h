#ifndef HELPERS_H
#define HELPERS_H

#include <stdlib.h>

#define USER_FOUND 1
#define USER_NOT_FOUND 0

#define TOKEN_MAX_LENGTH 256
#define TOKEN_RANDOM_CHARS 10

typedef struct user {
    char *username;
    char *auth_token;
    char *access_token;
    int available_actions;
    char *renew_token;
} user;

char *generate_jeton(char *clientIdToken) {
    int i;
    char aux;
    char buffer[] = "\0\0";
    char *auth_token = (char *)malloc(TOKEN_MAX_LENGTH * sizeof(char));

    strcpy(auth_token, clientIdToken);
    for (i = 0; i < TOKEN_RANDOM_CHARS; i++) {
        aux = rand() % 26 + 65;
        buffer[0] = aux;
        strcat(auth_token, buffer);
    }
    
    return auth_token;
}

#endif

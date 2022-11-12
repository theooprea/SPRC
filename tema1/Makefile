# Parameters

CLIENT = client
SERVER = server

SOURCES_CLNT.c = 
SOURCES_CLNT.h = 
SOURCES_SVC.c = 
SOURCES_SVC.h = 
SOURCES.x = oauth.x

TARGETS_SVC.c = oauth_server.cpp oauth_xdr.c 
TARGETS_CLNT.c = oauth_clnt.c oauth_client.cpp oauth_xdr.c 
TARGETS = oauth.h oauth_xdr.c oauth_clnt.c oauth_svc.c

OBJECTS_CLNT = oauth_clnt.o oauth_client.o oauth_xdr.o
OBJECTS_SVC = oauth_server.o oauth_xdr.o
# Compiler flags 

CFLAGS += -g 
LDLIBS += -lnsl
RPCGENFLAGS = 

# Targets 

all : $(CLIENT) $(SERVER)

$(TARGETS) : $(SOURCES.x) 
	rpcgen $(RPCGENFLAGS) $(SOURCES.x)
	rpcgen -C -m oauth.x > oauth_svc.h
	rm oauth_svc.c

$(OBJECTS_CLNT) : $(SOURCES_CLNT.c) $(SOURCES_CLNT.h) $(TARGETS_CLNT.c)

$(OBJECTS_SVC) : $(SOURCES_SVC.c) $(SOURCES_SVC.h) $(TARGETS_SVC.c) 

$(CLIENT) : $(OBJECTS_CLNT) 
	$(LINK.c) -o $(CLIENT) $(OBJECTS_CLNT) $(LDLIBS) 

$(SERVER) : $(OBJECTS_SVC) 
	$(LINK.c) -o $(SERVER) $(OBJECTS_SVC) $(LDLIBS)

clean:
	$(RM) core *.o client server oauth_svc.h oauth_xdr.c oauth_clnt.c oauth.h

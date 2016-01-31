import socketserver
import socket
import errno

RECEIVED_MSG = "received"
SUCCESS_MSG = "success"
ERROR_MSG = "error"
NOT_VALID = -1

JOIN_REQ_CMD = "join"
QUIT_REQ_CMD = "quit"
JOIN_CMD = "0000"
QUIT_CMD = "0001"

# A mapping of <ControllerId> to (<Occupied>, <Usernames>) tuple
ControllerMapping = {}
for i in range(4):
    ControllerMapping[i] = (0, "")

# Handles TCP request from CloudyLauncher, request access to CPP
class MyTCPHandler(socketserver.BaseRequestHandler):

    #Receives TCP request and handles it
    def handle(self):
        
        # Read the requested message
        print (RECEIVED_MSG)
        self.data = self.request.recv(1024).strip()
        Client_IP = self.client_address[0]
        Client_PORT = self.client_address[1]
        RequestedMessage = self.data.decode("utf-8")
        # For debugging purposes
        print("{} {} wrote:".format(Client_IP, Client_PORT))
        print(RequestedMessage + "\n")
        # Convert to desired format
        requestedCommand = RequestedMessage.split(' ')[0]
        username = RequestedMessage.split(' ')[1]

        if(requestedCommand == "join"):
            joinReq(self, username)              
        elif(requestedCommand == "quit"):
            quitReq(self, username)
        # Invalid request
        else:
            self.request.sendall(ERROR_MSG.encode("utf-8"))

    # Send join request
    def joinReq(self, username):
        # Get index
        index = getNewControllerID(username)

        if(index != NOT_VALID):
            command = JOIN_CMD + str(index).zfill(4)
            result = connectToCPP(command)
            if(result != ERROR_MSG):
                # Request success
                ControllerMapping[index] = (1, username)
                self.request.sendall(str(index).encode("utf-8"))
                print ('sent controller id mapped.\n')
                print (str(ControllerMapping) + "\n")
            # Request denied
            else:
                self.request.sendall(result.encode("utf-8"))
        # Invalid request
        else:
            self.request.sendall(ERROR_MSG.encode("utf-8"))

    # Send quit request
    def quitReq(self, username):
        # Find index
        index = findControllerID(username)

        if(index != NOT_VALID):
            command = QUIT_CMD + str(index).zfill(4)
            result = connectToCPP(command)
            if (result != ERROR_MSG):
                # Request success
                ControllerMapping[index] = (0, "")
                self.request.sendall(result.encode("utf-8"))
                print ('player removed')
                print (str(ControllerMapping) + "\n")
            # Request denied
            else:
                self.request.sendall(result.encode("utf-8"))
        # Invalid request
        else:
            self.request.sendall(ERROR_MSG.encode("utf-8"))        

def getNewControllerID(username):
    # ensure unique username
    for occupied, playername in ControllerMapping.values():
        if (username == playername):
            print ('error: player already joined')
            return NOT_VALID
    
    # get next available controller id.
    for i in range(4):
        if(ControllerMapping[i][0] == 0):
            return i
    print ('error: players maxed out')
    return NOT_VALID

def findControllerID(username):
    for i in range(4):
        if(ControllerMapping[i][1] == username):
            return i
    print ('error: player not found')
    return NOT_VALID

def connectToCPP(COMMAND):
    response = ""
    IP = '127.0.0.1'
    PORT_NO = 55556
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((IP, PORT_NO))
        s.sendall(COMMAND.encode("utf-8"))
        response = s.recv(BUFFER_SIZE).decode("utf-8")
        print ("response: ", response)
    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            response = ERROR_MSG
        else:
            raise
    finally:
        s.close()
        return response

if __name__ == '__main__':

    # Settings
    HOST = '127.0.0.1'
    PORT = 55550
    BUFFER_SIZE = 1024

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print("Server is running...\n")
    server.serve_forever()

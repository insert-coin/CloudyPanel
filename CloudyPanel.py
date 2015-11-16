import socketserver
import socket
import errno

SUCCESS_MSG = "success"
ERROR_MSG = "error"


# A mapping of <ControllerId> to (<Occupied>, <Usernames>) tuple
ControllerMapping = {}
for i in range(4):
    ControllerMapping[i] = (0, "")

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print ('received.')
        self.data = self.request.recv(1024).strip()
        Client_IP = self.client_address[0]
        Client_PORT = self.client_address[1]
        RequestedMessage = self.data.decode("utf-8")
        
        print("{} {} wrote:".format(Client_IP, Client_PORT))
        print(RequestedMessage + "\n")

        requestedCommand = RequestedMessage.split(' ')[0]
        username = RequestedMessage.split(' ')[1]

        if(requestedCommand == "join"):
            index = getNewControllerID(username)
            if(index != -1):
                command = "join " + str(index)
                result = connectToCPP(command)
                if(result != ERROR_MSG):
                    ControllerMapping[index] = (1, username)
                    self.request.sendall(str(index).encode("utf-8"))
                    print ('sent controller id mapped.\n')
                    print (str(ControllerMapping) + "\n")
                else:
                    self.request.sendall(result.encode("utf-8"))
            else:
                self.request.sendall(ERROR_MSG.encode("utf-8"))
                
        elif(requestedCommand == "quit"):
            index = findControllerID(username)
            if(index != -1):
                command = "quit " + str(index)
                result = connectToCPP(command)
                if (result != ERROR_MSG):
                    ControllerMapping[index] = (0, "")
                self.request.sendall(result.encode("utf-8"))
                print ('player removed')
                print (str(ControllerMapping) + "\n")
            else:
                self.request.sendall(ERROR_MSG.encode("utf-8"))
        else:
            self.request.sendall(ERROR_MSG.encode("utf-8"))


def getNewControllerID(username):
    
    # ensure unique username
    for occupied, playername in ControllerMapping.values():
        if (username == playername):
            print ('error: player already joined')
            return -1
    
    # get next available controller id.
    for i in range(4):
        if(ControllerMapping[i][0] == 0):
            return i
    print ('error: players maxed out')
    return -1

def findControllerID(username):
    for i in range(4):
        if(ControllerMapping[i][1] == username):
            return i
    print ('error: player not found')
    return -1

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

    HOST = '127.0.0.1'
    PORT = 55550
    BUFFER_SIZE = 1024

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print("Server is running...\n")
    server.serve_forever()

import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data.decode("utf-8") + "\n")
        self.request.sendall("done".encode("utf-8"))

if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = 55555
    BUFFER_SIZE = 1024

    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    print("CPP is listening..\n")
    server.serve_forever()

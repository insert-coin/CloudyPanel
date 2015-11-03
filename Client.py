import socket
import errno
import time
import sys


if __name__ == '__main__':
    
    TCP_IP = '127.0.0.1'
    TCP_PORT = 55550
    BUFFER_SIZE = 1024
    MESSAGE = ''
    if len(sys.argv) == 2:
        MESSAGE = sys.argv[1]
    else:
        MESSAGE = 'join player1'
    MESSAGE_BYTE = MESSAGE.encode("utf-8")
##    MESSAGE1 = "join player1"
##    MESSAGE2 = "join player2"
##    MESSAGE3 = 'quit player1'
##    MESSAGE4 = 'quit player2'
##    MESSAGE_BYTE1 = MESSAGE1.encode("utf-8")
##    MESSAGE_BYTE2 = MESSAGE2.encode("utf-8")
##    MESSAGE_BYTE3 = MESSAGE3.encode("utf-8")
##    MESSAGE_BYTE4 = MESSAGE4.encode("utf-8")
    
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((TCP_IP, TCP_PORT))
        print('sent message: ' + MESSAGE)
        s.sendall(MESSAGE_BYTE)
        response = s.recv(BUFFER_SIZE)
        print ("response: ", response.decode("utf-8"))

##        time.sleep(2)
##
##        s.sendall(MESSAGE_BYTE2)
##        print('sent message2: ' + MESSAGE2)
##        response = s.recv(BUFFER_SIZE)
##        print ("response: ", response.decode("utf-8"))

    except socket.error as error:
        if error.errno == errno.WSAECONNRESET:
            print ("socket error")
        else:
            raise
    finally:
        s.close()

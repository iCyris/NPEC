# coding = utf-8

"""

ChatRoom V1.0
Client part

Author: Cyris

"""

import argparse, socket, threading
from user_app import *

BUFSIZE = 65535

intro = """
    ########################################
    #                                      #
    #  Welcome to Cyris's Chat Room(V1.0)  #
    #                                      #
    ########################################

    1. Login - /login [username] [password]
    2. Register - /reg [username] [password]
    3. Send message - [words] (if online)
    4. Send message privatly - /send [target_user_name] [word]
    5. Exit - /exit
    """

def send_message_thread(sock):
    while(True):
        mesg = input('')
        sock.send(mesg.encode("utf-8"))

def receive_message_thread(sock):
    while(True):
        mesg = sock.recv(BUFSIZE)
        print(mesg.decode("utf-8"))

def client(hostname, port, args):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port))

    sendThread = threading.Thread(target = send_message_thread, args=(sock,))
    sendThread.start()

    reveiveThread = threading.Thread(target = receive_message_thread, args=(sock,))
    reveiveThread.start()

    sendThread.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chat Client V1.0')
    parser.add_argument('host', help='chat server name or address')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    print(intro)
    client(args.host, args.port, args)

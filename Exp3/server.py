# coding = utf-8
# server type: multithreading

import argparse, socket
import threading
import os
import app

__author__ = 'Cyris'

def server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(15)
    print ('Listen at', sock.getsockname())
    while True:
        sc, sockname = sock.accept()
        print('Connected by {}'.format(sockname))
        serverClient_Thread = threading.Thread(target = app.serveClient, args=(sc,))
        serverClient_Thread.start()
    sock.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP File Server')
    parser.add_argument('host', help='host or ip adress to bind')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args()
    server(args.host, args.port)
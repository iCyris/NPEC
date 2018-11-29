# coding = utf-8
# server type: asyncio - select

import argparse, socket
import select
import os
import app

__author__ = 'Cyris'

def srv_select(listener):
    socket_list = [listener]
    bytes_received = {}

    while True:
        readable, writable, exceptional = select.select(socket_list, [], socket_list)

        for sock in readable:
            if (sock == listener):
                client_socket, client_addr = listener.accept()
                print('client accept:', client_addr)
                socket_list.append(client_socket)
            else:
                client_socket = sock
                more_data = client_socket.recv(1024)
                if len(more_data)>0:
                    data = bytes_received.pop(client_socket, b'') + more_data
                    if (data.decode('gbk').endswith('$')):
                        file_path = data.decode('gbk')[0:-1]
                        print(file_path)
                        app.serveClient__type_2(client_socket, file_path)
                        socket_list.remove(client_socket)
                        client_socket.close()
                    else:
                        bytes_received[client_socket] = data
                else:
                    print("client colse", client_socket.getpeername())
                    socket_list.remove(client_socket)
                    client_socket.close()

        for sock in exceptional:
            print("client exception:", sock.getpeername())
            socket_list.remove(sock)
            sock.close()

if __name__ == '__main__':
    address = app.parse_command_line()
    listener = app.create_srv_socket(address)
    srv_select(listener)
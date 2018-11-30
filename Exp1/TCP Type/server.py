"""

ChatRoom V2.0
Server part

Author: Cyris

"""

import argparse, socket, threading
import asyncio
import functions
from user_app import *

@asyncio.coroutine
def handle_conversation(reader, writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        data = b''
        while not data.decode('gbk').endswith('$'):
            more_data = yield from reader.read(4096)
            if not more_data:
                if data:
                    print('Client {} sent {!r} but then closed'
                          .format(address, data))
                else:
                    print('Client {} closed socket normally'.format(address))
                return
            data += more_data
        client_request = data.decode('gbk')[0:-1].split()

        try:
            mark, feedback = functions.catch_order(client_request, reader, writer)

            if (mark == 0 or mark == 1):
                functions.srv_sendPacket(writer, feedback.encode('gbk'))
            
            if (mark == 2):
                functions.broadcast(feedback)
            
            if (mark == 3):
                target_user_name = client_request[1]
                target_writer = functions.get_target_writer(target_user_name)
                functions.srv_sendPacket(target_writer, feedback.encode('gbk'))

        except Exception as e:
            feedback = "\033[1;31;40m[System]\033[0m Please login first or use the correct order."
            print(e)
            functions.srv_sendPacket(writer, feedback.encode('gbk'))
        
if __name__ == '__main__':
    address = functions.parse_command_line()
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
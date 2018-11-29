#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter07/srv_asyncio2.py
# Asynchronous I/O inside an "asyncio" coroutine.

import asyncio, app, os

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
        file_path = data.decode('gbk')[0:-1]  

        # new serve client part
        try:
            if(app.checkFile(file_path)):
                feedback_msg = "\033[1;32;40m[Info]\033[0m Start downloading...".encode('gbk')
                app.sendPacket__type_3(writer, feedback_msg, '0')

                with open(file_path, 'rb') as f:
                    part = f.read(4096)
                    while(part):
                        len_data = "{:05d}".format(len(part))
                        send_type = '1'.encode("gbk")
                        len_data = len_data.encode("gbk")
                        writer.write(send_type + len_data + part)
                        yield from writer.drain() # important for large file transmission
                        part = f.read(4096)

                file_size = app.getFileSize(file_path)
                app.sendPacket__type_3(writer, str(file_size).encode('gbk'), '2') # 2 for check
            else:
                feedback_msg = "\033[1;31;40m[Error]\033[0m File not found, please try again".encode('gbk')
                app.sendPacket__type_3(writer, feedback_msg, '0')
        except (Exception, OSError) as e:
            pass

if __name__ == '__main__':
    address = app.parse_command_line()
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
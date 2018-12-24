# -*- coding: utf-8 -*-

import socket
import json
from urllib.parse import quote_plus

request_text = """\
GET /maps/api/geocode/json?address={}&sensor=false HTTP/1.1\r\n\
Host: ditu.google.cn:80\r\n\
User-Agent: HDU Network Programming Class\r\n\
Connection: close\r\n\
\r\n\
"""

def geocode4(address):
    sock = socket.socket() #建立 Socket
    sock.connect(('ditu.google.cn', 80))
    request = request_text.format(quote_plus(address))
    sock.sendall(request.encode('ascii'))
    raw_reply = b''
    while True:
        more = sock.recv(4096)
        if not more:
            break
        raw_reply += more
    sock.close()
    reply = raw_reply.decode('utf-8')
    reply_arr = reply.split("\r\n\r\n")
    json_res = json.loads(reply_arr[1])
    return json_res['results'][0]['formatted_address']

if __name__ == '__main__':
    print((geocode4('hangzhou dianzi university')).split(' ', 1)[0])

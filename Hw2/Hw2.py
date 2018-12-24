# -*- coding: utf-8 -*- 

import argparse, socket

MAX_BYTES = 65535

def server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #服务器间通信，UDP 模式
    sock.bind(('127.0.0.1', port))
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        text = data.decode('utf-8')
        text = searchDict(text)
        data = text.encode('utf-8')
        sock.sendto(data, address)

def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    text = input()
    data = text.encode('utf-8')
    sock.sendto(data, ('127.0.0.1', port))
    data, address = sock.recvfrom(MAX_BYTES)
    text = data.decode('utf-8')
    print(text)

def getDict():
    """
    将txt转化为字典形式方便查询
    """
    rawData = ''
    newDict = {}
    with open("./dict2.txt", "r", encoding='utf-8') as file:
        rawData = file.readlines()
    for i in range(0, rawData.__len__(), 1):
        tempList = []
        for word in rawData[i].split():
            tempList.append(word)
        newDict[tempList[0]] = tempList[1]
    return newDict

def searchDict(word):
    """
    查询字典
    """
    Dict = getDict()
    if word in Dict:
        return word + ': ' + Dict[word]
    return word + ': ' + '查询不到'

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP locally')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)
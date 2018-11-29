# coding = utf-8

import argparse, socket
import threading
import os

__author__ = 'Cyris'

def getFileSize(filePath):
    """
    :return : file size
    """
    filePath = filePath.encode('gbk')
    fileSize = os.path.getsize(filePath)
    return fileSize

def checkFileSize(filePath, remoteSize):
    """
    Check the file integrity
    """
    local_file_size = str(getFileSize(filePath))
    remote_file_size = remoteSize.decode('gbk')
    if (local_file_size == remote_file_size):
        return True
    else:
        return False

# inspired from zizi's code
def sock_readn(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return data
        data += more
    return data

def sendFilePath(sock, remoteFile):
    remote_path = remoteFile + '$'
    sock.sendall(remote_path.encode('gbk'))

def recvPacket(sock):
    data_type = '10' # Nothing
    data = b''
    data_head = sock_readn(sock, 6).decode("gbk")
    data_type = data_head[0:1]
    if (len(data_head) < 6):
        return data_type, data
    data_length = int(data_head[1:6])
    # print('data_head: {}, data_type: {}'.format(data_head, data_type))
    data = sock_readn(sock, data_length)
    return data_type, data

def handleServer(sock, localFile):
    while True:
        try:
            msg_pack = recvPacket(sock)
            if (msg_pack[0] == '0'):
                print(msg_pack[1].decode('gbk'))
            elif (msg_pack[0] == '1'):
                # print(msg_pack[1])
                if (msg_pack[1] == b''):
                    break
                with open(localFile, 'ab') as f:
                    f.write(msg_pack[1])
            elif (msg_pack[0] == '2'):
                remote_size = msg_pack[1]
                print("--- file download statistics ---")
                if (checkFileSize(localFile, remote_size)):
                    print("\033[1;32;40m[Done]\033[0m 1 file transmitted, 1 file received, 0.0% packet loss")
                    sock.close()
                else:
                    print("\033[1;31;40m[Error]\033[0m Some packet loss! please try again")
                    sock.close()
            else:
                print('\033[1;32;40m[Info]\033[0m Sock closed by server')
                break
        except Exception as e:
            break
        
def client(host, port, remoteFile, localFile):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    sendThread = threading.Thread(target = sendFilePath, args=(sock, remoteFile,))
    sendThread.start()

    recvThread = threading.Thread(target = handleServer, args=(sock, localFile,))
    recvThread.start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP File Client')
    parser.add_argument('host', help='host or ip adress to bind')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='client port (default 1060)')
    parser.add_argument('remoteFile', help='remote file path to download')
    parser.add_argument('localFile', help='local file path to save')
    args = parser.parse_args()
    client(args.host, args.port, args.remoteFile, args.localFile)
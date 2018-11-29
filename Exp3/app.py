# coding = utf-8

import argparse, socket, asyncio
import os

__author__ = 'Cyris'

def parse_command_line():
    parser = argparse.ArgumentParser(description='TCP File Server')
    parser.add_argument('host', help='host or ip adress to bind')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args()
    address = (args.host, args.port)
    return address

def create_srv_socket(address):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(address)
    listener.listen(64)
    print('Listening at {}'.format(address))
    return listener

def checkFile(path):
    """
    :param path  : the path of the file Client sent
    """
    feedback = False
    if (os.path.exists(path)):
        feedback = True
    return feedback

def recvPacket(sock):
    """
    Receive the file path from client by using '$' as a end mark
    return: raw file path
    """
    file_path = b''
    data = b''
    while (data!=b'$'):
        data = sock.recv(1)
        if (data == b''):
            break
        file_path += data
    file_path = file_path.decode('gbk')[0:-1]

    return file_path

def sendPacket(sock, data, send_type):
    """
    :param data : the data server sent to client, must be encoded
    :param send_type : the type of the data sent to client, three choices(server_info, sending, sending success)
    struct: type(:01d) + len_data(:05d) + data
    """
    len_data = "{:05d}".format(len(data))
    send_type = send_type.encode("gbk")
    len_data = len_data.encode("gbk")
    sock.sendall(send_type + len_data + data)

def sendFile(sock, file_path):
    """
    send the file
    """
    send_type = '1'

    with open(file_path, 'rb') as f:
        part = f.read(4096)
        while (part):
            sendPacket(sock, part, send_type)
            part = f.read(4096)

def getFileSize(filePath):
    """
    :param filePath : raw file path
    :return : file size
    """
    filePath = filePath.encode('gbk')
    fileSize = os.path.getsize(filePath)
    return fileSize

def serveClient(sock):
    while True:
        try:
            file_path = recvPacket(sock)
            print (file_path)
            if (checkFile(file_path)):
                feedback_msg = "\033[1;32;40m[Info]\033[0m Start downloading...".encode('gbk')
                sendPacket(sock, feedback_msg, '0') # Server message
                sendFile(sock, file_path) # Start sending file

                # Send the total file size
                file_size = getFileSize(file_path)
                sendPacket(sock, str(file_size).encode('gbk'), '2') # 2 for check
            else:
                feedback_msg = "\033[1;31;40m[Error]\033[0m File not found, please try again".encode('gbk')
                sendPacket(sock, feedback_msg, '0')
                sock.close()
        except (Exception, OSError) as e:
            break
        except EOFError:
            print('Client socket to {} has closed'.format(sock.getsockname()))
        finally:
            sock.close()

def serveClient__type_2(sock, file_path):
    try:
        if (checkFile(file_path)):
            feedback_msg = "\033[1;32;40m[Info]\033[0m Start downloading...".encode('gbk')
            sendPacket(sock, feedback_msg, '0') # Server message
            sendFile(sock, file_path) # Start sending file

            file_size = getFileSize(file_path)
            sendPacket(sock, str(file_size).encode('gbk'), '2') # 2 for check
        else:
            feedback_msg = "\033[1;31;40m[Error]\033[0m File not found, please try again".encode('gbk')
            sendPacket(sock, feedback_msg, '0')
            sock.close()
    except (Exception, OSError) as e:
        pass
    except EOFError:
        print('Client socket to {} has closed'.format(sock.getsockname()))

###################### for asyncio.py ######################

def sendPacket__type_3(writer, data, send_type):
    """
    :param data : the data server sent to client, must be encoded
    :param send_type : the type of the data sent to client, three choices(server_info, sending, sending success)
    struct: type(:01d) + len_data(:05d) + data
    """
    len_data = "{:05d}".format(len(data))
    send_type = send_type.encode("gbk")
    len_data = len_data.encode("gbk")
    writer.write(send_type + len_data + data)

def sendFile__type_3(writer, file_path):
    """
    send the file
    """
    send_type = '1'

    with open(file_path, 'rb') as f:
        part = f.read(4096)
        while (part):
            sendPacket__type_3(writer, part, send_type)
            part = f.read(4096)

if __name__ == '__main__':
    pass
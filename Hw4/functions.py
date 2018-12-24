# coding = utf-8

"""

ChatRoom V2.0
Functions part

Author: Cyris

"""

import socket, argparse
import asyncio
import user_app

############### Send / Receive ###############

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

def srv_sendPacket(address, data):
    """
    :param data : the data server sent to client, must be encoded
    :param send_type : the type of the data sent to client, three choices(server_info, sending, sending success)
    struct: len_data(:05d) + data
    """
    len_data = "{:05d}".format(len(data))
    len_data = len_data.encode("gbk")
    socket.sendall(data, address)

def srv_sendPacket(writer, data):
    """
    :param data : the data server sent to client, must be encoded
    :param send_type : the type of the data sent to client, three choices(server_info, sending, sending success)
    struct: len_data(:05d) + data
    """
    len_data = "{:05d}".format(len(data))
    len_data = len_data.encode("gbk")
    writer.write(len_data + data)

def clt_recvPacket(sock):
    data = b''
    data_head = sock_readn(sock, 5).decode("gbk")
    if (len(data_head) < 5):
        return data
    data_length = int(data_head)
    data = sock_readn(sock, data_length)
    return data

def sock_readn(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            return data
        data += more
    return data


########### Normal functions for server ###########

client_list = {}

def room_login(username, password):
    """
    : function check_user(): on user_app.py, for login check.
    : param mark: 0 for True, 1 for False, 2 for broadcast message, 3 for private message.
    """
    if (user_app.check_user(username, password)):
        mesg =  "\033[1;31;40m[System]\033[0m Login Success!"
        mark = 0
        return mark, mesg
    else:
        mesg = "\033[1;31;40m[System]\033[0m Wrong password or the user donsn't exit, Please try again."
        mark = 1
        return mark, mesg

def room_register(username, password):
    if(user_app.register(username, password)):
        mesg = "\033[1;31;40m[System]\033[0m Register Success! Please login to continue."
        mark = 0
        return mark, mesg
    else:
        mesg = "\033[1;31;40m[System]\033[0m The username already exits, please try again."
        mark = 1
        return mark, mesg

def catch_order(data, reader, writer):
    """
    Deal with the orders:
    : order '/login': Login
    : order '/reg': Register
    : order '/send': Send mesg to other users online
    : order '/exit': Exit the Chat Room
    : param data: The data (after dealing) receive from client
    """

    global client_list # [name: (reader, writer)]

    if(data[0] == '/login'):
        """
        : param data: data[0]=order, data[1]=username, data[2]=password
        """
        mark, message = room_login(data[1], data[2])
        if(mark == 0):
            client_list[data[1]] = (reader, writer)
        return mark, message
    
    elif(data[0] == '/reg'):
        """
        : param data: data[0]=order, data[1]=username, data[2]=password
        """
        mark, message = room_register(data[1], data[2])
        return mark, message
    
    elif(data[0] == '/send'):
        """
        : param data: data[0]=order, data[1]=target_username, after data[1] is the message
        """
        target_username = data[1]

        mark = 1 # No such user
        
        if (check_self_online(client_list, writer)):
            if (check_target_online(client_list, target_username)):
                own_name = get_key(client_list, writer)
                message = recovery_sentence(data)
                message = message.split(' ', 2)[2] # Get the true message
                message = "\033[1;32;40m" + "[Private] " + own_name +  "\033[0m" + ' ---> ' + message
                mark = 3 # Private mode
                return mark, message

            if (mark == 1):
                message = "\033[1;31;40m[System]\033[0m Sorry, the, user is not online"
                return mark, message
        else:
            mark = 1
            message = "\033[1;31;40m[System]\033[0m Please login first!"

    elif(data[0] == '/exit'):
        mark = 1
        message = "\033[1;31;40m[System]\033[0m Byebye ~"
        t_key = get_key(client_list, writer)
        if (t_key): 
            client_list.pop(t_key)
        return mark, message

    else:
        message = recovery_sentence(data)
        
        for key, values in client_list.items():
            if(values[1] == writer):
                mark = 2 # broadcast mode
                message = '\033[1;34;40m' + "[Public] " + key + '\033[0m' + ' ---> ' + message
                return mark, message
        
        mark = 1 # False
        message = "\033[1;31;40m[System]\033[0m Please login first or use the correct order!"
        return mark, message
    
def recovery_sentence(data):
    """
    Recovery the dealed data (The complete sentence)
    """
    temp = ""
    for i in data:
        temp += i + ' '
    temp = temp.strip()
    return temp

def get_key(dictin, writer):
    for key, values in dictin.items():
        if(values[1] == writer):
            return key
    return 

def check_self_online(input_list, writer):
    for self_reader, self_writer in input_list.values():
        if self_writer == writer:
            return True
    return False

def check_target_online(input_list, target_username):
    if target_username in input_list:
        return True
    return False

def get_target_writer(target_username):
    for key, values in client_list.items():
        if key == target_username:
            return values[1]

def broadcast(message):
    for reader, writer in client_list.values():
        srv_sendPacket(writer, message.encode('gbk'))
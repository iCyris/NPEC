"""

ChatRoom V1.0
Server part

Author: Cyris

"""

import argparse, socket, threading
from user_app import *

BUFSIZE = 65535
client_list = {}

def room_login(username, password):
    """
    : function check_user(): on user_app.py, for login check.
    : param mark: 0 for True, 1 for False, 2 for broadcast message, 3 for private message.
    """
    if (check_user(username, password)):
        mesg =  "\033[1;31;40m[System]\033[0m Login Success!"
        mark = 0
        return mark, mesg
    else:
        mesg = "\033[1;31;40m[System]\033[0m Password error or the user dosn't exit, Please try again."
        mark = 1
        return mark, mesg

def room_register(username, password):
    if(register(username, password)):
        mesg = "\033[1;31;40m[System]\033[0m Register Success! Please login to continue."
        mark = 0
        return mark, mesg
    else:
        mesg = "\033[1;31;40m[System]\033[0m The username already exits, please try again."
        mark = 1
        return mark, mesg

def catch_order(data, address):
    """
    Deal with the orders:
    : order '/login': Login
    : order '/reg': Register
    : order '/send': Send mesg to other users online
    : order '/exit': Exit the Chat Room
    : param data: The data (after dealing) receive from client
    """

    global client_list

    if(data[0] == '/login'):
        """
        : param data: data[0]=order, data[1]=username, data[2]=password
        """
        mark, message = room_login(data[1], data[2])
        if(mark == 0):
            client_list[data[1]] = address
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
        
        if (check_online(client_list, address)):
            if (get_target_user_address(client_list, target_username)):
                message = recovery_sentence(data)
                message = message.split(' ', 2)[2] # Get the true message
                message = "\033[1;32;40m" + "[Private] " +target_username +  "\033[0m" + ' ---> ' + message
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
        t_key = get_key(client_list, address)
        if (t_key): 
            client_list.pop(t_key)
        return mark, message

    else:
        message = recovery_sentence(data)
        
        for key, value in client_list.items():
            if(value == address):
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

def get_key(dictin, target):
    for key, value in dictin.items():
        if(value == target):
            return key
    return 

def get_target_user_address(input_list, name):
    for key in input_list:
        if (name == key):
            return input_list[key]
    return False # Not found

def check_online(input_list, address):
    for value in input_list.values():
        if (value == address):
            return True
    return False

def server(host, port, args):
    """
    : param client_list: Store the name and address who is online (dict type, 'name':'address (ip + port)')
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    
    global client_list

    while True:
        mesg_to_client = '' # sendto client
        data, address = sock.recvfrom(BUFSIZE)
        dealed_data = data.decode('utf-8').split() # bytes -> str

        try:
            t_mark, t_message = catch_order(dealed_data, address)
            mesg_to_client = t_message
            
            if(t_mark == 0 or t_mark == 1):
                sock.sendto(mesg_to_client.encode('utf-8'), address)

            if(t_mark == 2): # broadcast
                for addr in client_list.values():
                    print(addr)
                    sock.sendto(mesg_to_client.encode('utf-8'), addr)
                print()
            
            if(t_mark == 3): # private chat
                addr = get_target_user_address(client_list, dealed_data[1])
                sock.sendto(mesg_to_client.encode('utf-8'), addr)
            
        except Exception as e:
            mesg_to_client = "\033[1;31;40m[System]\033[0m Something error... please contact zz for help~"
            sock.sendto(mesg_to_client.encode('utf-8'), address)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chat Room V1.0') #创建解析对象
    parser.add_argument('host', help='server listening interface')
    parser.add_argument('-p', '--port', metavar='PORT', type=int, default=1060,
                        help='server port (default 1060)')
    args = parser.parse_args() #进行解析
    server(args.host, args.port, args)
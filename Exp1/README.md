利用 UDP 实现聊天室功能（公聊，私聊）：

用户发送的语句状态：
1. Login: login username password
2. Register: reg username password
3. Send message: send words



self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())


{
    'option': 'login' / 'reg' / 'send',
    'username': username,
    'password': password,
    'state': 0 (未登入),
    'type': 'broadcast' / 'private'
    'target': None / target_username
}

client_list: [[ip1, name1], [ip2, name2], [ip3, name3]]



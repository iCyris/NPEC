# -*- coding: utf-8 -*-

import requests

def geocode2(address):
    parameters = {'address': address, 'sensor': 'false'}
    base = 'http://ditu.google.cn/maps/api/geocode/json' #API Json
    response = requests.get(base, params=parameters) #用GET方法获取内容
    answer = response.json()
    return answer['results'][0]['formatted_address'] #获得需要的地址信息

if __name__ == '__main__':
    result = geocode2('杭州电子科技大学')
    print (result.split(' ', 1)[0])

# -*- coding: utf-8 -*-

import sys
import http.client
import json
from urllib.parse import quote_plus

base = '/maps/api/geocode/json'
def geocode3(address):
    path = '{}?address={}&sensor=false'.format(base, quote_plus(address))
    connection = http.client.HTTPConnection('ditu.google.cn')
    connection.request('GET', path)
    rawreply = connection.getresponse().read()
    reply = json.loads(rawreply.decode('utf-8'))
    return reply['results'][0]['formatted_address']

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        address = sys.argv[1]
    else:
        address = '杭州电子科技大学下沙校区'
    result = geocode3('hangzhou dianzi university')
    print (result.split(' ', 1)[0])
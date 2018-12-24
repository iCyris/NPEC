# -*- coding: utf-8 -*-

from pygeocoder import Geocoder

if __name__ == '__main__':
    address = 'hangzhou dianzi university'
    a = Geocoder.geocode(address)[0] #直接通过 Geocoder 函数获得地址信息
    print(str(a).split(' ', 1)[0])

    '''
    list = [a.country, a.province, a.city, a.sublocality, a.neighborhood, a.route, a.street_number]
    for i in list:
        print(i,end='')
    print(a)
    '''
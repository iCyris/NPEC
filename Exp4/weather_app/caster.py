# Weather Caster v1.0
# -*- coding: utf-8 -*- 

__author__ = 'Cyris'

from bs4 import BeautifulSoup
import re
import requests
import random
import http.client
import time
import socket

class WeatherCaster():
    def __init__(self):
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate,sdch',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }

    def get_url(self,cityName):
        city_code = None

        f = open('./weather_app/dict.txt','rb').readlines()
        for i in f:
            if cityName in bytes.decode(i):
                city_code = re.sub("\D","",bytes.decode(i))

        if (city_code is None):
            print ('Sorry, there is no such city, please search for another.\n')
            return None

        else:
            weather_url = "http://www.weather.com.cn/weather/%s.shtml" % city_code
            return weather_url

    def get_html(self,url,data=None):
        # error handing
        timeout = random.choice(range(80,180))
        while True:
            try:
                rep = requests.get(url,headers=self.headers,timeout=timeout)
                rep.encoding = "utf-8"
                #print(rep.text)
                break
            except socket.timeout as e:
                print ("3:",e)
                time.sleep(random.choice(range(8,15)))

            except socket.error as e:
                print ("4:",e) 
                time.sleep(random.choice(range(20,60)))

            except http.client.BadStatusLine as e:
                print("5:",e)
                time.sleep(random.choice(range(30,80)))

            except http.client.IncompleteRead as e:
                print("6:",e)
                time.sleep(random.choice(range(5,15)))

        return rep.text


    def get_data(self,html_txt):
        final = []
        bs = BeautifulSoup(html_txt, "html.parser")
        body = bs.body
        data = body.find("div",{"id":"7d"})
        ul = data.find("ul")
        li = ul.find_all("li")

        for each_day in li:
            temp = []
            date = each_day.find("h1").string   # get the date
            temp.append(date)
            detail = each_day.find_all("p")
            temp.append(detail[0].string)

            if detail[1].find("span") is None:
                temphigh = None
            else:
                temphigh = detail[1].find("span").string
                temphigh = temphigh.replace('℃','')
            
            templow = detail[1].find("i").string
            templow = templow.replace('℃','')

            temp.append(temphigh)
            temp.append(templow)
            final.append(temp)

        return final


    def main(self,cityName):
        weather_url = self.get_url(cityName)
        if (weather_url != None):
            html_txt = self.get_html(weather_url)
            result = self.get_data(html_txt)
            return result
            #for i in result:
            #    print (i)
        else:
            pass
    

if __name__ == "__main__":
    weather = WeatherCaster()
    weather.main(cityName = input('Please input the city name: '))

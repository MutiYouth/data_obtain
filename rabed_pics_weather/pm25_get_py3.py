# -*- coding: utf-8 -*-
"""
multithreading pm2.5 data fetch program

by weng 20181103 1527 v1.0
"""
from urllib.request import urlopen
import threading
from time import ctime
from bs4 import BeautifulSoup


def get_pm25(city_name):
    site = 'http://www.pm25.com/' + city_name + '.html'
    html = urlopen(site)
    soup = BeautifulSoup(html)
    city = soup.find(class_='bi_loaction_city')  # 城市名称
    aqi = soup.find("a", {"class", "bi_aqiarea_num"})  # AQI指数
    quality = soup.select(".bi_aqiarea_right span")  # 空气质量等级
    result = soup.find("div", class_='bi_aqiarea_bottom')  # 空气质量描述
    print(city.text + u'AQI指数：' + aqi.text + u'\n空气质量：' + quality[0].text + result.text + '*' * 20 + ctime() + '*' * 20)

def one_thread():  # 单线程
    print('One_thread Start: ' + ctime() + '\n')
    get_pm25('hangzhou')
    get_pm25('shanghai')


def two_thread():  # 多线程
    print('Two_thread Start: ' + ctime() + '\n')
    threads = []
    t1 = threading.Thread(target=get_pm25, args=('hangzhou',))
    threads.append(t1)
    t2 = threading.Thread(target=get_pm25, args=('shanghai',))
    threads.append(t2)
    for t in threads:
        # t.setDaemon(True)
        t.start()

# run the program
if __name__ == '__main__':
    one_thread()
    print('\n' * 2)
    two_thread()

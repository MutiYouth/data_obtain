# -*- coding: utf-8 -*-
from urllib import parse
from urllib.request import Request, urlopen
import json
import datetime
import os


# 江苏水雨情
# 数据爬虫，获取几大水域的站点水位数据
# 版本1.0 JC
# 版本1.0.1 WENG
# 2016-9-29 0015

def url_open(url, para_data):
    while True:
        try:
            req = Request(url)
            post_data = parse.urlencode(para_data)
            response = urlopen(req, data=post_data.encode())
            return response.read().decode()
        except Exception as e:
            print("time out\n", e)
            continue


"""
get request paras of map
"""


def get_map_para(index):
    dic = {"ajaxVal": "4",
           "waterType": "1-2-3-4-5",
           "startTime": "2016-08-24+08:00:00",
           "endTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "type": str(stparas[index][0]),
           "id": str(stparas[index][1]),
           "timestamp": "1474889135183",
           "tId": "null",
           "isTopic": "null"}
    return dic


"""
Add station to list if it's not exist
"""


def add2list(st_list, st):
    for i in st_list:
        if i.Equal(st):
            return
    st_list.append(st)


class Station:
    """a station"""
    def __init__(self, dic):
        self.stcd = dic["STCD"]
        self.sttp = dic["STTP"]
        self.name = dic["SITENAME"]
        self.X_R = dic["X_R"]
        self.Y_R = dic["Y_R"]

    def GetPara(self):
        dic = {"startTime": "2016-07-24 11:15:00",
               "stcd": self.stcd,
               "endTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               "sttp": self.sttp}
        return dic

    def Equal(self, sttn):  # is equal?
        if self.stcd == sttn.stcd and self.sttp == sttn.sttp:
            return True
        return False


"""
start the main segments
"""

u2 = 'http://221.226.28.67:88/jsswxxSSI/water_selectWaterDataJson.action'
u1 = 'http://221.226.28.67:88/jsswxxSSI/water_selectWaterAndStStbprpBAndWaterWarJson.action'

stids = [0, 1, 2, 3, 5, 0, 2, 4, 6, 7, 8, 9, 11, 12, 15, 16, 17, 18, 20]
stparas = [[1 if i < 5 else 0, stids[i]] for i in range(len(stids))]  # save paras of map

# save all stations
allst = []
for i in range(len(stparas)):
    para = get_map_para(i)
    s = url_open(u1, para)
    js = json.loads(s)
    stations = js["DATA"]
    n = len(allst)
    for j in stations:
        st = Station(j)
        add2list(allst, st)
    print(stparas[i], len(stations), len(allst), len(allst) - n)

# 路径判断与创建
if not os.path.exists('levels\\'):
    os.makedirs('levels\\')

# 文件存储
n = 0
for i in allst:
    n += 1
    para = i.GetPara()
    s = url_open(u2, para)
    if s != "null":
        js = json.loads(json.loads(s))
        name = i.name + "_" + i.stcd + "_" + i.sttp
        f = open("levels\\" + name + ".csv", 'w')
        data = js["data"]["data"]
        f.write(name + '\n')
        keys = [] if len(data) <= 0 else data[0].keys()
        j = -1

        for d in data:
            line = ""
            j += 1
            if j == 0:
                line = ",".join(keys) + '\n'
            for k in keys:
                line += (str(d[k]) + ',')
            line += '\n'
            f.write(line)
        print("%d/%d" % (n, len(allst)), '\t', name, '\t', len(data), '\t', len(keys))
        f.close()

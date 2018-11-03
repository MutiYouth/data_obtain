# python 3

import csv
import json
import os
import time
import urllib.request

import collections
from PIL.features import codecs



# 请求数据
def parse_data(web_data):
    # web_data = '{"name":"aspiring", "age": 17, "hobby": ["money","power", "read"],"xxx":{"a":1,"b":2}}'
    json_res = json.loads(web_data, encoding='utf-8')       # 输入str，返回json数据,BUGS FIND HERE,20181103 1600
    encoded_json = json.dumps(json_res, sort_keys=True)     # 输入json，返回str，目的是排序
    result = json.loads(encoded_json, encoding='utf-8')     # 输入str，返回json，务必要以utf-8加载json数据
    return result

# 输出数据
def out_data_csv(fn_out, data):
    if not os.path.exists(fn_out):
        print(fn_out)
        header = False
    else:
        header = True
    _f = codecs.open(fn_out, 'a', 'gbk')
    dict_writer = csv.DictWriter(_f, list(data.keys()))

    # only write header when create a new csv
    if not header:
        dict_writer.writeheader()
    dict_writer.writerow(data)
    _f.close()

# 主程序
if __name__ == '__main__':


    # 创建request请求
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    request_url = 'http://www.pm25.com/city/hangzhou.html'
    print(request_url+',\t... ', end="")
    url_request = urllib.request.Request(request_url, data=None, headers=headers)

    # 打开网址
    web_html_data = urllib.request.urlopen(url_request)
    if web_html_data.getcode() != 200:
        raise Exception('Server connection error, status code:' + ' ')
    else:
        print('net data read ok!')

    # parse data

    decoded_data = web_html_data.read().decode('utf-8')
    # should parse the json data using re match
    # under finishing 18.11.3 1650
    # ...
    # -------------------------------------------
    json_raw_data = parse_data(decoded_data)
    # save json type weather data to file 'data_json.txt'
    f = open('data_json.txt', 'w', encoding='utf-8')
    json.dump(json_raw_data, f)
    f.close()


    # save  net data to csv file
    # 下面一句是当数据文件为本机的文件时，才用到的必须加utf_8_sig
    # data_final=open(r'c:\Python33\11.txt',encoding='utf_8_sig').read()
    # data_file  = open(r'c:\Python33\all_data',encoding='utf_8_sig').read()
    now_time = time.localtime()
    out_file = time.strftime('%Y%m%d', now_time) + '.csv'
    d = collections.OrderedDict()

    for element in json_raw_data:
        print(element)
        d['area'] = element['area']
        d['position_name'] = element['position_name']
        d['aqi'] = element['aqi']
        d['co'] = element['co']
        d['co_24h'] = element['co_24h']
        d['no2'] = element['no2']
        d['no2_24h'] = element['no2_24h']
        d['o3'] = element['o3']
        d['o3_24h'] = element['o3_24h']
        d['o3_8h'] = element['o3_8h']
        d['o3_8h_24h'] = element['o3_8h_24h']
        d['pm10'] = element['pm10']
        d['pm10_24h'] = element['pm10_24h']
        d['pm2_5'] = element['pm2_5']
        d['pm2_5_24h'] = element['pm2_5_24h']
        d['primary_pollutant'] = element['primary_pollutant']
        d['quality'] = element['quality']
        d['so2'] = element['so2']
        d['so2_24h'] = element['so2_24h']
        d['station_code'] = element['station_code']
        d['time_point'] = element['time_point']

        # 逐行写excel文件
        out_data_csv(out_file, d)

        print('done!')
        # os.system('pause')
        # time.sleep(180)

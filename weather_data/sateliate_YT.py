# -*- coding: utf-8 -*-
"""
 satellite cloud picture download 
 weng, hurricanblue@126.com
 2016-9-29 0057

modified by weng 2018-2-8 v1.0


update the project to idea project manner
add other type of satellite source
add support of other type sensor images source.

by weng 20181102 1828 v1.1
"""


import datetime
import os
# import urllib2
from urllib.request import urlopen


# 时间列表生成函数
# 提供风云二号卫星云图的这家站点，每半个小时更新一幅图。另外图片的url中也包含有时间信息。故用这个函数生成列表
# usages
# alt+Enter，选择忽略（Ignore）这个错误即好


def time_list_gen(time_s, time_e, satellite_mode, hour_offset=8):
    # 获取FY4的时间列表 UTC 0
    time_seq_dic = {"FY2": [15, 45],
                    "FY4": [0, 15, 30, 34, 38, 45, 49, 53],
                    "RADAR": [0, 6, 12, 18, 24, 30, 36, 42, 48, 54],
                    "RAIN": [0]}

    # hour offset
    if hour_offset != 0:
        time_s -= datetime.timedelta(hours=hour_offset)
        time_e -= datetime.timedelta(hours=hour_offset)

    result = []  # 集合
    time_min_adds = time_seq_dic[satellite_mode]
    time_hour_start = time_s + datetime.timedelta(minutes=-time_s.minute)
    while True:

        lst_ele = time_hour_start
        for tmp_add in time_min_adds:
            lst_ele = time_hour_start + datetime.timedelta(minutes=tmp_add)
            if lst_ele > time_e:  # end session area
                break
            elif lst_ele < time_s:  # pre area
                continue
            # v3.0 add datetime
            result.append(lst_ele)

        # nest hour
        if lst_ele > time_e:
            break
        time_hour_start += datetime.timedelta(hours=1)

    return result


def url_data_read(url):
    i_count = 0  # try times count

    while True:
        i_count += 1

        socket = urlopen(url)
        data = socket.read()
        socket.close()
        if data[0] != "<" and len(data) > 100 * 1024:
            # Download ok!
            return data
        else:
            if i_count == 1:
                print("Retrying ...", end="")
            elif (i_count >= 2) and (i_count <= 20):
                if (i_count % 2) == 0:
                    print("\rRetrying ", end="")
                else:
                    print("\rRetrying ...", end="")
            else:
                print("\rError to down res: {0}".format(url))
                return ''
            continue


def del_path(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_path(c_path)
        else:
            os.remove(c_path)


# 下载卫星云图文件函数
# 将所有图片下载到当前目录下的jpg子文件夹中
# noinspection PyTypeChecker
def main_download(time_list, satellite_mode):
    i_count = 0
    i_totall = len(time_list)

    #  http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxcl_asc_e99_achn_lno_py_20160928154500000.jpg
    #  http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy4a_etcc_achn_lno_py_20181102131500000.jpg
    url_dic = {"FY2": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxcl_asc_e99_achn_lno_py_",  # [风云2号]
               "FY2_ML_HW": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_asc_eir_achn_lno_py_",
               # [风云2号,大陆区域红外]
               "FY2_ML_SQ": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy2e_ewvp_achn_lno_py_",
               # [风云2号,大陆区域水汽]
               "FY2_ZHW": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy2g_emir_achn_lno_py_",
               # [风云2号,中红外圆盘图]
               "FY2_Y_C": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy2g_ecn_achn_lno_py_",
               # [风云2号,彩色圆盘图]
               "FY2_Y_SQ": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy2g_ewvp_achn_lno_py_",
               # [风云2号,水汽圆盘]
               "FY2_Y_V": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy2g_evl_achn_lno_py_",
               # [风云2号,可见光圆盘]
               "FY2_SEA_HW": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxsp_asc_eir_acwp_lno_py_",
               # [风云2号,海区红外]

               "FY4": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy4a_etcc_achn_lno_py_",  # [风云4号, 真彩色]
               "FY4_KJG": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy4a_ec001_achn_lno_py_",
               # [风云4号, 可见光]
               "FY4_HW": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy4a_ec012_achn_lno_py_",  # [风云4号，红外]
               "FY4_SQ": "http://pi.weather.com.cn/i/product/pic/l/sevp_nsmc_wxbl_fy4a_ec009_achn_lno_py_",  # [风云4号，水汽]

               "RADAR": "http://pi.weather.com.cn/i/product/pic/l/sevp_aoc_rdcp_sldas_ebref_achn_l88_pi_",  # [雷达，全国]
               "RADAR_HZ": "http://pi.weather.com.cn/i/product/pic/l/sevp_aoc_rdcp_sldas_ebref_accn_l88_pi_",  # [雷达，华中]
               "RADAR_HD": "http://pi.weather.com.cn/i/product/pic/l/sevp_aoc_rdcp_sldas_ebref_aecn_l88_pi_",  # [雷达，华东]
               "RADAR_HB": "http://pi.weather.com.cn/i/product/pic/l/sevp_aoc_rdcp_sldas_ebref_ancn_l88_pi_",

               "RAIN": "http://pi.weather.com.cn/i/product/share/pic/l/PWCP_TWC_WEAP_SFER_ER1_TWC_L88_P9_"}  # [降雨，逐时]

    for img_name_dt in time_list:

        # 下载卫星云图
        img_file_name_utc0 = img_name_dt.strftime('%Y%m%d%H%M') + '00'
        # str-->datetime eg: image_file_name_time = datetime.datetime.strptime(img_file_name_utc0, '%Y%m%d%H%M%S')
        url = url_dic[satellite_mode] + img_file_name_utc0 + ("001.png" if satellite_mode.find("RADAR") >= 0
                                                              else (
            "000.JPG" if satellite_mode.find("RAIN") >= 0 else "000.jpg"))
        img_data = url_data_read(url)

        # save img
        image_file_name_time = img_name_dt + datetime.timedelta(hours=HOUR_OFFSET)
        img_file_name_utc_e8 = image_file_name_time.strftime('%Y%m%d%H%M%S')
        i_count += 1
        if img_data is not None and len(img_data) > 50 * 1024:  # data is not None , data != None
            # 如果数据开头是<符号，说明返回的不是图片数据而是html数据,也就是说，网站的404返回页面。此时本图片不存在，跳过不下载。
            # 只有数据开头不是<符号，才执行后续下载路径判断与创建
            download_path = RESULT_DIR + img_file_name_utc_e8 + ".jpg"
            with open(download_path, "wb") as jpg:
                jpg.write(img_data)

            # print status
            # old print manner: print("%d/%d" % (i_count, i_totall), '\t', img_file_name_utc_e8 + ".jpg", '\tSuccess')
            print('{0}/{1}\t{2}.jpg,\tSuccess'.format(i_count, i_totall, img_file_name_utc_e8))
        else:
            print('{0}/{1}\t{2}.jpg,\tError'.format(i_count, i_totall, img_file_name_utc_e8))




# 执行下载气象数据
# ---------------------------------------------------------------------------------------
time_start = datetime.datetime(2018, 11, 3, 8, 15, 0)       # START TIME
time_end = datetime.datetime(2018, 11, 3, 12, 30, 0)        # END TIME
HOUR_OFFSET = 0                                             # 去除时间偏移的影响
RESULT_DIR = 'satellites_image\\'                           # 下载到的目录
if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)
else:
    del_path(RESULT_DIR)
main_download(time_list_gen(time_start, time_end, 'RAIN', HOUR_OFFSET), 'RAIN')

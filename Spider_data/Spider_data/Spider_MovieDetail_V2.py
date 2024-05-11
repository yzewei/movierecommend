#!/usr/bin/env python
# coding:utf8
import os
import random
import sys
import urllib.request as urllib2
import json
import time
import gzip
from urllib.parse import quote
from bs4 import BeautifulSoup
import numpy
import requests

from lxml import etree


class MovieSpider:
    # 创建一个session对象
    session = requests.Session()

    def __init__(self):
        self.headers = [
            {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/72.0.3626.121 Safari/537.36',
                'Cookie': 'bid=Gd0_meo9qvo; ll="118284"; ct=y; gr_user_id=87e98c9c-ab19-4fb3-b817-1ba2a0671073; '
                          'push_noty_num=0; '
                          'push_doumail_num=0; ap_v=0,6.0; dbcl2="253033674:wdcoI8djM0c"; ck=CsYd '
            },
            {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.87 Mobile Safari/537.36',
                'Cookie': 'bid=Gd0_meo9qvo; ll="118284"; ct=y; gr_user_id=87e98c9c-ab19-4fb3-b817-1ba2a0671073; '
                          'push_noty_num=0; push_doumail_num=0; ap_v=0,6.0; dbcl2="253031514:tWK61E7YZoU"; ck=mhSu '
            },
            {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.87 Mobile Safari/537.36',
                'Cookie': 'bid=Gd0_meo9qvo; ll="118284"; ct=y; gr_user_id=87e98c9c-ab19-4fb3-b817-1ba2a0671073; '
                          'push_noty_num=0; push_doumail_num=0; ap_v=0,6.0; dbcl2="253034514:D8hoOuxLx/U"; ck=8BPk',

            },
            {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/56.0.2924.87 Mobile Safari/537.36',
                'Cookie': 'bid=Gd0_meo9qvo; ll="118284"; ct=y; gr_user_id=87e98c9c-ab19-4fb3-b817-1ba2a0671073; '
                          'dbcl2="184087665:PrESujE3XTM"; ck=4vAX; push_noty_num=0; push_doumail_num=0; ap_v=0,6.0',
            }]
        # 默认为2
        #419
        self.errorLine = 429

    # 创建文件表头
    def mkfile(self):
        outputFile = 'movies_detail.csv'
        # 判断文件是否存在，不存在则写入表头
        if not os.path.exists(outputFile):
            fw = open(outputFile, 'w')
            fw.write('id^title^url^cover^rate^director^composer^actor^category^region^language^showtime^length'
                     '^othername^Imdb\n')
            fw.close()
            print("已创建文件，并写入表头!!")
        else:
            print("文件已存在!!")

    # 将字符串的压缩字节解压缩为原始字符串
    def ungzip1(self, data):
        try:
            data = gzip.decompress(data)
        except:
            pass
        return data

    # 爬取方式
    def sprider_detail(self, headers, errorLine):
        print("Spider-Man来了!!!!")
        headers_new = headers
        header = headers[random.randint(0, 3)]
        # 读取电影url数据
        inputFile = 'movies_url.csv'
        fr = open(inputFile, 'r', encoding='utf-8')
        # 准备写入电影详细页面数据
        outputFile = 'movies_detail.csv'
        fw = open(outputFile, 'a+', encoding='utf-8')
        # count 代表了当前行，从1开始表示第一行，即表头
        count = 0
        for line in fr:
            count = count + 1
            # 跳过首行 和 已爬取的url
            if count < errorLine:
                continue
            line = line.split(',')
            movieId = line[2]
            title = line[3]
            url = line[4].split('"')[1]
            cover = line[5]
            rate = line[6]
            print("正在爬取第 " + str(count) + " 行： " + url + "  内容")
            time.sleep(15)
            try:
                request = urllib2.Request(url=url, headers=header)
                response = urllib2.urlopen(request)
                html = BeautifulSoup(response.read(), "html.parser")

                # 电影简介
                # description = html.find_all("p", attrs={"data-clamp": "3"})[0].get_text()
                # description = description.lstrip().lstrip('\n\t').rstrip().rstrip('\n\t').replace('\n', '\t')
                # print("爬取第 " + str(count) + " 行描述" + description + "成功!!!!")

                info = html.select('#info')[0]
                info = info.get_text().split('\n')
                # print(info)

                # 电影基本信息
                director = info[1].split(':')[-1].strip()  # 导演
                composer = info[2].split(':')[-1].strip()  # 编剧
                actor = info[3].split(':')[-1].strip()  # 演员
                category = info[4].split(':')[-1].strip()  # 类别
                region = info[5].split(':')[-1].strip()  # 制片地区
                showtime = info[6].split(':')[-1].strip()  # 上映时间
                language = info[7].split(':')[-1].strip()  # 语言
                length = info[8].split(':')[-1].strip()  # 片长
                othername = info[9].split(':')[-1].strip()  # 别名
                Imdb = info[10].split(':')[-1].strip()  # IMDb
                print("爬取电影基本信息：" + title + "......." + Imdb)

                # 写入数据
                record = str(movieId) + '^' + \
                         title + '^' + \
                         url + '^' + \
                         cover + '^' + \
                         str(rate) + '^' + \
                         director + '^' + \
                         composer + '^' + \
                         actor + '^' + \
                         category + '^' + \
                         region + '^' + \
                         language + '^' + \
                         showtime + '^' + \
                         length + '^' + \
                         othername + '^' + \
                         str(Imdb) + '\n'
                fw.write(record)
            except Exception as e:
                print("Spider-Man被 " + str(e) + "偷袭了!!!!        重新爬取第：" + str(count) + " 行url的内容")
                print("Spider-Man永不放弃!!!!\n\n")
                time.sleep(0)
                self.sprider_detail(headers_new, count)

    # 开始爬取
    def start_spider(self):
        self.sprider_detail(self.headers, self.errorLine)


spider = MovieSpider()
spider.mkfile()
spider.start_spider()

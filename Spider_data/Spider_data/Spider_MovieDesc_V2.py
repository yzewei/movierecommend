#!/usr/bin/env python
# coding:utf8
import os
import random
import urllib.request as urllib2
import time
from bs4 import BeautifulSoup
import requests


def mkfile():
    outputFile = 'movies_desc.csv'
    # 判断文件是否存在，不存在则写入表头
    if not os.path.exists(outputFile):
        fw = open(outputFile, 'w')
        fw.write('id^description\n')

        fw.close()
        print("已创建文件，并写入表头!!")
    else:
        print("文件已存在!!")


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
                          'push_noty_num=0; push_doumail_num=0; dbcl2="253034514:D8hoOuxLx/U"; ck=8BPk '
            },
            {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) '
                              'Chrome/56.0.2924.87 Mobile Safari/537.36',
                'Cookie': 'bid=Gd0_meo9qvo; ll="118284"; ct=y; gr_user_id=87e98c9c-ab19-4fb3-b817-1ba2a0671073; '
                          'push_noty_num=0; push_doumail_num=0; dbcl2="253034514:D8hoOuxLx/U"; ck=8BPk '
            },
            {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) '
                              'Chrome/56.0.2924.87 Mobile Safari/537.36',
                'Cookie': 'bid=Gd0_meo9qvo; ll="118284"; ct=y; gr_user_id=87e98c9c-ab19-4fb3-b817-1ba2a0671073; '
                          'push_noty_num=0; push_doumail_num=0; dbcl2="253034514:D8hoOuxLx/U"; ck=8BPk',

            },
            {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
                              'like Gecko) '
                              'Chrome/56.0.2924.87 Mobile Safari/537.36',
                'Cookie': 'bid=Gd0_meo9qvo; ll="118284"; ct=y; gr_user_id=87e98c9c-ab19-4fb3-b817-1ba2a0671073; '
                          'push_noty_num=0; push_doumail_num=0; dbcl2="253034514:D8hoOuxLx/U"; ck=8BPk',
            }]
        # 默认为2
        self.errorLine = 3729

    # 爬取方式
    def spider_detail(self, headers, errorLine):
        print("Spider-Man来了!!!!")
        time.sleep(5)
        headers_new = headers
        header = headers[random.randint(0, 3)]
        # 读取电影url数据
        inputFile = 'movies_url.csv'
        fr = open(inputFile, 'r', encoding='utf-8')
        # 准备写入电影详细页面数据
        outputFile = 'movies_desc.csv'
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
            # url = line[4].split('"')[1]
            url = 'https://movie.douban.com/subject/' + movieId.split('"')[1]
            print("正在爬取第 " + str(count) + " 行： " + url + "  内容")
            time.sleep(15)
            request2 = urllib2.Request(url=url, headers=header)
            response2 = urllib2.urlopen(request2)
            html2 = BeautifulSoup(response2.read(), "html.parser")
            # print(html2)
            try:
                # 电影简介
                description = html2.find_all("p", attrs={"data-clamp": "3"})[0].get_text()
                description = description.lstrip().lstrip('\n\t').rstrip().rstrip('\n\t').replace('\n', '\t')
                print("爬取第 " + str(count) + " 行描述" + description + "成功!!!!")
                # 写入数据
                record = str(movieId) + '^' + description + '\n'
                fw.write(record)
            except Exception as e:
                print("Spider-Man被 " + str(e) + "偷袭了!!!!        重新爬取第：" + str(count) + " 行url的内容")
                print("Spider-Man永不放弃!!!!\n\n")
                self.spider_detail(headers_new, count + 1)

    # 开始爬取
    def start_spider(self):
        self.spider_detail(self.headers, self.errorLine)


spider = MovieSpider()
mkfile()
spider.start_spider()

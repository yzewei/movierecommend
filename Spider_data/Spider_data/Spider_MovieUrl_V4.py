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


class MovieSpider:

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
        self.tags = ["剧情", "喜剧", "动作", "爱情", "科幻", "动画", "悬疑", "惊悚", "恐怖9", "犯罪", "同性", "音乐", "歌舞", "传记", "历史",
                     "战争", "西部", "奇幻", "冒险", "灾难", "武侠", "情色"]
        self.countries = ["中国大陆", "欧美", "美国", "中国香港", "中国台湾", "日本", "韩国", "英国", "法国", "德国", "意大利", "西班牙", "印度",
                          "泰国", "俄罗斯", "伊朗", "加拿大", "澳大利亚", "爱尔兰", "瑞典", "巴西", "丹麦"]
        self.start = 0

    # 创建文件表头
    def mkfile(self):
        outputFile = 'movies_url.csv'
        # 判断文件是否存在，不存在则写入表头
        if not os.path.exists(outputFile):
            fw = open(outputFile, 'a+', encoding='utf-8')
            fw.write('tag,countrie,id,title,url,cover,rate\n')
            fw.close()
            print("已创建文件，并写入表头!!")
        else:
            print("文件已存在!!")

    def ungzip1(self, data):
        try:
            data = gzip.decompress(data)
        except:
            pass
        return data

    # 开始
    def sprider_url(self, tags, countries, headers, start):
        # 如果tags的数据为0，则表示已全部爬取完毕，程序退出
        if len(tags) == 0:
            sys.exit()
        headers_new = headers
        header = headers[random.randint(0, 3)]
        outputFile = 'movies_url.csv'
        fw = open(outputFile, 'a+', encoding='utf-8')
        print("********** 开始游击爬取 **********")
        # 如果该类别的所有地区已爬取完，则更换为全部地区的数据，供下一类别使用
        if len(countries) == 0:
            countries = ["中国大陆", "欧美", "美国", "中国香港", "中国台湾", "日本", "韩国", "英国", "法国", "德国", "意大利", "西班牙", "印度",
                         "泰国", "俄罗斯", "伊朗", "加拿大", "澳大利亚", "爱尔兰", "瑞典", "巴西", "丹麦"]
        # 已类别为基准，爬取全部地区的电影数据，tags的数据会随着爬取而减少
        for tag in tags:
            i = tags.index(tag)
            for countrie in countries:
                j = countries.index(countrie)
                while True:
                    tag1 = quote(tag)
                    countrie1 = quote(countrie)
                    a = quote("电影")
                    url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=" + a + "&start=" + str(
                        start) + "&genres=" + tag1 + "&countries=" + countrie1
                    request = urllib2.Request(url=url, headers=header)
                    response = urllib2.urlopen(request)
                    b = self.ungzip1(response.read())
                    print("\n正在爬取" + tag + "类别," + countrie + "地区的第" + str(start) + "页的20条数据")  # 0为0-19
                    print("爬取的网址：" + url)
                    print("爬取的内容：" + str(b))
                    # 记录当前 剩余类别和其对应的地区 数组
                    tags_new = tags[i:]
                    countries_new = countries[j:]
                    # 如果返回报错msg,则将爬取参数传递给自身，重新调用自身继续爬取
                    try:
                        movies = json.loads(b)['data']
                        # 判断该类别是否爬完
                        if len(movies) == 0 or start == 2000:
                            # 判断该类别的全部地区是否都爬完
                            if j == len(countries) + 1:
                                # 如果类别爬取完毕则爬取 下一类别，全部地区 的数据
                                tags_new = tags[i + 1:]
                                countries = ["中国大陆", "欧美", "美国", "中国香港", "中国台湾", "日本", "韩国", "英国", "法国", "德国", "意大利",
                                             "西班牙",
                                             "印度", "泰国", "俄罗斯", "伊朗", "加拿大", "澳大利亚", "爱尔兰", "瑞典", "巴西", "丹麦"]
                                start = 0
                                print(
                                    "********** 所有" + tag + "类别的全部地区已爬取完成 **********\n********** 休息三秒继续爬取 **********\n\n")
                                time.sleep(3)
                                self.sprider_url(tags_new, countries, headers_new, start)
                            # 如果地区没爬完，则传递 该类别，和下一的地区 的数据继续爬取
                            else:
                                tags_new = tags[i:]
                                countries_new = countries[j + 1:]
                                start = 0
                                print(
                                    "********** 该" + tag + "的" + countrie + "地区已爬取完成 **********\n********** 休息三秒继续爬取 **********\n\n")
                                time.sleep(3)
                                self.sprider_url(tags_new, countries_new, headers_new, start)
                        # 将每一页json的20条数据循环写入csv文件
                        for item in movies:
                            tag = tag  # 类别
                            countrie1 = countrie  # 地区
                            rate = item['rate']  # 电影评分
                            title = item['title']  # 电影名称
                            url = item['url']  # 电影详细页面的url
                            cover = item['cover']  # 图片链接
                            movieId = item['id']  # 电影id
                            record = tag + ',' + countrie1 + ',' + str(movieId) + ',' + title + ',' + url + ',' \
                                     + cover + ',' + str(rate) + '\n '
                            fw.write(record)
                        # 下一页
                        start = start + 20
                        fw.close()
                        time.sleep(0)
                    except:
                        # 如果报错，则传递当前爬取所剩余类别，地区，页数，以此为开始
                        print("被小气鬼狙击了    类别：" + tag + "      地区：" + countrie + "    第" + str(start) + "页")
                        print("                              Spider-Man永不放弃！！！\n\n")
                        self.sprider_url(tags_new, countries_new, headers_new, start)

    def start_spider(self):
        self.sprider_url(self.tags, self.countries, self.headers, self.start)


spider = MovieSpider()
spider.mkfile()
spider.start_spider()

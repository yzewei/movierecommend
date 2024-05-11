import requests
from django.shortcuts import render, HttpResponse, redirect
from django.utils.safestring import mark_safe
# Create your views here.
from webapp import models

# 可以封装成函数，方便 Python 的程序调用
import socket

from webapp.pagination import Pagination


# 获取ip
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        return ip
    finally:
        s.close()
    return ip


from django.db.models import Q


# 首页
def index(request):
    # 判断用户是否登录
    info = request.session.get("info")
    tag = request.GET.get("tag", "剧情")

    rate_list = models.MaxRateMovie.objects.filter(tag=tag)
    date_list = models.MaxDateMovie.objects.filter(tag=tag)
    dis_tag = models.MaxDateMovie.objects.values("tag").distinct()
    # print(dis_tag)
    if not info:
        return redirect('/login/')

    return render(request, "index.html", {"rate_list": rate_list, "date_list": date_list, "dis_tag": dis_tag})


# 登录操作，如果用户名称和密码正确则跳转到index，并将登录信息写入登录信息表中
def login(requset):
    if requset.method == 'GET':
        return render(requset, 'login.html')
    else:
        # print(requset.POST)
        user = requset.POST.get("username")
        password = requset.POST.get("password")
        user_list = models.UserInfo.objects.filter(uid=user).values("uid", "password").first()
        try:
            uid = user_list["uid"]
            passw = user_list["password"]
        except:
            error_name = '%s用户名不存在' % user
            return render(requset, 'login.html', {'error_name': error_name})
        if user == uid and password == passw:
            # return HttpResponse("登录成功")
            IP = get_host_ip()
            user = models.WebUserLoginInfo.objects.create(uid=user,
                                                          ip=IP
                                                          )
            user.save()
            # 生成session
            requset.session["info"] = uid
            return redirect('/index/')
        elif password != passw:
            error_password = '密码错误'
            return render(requset, 'login.html', {"error_password": error_password})
        return render(requset, 'login.html')


# 注册操作，如果用户名不重复则写入数据库中，并跳转到登录页面
def register(request):
    # 定义一个错误提示为空
    error_name = ''
    if request.method == 'POST' and request.POST.get('username'):
        user = request.POST.get('username')
        password = request.POST.get('password')
        tag = request.POST.get('tag')
        user_list = models.UserInfo.objects.filter(uid=user)
        if user_list:
            # 注册失败
            error_name = '%s用户名已经存在了' % user
            # 返回到注册页面，并且把错误信息报出来
            return render(request, 'register.html', {'error_name': error_name})
        else:
            # 数据保存在数据库中，并返回到登录页面

            user = models.UserInfo.objects.create(uid=user,
                                                  password=password,
                                                  tag=tag
                                                  )
            user.save()
            # 注册成功则跳到login下的login.html
            return redirect('/login/')
    # 注册错误则跳回本页
    return render(request, 'register.html')


# 注销 清除cookie
def logout(request):
    # request.session.clear()
    del request.session["info"]
    return redirect('/login/')


# 搜索展示
def search_movie(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict["name__contains"] = search_data
    queryset = models.MoviesDetail.objects.filter(**data_dict)
    # 2.实例化分页对象
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, "search_movie.html", context)


# 电影详情
def movie_detail(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    # 获取当前用户名字
    userid = request.session.get("info")
    # 获取当前电影id
    mid = request.GET.get("mid")

    if models.UserMovieCollect.objects.filter(uid=userid, mid=mid).count() > 0:
        # 收藏图标
        pic = '<span class="glyphicon glyphicon-star" aria-hidden="true"></span>'
        stat = '取消收藏'
    else:
        # 未收藏图标
        pic = '<span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>'
        stat = '收藏'
    pic = mark_safe(pic)

    # request.session["movie_id"] = mid
    from django.core import serializers
    # 获取当前电影id
    # dataid = models.MoviesDetail.objects.filter(name=name).values("dataid")[:1]
    # mid = models.MoviesDetail.objects.filter(name=name)
    # for a in mid:
    #     print(a.dataid)
    #     request.session["movie_id"]=a.dataid

    # 判断当前电影有无在用户评分表中
    if models.UserMovieScore.objects.filter(uid=userid, mid=mid).count() > 0:
        # 获取当前电影在用户评分表中的评分
        rating = models.UserMovieScore.objects.filter(uid=userid, mid=mid)
        # print("历史评分"+str(rating))
        # # rating=rating1['rating']
        # # 判断用户是否评分
        # if request.GET.get("rate") != None:
        #     rate = request.GET.get("rate")
        #     # 更改评分
        #     mid = request.session.get("movie_id")
        #     print("更新数据"+str(mid))
        #     models.UserMovieScore.objects.filter(uid=userid, mid=mid).update(rating=rate)
    else:
        rating = " "
        print("没有评分过" + str(mid))
        # if request.GET.get("rate") != None:
        #     rate = request.GET.get("rate")
        #     # 插入评分
        #     mid = request.session.get("movie_id")
        #     print("插入数据"+str(mid))
        #     models.UserMovieScore.objects.create(uid=userid, mid=mid, rating=rate)
    # mid = request.session.get("movie_id")
    # 获取其他电影数据
    detail = models.MoviesDetail.objects.filter(dataid=mid)
    tag = ""
    for i in detail:
        if i.style2 == None and i.style3 == None:
            tag = i.style1
        elif i.style2 is not None and i.style3 == None:
            tag = i.style2
        elif i.style2 != None and i.style3 != None:
            tag = i.style1 + " " + i.style2 + " " + i.style3

    return render(request, "movie_detail.html",
                  {"detail": detail, "tag": tag, "rating": rating, "pic": pic, "stat": stat})


# 添加评分
def fav_add(request, dataid):
    rate = request.GET.get("rate", '0')
    userid = request.session.get("info")
    if models.UserMovieCollect.objects.filter(uid=userid, mid=dataid).count() > 0:
        # 收藏图标
        pic = '<span class="glyphicon glyphicon-star" aria-hidden="true"></span>'
        stat = '取消收藏'
    else:
        # 未收藏图标
        pic = '<span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>'
        stat = '收藏'
    pic = mark_safe(pic)
    # 用户点击评分
    if rate != None:
        # 判断用户是否有历史评分
        if models.UserMovieScore.objects.filter(uid=userid, mid=dataid).count() > 0:
            # 更改评分
            print("更新评分" + str(rate))
            models.UserMovieScore.objects.filter(uid=userid, mid=dataid).update(rating=rate)
        else:
            print("添加评分" + str(dataid))
            models.UserMovieScore.objects.create(uid=userid, mid=dataid, rating=rate)
        detail = models.MoviesDetail.objects.filter(dataid=dataid)
        tag = ""
        for i in detail:
            if i.style2 == None and i.style3 == None:
                tag = i.style1
            elif i.style2 is not None and i.style3 == None:
                tag = i.style2
            elif i.style2 != None and i.style3 != None:
                tag = i.style1 + " " + i.style2 + " " + i.style3
        rating = models.UserMovieScore.objects.filter(uid=userid, mid=dataid)
        return render(request, "movie_detail.html",
                      {"detail": detail, "tag": tag, "rating": rating, "pic": pic, "stat": stat})


# 添加收藏
def fav_add2(request, dataid, stat):
    userid = request.session.get("info")
    if stat == "收藏":
        models.UserMovieCollect.objects.create(uid=userid, mid=dataid)
    else:
        models.UserMovieCollect.objects.filter(uid=userid, mid=dataid).delete()

    if models.UserMovieCollect.objects.filter(uid=userid, mid=dataid).count() > 0:

        # 收藏图标
        pic = '<span class="glyphicon glyphicon-star" aria-hidden="true"></span>'
        stat = '取消收藏'
    else:
        # 未收藏图标
        pic = '<span class="glyphicon glyphicon-star-empty" aria-hidden="true"></span>'
        stat = '收藏'
    pic = mark_safe(pic)
    detail = models.MoviesDetail.objects.filter(dataid=dataid)
    tag = ""
    for i in detail:
        if i.style2 == None and i.style3 == None:
            tag = i.style1
        elif i.style2 is not None and i.style3 == None:
            tag = i.style2
        elif i.style2 != None and i.style3 != None:
            tag = i.style1 + " " + i.style2 + " " + i.style3
    rating = models.UserMovieScore.objects.filter(uid=userid, mid=dataid)
    return render(request, "movie_detail.html",
                  {"detail": detail, "tag": tag, "rating": rating, "pic": pic, "stat": stat})


# 收藏列表
def collect_list(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    userid = request.session.get("info")
    queryset1 = models.UserMovieCollect.objects.filter(uid=userid)
    print(queryset1)
    li = []
    for i in queryset1:
        li.append(i.mid)
    print(li)
    queryset = models.MoviesDetail.objects.filter(dataid__in=li)
    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, "collect_list.html", context)


# 评分列表
def rate_list(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    userid = request.session.get("info")
    queryset1 = models.UserMovieScore.objects.filter(uid=userid)
    print(queryset1)
    li = []
    for i in queryset1:
        li.append(i.mid)
    print(li)
    queryset = models.MoviesDetail.objects.filter(dataid__in=li)
    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, "rate_list.html", context)


# 标签推荐
def tag_list(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    userid = request.session.get("info")
    queryset1 = models.CbTagSimilar.objects.filter(uid=userid).order_by('-similar')
    # print(queryset1)
    # 存放标签推荐的电影id
    li = []
    for i in queryset1:
        li.append(i.mid)
    # 存放已评分和收藏过的电影id
    queryset2 = models.UserMovieScore.objects.filter(uid=userid)
    queryset3 = models.UserMovieCollect.objects.filter(uid=userid)
    his_mid = []
    for j in queryset2:
        his_mid.append(j.mid)
    for k in queryset3:
        his_mid.append(k.mid)

    # 通过标签推荐的电影id来筛选电影数据集里的电影，并将已评分和收藏过的电影给过滤掉
    queryset = models.MoviesDetail.objects.filter(dataid__in=li).exclude(dataid__in=his_mid).order_by('-rate')
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, "tag_list.html", context)


# 偏好推荐
def like_list(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    userid = request.session.get("info")
    # 提取用户收藏和评分高的电影id
    user_score = models.UserMovieScore.objects.filter(uid=userid, rating__gte=7)
    user_collect = models.UserMovieCollect.objects.filter(uid=userid)
    movie_id = []
    for i in user_score:
        movie_id.append(i.mid)
    for i in user_collect:
        movie_id.append(i.mid)
    print(movie_id)
    # 根据用户偏好电影去寻找相似电影id
    queryset1 = models.CbLikesSimilar.objects.filter(uid__in=movie_id)
    # print(queryset1)

    # 过滤用户看过的电影id
    user_score1 = models.UserMovieScore.objects.filter(uid=userid)
    movie_id1 = []
    for i in user_score1:
        movie_id1.append(i.mid)
    for i in user_collect:
        movie_id1.append(i.mid)

    li = []
    for i in queryset1:
        li.append(i.mid)
    # print(li)
    queryset = models.MoviesDetail.objects.filter(dataid__in=li).exclude(dataid__in=movie_id1)
    # 2.实例化分页对象
    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, "like_list.html", context)


# 电影数据可视化
def movie_show(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')
    return render(request, "movie_show.html")



# 电影数据可视化
def movie_echarts(request):
    import pymysql
    from pyecharts.charts import Bar, Line, Scatter, EffectScatter, Grid, Map, Page, Pie, WordCloud, Funnel, Gauge

    from pyecharts import options as opts
    import pandas as pd

    # 连接数据库
    conn = pymysql.connect(host='192.168.152.128', user='root', passwd='root', db='douban')

    # 1各年份上映电影数量 折线图
    sql = 'select date,count(*) from movies_detail where date >=1900 group by date HAVING count(*)>10 ORDER BY count(*) desc limit 10'
    df = pd.read_sql(sql, conn)
    c1 = (
        Line(init_opts=opts.InitOpts(chart_id='1'))
            .add_xaxis(list(df['date']))
            .add_yaxis("年份", list(df['count(*)']))
            .set_global_opts(title_opts=opts.TitleOpts(title="年份电影数量前十"))
    )

    # 2各地区上映电影数量 饼图
    sql2 = 'select country,count(*) from movies_detail group by country HAVING count(*)>10 ORDER BY count(*) desc limit 10'
    df2 = pd.read_sql(sql2, conn)
    c2 = (
        Pie(init_opts=opts.InitOpts(chart_id='2'))
            .add("", [list(z) for z in zip(list(df2['country']), list(df2['count(*)']))])
            .set_global_opts(title_opts=opts.TitleOpts(title="地区电影数量前十"),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_top="5%", pos_left="2%"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render('test.html')
    )

    # 3电影类型数量漏斗图
    sql3 = 'select style1,count(*) from movies_detail  group by style1 HAVING count(*)>100 ORDER BY count(*) desc'
    df3 = pd.read_sql(sql3, conn)
    c3 = Funnel(init_opts=opts.InitOpts(chart_id='3'))
    c3.add('数量', [list(z) for z in zip(df3['style1'], df3['count(*)'])])
    # c3.render('test.html')

    # 4评分平均分前十地区词云
    sql4 = 'select country,ROUND(avg(rate),2) from movies_detail where country in (SELECT country from movies_detail GROUP BY country HAVING count(country)>100) group by country ORDER BY avg(rate) desc limit 10'
    df4 = pd.read_sql(sql4, conn)
    words = [tuple(z) for z in zip(df4['country'], df4['ROUND(avg(rate),2)'])]
    c4 = WordCloud(init_opts=opts.InitOpts(chart_id='4'))
    c4.add("平均分", words, word_size_range=[30, 100], shape='circle').set_global_opts(
        title_opts=opts.TitleOpts(title="评分平均分前十地区"))
    # c4.render('test.html')

    # 5评分最高前十的演员 环形图
    sql5 = 'select actors,count(*) from movies_detail where actors!="" and actors in (SELECT actors from movies_detail GROUP BY actors HAVING avg(rate)>8) group by actors ORDER BY count(*) desc limit 10'
    df5 = pd.read_sql(sql5, conn)
    c5 = (
        Pie(init_opts=opts.InitOpts(chart_id='5'))
            .add("", [list(z) for z in zip(list(df5['actors']), list(df5['count(*)']))], radius=[80, 150])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(title_opts=opts.TitleOpts(title="评分最高的演员前十"),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_top="5%", pos_left="2%"))  # 图例位置和垂直显示
        # .render('test.html')
    )

    # 6各地区电影数量 地图
    nameMap = {
        'Singapore Rep.': '新加坡',
        'Dominican Rep.': '多米尼加',
        'Palestine': '巴勒斯坦',
        'Bahamas': '巴哈马',
        'Timor-Leste': '东帝汶',
        'Afghanistan': '阿富汗',
        'Guinea-Bissau': '几内亚比绍',
        "Côte d'Ivoire": '科特迪瓦',
        'Siachen Glacier': '锡亚琴冰川',
        "Br. Indian Ocean Ter.": '英属印度洋领土',
        'Angola': '安哥拉',
        'Albania': '阿尔巴尼亚',
        'United Arab Emirates': '阿联酋',
        'Argentina': '阿根廷',
        'Armenia': '亚美尼亚',
        'French Southern and Antarctic Lands': '法属南半球和南极领地',
        'Australia': '澳大利亚',
        'Austria': '奥地利',
        'Azerbaijan': '阿塞拜疆',
        'Burundi': '布隆迪',
        'Belgium': '比利时',
        'Benin': '贝宁',
        'Burkina Faso': '布基纳法索',
        'Bangladesh': '孟加拉国',
        'Bulgaria': '保加利亚',
        'The Bahamas': '巴哈马',
        'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
        'Belarus': '白俄罗斯',
        'Belize': '伯利兹',
        'Bermuda': '百慕大',
        'Bolivia': '玻利维亚',
        'Brazil': '巴西',
        'Brunei': '文莱',
        'Bhutan': '不丹',
        'Botswana': '博茨瓦纳',
        'Central African Rep.': '中非',
        'Canada': '加拿大',
        'Switzerland': '瑞士',
        'Chile': '智利',
        'China': '中国大陆',
        'Ivory Coast': '象牙海岸',
        'Cameroon': '喀麦隆',
        'Dem. Rep. Congo': '刚果民主共和国',
        'Congo': '刚果',
        'Colombia': '哥伦比亚',
        'Costa Rica': '哥斯达黎加',
        'Cuba': '古巴',
        'N. Cyprus': '北塞浦路斯',
        'Cyprus': '塞浦路斯',
        'Czech Rep.': '捷克',
        'Germany': '德国',
        'Djibouti': '吉布提',
        'Denmark': '丹麦',
        'Algeria': '阿尔及利亚',
        'Ecuador': '厄瓜多尔',
        'Egypt': '埃及',
        'Eritrea': '厄立特里亚',
        'Spain': '西班牙',
        'Estonia': '爱沙尼亚',
        'Ethiopia': '埃塞俄比亚',
        'Finland': '芬兰',
        'Fiji': '斐',
        'Falkland Islands': '福克兰群岛',
        'France': '法国',
        'Gabon': '加蓬',
        'United Kingdom': '英国',
        'Georgia': '格鲁吉亚',
        'Ghana': '加纳',
        'Guinea': '几内亚',
        'Gambia': '冈比亚',
        'Guinea Bissau': '几内亚比绍',
        'Eq. Guinea': '赤道几内亚',
        'Greece': '希腊',
        'Greenland': '格陵兰',
        'Guatemala': '危地马拉',
        'French Guiana': '法属圭亚那',
        'Guyana': '圭亚那',
        'Honduras': '洪都拉斯',
        'Croatia': '克罗地亚',
        'Haiti': '海地',
        'Hungary': '匈牙利',
        'Indonesia': '印度尼西亚',
        'India': '印度',
        'Ireland': '爱尔兰',
        'Iran': '伊朗',
        'Iraq': '伊拉克',
        'Iceland': '冰岛',
        'Israel': '以色列',
        'Italy': '意大利',
        'Jamaica': '牙买加',
        'Jordan': '约旦',
        'Japan': '日本',
        'Japan': '日本本土',
        'Kazakhstan': '哈萨克斯坦',
        'Kenya': '肯尼亚',
        'Kyrgyzstan': '吉尔吉斯斯坦',
        'Cambodia': '柬埔寨',
        'Korea': '韩国',
        'Kosovo': '科索沃',
        'Kuwait': '科威特',
        'Lao PDR': '老挝',
        'Lebanon': '黎巴嫩',
        'Liberia': '利比里亚',
        'Libya': '利比亚',
        'Sri Lanka': '斯里兰卡',
        'Lesotho': '莱索托',
        'Lithuania': '立陶宛',
        'Luxembourg': '卢森堡',
        'Latvia': '拉脱维亚',
        'Morocco': '摩洛哥',
        'Moldova': '摩尔多瓦',
        'Madagascar': '马达加斯加',
        'Mexico': '墨西哥',
        'Macedonia': '马其顿',
        'Mali': '马里',
        'Myanmar': '缅甸',
        'Montenegro': '黑山',
        'Mongolia': '蒙古',
        'Mozambique': '莫桑比克',
        'Mauritania': '毛里塔尼亚',
        'Malawi': '马拉维',
        'Malaysia': '马来西亚',
        'Namibia': '纳米比亚',
        'New Caledonia': '新喀里多尼亚',
        'Niger': '尼日尔',
        'Nigeria': '尼日利亚',
        'Nicaragua': '尼加拉瓜',
        'Netherlands': '荷兰',
        'Norway': '挪威',
        'Nepal': '尼泊尔',
        'New Zealand': '新西兰',
        'Oman': '阿曼',
        'Pakistan': '巴基斯坦',
        'Panama': '巴拿马',
        'Peru': '秘鲁',
        'Philippines': '菲律宾',
        'Papua New Guinea': '巴布亚新几内亚',
        'Poland': '波兰',
        'Puerto Rico': '波多黎各',
        'Dem. Rep. Korea': '朝鲜',
        'Portugal': '葡萄牙',
        'Paraguay': '巴拉圭',
        'Qatar': '卡塔尔',
        'Romania': '罗马尼亚',
        'Russia': '俄罗斯',
        'Rwanda': '卢旺达',
        'W. Sahara': '西撒哈拉',
        'Saudi Arabia': '沙特阿拉伯',
        'Sudan': '苏丹',
        'S. Sudan': '南苏丹',
        'Senegal': '塞内加尔',
        'Solomon Is.': '所罗门群岛',
        'Sierra Leone': '塞拉利昂',
        'El Salvador': '萨尔瓦多',
        'Somaliland': '索马里兰',
        'Somalia': '索马里',
        'Serbia': '塞尔维亚',
        'Suriname': '苏里南',
        'Slovakia': '斯洛伐克',
        'Slovenia': '斯洛文尼亚',
        'Sweden': '瑞典',
        'Swaziland': '斯威士兰',
        'Syria': '叙利亚',
        'Chad': '乍得',
        'Togo': '多哥',
        'Thailand': '泰国',
        'Tajikistan': '塔吉克斯坦',
        'Turkmenistan': '土库曼斯坦',
        'East Timor': '东帝汶',
        'Trinidad and Tobago': '特里尼达和多巴哥',
        'Tunisia': '突尼斯',
        'Turkey': '土耳其',
        'Tanzania': '坦桑尼亚',
        'Uganda': '乌干达',
        'Ukraine': '乌克兰',
        'Uruguay': '乌拉圭',
        'United States': '美国',
        'Uzbekistan': '乌兹别克斯坦',
        'Venezuela': '委内瑞拉',
        'Vietnam': '越南',
        'Vanuatu': '瓦努阿图',
        'West Bank': '西岸',
        'Yemen': '也门',
        'South Africa': '南非',
        'Zambia': '赞比亚',
        'Zimbabwe': '津巴布韦'
    }

    sql6 = 'select country,count(*) from movies_detail where country !="" and country in (SELECT country from movies_detail GROUP BY country HAVING count(*) >100) group by country '
    df6 = pd.read_sql(sql6, conn)
    c6 = (
        Map(init_opts=opts.InitOpts(chart_id='6'))
            # 添加数据系列名称, 数据(list格式), 地图名称, 不显示小红点
            .add("", [list(z) for z in zip(df6['country'], df6['count(*)'])], "world", is_map_symbol_show=False,
                 name_map=nameMap)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 标签不显示(国家名称不显示)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各地区电影数量"),  # 主标题与副标题名称
            visualmap_opts=opts.VisualMapOpts(max_=20000),  # 值映射最大值
        )
    )
    # c6.render('test.html')

    # 7评分最高前十的导演 环形图
    sql7 = 'select directors,count(*) from movies_detail where directors!="" and directors in (SELECT directors from movies_detail GROUP BY directors HAVING avg(rate)>8) group by directors ORDER BY count(*) desc limit 10'
    df7 = pd.read_sql(sql7, conn)
    c7 = (
        Pie(init_opts=opts.InitOpts(chart_id='7'))
            .add("", [list(z) for z in zip(list(df7['directors']), list(df7['count(*)']))], radius=[80, 150])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(title_opts=opts.TitleOpts(title="评分最高前十的导演"),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_top="5%", pos_left="2%"))  # 图例位置和垂直显示
        # .render('test.html')
    )

    # 好评率
    sql8 = 'select count(rate) from movies_detail where rate>1'
    sql9 = 'select count(rate) from movies_detail where rate>8'
    df8 = pd.read_sql(sql8, conn)
    df9 = pd.read_sql(sql9, conn)
    rate10 = round(df9['count(rate)'] / df8['count(rate)'], 2)
    rate10 = int(rate10 * 100)
    # print(rate10)
    c8 = Gauge(init_opts=opts.InitOpts(chart_id='8'))
    c8.add("电影好评率", [("", rate10)], axisline_opts=opts.AxisLineOpts(
        linestyle_opts=opts.LineStyleOpts(color=[(0.3, "#67e0e3"),
                                                 (0.7, "#37a2da"), (1, "#fd666d")], width=30)))
    # c8.render("test.html")

    page1 = Page(page_title="电影数据可视化", layout=Page.DraggablePageLayout)
    page1.add(c1, c2, c3, c4, c5, c6, c7, c8)
    page1.render('组合图2.html')
    Page.save_resize_html(source='组合图2.html', cfg_file="chart_config (4).json", dest="C:/Users/admin/Desktop/毕设/Movie_Recommendation_Spark_Django/webapp/templates/movie_result.html")
    return render(request, "movie_result.html")


# 修改个人信息
def edit_me(request):
    # 判断用户是否登录
    info = request.session.get("info")
    if not info:
        return redirect('/login/')

    userid = request.session.get("info")
    if request.method == "GET":
        row_object = models.UserInfo.objects.filter(uid=userid).first()
        return render(request, "edit_me.html", {"row_object": row_object})
    password = request.POST.get("password")
    tag = request.POST.get("tag")
    models.UserInfo.objects.filter(uid=userid).update(password=password, tag=tag)
    return redirect("/index/")

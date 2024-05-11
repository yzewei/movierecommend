import pymysql
from pyecharts.charts import Bar, Line, Scatter, EffectScatter, Grid, Map, Page, Pie, WordCloud, Funnel, Gauge

from pyecharts import options as opts
import pandas as pd

# 连接数据库
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='douban')

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
        .set_global_opts(title_opts=opts.TitleOpts(title="地区电影数量前十"),legend_opts=opts.LegendOpts( orient="vertical", pos_top="5%", pos_left="2%" ))
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
c4.add("平均分", words, word_size_range=[30, 100], shape='circle') .set_global_opts(title_opts=opts.TitleOpts(title="评分平均分前十地区"))
# c4.render('test.html')

# 5评分最高前十的演员 环形图
sql5 = 'select actors,count(*) from movies_detail where actors!="" and actors in (SELECT actors from movies_detail GROUP BY actors HAVING avg(rate)>8) group by actors ORDER BY count(*) desc limit 10'
df5 = pd.read_sql(sql5, conn)
c5 = (
    Pie(init_opts=opts.InitOpts(chart_id='5'))
        .add("", [list(z) for z in zip(list(df5['actors']), list(df5['count(*)']))], radius=[80, 150])
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .set_global_opts( title_opts=opts.TitleOpts(title="评分最高的演员前十"),legend_opts=opts.LegendOpts( orient="vertical", pos_top="5%", pos_left="2%" )) # 图例位置和垂直显示
        # .render('test.html')
)

# 6各地区电影数量 地图
nameMap = {
        'Singapore Rep.':'新加坡',
        'Dominican Rep.':'多米尼加',
        'Palestine':'巴勒斯坦',
        'Bahamas':'巴哈马',
        'Timor-Leste':'东帝汶',
        'Afghanistan':'阿富汗',
        'Guinea-Bissau':'几内亚比绍',
        "Côte d'Ivoire":'科特迪瓦',
        'Siachen Glacier':'锡亚琴冰川',
        "Br. Indian Ocean Ter.":'英属印度洋领土',
        'Angola':'安哥拉',
        'Albania':'阿尔巴尼亚',
        'United Arab Emirates':'阿联酋',
        'Argentina':'阿根廷',
        'Armenia':'亚美尼亚',
        'French Southern and Antarctic Lands':'法属南半球和南极领地',
        'Australia':'澳大利亚',
        'Austria':'奥地利',
        'Azerbaijan':'阿塞拜疆',
        'Burundi':'布隆迪',
        'Belgium':'比利时',
        'Benin':'贝宁',
        'Burkina Faso':'布基纳法索',
        'Bangladesh':'孟加拉国',
        'Bulgaria':'保加利亚',
        'The Bahamas':'巴哈马',
        'Bosnia and Herz.':'波斯尼亚和黑塞哥维那',
        'Belarus':'白俄罗斯',
        'Belize':'伯利兹',
        'Bermuda':'百慕大',
        'Bolivia':'玻利维亚',
        'Brazil':'巴西',
        'Brunei':'文莱',
        'Bhutan':'不丹',
        'Botswana':'博茨瓦纳',
        'Central African Rep.':'中非',
        'Canada':'加拿大',
        'Switzerland':'瑞士',
        'Chile':'智利',
        'China':'中国大陆',
        'Ivory Coast':'象牙海岸',
        'Cameroon':'喀麦隆',
        'Dem. Rep. Congo':'刚果民主共和国',
        'Congo':'刚果',
        'Colombia':'哥伦比亚',
        'Costa Rica':'哥斯达黎加',
        'Cuba':'古巴',
        'N. Cyprus':'北塞浦路斯',
        'Cyprus':'塞浦路斯',
        'Czech Rep.':'捷克',
        'Germany':'德国',
        'Djibouti':'吉布提',
        'Denmark':'丹麦',
        'Algeria':'阿尔及利亚',
        'Ecuador':'厄瓜多尔',
        'Egypt':'埃及',
        'Eritrea':'厄立特里亚',
        'Spain':'西班牙',
        'Estonia':'爱沙尼亚',
        'Ethiopia':'埃塞俄比亚',
        'Finland':'芬兰',
        'Fiji':'斐',
        'Falkland Islands':'福克兰群岛',
        'France':'法国',
        'Gabon':'加蓬',
        'United Kingdom':'英国',
        'Georgia':'格鲁吉亚',
        'Ghana':'加纳',
        'Guinea':'几内亚',
        'Gambia':'冈比亚',
        'Guinea Bissau':'几内亚比绍',
        'Eq. Guinea':'赤道几内亚',
        'Greece':'希腊',
        'Greenland':'格陵兰',
        'Guatemala':'危地马拉',
        'French Guiana':'法属圭亚那',
        'Guyana':'圭亚那',
        'Honduras':'洪都拉斯',
        'Croatia':'克罗地亚',
        'Haiti':'海地',
        'Hungary':'匈牙利',
        'Indonesia':'印度尼西亚',
        'India':'印度',
        'Ireland':'爱尔兰',
        'Iran':'伊朗',
        'Iraq':'伊拉克',
        'Iceland':'冰岛',
        'Israel':'以色列',
        'Italy':'意大利',
        'Jamaica':'牙买加',
        'Jordan':'约旦',
        'Japan':'日本',
        'Japan':'日本本土',
        'Kazakhstan':'哈萨克斯坦',
        'Kenya':'肯尼亚',
        'Kyrgyzstan':'吉尔吉斯斯坦',
        'Cambodia':'柬埔寨',
        'Korea':'韩国',
        'Kosovo':'科索沃',
        'Kuwait':'科威特',
        'Lao PDR':'老挝',
        'Lebanon':'黎巴嫩',
        'Liberia':'利比里亚',
        'Libya':'利比亚',
        'Sri Lanka':'斯里兰卡',
        'Lesotho':'莱索托',
        'Lithuania':'立陶宛',
        'Luxembourg':'卢森堡',
        'Latvia':'拉脱维亚',
        'Morocco':'摩洛哥',
        'Moldova':'摩尔多瓦',
        'Madagascar':'马达加斯加',
        'Mexico':'墨西哥',
        'Macedonia':'马其顿',
        'Mali':'马里',
        'Myanmar':'缅甸',
        'Montenegro':'黑山',
        'Mongolia':'蒙古',
        'Mozambique':'莫桑比克',
        'Mauritania':'毛里塔尼亚',
        'Malawi':'马拉维',
        'Malaysia':'马来西亚',
        'Namibia':'纳米比亚',
        'New Caledonia':'新喀里多尼亚',
        'Niger':'尼日尔',
        'Nigeria':'尼日利亚',
        'Nicaragua':'尼加拉瓜',
        'Netherlands':'荷兰',
        'Norway':'挪威',
        'Nepal':'尼泊尔',
        'New Zealand':'新西兰',
        'Oman':'阿曼',
        'Pakistan':'巴基斯坦',
        'Panama':'巴拿马',
        'Peru':'秘鲁',
        'Philippines':'菲律宾',
        'Papua New Guinea':'巴布亚新几内亚',
        'Poland':'波兰',
        'Puerto Rico':'波多黎各',
        'Dem. Rep. Korea':'朝鲜',
        'Portugal':'葡萄牙',
        'Paraguay':'巴拉圭',
        'Qatar':'卡塔尔',
        'Romania':'罗马尼亚',
        'Russia':'俄罗斯',
        'Rwanda':'卢旺达',
        'W. Sahara':'西撒哈拉',
        'Saudi Arabia':'沙特阿拉伯',
        'Sudan':'苏丹',
        'S. Sudan':'南苏丹',
        'Senegal':'塞内加尔',
        'Solomon Is.':'所罗门群岛',
        'Sierra Leone':'塞拉利昂',
        'El Salvador':'萨尔瓦多',
        'Somaliland':'索马里兰',
        'Somalia':'索马里',
        'Serbia':'塞尔维亚',
        'Suriname':'苏里南',
        'Slovakia':'斯洛伐克',
        'Slovenia':'斯洛文尼亚',
        'Sweden':'瑞典',
        'Swaziland':'斯威士兰',
        'Syria':'叙利亚',
        'Chad':'乍得',
        'Togo':'多哥',
        'Thailand':'泰国',
        'Tajikistan':'塔吉克斯坦',
        'Turkmenistan':'土库曼斯坦',
        'East Timor':'东帝汶',
        'Trinidad and Tobago':'特里尼达和多巴哥',
        'Tunisia':'突尼斯',
        'Turkey':'土耳其',
        'Tanzania':'坦桑尼亚',
        'Uganda':'乌干达',
        'Ukraine':'乌克兰',
        'Uruguay':'乌拉圭',
        'United States':'美国',
        'Uzbekistan':'乌兹别克斯坦',
        'Venezuela':'委内瑞拉',
        'Vietnam':'越南',
        'Vanuatu':'瓦努阿图',
        'West Bank':'西岸',
        'Yemen':'也门',
        'South Africa':'南非',
        'Zambia':'赞比亚',
        'Zimbabwe':'津巴布韦'
    }

sql6 = 'select country,count(*) from movies_detail where country !="" and country in (SELECT country from movies_detail GROUP BY country HAVING count(*) >100) group by country '
df6 = pd.read_sql(sql6, conn)
c6 = (
    Map(init_opts=opts.InitOpts(chart_id='6'))
    # 添加数据系列名称, 数据(list格式), 地图名称, 不显示小红点
    .add("", [list(z) for z in zip(df6['country'], df6['count(*)'])], "world",is_map_symbol_show=False,name_map=nameMap)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 标签不显示(国家名称不显示)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各地区电影数量"),   # 主标题与副标题名称
        visualmap_opts=opts.VisualMapOpts(max_=20000),               # 值映射最大值
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
        .set_global_opts( title_opts=opts.TitleOpts(title="评分最高前十的导演"),legend_opts=opts.LegendOpts( orient="vertical", pos_top="5%", pos_left="2%" )) # 图例位置和垂直显示
        # .render('test.html')
)

# 好评率
sql8='select count(rate) from movies_detail where rate>1'
sql9='select count(rate) from movies_detail where rate>8'
df8 = pd.read_sql(sql8, conn)
df9 = pd.read_sql(sql9, conn)
rate10=round(df9['count(rate)']/df8['count(rate)'],2)
rate10=int(rate10*100)
# print(rate10)
c8 = Gauge(init_opts=opts.InitOpts(chart_id='8'))
c8.add("电影好评率",[("", rate10)],axisline_opts=opts.AxisLineOpts(
linestyle_opts=opts.LineStyleOpts(color=[(0.3, "#67e0e3"),
 (0.7, "#37a2da"), (1, "#fd666d")], width=30)))
# c8.render("test.html")


page1 = Page(page_title="电影数据可视化", layout=Page.DraggablePageLayout)
page1.add(c1,c2,c3,c4,c5,c6,c7,c8)
page1.render('组合图2.html')
Page.save_resize_html(source='组合图2.html', cfg_file="chart_config (4).json", dest="movie_result2.html")


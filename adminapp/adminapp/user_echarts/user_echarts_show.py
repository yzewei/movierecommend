import numpy
from pyecharts.charts import Bar, Line, Scatter, EffectScatter, Grid, Map, Page, WordCloud, Gauge
from pyecharts.faker import Faker
from pyecharts import options as opts

date=[]
for i in range(1,31):
    date.append(i)



bar1 = (Bar().add_xaxis(Faker.week).add_yaxis('数量', Faker.values()).set_global_opts(
    title_opts=opts.TitleOpts(title="日活跃用户数"),
    xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
    datazoom_opts=opts.DataZoomOpts(type_="slider")))

line = Line()
line.add_xaxis(Faker.week)
line.add_yaxis("日增", Faker.values())
line.set_global_opts(title_opts=opts.TitleOpts(title="日增用户数"),
                     legend_opts=opts.LegendOpts(pos_top="1%"))

l1 = Faker.provinces
n1 = Faker.values()
data_prov_city = [tuple(z) for z in zip(l1, n1)]
province_city = Map()
province_city.add("地区", data_prov_city)
province_city.set_global_opts(
    title_opts=opts.TitleOpts(title="用户分布"),
    visualmap_opts=opts.VisualMapOpts(
        min_=0,
        max_=3000,
        is_piecewise=False))

# 用户最喜欢的电影类型
tags=['剧情','悬疑','恐怖','动作','爱情','动画','科幻','冒险','战争','灾难','武侠']
num=[1000,800,600,500,400,300,800,600,500,500,300]
words = [tuple(z) for z in zip(tags, num)]
c4 = WordCloud()
c4.add("用户最喜欢的电影类型", words, word_size_range=[30, 100], shape='circle') .set_global_opts(title_opts=opts.TitleOpts(title="用户最喜欢的电影类型"))

# 用户好评率
c8 = Gauge()
c8.add("好评率",[("", 18)],axisline_opts=opts.AxisLineOpts(
    linestyle_opts=opts.LineStyleOpts(color=[(0.3, "#67e0e3"),
                                             (0.7, "#37a2da"), (1, "#fd666d")], width=30)))


# 用户差评率
c9 = Gauge()
c9.add("差评率",[("", 34)],axisline_opts=opts.AxisLineOpts(
    linestyle_opts=opts.LineStyleOpts(color=[(0.3, "#67e0e3"),
                                             (0.7, "#37a2da"), (1, "#fd666d")], width=30)))





#
# page1 = Page(page_title="Covid-19 World vaccinated", layout=Page.DraggablePageLayout)
# page1.add(bar1, line, province_city,c4,c8,c9)
# page1.render('组合图.html')
Page.save_resize_html(source='组合图.html', cfg_file="chart_config.json", dest="result.html")
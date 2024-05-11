from pyspark.sql import SparkSession
from pyspark import SparkContext
import pyspark.sql.functions as F
from pyspark.sql.types import Row


spark = SparkSession \
    .builder \
    .appName("score_date") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate() 

# 写入数据库时的配置文件
prop = {}
prop['user'] = 'root'
prop['password'] = 'root'
prop['driver'] = "com.mysql.jdbc.Driver"

# 读取本地电影数据集
# read_filepath='file:////home/master/movie/movies_detail.csv'

# 获取web当前用户id 将用户id写入标签推荐里
# df = spark.read.format('jdbc').options(url='jdbc:mysql://192.168.152.128',dbtable='douban.web_user_login_info',user='root',password='root' ).load()
#uid=df.select('uid').sort(df.date.desc()).limit(1)
#l0=df.collect()
#uid=[]
#for i in l0:
#    uid=i[1]

# 通过id去读取用户填写的标签
df2 = spark.read.format('jdbc').options(
    url='jdbc:mysql://192.168.152.128',
    dbtable='douban.user_info',
    user='root',
    password='root' 
    ).load()
#df3=df2.join(df, on="uid").sort(df.date.desc()).limit(1)
# 将用户标签转为列表
#l=df3.collect()

#for i in l:
#    print("用户标签:  "+i[2])
#    list1=i[2]
#user_tag=list1.split(" ")
#print(user_tag)
#存储用户和标签
dict=[]
for i in df2.collect():
     dict.append([i[0],i[2]])





# 查询电影标签,先将一整行数据转换为列表
df4=spark.read.format('jdbc').options(
    url='jdbc:mysql://192.168.152.128',
    dbtable='douban.movies_detail',
    user='root',
    password='root' 
    ).load()
l2=df4.collect()


# 获取用户评分和收藏过的电影id
df5 = spark.read.format('jdbc').options(
    url='jdbc:mysql://192.168.152.128',
    dbtable='douban.user_movie_collect',
    user='root',
    password='root' 
    ).load()
df5_1=df5.join(df, on="uid")
df6 = spark.read.format('jdbc').options(
    url='jdbc:mysql://192.168.152.128',
    dbtable='douban.user_movie_score',
    user='root',
    password='root' 
    ).load()
df6_1=df6.join(df, on="uid")
coll=df5_1.collect()
rate=df6_1.collect()
all_mid=[]
for j in coll:
    all_mid.append(j[2])
for k in rate:
    all_mid.append(k[2])

#  提取行数据里相应位置的电影标签
cb_list=[]
for i in l2:
    if i[14] in all_mid:
         continue
    movie_tag=[]
    if i[6] !=None:
        movie_tag.append(i[6])
    if i[7] !=None:
    	movie_tag.append(i[7])
    if i[8] !=None:
    	movie_tag.append(i[8])
    # 用户标签和电影标签的全集
    all_tag=user_tag+movie_tag

    # 去重
    set_all = set(all_tag)
    # 判断用户标签和电影标签有无重复项
    if len(all_tag) == len(set_all):
        print("《" + i[0] + "》这部电影的类型不是用户喜欢的")
    else:
        num = (len(all_tag) - len(set_all)) / len(set_all)  # 杰卡德系数
        data = [str(uid), i[14], num] 
        cb_list.append(data)
#print(cb_list)
cb_df = spark.createDataFrame(cb_list,['uid', 'mid',"similar"])

        #cb_df.show()
cb_df.select("uid","mid","similar").orderBy("similar",ascending=False).limit(1000).write.jdbc("jdbc:mysql://192.168.152.128:3306/douban",'cb_tag_similar','append', prop)
       	#print( "《" + i[0] + "》的用户匹配度：" + str(num) + "   匹配标签为：" + str(movie_tag))
       	






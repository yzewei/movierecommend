from pyspark.sql import SparkSession
from pyspark import SparkContext
import pyspark.sql.functions as F

spark = SparkSession \
    .builder \
    .appName("score_date") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate() 


prop = {}
prop['user'] = 'root'
prop['password'] = 'root'
prop['driver'] = "com.mysql.jdbc.Driver"




read_filepath='file:////home/master/movie/movies_detail.csv'
write_scorepath='file:////home/master/movie/score_movie.csv'
write_datepath='file:////home/master/movie/date_movie.csv'


# 将电影数据作为dataframe


# 提取所以电影标签的类别27

tags=["剧情","喜剧","纪录片","悬疑","恐怖","动作","爱情","动画","科幻","家庭","惊悚","奇幻","短片","犯罪","冒险","西部","音乐","战争","灾难","同性","情色","历史","儿童","传记","歌舞","真人秀","武侠"]

# 拿出每个标签下电影数据，并按评分排序，从而得出各类别的高分电影
def score():
    tags=["剧情","喜剧","纪录片","悬疑","恐怖","动作","爱情","动画","科幻","家庭","惊悚","奇幻","短片","犯罪","冒险","西部","音乐","战争","灾难","同性","情色","历史","儿童","传记","歌舞","真人秀","武侠"]
    for i in range(len(tags)):
        df=spark.read.option("header", "true").csv(read_filepath)
        df1=df.filter((df['style1']==tags[i] )| (df['style2']==tags[i]) | (df['style3']==tags[i] )).sort(df.rate.desc()).limit(10)
        df1=df1.withColumn("tag", F.lit(tags[i]))
        # df1.select("dataID", "name","tag","rate","pic").write.csv(write_scorepath, encoding="utf-8", header=True)
        df1.select("dataID", "name","tag","rate","pic").write.jdbc("jdbc:mysql://192.168.152.128:3306/douban",'max_rate_movie','append', prop)
    
    
# 拿出每个标签下电影数据，并按上映日期排序，从而得出各类别的最新电影   
def date():    
    tags=["剧情","喜剧","纪录片","悬疑","恐怖","动作","爱情","动画","科幻","家庭","惊悚","奇幻","短片","犯罪","冒险","西部","音乐","战争","灾难","同性","情色","历史","儿童","传记","歌舞","真人秀","武侠"]
    for i in range(len(tags)):
        df=spark.read.option("header", "true").csv(read_filepath)
        df2=df.filter((df['style1']==tags[i] )| (df['style2']==tags[i]) | (df['style3']==tags[i] )).sort(df.date.desc()).limit(10)
        df2=df2.withColumn("tag", F.lit(tags[i]))
        # df2.select("dataID", "name","tag","date","pic").write.format("csv").save(write_datepath)
        df2.select("dataID", "name","tag","date","pic").write.jdbc("jdbc:mysql://192.168.152.128:3306/douban",'max_date_movie','append', prop)




if __name__ == "__main__":
    #score()
    date()






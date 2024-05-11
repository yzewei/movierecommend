from pyspark.sql import SparkSession
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pyspark.sql.functions as F
from pyspark.mllib.feature import HashingTF
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.sql import SparkSession,SQLContext
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

from queue import Queue


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

# 读取电影数据集为dataframe
# df=pd.read_csv()
df = spark.read.format('jdbc').options(
    url='jdbc:mysql://192.168.152.128',
    dbtable='douban.movies_detail',
    user='root',
    password='root'
).load()
mid = []
for i in df.collect():
    mid.append(i[14])

#将缺失值替换为unkown
df=df.fillna('unkown')
print("----------------------------------")
df.show(20,False)
# 2.将dataframe分为 电影id和电影特征 两列
df.createOrReplaceTempView("data1")
df=spark.sql("select dataID,concat_ws(' ',directors, writer, actors, style1, style2, style3, country, language,date) as FullTag from data1 where directors !='unkown' and writer != 'unkown' and actors !='unkown' ")


#分词
print("----------分词------------")
tokenizer = Tokenizer(inputCol="FullTag", outputCol="tag")
wordsData = tokenizer.transform(df)
wordsData.show()

# 单词频数计算
from pyspark.ml.feature import CountVectorizer,CountVectorizerModel
cv = CountVectorizer(inputCol="tag", outputCol="features", vocabSize=800000, minDF=1.0)

# 训练模型
model = cv.fit(wordsData)

# 测试模型
print("----------测试模型------------")
result = model.transform(wordsData)
result.show(20,False)


# idf模型计算
print("----------idf模型计算------------")
idf = IDF(inputCol="features", outputCol="features2")
idfModel = idf.fit(result)
rescaledData = idfModel.transform(result)
rescaledData.select("dataID","tag","features", "features2").show(20,False)


# LSH 局部敏感哈希
from pyspark.ml.feature import BucketedRandomProjectionLSH, MinHashLSH

train = rescaledData.select(['dataID', 'features2'])
train.show(20,False)
print("----------BucketedRandomProjectionLSH获取所有相似对------------")
# 1.BucketedRandomProjectionLSH
brp = BucketedRandomProjectionLSH(inputCol='features2', outputCol='hashes', numHashTables=4.0, bucketLength=10.0)
model = brp.fit(train)
# 欧式距离:EuclideanDistance
similar = model.approxSimilarityJoin(train,train, 16.0, distCol='EuclideanDistance')
similar.filter(similar.datasetA != similar.datasetB).show(10)
#similar.filter(similar.datasetA != similar.datasetB).filter(similar.datasetA.dataID == '25845392').show()
#2.MinHashLSH
#brp = BucketedRandomProjectionLSH(inputCol='features2', outputCol='hashes', numHashTables=4.0, bucketLength=10.0)
#model = brp.fit(train)
# 杰卡德距离:JaccardDistance 最远距离限制10.0
#similar = model.approxSimilarityJoin(train,train, 10.0, distCol='JaccardDistance ')
#similar.filter(similar.datasetA != similar.datasetB).show(10)



#存入数据库中
similar.createOrReplaceTempView("similar1")
similar2 = spark.sql("select datasetA.dataID as uid, datasetB.dataID as mid , EuclideanDistance as similar from similar1 where datasetA != datasetB ")
similar2.select("uid","mid","similar").write.jdbc("jdbc:mysql://192.168.152.128:3306/douban",'cb_likes_similar','append', prop)







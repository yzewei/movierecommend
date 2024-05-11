import os


def file_url():
    outputFile = 'movies_url.csv'
    # 判断文件是否存在，不存在则写入表头
    if not os.path.exists(outputFile):
        fw = open(outputFile, 'a+', encoding='utf-8')
        fw.write('tag,countrie,id,title,url,cover,rate\n')
        fw.close()
        print("已创建文件，并写入表头!!")
    else:
        print("文件已存在!!")


def file_detail():
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


def file_desc():
    outputFile = 'movies_desc.csv'
    # 判断文件是否存在，不存在则写入表头
    if not os.path.exists(outputFile):
        fw = open(outputFile, 'w')
        fw.write('id^description\n')
        fw.close()
        print("已创建文件，并写入表头!!")
    else:
        print("文件已存在!!")


file_url()
file_desc()
file_detail()

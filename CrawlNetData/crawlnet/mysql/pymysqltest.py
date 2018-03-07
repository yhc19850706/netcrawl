import pymysql  #导入 pymysql


def create_news(sqlstr):
    #打开数据库连接
    db= pymysql.connect(host="127.0.0.1",user="yhc",
                        password="yhc",db="demo",port=3306)

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    sql_insert ="""insert into news_content(WEBSITE_ID,CRAWL_URL,NEWS_NAME,NEWS_URL,NEWS_IMAGE,NEWS_DESC,KEYWORDS,PUBLISH_TIME,NEWS_RESOURCE,NEWS_AUTHOR) 
            values("""+sqlstr+""")"""

    try:
        cur.execute(sql_insert)
        #提交
        db.commit()
    except Exception as e:
        #错误回滚
        db.rollback()
    finally:
        db.close()

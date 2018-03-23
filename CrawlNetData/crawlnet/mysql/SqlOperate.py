from sqlalchemy import  create_engine, exc, orm
from mysql.models import *
import time



class SqlOperate(object):
    def __init__(self):
        try:
            engine = create_engine("mysql+pymysql://yhc:yhc@127.0.0.1:3306/netdata?charset=utf8", echo=False, max_overflow=5, encoding='utf-8')
        except ImportError:
            raise RuntimeError
        engine.connect()
        #yhc:yhc@127.0.0.1
        # sessionmaker is a factory obj, generate a Session instance, reload __call__ function
        # __call__ function will return a session class each time
        Session = orm.sessionmaker(bind=engine)
        # use Session() to create a class, and assign it to an attribute
        self.session = Session()



if __name__ == '__main__':
    ses = SqlOperate()
    session=ses.session
    criteria = NewsCriteria()
    criteria.keItem = '7*24小时'
    criteria.newsDate=time.strftime("%Y-%m-%d", time.localtime())
    criteria.newsResource='腾讯'
    criteria.newsLink='http://www.qq.com/news'
    criteria.newsName='金融科技'
    criteria.newsContent = '互联网金融时代到来'
    #NewsService.add(criteria, session)
    newsList=NewsService.findall(criteria,session)
    if newsList and len(newsList)>0:
        for new in newsList:
            print(new.newsName)
    criteria.id=5
    news=NewsService.findOne(criteria,session)
    if news:
       print(news.newsContent)
    criteria.newsContent='丑'
    r=NewsService.modify(criteria,session)
    print(r)
    news=NewsService.findOne(criteria,session)
    if news:
        print(news.newsContent)
    #tyty
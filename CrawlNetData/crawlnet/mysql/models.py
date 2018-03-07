from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table, Column,MetaData
from sqlalchemy.sql.sqltypes import Integer, VARCHAR, TEXT,DATE

Base = declarative_base()
metadata = MetaData()
class News(Base):
    __table__ =Table('36ke_news',
                     Base.metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('ke_item', VARCHAR(64)),
                     Column('news_lable', VARCHAR(256)),
                     Column('news_name', VARCHAR(256)),
                     Column('news_content', TEXT),
                     Column('news_link', VARCHAR(256)),
                     Column('news_resource', VARCHAR(128)),
                     Column('news_date', DATE),
                     Column('published_time', DATE))
class NewsCriteria():
    def __init__(self, **kwargs):
        self.id = None
        self.keItem = None
        self.newsLable = None
        self.newsName = None
        self.newsContent = None
        self.newsLink = None
        self.newsResource = None
        self.newsDate = None
        self.publishedTime=None

        for field, argument in kwargs.items():
            if str(field) == 'id':
                self.id = argument
            if str(field) == 'ke_item':
                self.keItem = argument
            if str(field) == 'news_lable':
                self.newsLable = argument
            if str(field) == 'news_name':
                self.newsName = argument
            if str(field) == 'news_content':
                self.newsContent = argument
            if str(field) == 'news_link':
                self.newsLink = argument
            if str(field) == 'news_resource':
                self.newsResource = argument
            if str(field) == 'news_date':
                self.newsDate = argument
            if str(field) == 'published_time':
                self.publishedTime = argument


class NewsService():

    @staticmethod
    def _criteria_builder(news_criteria):
        clauses = []
        if news_criteria.id:
            clauses.append(News.id == news_criteria.id)
        if news_criteria.keItem:
            clauses.append(News.ke_item == news_criteria.keItem)
        if news_criteria.newsLink:
            clauses.append(News.news_link == news_criteria.newsLink)
        return clauses
    @staticmethod
    def _update_builder(news_criteria):
        clauses = {}
        if news_criteria.keItem:
           clauses[News.ke_item] = news_criteria.keItem
        if news_criteria.newsName:
            clauses[News.news_name] =news_criteria.newsName
        if news_criteria.newsLable:
            clauses[News.news_lable] = news_criteria.newsLable
        if news_criteria.newsContent:
            clauses[News.news_content] = news_criteria.newsContent
        if news_criteria.newsLink:
            clauses[News.news_link] = news_criteria.newsLink
        if news_criteria.newsResource:
            clauses[News.news_resource] = news_criteria.newsResource
        if news_criteria.newsDate:
            clauses[News.news_date] = news_criteria.newsDate
        return clauses
    @staticmethod
    def _news_builder(news_criteria):
        news = News()
        if news_criteria.keItem:
            news.ke_item=news_criteria.keItem
        if news_criteria.newsLable:
            news.news_lable=news_criteria.newsLable
        if news_criteria.newsName:
            news.news_name=news_criteria.newsName
        if news_criteria.newsContent:
            news.news_content=news_criteria.newsContent
        if news_criteria.newsLink:
            news.news_link=news_criteria.newsLink
        if news_criteria.newsResource:
            news.news_resource = news_criteria.newsResource
        if news_criteria.newsDate:
            news.news_date=news_criteria.newsDate
        if news_criteria.publishedTime:
            news.published_time=news_criteria.publishedTime
        return news

    @staticmethod
    def _newsCriteria_builder(news):
        news_criteria = NewsCriteria()
        if news.ke_item:
            news_criteria.keItem=news.ke_item
        if news.news_lable:
            news_criteria.newsLable=news.news_lable
        if news.news_name:
            news_criteria.newsName=news.news_name
        if news.news_content:
            news_criteria.newsContent=news.news_content
        if news.news_link:
            news_criteria.newsLink=news.news_link
        if news.news_resource:
            news_criteria.newsResource = news.news_resource
        if news.news_date:
            news_criteria.newsDate=news.news_date
        if news.published_time:
            news_criteria.publishedTime=news.published_time
        if news.id:
            news_criteria.id=news.id
        return news_criteria

    @staticmethod
    def findall(news_criteria, session):
        # Build clauses for session filter
        clauses = NewsService._criteria_builder(news_criteria)
        # Query News and filter according to clauses, use all() function to return as list
        queryResult = session.query(News).filter(*clauses).all()
        if queryResult and len(queryResult)>0:
            aa=[]
            for result in queryResult:
                criteria=NewsService._newsCriteria_builder(result)
                aa.append(criteria)
            return aa
        return None

    @staticmethod
    def findOne(news_criteria, session):
        # Build clauses for session filter
        clauses = NewsService._criteria_builder(news_criteria)
        # Query News and filter according to clauses, use all() function to return as list
        queryOne = session.query(News).filter(*clauses).one()
        criteria = NewsService._newsCriteria_builder(queryOne)
        return criteria

    @staticmethod
    def add(news_criteria, session):
        query = NewsService.findOne(news_criteria,session)
        if query:
            return 0
        else:
            news = NewsService._news_builder(news_criteria)
            session.add(news)
            session.commit()
        return 1

    @staticmethod
    def modify(news_criteria,session):
        clasuses=NewsService._update_builder(news_criteria)
        r=session.query(News).filter(News.id==news_criteria.id).update(clasuses)
        return r


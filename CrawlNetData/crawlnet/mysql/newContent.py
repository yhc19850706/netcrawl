from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table, Column,MetaData
from sqlalchemy.sql.sqltypes import Integer, VARCHAR, TEXT,DATE

Base = declarative_base()
metadata = MetaData()
class NewsContent(Base):
    __table__ =Table('news_content',
                     Base.metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('WEBSITE_ID', Integer),
                     Column('CRAWL_URL', VARCHAR(100)),
                     Column('NEWS_NAME', VARCHAR(100)),
                     Column('NEWS_URL', VARCHAR(100)),
                     Column('NEWS_IMAGE', VARCHAR(100)),
                     Column('NEWS_DESC', TEXT),
                     Column('KEYWORDS', VARCHAR(100)),
                     Column('PUBLISH_TIME', DATE),
                     Column('NEWS_RESOURCE',VARCHAR(50)),
                     Column('NEWS_AUTHOR',VARCHAR(50)),
                     Column('COMMENT_NUM',Integer),
                     Column('READ_NUM',Integer))
class NewsCriteria():
    def __init__(self, **kwargs):
        self.id = None
        self.website_id = None
        self.crawl_url = None
        self.news_name = None
        self.news_url = None
        self.news_image = None
        self.news_desc = None
        self.keywords = None
        self.publish_time = None
        self.news_resource = None
        self.news_author = None
        self.comment_num = None
        self.read_num = None

        for field, argument in kwargs.items():
            if str(field) == 'website_id':
                self.website_id = argument
            if str(field) == 'crawl_url':
                self.crawl_url = argument
            if str(field) == 'news_name':
                self.news_name = argument
            if str(field) == 'news_name':
                self.news_name = argument
            if str(field) == 'news_url':
                self.news_url = argument
            if str(field) == 'news_image':
                self.news_image = argument
            if str(field) == 'news_desc':
                self.news_desc = argument
            if str(field) == 'keywords':
                self.keywords = argument
            if str(field) == 'publish_time':
                self.publish_time = argument
            if str(field) == 'news_resource':
                self.news_resource = argument
            if str(field) == 'news_author':
                self.news_author = argument
            if str(field) == 'comment_num':
                self.comment_num = argument
            if str(field) == 'read_num':
                self.read_num = argument

class NewsService():

    @staticmethod
    def _criteria_builder(news_criteria):
        clauses = []
        if news_criteria.id:
            clauses.append(NewsContent.id == news_criteria.id)
        if news_criteria.news_name:
            clauses.append(NewsContent.NEWS_NAME == news_criteria.news_name)
        if news_criteria.news_url:
            clauses.append(NewsContent.NEWS_URL == news_criteria.news_url)
        return clauses

    @staticmethod
    def _news_builder(news_criteria):
        news = NewsContent()
        if news_criteria.news_name:
            news.NEWS_NAME = news_criteria.news_name
        if news_criteria.news_url:
            news.NEWS_URL = news_criteria.news_url
        if news_criteria.website_id:
            news.WEBSITE_ID=news_criteria.website_id
        if news_criteria.crawl_url:
            news.CRAWL_URL=news_criteria.crawl_url
        if news_criteria.news_image:
            news.NEWS_IMAGE=news_criteria.news_image
        if news_criteria.news_desc:
            news.NEWS_DESC=news_criteria.news_desc
        if news_criteria.keywords:
            news.KEYWORDS = news_criteria.keywords
        if news_criteria.publish_time:
            news.PUBLISH_TIME=news_criteria.publish_time
        if news_criteria.news_resource:
            news.NEWS_RESOURCE=news_criteria.news_resource
        if news_criteria.news_author:
            news.NEWS_AUTHOR=news_criteria.news_author
        if news_criteria.comment_num:
            news.COMMENT_NUM=news_criteria.comment_num
        if news_criteria.read_num:
            news.READ_NUM=news_criteria.read_num
        return news

    @staticmethod
    def _newsCriteria_builder(news_criteria):
        news= NewsCriteria()
        if news_criteria.NEWS_NAME:
            news.news_name = news_criteria.NEWS_NAME
        if news_criteria.NEWS_URL:
            news.news_url = news_criteria.NEWS_URL
        if news_criteria.WEBSITE_ID:
            news.website_id=news_criteria.WEBSITE_ID
        if news_criteria.CRAWL_URL:
            news.crawl_url=news_criteria.CRAWL_URL
        if news_criteria.NEWS_IMAGE:
            news.news_image=news_criteria.NEWS_IMAGE
        if news_criteria.NEWS_DESC:
            news.NEWS_DESC=news_criteria.NEWS_DESC
        if news_criteria.KEYWORDS:
            news.keywords = news_criteria.KEYWORDS
        if news_criteria.PUBLISH_TIME:
            news.publish_time = news_criteria.PUBLISH_TIME
        if news_criteria.NEWS_RESOURCE:
            news.news_resource = news_criteria.NEWS_RESOURCE
        if news_criteria.NEWS_AUTHOR:
            news.news_author = news_criteria.NEWS_AUTHOR
        if news_criteria.COMMENT_NUM:
            news.comment_num = news_criteria.COMMENT_NUM
        if news_criteria.READ_NUM:
            news.read_num = news_criteria.READ_NUM
        return news

    @staticmethod
    def findall(news_criteria, session):
        # Build clauses for session filter
        clauses = NewsService._criteria_builder(news_criteria)
        # Query News and filter according to clauses, use all() function to return as list
        queryResult = session.query(NewsContent).filter(*clauses).all()
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
        queryOne = session.query(NewsContent).filter(*clauses).one()
        criteria = NewsService._newsCriteria_builder(queryOne)
        return criteria

    @staticmethod
    def add(news_criteria, session):
        query = NewsService.findall(news_criteria,session)
        if query and len(query)>0:
            return 0
        else:
            news = NewsService._news_builder(news_criteria)
            session.add(news)
            session.commit()
        return 1

    @staticmethod
    def modify(news_criteria,session):
        clasuses=NewsService._update_builder(news_criteria)
        r=session.query(NewsContent).filter(NewsContent.id==news_criteria.id).update(clasuses)
        return r


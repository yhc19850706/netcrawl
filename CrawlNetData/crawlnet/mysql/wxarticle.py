from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table, Column,MetaData
from sqlalchemy.sql.sqltypes import Integer, VARCHAR, TEXT,DATE
from sqlalchemy.orm.exc import NoResultFound
Base = declarative_base()
metadata = MetaData()
class WxArticle(Base):
    __table__ =Table('wx_public_no',
                     Base.metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('article_name', VARCHAR(256)),
                     Column('article_content', TEXT),
                     Column('article_link', VARCHAR(256)),
                     Column('link_md5',VARCHAR(128)),
                     Column('public_no', VARCHAR(128)),
                     Column('public_no_link', VARCHAR(256)),
                     Column('published_time', DATE))

class ArticleCriteria():
    def __init__(self, **kwargs):
        self.id = None
        self.article_name = None
        self.article_content = None
        self.article_link = None
        self.public_no = None
        self.public_no_link = None
        self.published_time=None

        for field, argument in kwargs.items():
            if str(field) == 'id':
                self.id = argument
            if str(field) == 'article_name':
                self.article_name = argument
            if str(field) == 'article_content':
                self.article_content = argument
            if str(field) == 'article_link':
                self.article_link = argument
            if str(field) == 'link_md5':
                self.link_md5 = argument
            if str(field) == 'public_no':
                self.public_no = argument
            if str(field) == 'public_no_link':
                self.public_no_link = argument
            if str(field) == 'published_time':
                self.published_time = argument


class ArticleService():

    @staticmethod
    def _criteria_builder(article_criteria):
        clauses = []
        if article_criteria.id:
            clauses.append(WxArticle.id == article_criteria.id)
        if article_criteria.article_name:
            clauses.append(WxArticle.article_name == article_criteria.article_name)
        if article_criteria.public_no:
            clauses.append(WxArticle.public_no == article_criteria.public_no)
        return clauses

    @staticmethod
    def _article_builder(article_criteria):
        article = WxArticle()
        if article_criteria.article_name:
            article.article_name=article_criteria.article_name
        if article_criteria.article_content:
            article.article_content=article_criteria.article_content
        if article_criteria.article_link:
            article.article_link=article_criteria.article_link
        if article_criteria.link_md5:
            article.link_md5=article_criteria.link_md5
        if article_criteria.public_no:
            article.public_no=article_criteria.public_no
        if article_criteria.public_no_link:
            article.public_no_link=article_criteria.public_no_link
        if article_criteria.published_time:
            article.published_time = article_criteria.published_time
        return article

    @staticmethod
    def _articleCriteria_builder(article_criteria):
        article = ArticleCriteria()
        if article_criteria.article_name:
            article.article_name=article_criteria.article_name
        if article_criteria.article_content:
            article.article_content=article_criteria.article_content
        if article_criteria.article_link:
            article.article_link=article_criteria.article_link
        if article_criteria.link_md5:
            article.link_md5=article_criteria.link_md5
        if article_criteria.public_no:
            article.public_no=article_criteria.public_no
        if article_criteria.public_no_link:
            article.public_no_link=article_criteria.public_no_link
        if article_criteria.published_time:
            article.published_time = article_criteria.published_time
        if article.id:
            article.id=article_criteria.id
        return article

    @staticmethod
    def findall(article_criteria, session):
        # Build clauses for session filter
        clauses = ArticleService._criteria_builder(article_criteria)
        # Query article and filter according to clauses, use all() function to return as list
        queryResult = session.query(WxArticle).filter(*clauses).all()
        if queryResult and len(queryResult)>0:
            aa=[]
            for result in queryResult:
                criteria=ArticleService._articleCriteria_builder(result)
                aa.append(criteria)
            return aa
        return None

    @staticmethod
    def findOne(article_criteria, session):
        # Build clauses for session filter
        clauses = ArticleService._criteria_builder(article_criteria)
        # Query article and filter according to clauses, use all() function to return as list
        try:
            queryOne = session.query(WxArticle).filter(*clauses).one()
            criteria = ArticleService._articleCriteria_builder(queryOne)
            return criteria
        except NoResultFound as e:
             print(e)
             return None

    @staticmethod
    def add(article_criteria, session):
        query = ArticleService.findOne(article_criteria,session)
        if query:
            return 0
        else:
            article = ArticleService._article_builder(article_criteria)
            session.add(article)
            session.commit()
        return 1


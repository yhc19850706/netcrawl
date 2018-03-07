from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Table, Column,MetaData
from sqlalchemy.sql.sqltypes import Integer, VARCHAR, TEXT,DATE

Base = declarative_base()
metadata = MetaData()
class jianshu_blog(Base):
    __table__ =Table('jianshu_blog',
                     Base.metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('main_topic', VARCHAR(64)),
                     Column('topic_link', VARCHAR(256)),
                     Column('blog_name', VARCHAR(256)),
                     Column('blog_content', TEXT),
                     Column('blog_link', VARCHAR(256)),
                     Column('published_time', DATE),
                     Column('blog_author',VARCHAR(128)),
                     Column('author_link',VARCHAR(256)),
                     Column('read_num', Integer),
                     Column('comment_num', Integer),
                     Column('like_num', Integer),
                     Column('support_num', Integer)
                     )
class JianshuBlog():
    def __init__(self, **kwargs):
        self.id = None
        self.main_topic = None
        self.topic_link=None
        self.blog_name = None
        self.blog_content = None
        self.blog_link = None
        self.published_time = None
        self.blog_author=None
        self.author_link=None
        self.read_num = None
        self.comment_num = None
        self.like_num=None
        self.support_num=None

        for field, argument in kwargs.items():
            if str(field) == 'id':
                self.id = argument
            if str(field) == 'main_topic':
                self.main_topic = argument
            if str(field) == 'topic_link':
                self.topic_link = argument
            if str(field) == 'blog_name':
                self.blog_name = argument
            if str(field) == 'blog_content':
                self.blog_content = argument
            if str(field) == 'blog_link':
                self.blog_link = argument
            if str(field) == 'published_time':
                self.published_time = argument
            if str(field) == 'author_link':
                self.author_link = argument
            if str(field) == 'blog_author':
                self.blog_author = argument
            if str(field) == 'read_num':
                self.read_num = argument
            if str(field) == 'comment_num':
                self.comment_num = argument
            if str(field) == 'like_num':
                self.like_num = argument
            if str(field) == 'support_num':
                self.support_num = argument


class JianshuBlogService():

    @staticmethod
    def _criteria_builder(jsblog):
        clauses = []
        if jsblog.id:
            clauses.append(jianshu_blog.id == jsblog.id)
        if jsblog.blog_name:
            clauses.append(jianshu_blog.blog_name == jsblog.blog_name)
        if jsblog.blog_link:
            clauses.append(jianshu_blog.blog_link == jsblog.blog_link)
        return clauses

    @staticmethod
    def _news_builder(jsblog):
        js_blog=jianshu_blog()
        if jsblog.main_topic:
            js_blog.main_topic=jsblog.main_topic
        if jsblog.topic_link:
            js_blog.topic_link=jsblog.topic_link
        if jsblog.blog_name:
            js_blog.blog_name=jsblog.blog_name
        if jsblog.blog_content:
            js_blog.blog_content=jsblog.blog_content
        if jsblog.blog_link:
            js_blog.blog_link=jsblog.blog_link
        if jsblog.published_time:
            js_blog.published_time=jsblog.published_time
        if jsblog.blog_author:
            js_blog.blog_author=jsblog.blog_author
        if jsblog.author_link:
            js_blog.author_link=jsblog.author_link
        if jsblog.read_num:
            js_blog.read_num=jsblog.read_num
        if jsblog.comment_num:
            js_blog.comment_num=jsblog.comment_num
        if jsblog.like_num:
            js_blog.like_num=jsblog.like_num
        if jsblog.support_num:
            js_blog.support_num=jsblog.support_num
        return js_blog

    @staticmethod
    def _newsCriteria_builder(jsblog):
        js_blog=JianshuBlog()
        if jsblog.id:
            js_blog.id=jsblog.id
        if jsblog.main_topic:
            js_blog.main_topic=jsblog.main_topic
        if jsblog.topic_link:
            js_blog.topic_link=jsblog.topic_link
        if jsblog.blog_name:
            js_blog.blog_name=jsblog.blog_name
        if jsblog.blog_content:
            js_blog.blog_content=jsblog.blog_content
        if jsblog.blog_link:
            js_blog.blog_link=jsblog.blog_link
        if jsblog.published_time:
            js_blog.published_time=jsblog.published_time
        if jsblog.blog_author:
            js_blog.blog_author=jsblog.blog_author
        if jsblog.author_link:
            js_blog.author_link=jsblog.author_link
        if jsblog.read_num:
            js_blog.read_num=jsblog.read_num
        if jsblog.comment_num:
            js_blog.comment_num=jsblog.comment_num
        if jsblog.like_num:
            js_blog.like_num=jsblog.like_num
        if jsblog.support_num:
            js_blog.support_num=jsblog.support_num
        return js_blog

    @staticmethod
    def findall(news_criteria, session):
        # Build clauses for session filter
        clauses = JianshuBlogService._criteria_builder(news_criteria)
        # Query News and filter according to clauses, use all() function to return as list
        queryResult = session.query(jianshu_blog).filter(*clauses).all()
        if queryResult and len(queryResult)>0:
            aa=[]
            for result in queryResult:
                criteria=JianshuBlogService._newsCriteria_builder(result)
                aa.append(criteria)
            return aa
        return None

    @staticmethod
    def findOne(jsblog, session):
        # Build clauses for session filter
        clauses = JianshuBlogService._criteria_builder(jsblog)
        # Query News and filter according to clauses, use all() function to return as list
        queryOne = session.query(jianshu_blog).filter(*clauses).first()
        if queryOne:
           criteria = JianshuBlogService._newsCriteria_builder(queryOne)
           return criteria
        return None

    @staticmethod
    def add(jsblog, session):
        query = JianshuBlogService.findOne(jsblog,session)
        if query:
            return 0
        else:
            news = JianshuBlogService._news_builder(jsblog)
            session.add(news)
            session.commit()
        return 1


from pyutils.ContextUtil import ContextUtil
from  mysql.models import *
from mysql.SqlOperate import SqlOperate
import re
import json
import time
def crawlQuickNews():
    website='https://36kr.com/api/newsflash'
    proxy_address = {'http':'http://122.72.18.34:80'}
    headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    contextUtil = ContextUtil(proxy_address, website, headers,3000)
    res=contextUtil.get_crawler({'per_page': 40})
    if res:
        selector = json.loads(res.text)
        items=selector["data"]["items"]
        if items and len(items)>0:
            operate = SqlOperate()
            for item in items:
                news = NewsCriteria()
                news.keItem = '7*24快讯'
                news.newsName = item['title']
                news.newsContent = item['description']
                news.newsLink = item['news_url']
                resource=re.findall(r'[^（）]+', item['description'])
                if resource and len(resource)>1:
                    news.newsResource = resource[len(resource)-1]
                news.newsLable = item['column']['name']
                news.publishedTime = item['published_at']
                news.newsDate = item['published_at']
                NewsService.add(news,operate.session)

def crawlMainPage():
    website='https://36kr.com/api/search-column/mainsite'
    proxy_address = {'http':'http://122.72.18.34:80'}
    headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    contextUtil = ContextUtil(proxy_address, website, headers,3000)
    res=contextUtil.get_crawler({'per_page': 40,'page': 1})
    if res:
        selector = json.loads(res.text)
        items=selector["data"]["items"]
        if items and len(items)>0:
            operate = SqlOperate()
            for item in items:
                news = NewsCriteria()
                news.keItem = '主页'
                news.newsName = item['title']
                news.newsContent = item['summary']
                news.newsLink = 'http://36ke.com/p'+str(item['id'])+'.html'
                news.newsLable = item['extraction_tags']
                news.publishedTime = time.strptime(item['published_at'], "%Y-%m-%dT%H:%M:%S+08:00")
                news.newsDate = time.strptime(item['published_at'], "%Y-%m-%dT%H:%M:%S+08:00")
                NewsService.add(news,operate.session)

#crawlQuickNews()
#crawlMainPage()
print('end....')

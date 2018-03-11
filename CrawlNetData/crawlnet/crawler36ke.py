from pyutils.ContextUtil import ContextUtil
from  mysql.models import *
from mysql.SqlOperate import SqlOperate
from mysql.newContent import *
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
                resource=re.findall(r'[^（）]+', item['description'])
                criteria=NewsCriteria()
                criteria.website_id = 11
                criteria.crawl_url = 'https://36kr.com/api/newsflash'
                criteria.news_name = item['title']
                criteria.news_url = item['news_url']
                criteria.keywords = item['column']['name']
                criteria.news_desc=item['description']
                criteria.publish_time = item['published_at']
                if resource and len(resource)>1:
                    criteria.news_resource = resource[len(resource)-1]
                NewsService.add(criteria,operate.session)

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
                criteria=NewsCriteria()
                criteria.website_id = 12
                criteria.crawl_url = website
                criteria.news_name = item['title']
                criteria.news_url = 'http://36ke.com/p'+str(item['id'])+'.html'
                criteria.keywords = item['extraction_tags']
                criteria.news_desc=item['summary']
                criteria.publish_time = time.strptime(item['published_at'], "%Y-%m-%dT%H:%M:%S+08:00")
                NewsService.add(criteria,operate.session)

#crawlQuickNews()
#crawlMainPage()
print('end....')

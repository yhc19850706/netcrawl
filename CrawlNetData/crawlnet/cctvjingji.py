from pyutils.ContextUtil import ContextUtil
from lxml import etree
import requests
from mysql.SqlOperate import SqlOperate
from mysql.newContent import *
from datetime import datetime

def crawlcctv2():
    operate = SqlOperate()
    website='http://jingji.cctv.com/caijing/index.shtml'
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res.text)[0]))
        zixuns=selector.xpath('//*[@id="SUBD1510297095495251"]/div/ul/li/a')
        if zixuns and len(zixuns)>0:
            for zx in zixuns:
                title_name=zx.text
                link=zx.attrib['href']
                newsinfo=crawlurl(link)
                criteria=NewsCriteria()
                criteria.website_id = 3
                criteria.crawl_url = 'http://jingji.cctv.com/caijing/index.shtml'
                criteria.news_name = title_name
                criteria.news_url = link
                if newsinfo:
                    if newsinfo.get('publishtime'):
                        criteria.publish_time= newsinfo['publishtime']
                    if newsinfo.get('laiyuan'):
                        criteria.news_resource = newsinfo['laiyuan']
                NewsService.add(criteria,operate.session)


    newsjson=ContextUtil('http://jingji.cctv.com/caijing/data/index.json')
    res=newsjson.get_crawler_noproxy({})
    if res:
        jsonArry=res.json()['rollData']
        if jsonArry and len(jsonArry)>0:
            for news in jsonArry:
                title_name=news['title']
                link=news['url']
                desc=news['description']
                lables=news['content']
                publishtime=news['dateTime']
                newsinfo=crawlurl(link)
                criteria=NewsCriteria()
                criteria.website_id = 3
                criteria.crawl_url = 'http://jingji.cctv.com/caijing/data/index.json'
                criteria.news_name = title_name
                criteria.news_url = link
                criteria.keywords = lables
                criteria.news_desc=desc
                criteria.publish_time = publishtime
                if newsinfo:
                    if newsinfo.get('laiyuan'):
                        criteria.news_resource = newsinfo['laiyuan']
                NewsService.add(criteria,operate.session)
    return 'ok'


def crawlurl(url):
    print(url)
    newsinfo={}
    contextUtil = ContextUtil(url)
    res=contextUtil.get_crawler_noproxy({})
    try:
        
         if res:
             selector = etree.HTML(res.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res.text)[0]))
             subst = selector.xpath('//*[@class="function"]/span[1]/i/a')
             substtext=selector.xpath('//*[@class="function"]/span[1]/i/text()')
             if subst and substtext and len(substtext)>1:
                newsinfo['laiyuan'] = subst[0].text
                newsinfo["publishtime"]=datetime.strptime(substtext[1].replace(' ',''),'%Y年%m月%d日%H:%M').strftime('%Y-%m-%d %H:%M')

             else:
                 if substtext and len(substtext) == 1:
                     newsinfo['laiyuan'] = substtext[0]
             return newsinfo
    except OSError as err:
           print("craw error"+err)
           return None
    return None

crawlcctv2()
#print('end......')
#crawlurl('http://jingji.cctv.com/2018/02/12/ARTImBsubbP26oZPEHZa13AR180212.shtml')
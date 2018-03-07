from pyutils.ContextUtil import ContextUtil
from lxml import etree
from datetime import datetime
from mysql.SqlOperate import SqlOperate
from mysql.newContent import *
import requests
import json

def crawlsport():
    operate = SqlOperate()
    website='http://sports.sina.com.cn/'
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        res.encoding = 'utf-8'
        selector = etree.HTML(res.text)
        tytopwrap=selector.xpath('//*[@id="ty-top-ent0"]/div')
        if tytopwrap and len(tytopwrap)>0:
            for tytop in tytopwrap:
                h3a=tytop.xpath('./h3/a');
                if h3a and len(h3a)>0:
                    for redty in h3a:
                        title_name=redty.text
                        link=redty.attrib['href']
                        criteria=NewsCriteria()
                        criteria.website_id = 5
                        criteria.crawl_url = website
                        criteria.news_name = title_name
                        criteria.news_url = link
                        NewsService.add(criteria,operate.session)
                pas=tytop.xpath('./div/div[2]/p/a');
                if pas and len(pas)>0:
                    for pa in pas:
                        title_name=pa.text
                        link=pa.attrib['href'].replace('//','http://')
                        newsinfo=crawlurl(link)
                        criteria=NewsCriteria()
                        criteria.website_id = 5
                        criteria.crawl_url = website
                        criteria.news_name = title_name
                        criteria.news_url = link
                        if newsinfo:
                            if newsinfo.get('publishtime'):
                                criteria.publish_time= newsinfo['publishtime']
                            if newsinfo.get('laiyuan'):
                                criteria.news_resource = newsinfo['laiyuan']
                            if newsinfo.get('zuozhe'):
                                criteria.news_author=newsinfo['zuozhe']
                        NewsService.add(criteria,operate.session)

    return 'ok'


def crawlurl(url):
    print(url)
    newsinfo={}
    contextUtil = ContextUtil(url)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        res.encoding = 'utf-8'
        selector = etree.HTML(res.text)
        ptime = selector.xpath('//*[@id="top_bar"]/div/div[2]/span')
        if ptime and ptime[0].text:
            newsinfo["publishtime"]=datetime.strptime(ptime[0].text,'%Y年%m月%d日 %H:%M').strftime('%Y-%m-%d %H:%M')
        laiyuan=selector.xpath('//*[@id="artibody"]/p[1]')
        if laiyuan and laiyuan[0].text and '来源' in laiyuan[0].text:
            newsinfo['laiyuan'] = laiyuan[0].text
        zuozhe=selector.xpath('//*[@id="artibody"]/p[2]')
        if zuozhe and zuozhe[0].text and '作者' in zuozhe[0].text:
            newsinfo['zuozhe']=zuozhe[0].text
        return newsinfo
    return None

crawlsport()
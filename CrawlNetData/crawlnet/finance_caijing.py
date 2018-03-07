from pyutils.ContextUtil import ContextUtil
from lxml import etree
from mysql.newContent import *
import requests
from mysql.SqlOperate import SqlOperate

#时事：25950 财经：2591 思想：2592 生活2593 默认首页
def crawlcaijingfinance():
    website='http://finance.caijing.com.cn/index.html'
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res.text)[0]))
        headnews=selector.xpath('//*[@class="head_news"]/li/a')
        operate = SqlOperate()
        if headnews and len(headnews)>0:
            for zx in headnews:
                title_name=zx.text
                link=zx.attrib['href']
                print(title_name)
                print(link)
                print('-------------')
                criteria=NewsCriteria()
                criteria.website_id = 1
                criteria.crawl_url = website
                criteria.news_name = title_name
                criteria.news_url = link
                NewsService.add(criteria,operate.session)
        mainnews=selector.xpath('//*[@id="main"]/section[1]/div')
        if mainnews and len(mainnews):
            for news in mainnews:
                title_name=news.xpath('./div/a')
                lables=news.xpath('./div/div/span[@class="from_cj"]')
                lablelist=[]
                if lables and len(lables):
                    for lable in lables:
                        lablelist.append(lable.text)
                publishtime=news.xpath('./div/div/span[@class="list_time"]')[0].text
                print(title_name[0].text)
                print(title_name[0].attrib['href'])
                print(str(lablelist))
                print(publishtime)
                criteria=NewsCriteria()
                criteria.website_id = 1
                criteria.crawl_url = website
                criteria.news_name = title_name[0].text
                criteria.news_url = title_name[0].attrib['href']
                criteria.keywords = str(lablelist)
                criteria.publish_time = publishtime
                NewsService.add(criteria,operate.session)


def crawlcaijingtech():
    website='http://tech.caijing.com.cn/internet/index.shtml'
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res.text)[0]))
        headnews=selector.xpath('//*[@class="ydhl_head"]/div')
        operate = SqlOperate()
        if headnews and len(headnews)>0:
            for zx in headnews:
                title_name=zx.xpath('./a')
                if len(title_name) == 0:
                   break
                link=title_name[0].attrib['href']
                content=zx.xpath('./p')
                newsinfo=crawlurl(link)
                criteria=NewsCriteria()
                criteria.website_id = 1
                criteria.crawl_url = website
                criteria.news_name = title_name[0].text
                criteria.news_url = link
                criteria.news_desc = content[0].text
                if newsinfo:
                    if newsinfo.get('publishtime'):
                        criteria.publish_time= newsinfo['publishtime']

                    if newsinfo.get('zuozhe'):
                        criteria.news_author=newsinfo['zuozhe']

                    if newsinfo.get('laiyuan'):
                        criteria.news_resource = newsinfo['laiyuan']
        mainnews=selector.xpath('//*[@id="main"]/section[1]/div')
        if mainnews and len(mainnews):
            for news in mainnews:
                img=news.xpath('./a/img')
                title_name=news.xpath('./div/a')
                if title_name == None:
                    break
                content=news.xpath('./div/p')
                lables=news.xpath('./div/div[2]/a')
                lablelist=[]
                if lables and len(lables):
                    for lable in lables:
                        lablelist.append(lable.text)
                publishtime=news.xpath('./div/div[1]/span')[0].text
                comments=news.xpath('./div/div[1]/div[1]/span')[0].text
                newsinfo=crawlurl(title_name[0].attrib['href'])
                criteria=NewsCriteria()
                criteria.website_id = 1
                criteria.crawl_url = website
                criteria.news_name = title_name[0].text
                criteria.news_url = title_name[0].attrib['href']
                criteria.keywords = str(lablelist)
                #criteria.publish_time = publishtime
                criteria.comment_num = comments
                criteria.news_desc = content[0].text
                if img:
                    criteria.news_image=img[0].attrib['src']
                else:
                    criteria.news_image=''
                if newsinfo:
                    if newsinfo.get('publishtime'):
                        criteria.publish_time= newsinfo['publishtime']
                    if newsinfo.get('zuozhe'):
                        criteria.news_author=newsinfo['zuozhe']
                    if newsinfo.get('laiyuan'):
                        criteria.news_resource = newsinfo['laiyuan']
                NewsService.add(criteria,operate.session)


def crawlurl(url):
    print(url)
    newsinfo={}
    contextUtil = ContextUtil(url)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res.text)[0]))
        subst=selector.xpath('//*[@class="sub_lt"]/span')
        if subst and len(subst)>0:
            for s in subst:
                if s.attrib['class']=='news_time':
                    newsinfo["publishtime"]=s.text
                if s.attrib['class']=='news_name' and '作者' in s.text:
                    newsinfo['zuozhe']=s.text
                if s.attrib['class']=='news_name' and '来源' in s.text:
                    newsinfo['laiyuan']=s.text.replace('来源：',"")
        return newsinfo
    return None
#crawlcaijingtech()

crawlcaijingfinance()
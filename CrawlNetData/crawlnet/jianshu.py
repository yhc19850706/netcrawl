from pyutils.ContextUtil import ContextUtil
from  mysql.jsblosModel import *
from mysql.SqlOperate import SqlOperate
from lxml import etree
from weixin.wxml import Wxml
import time

def crawljsmainpage():
    website='https://www.jianshu.com'
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler({'utm_medium': 'index-collections', 'utm_source': 'desktop'})
    if res:
        selector = etree.HTML(res.text)
        contents = selector.xpath('//*[@id="list-container"]/ul/li')
        if contents and len(contents) > 0:
           operate = SqlOperate()
           wxml=Wxml()
           buffer=''
           friend = wxml.find_friend('殷化程')
           for content in contents:
                msg={}
                txt = content.xpath('./div/p/text()')[0].replace('\n', '').replace(' ', '')
                link = content.xpath('./div/a')
                nickname = content.xpath('./div/div/div/a')
                ptime = content.xpath('./div/div/div/span')
                topic = content.xpath('./div/div[2]/a[1]')
                readnum = content.xpath('./div/div/a[2]/text()')[1].replace('\n', '').replace('\"', '').replace(' ', '')
                commentnum = content.xpath('./div/div/a[3]/text()')[1].replace('\n', '').replace('\"', '').replace(' ', '')
                likenum = content.xpath('./div/div/span[1]/text()')[0].replace('\n', '').replace('\"', '').replace(' ', '')
                suportnum = 0
                suporttab = content.xpath('./div/div/span[2]')
                if suporttab:
                   suportnum = content.xpath('./div/div/span[2]/text()')[0].replace('\n', '').replace('\"', '').replace(' ', '')
                jsblog = JianshuBlog()
                jsblog.main_topic = topic[0].text
                jsblog.topic_link = website+topic[0].attrib['href']
                jsblog.blog_name = link[0].text
                jsblog.blog_content = txt
                jsblog.blog_link = website+link[0].attrib['href']
                jsblog.blog_author = nickname[0].text
                jsblog.published_time = time.strptime(ptime[0].attrib['data-shared-at'], "%Y-%m-%dT%H:%M:%S+08:00")
                jsblog.author_link = website+nickname[0].attrib['href']
                jsblog.read_num = readnum
                jsblog.comment_num = commentnum
                jsblog.like_num = likenum
                jsblog.support_num = suportnum
                JianshuBlogService.add(jsblog,operate.session)
                buffer = buffer+'标题名称:'+jsblog.blog_name+'\n'
                buffer = buffer+'链接地址'+ jsblog.blog_link+'\n \n'
        Wxml.send_txt(friend,str(buffer))

def crawljstopic(topicname, topiclink):
    website='https://www.jianshu.com/'+topiclink
    proxy_address = {'http':'http://122.72.18.34:80'}
    headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    contextUtil = ContextUtil(proxy_address, website, headers,3000)
    res=contextUtil.get_crawler({'utm_medium': 'index-collections', 'utm_source': 'desktop'})
    if res:
        selector = etree.HTML(res.text)
        contents = selector.xpath('//*[@id="list-container"]/ul/li')
        if contents and len(contents) > 0:
            operate = SqlOperate()
            for content in contents:
                txt = content.xpath('./div/p/text()')[0].replace('\n', '').replace(' ', '')
                link = content.xpath('./div/a')
                nickname = content.xpath('./div/div[1]/div/a[1]')
                ptime = content.xpath('./div/div[1]/div/span')
                readnum = content.xpath('./div/div[2]/a[1]/text()')[1].replace('\n', '').replace('\"', '').replace(' ', '')
                commentnum = content.xpath('./div/div[2]/a[2]/text()')[1].replace('\n', '').replace('\"', '').replace(' ', '')
                likenum = content.xpath('./div/div[2]/span[1]/text()')[0].replace('\n', '').replace('\"', '').replace(' ', '')
                suportnum = 0
                suporttab = content.xpath('./div/div[2]/span[2]')
                if suporttab:
                    suportnum = content.xpath('./div/div[2]/span[2]/text()')[0].replace('\n', '').replace('\"', '').replace(' ', '')
                jsblog = JianshuBlog()
                jsblog.main_topic = topicname
                jsblog.topic_link = website+topiclink
                jsblog.blog_name = link[0].text
                jsblog.blog_content = txt
                jsblog.blog_link = website+link[0].attrib['href']
                jsblog.blog_author = nickname[0].text
                jsblog.published_time = time.strptime(ptime[0].attrib['data-shared-at'], "%Y-%m-%dT%H:%M:%S+08:00")
                jsblog.author_link = website+nickname[0].attrib['href']
                jsblog.read_num = readnum
                jsblog.comment_num = commentnum
                jsblog.like_num = likenum
                jsblog.support_num = suportnum
                JianshuBlogService.add(jsblog,operate.session)


crawljsmainpage()
print('end...')

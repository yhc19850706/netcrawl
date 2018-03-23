from pyutils.ContextUtil import ContextUtil
from mysql.wxarticle import *
from lxml import etree
import lxml
import hashlib
import time
import requests
import re
from mysql.SqlOperate import SqlOperate

m=hashlib.md5()
def crawwxsougou():
    website='http://weixin.sogou.com'
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res.text)[0]))
        articles=selector.xpath('//*[@id="pc_0_0"]/li/div[2]')
        if articles and len(articles)>0:
            operate = SqlOperate()
            for article in articles:
                name = article.xpath('./h3/a')
                content = article.xpath('./p')
                link = name[0].attrib['href']
                publicno = article.xpath('./div/a')
                publicnolink = publicno[0].attrib['href']
                publishtime = article.xpath('./div/span')[0].attrib['t']
                criteria=ArticleCriteria()
                criteria.article_name=name[0].text
                m.update(link)
                criteria.article_link=link
                criteria.link_md5=m.hexdigest()
                criteria.article_content=content[0].text
                criteria.public_no=publicno[0].text
                criteria.public_no_link=publicnolink
                criteria.published_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(publishtime)))
                ArticleService.add(criteria,operate.session)

def seachwxsougou(keyword):
    website='http://weixin.sogou.com/weixin'
    contextUtil = ContextUtil(website)
    page=1
    #循环爬取各页的文章链接
    for page in range(1,3+1):
        #分别构建各页的url链接，每次循环构建一次
        url="http://weixin.sogou.com/weixin?type=2&query="+keyword+"&page="+str(page)
        print("url="+url)
        contextUtil = ContextUtil(website)
        res=contextUtil.get_crawler_noproxy({'type':2,'query':keyword,'page':str(page)})
        if res:
            selector = etree.HTML(res.text)
            articles=selector.xpath('//*[@id="main"]/div[4]/ul/li/div[2]')
            if articles and len(articles)>0:
                operate = SqlOperate()
                for article in articles:
                    names = article.xpath('./h3/a/node()')
                    nm='';
                    for name in names:
                        if type(name)==lxml.etree._Element:
                            nm=nm+name.xpath('./text()')[0]
                        else:
                            nm=nm+str(name)
                    link = article.xpath('./h3/a')[0].attrib['href']
                    contents = article.xpath('./p/node()')
                    cn='';
                    for content in contents:
                        if type(content)==lxml.etree._Element:
                            cn=cn+content.xpath('./text()')[0]
                        else:
                            cn=cn+str(content)
                    publicno = article.xpath('./div/a')
                    publicnolink = publicno[0].attrib['href']
                    script=article.xpath('./div/span/script/text()')[0]
                    publishtime=re.search('\d+',script).group()
                    criteria=ArticleCriteria()
                    criteria.article_name=nm
                    m.update(link.encode('utf-8'))
                    criteria.article_link=link
                    criteria.link_md5=m.hexdigest()
                    criteria.article_content=cn
                    criteria.public_no=publicno[0].text
                    criteria.public_no_link=publicnolink
                    criteria.published_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(publishtime)))
                    ArticleService.add(criteria,operate.session)

seachwxsougou('美媒体最丢人一天')
print('end.....')

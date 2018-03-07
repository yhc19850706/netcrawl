from pyutils.ContextUtil import ContextUtil
from lxml import etree
from mysql.SqlOperate import SqlOperate
from mysql.newContent import *

#时事：25950 财经：2591 思想：2592 生活2593 默认首页
def crawlpengpai(channel=None):
    operate = SqlOperate()
    website='http://www.thepaper.cn'
    if channel:
        website=website+'/channel_'+str(channel)
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text)
        toutiao_title=selector.xpath('//*[@id="main_lt"]/div[1]/div[2]/div[1]/h2/a')
        toutiao_link=toutiao_title[0].attrib['href']
        toutiao_content=selector.xpath('//*[@id="main_lt"]/div[1]/div[2]/div[1]/p')
        totiao_resource=selector.xpath('//*[@id="main_lt"]/div[1]/div[2]/div[2]/a')
        published_time=selector.xpath('//*[@id="main_lt"]/div[1]/div[2]/div[2]/span[1]')
        ytndxsm=selector.xpath('//*[@id="main_lt"]/div[1]/div[2]/div[2]/span[2]')
        criteria=NewsCriteria()
        criteria.website_id = 3
        criteria.crawl_url = website
        criteria.news_name = toutiao_title[0].text
        criteria.news_url = 'http://www.thepaper.cn/'+toutiao_link
        if ytndxsm and len(ytndxsm) > 0:
           criteria.comment_num = ytndxsm[0].text
        criteria.news_resource=totiao_resource[0].text
        newsinfo=crawlurl(criteria.news_url)
        if newsinfo:
            if newsinfo.get('publishtime'):
                criteria.publish_time= newsinfo['publishtime']
            if newsinfo.get('zuozhe'):
                criteria.news_author = newsinfo['zuozhe']
        NewsService.add(criteria,operate.session)
        contents = selector.xpath('//*[@id="masonryContent"]/div')

        if contents and len(contents) > 0:
            for content in contents:
                toutiao_title = content.xpath('./h2/a')
                toutiao_content = content.xpath('./p')
                totiao_resource = content.xpath('./div[2]/a')
                ytndxsm = content.xpath('./div[2]/span[2]')

                criteria=NewsCriteria()
                criteria.website_id = 3
                criteria.crawl_url = website
                if toutiao_title and len(toutiao_title)==1:
                   criteria.news_name = toutiao_title[0].text
                   criteria.news_url = 'http://www.thepaper.cn/'+toutiao_title[0].attrib['href']
                if ytndxsm and len(ytndxsm) > 0:
                   criteria.comment_num = ytndxsm[0].text
                if totiao_resource and len(totiao_resource)==1:
                   criteria.news_resource=totiao_resource[0].text
                if toutiao_content and len(toutiao_content)==1:
                   criteria.news_desc=toutiao_content[0].text
                newsinfo=crawlurl(criteria.news_url)
                if newsinfo:
                    if newsinfo.get('publishtime'):
                        criteria.publish_time= newsinfo['publishtime']
                    if newsinfo.get('zuozhe'):
                        criteria.news_author = newsinfo['zuozhe']
                NewsService.add(criteria,operate.session)

def crawlpengpaivideo():
    website='http://www.thepaper.cn/channel_26916'
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text)
        videoMain=selector.xpath('//*[@class="video_slide"]/div[1]/div[1]')
        slide_name=videoMain[0].xpath('./li/div/div[1]')
        slide_time=videoMain[0].xpath('./li/div/div[2]')
        totiao_resource=videoMain[0].xpath('./li/div/div[3]/span[1]')
        published_time=videoMain[0].xpath('./li/div/div[3]/span[2]')
        ytndxsm=videoMain[0].xpath('./li/div/div[3]/span[3]')
        print(slide_name[0].text)
        print(slide_time[0].text)
        print(totiao_resource[0].text)
        print(published_time[0].text)
        if ytndxsm and len(ytndxsm) > 0:
            print(ytndxsm[0].text)
        print('---------------------------')
        contents = selector.xpath('//html/body/div[8]/div[3]/li')

        if contents and len(contents) > 0:
            for content in contents:
                slide_time=content.xpath('./div[1]/span')
                link=content.xpath('./a')
                toutiao_title = content.xpath('./a/div')
                toutiao_content = content.xpath('./p')
                totiao_resource = content.xpath('./div[2]/a')
                published_time = content.xpath('./div[2]/span[1]')
                ytndxsm = content.xpath('./div[2]/span[2]')
                if toutiao_title and len(toutiao_title)==1:
                    print(toutiao_title[0].text)
                    print(link[0].attrib['href'])
                if toutiao_content and len(toutiao_content)==1:
                    print(toutiao_content[0].text)
                if totiao_resource and len(totiao_resource)==1:
                    print(totiao_resource[0].text)
                if published_time and len(published_time)==1:
                    print(published_time[0].text)
                if ytndxsm and len(ytndxsm) > 0:
                    print(ytndxsm[0].text)
                if slide_time and len(slide_time) > 0:
                    print(slide_time[0].text)
                print('---------------------------')



def crawlurl(url):
    print(url)
    newsinfo={}
    contextUtil = ContextUtil(url)
    res=contextUtil.get_crawler_noproxy({})
    if res:
        selector = etree.HTML(res.text)
        subst = selector.xpath('//*[@class="news_about"]/p')
        if subst and  len(subst)>1:
            newsinfo["zuozhe"]=subst[0].text
            newsinfo['publishtime']=subst[1].text.replace('\t','').replace('\n','')

        return newsinfo
    return None
#crawlpengpaivideo()

crawlpengpai(25951)
crawlpengpai(25952)
crawlpengpai(25953)
#http://www.thepaper.cn/load_chosen.jsp?nodeids=25949&topCids=1986843,1985260,1986863,1986012,&pageidx=0

#crawlurl('http://www.thepaper.cn/newsDetail_forward_1996369')
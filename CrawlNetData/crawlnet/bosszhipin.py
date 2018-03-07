from pyutils.ContextUtil import ContextUtil
from  mysql.jsblosModel import *
from mysql.SqlOperate import SqlOperate
from lxml import etree
from weixin.wxml import Wxml
import time
from openpyxl import load_workbook
import pandas as pd

def crawboss():
    website='https://www.zhipin.com/c101210100-p100101'
    proxy_address = {'http':'http://115.46.64.105:8123'}
    contextUtil = ContextUtil(website)
    res=contextUtil.get_crawler({})
    if res:
        selector = etree.HTML(res.text)
        joblist = selector.xpath('//*[@id="main"]/div/div[2]/ul/li')
        if joblist and len(joblist) > 0:
            boss = open('boss.txt', 'w')
            jobtitles = []
            wagescope = []
            addresses = []
            workyears = []
            diplomas = []
            companys = []
            companyinfos = []
            rongzis = []
            companynums = []
            publishnames = []
            publishnamejobs = []
            publishtimes = []
            joblinks = []
            works =[]
            for job in joblist:
                job_title=job.xpath('./div/div[1]/h3/a/div[1]')
                job_link='https://www.zhipin.com/'+job.xpath('./div/div[1]/h3/a')[0].attrib['href']
                wage_scope=job.xpath('./div/div[1]/h3/a/span')
                address=job.xpath('./div/div[1]/p')
                work_years=job.xpath('./div/div[1]/p/text()[2]')[0]
                diploma=job.xpath('./div/div[1]/p/text()[3]')[0]
                company=job.xpath('./div/div[2]/div/h3/a')
                company_info=job.xpath('./div/div[2]/div/p')
                com=job.xpath('./div/div[2]/div/p/text()')
                if com and len(com) == 3:
                   rongzi=job.xpath('./div/div[2]/div/p/text()[2]')
                   companynum=job.xpath('./div/div[2]/div/p/text()[3]')
                if com and len(com) == 2:
                    rongzi=job.xpath('未融资')
                    companynum=job.xpath('./div/div[2]/div/p/text()[2]')
                publish_name=job.xpath('./div/div[3]/h3/text()[1]')
                publish_name_job=job.xpath('./div/div[3]/h3/text()[2]')
                publish_time=job.xpath('./div/div[3]/p')
                jobtitles.append(job_title[0].text)
                wagescope.append(wage_scope[0].text)
                addresses.append(address[0].text)
                workyears.append(work_years)
                diplomas.append(diploma)
                companys.append(company[0].text)
                companyinfos.append(company_info[0].text)
                rongzis.append(rongzi)
                companynums.append(companynum)
                publishnames.append(publish_name[0])
                publishnamejobs.append(publish_name_job[0])
                publishtimes.append(publish_time[0].text)
                joblinks.append(job_link)
                dtailUtil = ContextUtil(job_link)
                detail=dtailUtil.get_crawler({})
                workdetail=etree.HTML(detail.text).xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div/text()')
                workinfo=''
                if workdetail and len(workdetail)>0:
                    for work in workdetail:
                        workinfo=workinfo+work+'\n'
                works.append(workinfo)
            writer = pd.ExcelWriter('boss.xlsx')
            df1 = pd.DataFrame(data={'职位':jobtitles,'职位链接地址':joblinks,'岗位描述':works,'工资':wagescope,'公司地址':addresses,'从业时间':workyears,'学历':diplomas,'公司名称':companys,'公司背景':companyinfos,'融资情况':rongzis,'公司规模':companynums,'发布人':publishnames,'发布人岗位':publishnamejobs,'发布时间':publishtimes})
            df1.to_excel(writer,'Sheet1')
            writer.save()


crawboss()
print('end.....')
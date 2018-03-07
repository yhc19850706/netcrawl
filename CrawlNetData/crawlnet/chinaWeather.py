from pyutils.ContextUtil import ContextUtil
from  mysql.jsblosModel import *
from mysql.SqlOperate import SqlOperate
from lxml import etree
from weixin.wxml import Wxml
from xml.parsers.expat import ParserCreate
import requests
import xml.etree.cElementTree as ET

def tody_weather(city_name):
    website='http://wthrcdn.etouch.cn/WeatherApi?city='+city_name
    res = requests.get(website)
    result={}
    encoding=requests.utils.get_encodings_from_content(res.text)
    encode_content = res.content.decode(encoding[0], 'replace').encode('utf-8', 'replace')
    selector = etree.XML(encode_content)
    city=selector.xpath('//city/text()')
    result['城市']=city[0]
    updatetime=selector.xpath('//updatetime/text()')
    result['更新时间']=updatetime[0]
    wendu = selector.xpath('//wendu/text()')
    result['温度'] = wendu
    fengli=selector.xpath('//fengli/text()')
    result['风力']=fengli[0]
    shidu = selector.xpath('//shidu/text()')
    result['湿度']=shidu[0]
    fengxiang = selector.xpath('//fengxiang/text()')
    result['风向']=fengxiang[0]
    sunrise_1 = selector.xpath('//sunrise_1/text()')
    result['日升']=sunrise_1[0]
    sunset_1 = selector.xpath('//sunset_1/text()')
    result['日落']=sunset_1[0]
    aqi = selector.xpath('//aqi/text()')
    result['AQI指数']=aqi[0]
    pm25 = selector.xpath('//pm25/text()')
    result['PM2.5']=pm25[0]
    suggest = selector.xpath('//suggest/text()')
    result['建议']=suggest[0]
    quality = selector.xpath('//quality/text()')
    result['空气质量']=quality[0]
    pm10 = selector.xpath('//pm10/text()')
    result['PM10']=pm10[0]
    result['指数']=""
    zhishus=selector.xpath('//zhishus/zhishu/name')
    values=selector.xpath('//zhishus/zhishu/value')
    details=selector.xpath('//zhishus/zhishu/detail')
    for zhishu in range(len(zhishus)):
        result[zhishus[zhishu].text] = values[zhishu].text+';'+details[zhishu].text
    result['近5日天气情况']=""
    weathers=selector.xpath('//forecast/weather')
    dates=selector.xpath('//forecast/weather/date')
    highs=selector.xpath('//forecast/weather/high')
    lows=selector.xpath('//forecast/weather/low')
    daytypes=selector.xpath('//forecast/weather/day/type')
    dayfxs=selector.xpath('//forecast/weather/day/fengxiang')
    dayfls=selector.xpath('//forecast/weather/day/fengli')
    nighttypes=selector.xpath('//forecast/weather/night/type')
    nightfls=selector.xpath('//forecast/weather/night/fengli')
    nightfxs=selector.xpath('//forecast/weather/night/fengxiang')

    for weather in range(len(weathers)):
        result[dates[weather].text]= '温度:'+lows[weather].text+'_'+highs[weather].text \
                                     + '__白天天气:'+daytypes[weather].text +'_'+dayfxs[weather].text+dayfls[weather].text\
                                     + '__夜晚天气:'+nighttypes[weather].text +'_'+ nightfxs[weather].text+'_'+nightfls[weather].text
    wh=str([result]).replace('\'','').replace(',','\n')
    wxml=Wxml()
    friend = wxml.find_friend('殷化程')
    Wxml.send_txt(friend,str(wh))

tody_weather('北京')



import requests
from requests.auth import HTTPDigestAuth
import json
import random
class ContextUtil(object):
    def __init__(self, website,):
        self.proxy_address = {'http': 'http://124.67.10.191:61234'}
        self.website = website
        self.headers=["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                                 "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
                                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                                 "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                                 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
                                 ]
        self.request_timeout = 3000
        self.req = requests.Session()

    '''request_data 为字典 {'key1': 'value1', 'key2': 'value2'}'''
    def get_crawler(self, request_data):
        try:
            randdom_header=random.choice(self.headers)
            header={'User-Agent':randdom_header}
            r = self.req.get(self.website, params=request_data,
                             headers=header,
                             proxies=self.proxy_address,
                             timeout=self.request_timeout)
            if r.status_code == 200:
                return r
            else:
                return None
        except requests.RequestException as e:
            print(e)
            return None
        except OSError as err:
            print("craw error"+err)
            return None

    def get_crawler_noproxy(self, request_data):
        try:
            randdom_header=random.choice(self.headers)
            header={'User-Agent':randdom_header}
            r = self.req.get(self.website, params=request_data,
                             headers=header,

                             timeout=self.request_timeout)
            if r.status_code == 200:
                return r
            else:
                return None
        except requests.RequestException as e:
            print(e)
            return None
        except OSError as err:
            print("craw error"+err)
            return None
    '''传递元组
    payload1 = (('key1', 'value1'), ('key1', 'value2'))
    传递字典
    payload2 = {'key1': 'value1', 'key2': 'value2'}
    传递JSON字符串
    payload3 = {'some': 'data'}
    payload=json.dumps(payload3)
    r1 = requests.post('http://httpbin.org/post', data=payload)
    '''
    def post_tuple(self, request_data):
        try:
            randdom_header=random.choice(self.headers)
            header={'User-Agent':randdom_header}
            r = self.req.post(self.website, data=request_data,
                              headers=header,
                              proxies=self.proxy_address,
                              timeout=self.request_timeout)
            if r.status_code == 200:
                return r
            else:
                return None
        except requests.RequestException as e:
            print(e)
            return None
        except OSError as err:
            print("craw error"+err)
            return None


    ''' 传递JSON对象
       payload4 = {'some': 'data'}
       r1 = requests.post('http://httpbin.org/post', json=payload4)
    '''
    def post_tuple(self, request_data):
        try:
            randdom_header=random.choice(self.headers)
            header={'User-Agent':randdom_header}
            r = self.req.post(self.website, json=request_data,
                              headers=header,
                              proxies=self.proxy_address,
                              timeout=self.request_timeout)
            if r.status_code == 200:
                return r
            else:
                return None
        except requests.RequestException as e:
            print(e)
            return None
        except OSError as err:
            print("craw error"+err)
            return None

    '''
    # files = {'file': open('report.xls', 'rb')}

    # 显式地设置文件名，文件类型和请求头

    # files = {'file': ('report.xls', open('report.xls', 'rb'), 'application/vnd.ms-excel', {'Expires': '0'})}

    # 把字符串当做文件来发送

      files = {'file': ('report.xls', 'some,data,to,send\nanother,row,to,send\n')}

      r = requests.post(url, files=files)
    '''
    def upload_file(self,upload_file):
        try:
            randdom_header=random.choice(self.headers)
            header={'User-Agent':randdom_header}
            r = self.req.post(self.website, filse=upload_file,
                              headers=header,
                              proxies=self.proxy_address,
                              timeout=self.request_timeout)
            if r.status_code == 200:
                return r
            else:
                return None
        except requests.RequestException as e:
            print(e)
            return None
        except OSError as err:
            print("craw error"+err)
            return None

    def auth(self,username,password):
        try:
            randdom_header=random.choice(self.headers)
            header={'User-Agent':randdom_header}
            r = self.req.post(self.website,auth=HTTPDigestAuth(username, password),
                              headers=header,
                              proxies=self.proxy_address,
                              timeout=self.request_timeout)
            if r.status_code == 200:
                return r
            else:
                return None
        except requests.RequestException as e:
            print(e)
            return None
        except OSError as err:
            print("craw error"+err)
            return None
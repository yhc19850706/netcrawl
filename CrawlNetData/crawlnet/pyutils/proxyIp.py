# coding=utf-8
# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/  https://www.kuaidaili.com/free/
# 仅仅爬取首页IP地址就足够一般使用

from bs4 import BeautifulSoup
import requests
import random
import telnetlib

def get_kuaiproxy_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        if check_kuaiproxy_telnet(tds[0].text, tds[1].text):
            ip_list.append(tds[0].text + ':' + tds[1].text)
    print(ip_list)
    return ip_list

def get_xiciproxy_list():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    web_data = requests.get('http://www.xicidaili.com/nn/', headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        sd=tds[7].contents[1].attrs['title'].replace('秒','')
        if sd and float(sd)<0.05 and check_xiciproxy_telnet(tds[1].text, tds[2].text):
            ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

#使用telnet验证的方法
def check_xiciproxy_telnet(ip,prot):
    try:
        telnetlib.Telnet(ip, port=str(prot), timeout=0.1)
    except:
        return False
    else:
        return True

def check_kuaiproxy_telnet(ip,prot):
    try:
        telnetlib.Telnet(ip, port=str(prot), timeout=5)
    except:
        return False
    else:
        return True
#使用requests验证的方法
def check_ip_request(proxyIp):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
        }
        req = requests.get('http://www.csdn.net/', headers=headers, proxies={"http":"http://"+proxyIp})

    except:
        return False
    else:
        if req and req.status_code == 200:
            return True


if __name__ == '__main__':
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_xiciproxy_list()
    print(str(ip_list))
    proxies = get_random_ip(ip_list)
    print(proxies)
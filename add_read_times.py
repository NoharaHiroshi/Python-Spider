#! /usr/bin/env python3
from urllib import request
import random
import time

proxy_ip_list = [
    '222.185.110.137:8998',
    '117.145.254.100:8998',
    '113.24.122.43:8118',
    '114.135.45.113:8998',
    '117.37.184.145:80',
    '1.206.186.62:8998',
    '222.88.236.212:9999',
    '121.232.0.43:8118',
    '1.80.117.15:8080',
    '117.62.132.157:8998',
    '183.23.172.79:8998',
]

user_agent_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
]

def Proxy_read(proxy_ip_list, user_agent_list):
    proxy_ip = random.choice(proxy_ip_list)
    print('当前代理ip：%s'%proxy_ip)
    user_agent = random.choice(user_agent_list)
    print('当前代理user_agent：%s'%user_agent)
    sleep_time = random.randint(1,5)
    print('等待时间：%s' %sleep_time)
    time.sleep(sleep_time)
    print('开始获取')
    headers = {
            'Host': 'www.baidu.com',
            'User-Agent': user_agent,
            'Accept': r'application/json, text/javascript, */*; q=0.01',
            'Referer': r'http://www.cnblogs.com/Lands-ljk/p/5589888.html',
            }

    proxy_support = request.ProxyHandler({'http':proxy_ip})
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)

    req = request.Request(r'http://www.cnblogs.com/mvc/blog/ViewCountCommentCout.aspx?postId=5589888',headers=headers)
    try:
        html = request.urlopen(req).read().decode('utf-8')
    except Exception as e:
        print('打开失败！')
    else:
        print('OK!')

if __name__ == '__main__':
    for i in range(10):
        Proxy_read(proxy_ip_list, user_agent_list)
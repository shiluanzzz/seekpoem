# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import os
import random
import time
import requests

def GetUrlContent(url, flag=1):
    flag = int(flag)
    """
    :param url:
    :param flag: flag=1 返回text，flag=2 返回content
    :return:
    """
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]

    headers = {'User-Agent': random.choice(USER_AGENTS)}
    path=os.path.split(os.path.realpath(__file__))[0]
    if path[2]=="\'":
        json_path=path+'\ip.json'
    else:
        json_path=path+'/ip.json'
    with open(json_path, 'r') as file:
        data = json.load(file)
    try:
        r = requests.get(url=url, headers=headers, proxies=random.choice(data))
        r.raise_for_status()
        if flag == 1:
            return r.text
        elif flag == 2:
            return r.content
    except:
        time.sleep(1)
        return GetUrlContent(url, flag)

if __name__ == '__main__':
    path = os.path.split(os.path.realpath(__file__))[0]
    if path[0] == "F":
        json_path = path + '\ip.json'
    else:
        json_path = path + '/ip.json'
    print(json_path)
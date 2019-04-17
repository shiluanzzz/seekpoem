# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json

import pymysql
import traceback
from configparser import ConfigParser

def get_image_json():
    conf = ConfigParser()
    conf.read('db.cfg')
    section = conf.sections()[0]
    host = conf.get(section, 'host')
    db_name = conf.get(section, 'db')
    user = conf.get(section, 'user')
    passwd = conf.get(section, 'passwd')
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor=db.cursor()
    sql="SELECT image FROM Image"
    sql2="SELECT ip_image FROM Image_Poem"
    try:
        cursor.execute(sql2)
        result=cursor.fetchall()
        ll=[]
        for each in result:
            ll.append(each[0])
        result=list(set(ll))
        # print(result)
        with open('image.json','w')as f:
            json.dump(result,f,ensure_ascii=False)
            print("数据写入json成功！")

    except:
        traceback.print_exc()
        print("db error")

    db.close()

if __name__ == '__main__':
    get_image_json()
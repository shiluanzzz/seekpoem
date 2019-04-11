# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import random
import traceback

import pymysql

def get_poem(image):
    db = pymysql.connect("119.29.173.14", "root", "756896214", "xunshi")
    cursor = db.cursor()
    sql='SELECT * FROM Image WHERE image="{}"'.format(image)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        result=results[random.randint(0,len(results)-1)]
    except:
        # traceback.print_exc()
        db.close()
        return None
    db.close()
    return result

def update_cizu(old,new):
    sql='UPDATE Image_copy SET image = "{}" WHERE image= "{}"'.format(new,old)
    db=pymysql.connect("119.29.173.14", "root", "756896214", "xunshi")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        file=open('image.json','r')
        old_data=json.load(file)
        old_data=list(old_data)
        old_data.remove(old)
        print('更换成功')
    except:
        db.rollback()

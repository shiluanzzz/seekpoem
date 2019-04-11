# -*- coding:utf-8 -*-
# __author__ = "shitou6"
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
        # print(result)
    except:
        traceback.print_exc()
        db.close()
        return None
    db.close()
    return result
get_poem("虫")
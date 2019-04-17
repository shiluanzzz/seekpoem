# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import random
import traceback

import pymysql,logging
logger = logging.getLogger(__name__)  # 设置日志名称
logger.setLevel(logging.INFO)  # 设置日志打印等级
handler = logging.FileHandler("db_user.log")  # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志的打印格式
handler.setFormatter(formatter)  #
logger.addHandler(handler)

def get_poems(image):
    """
    根据意向获取匹配的所有诗
    :param image: 意向
    :return: 所有诗 如果这个意向在数据库不存在 则返回空。
    """
    print(image)
    db = pymysql.connect("119.29.173.14", "root", "756896214", "xunshi")
    cursor = db.cursor()
    sql = 'SELECT * FROM Image WHERE image="{}"'.format(image)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results[0])==0:
            print('no results')
            results=None
        else:
            pass
    except:
        # logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    return results

def get_poem(image):

    db = pymysql.connect("119.29.173.14", "root", "756896214", "xunshi")
    cursor = db.cursor()
    sql='SELECT * FROM Image WHERE image="{}"'.format(image)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        result=results[random.randint(0,len(results)-1)]
    except:
        logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    return result

def GetPoems_Random():
    db = pymysql.connect("119.29.173.14", "root", "756896214", "xunshi")
    cursor = db.cursor()
    sql = "SELECT * FROM Image WHERE id mod {}=0".format(random.randint(50,60))
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results[0]) == 0:
            print('no results')
            results = None
        print(len(results))
    except:
        logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    return results

def FindPoemByKey(key):
    """
    根据关键词查找
    :param key:
    :return:
    """
    db = pymysql.connect("119.29.173.14", "root", "756896214", "xunshi")
    cursor = db.cursor()
    sql1 = 'SELECT * FROM Image WHERE author ="{}"'.format(key)
    sql2 = 'SELECT * FROM Image WHERE title like "%{}%"'.format(key)
    try:
        cursor.execute(sql1)
        results1 = cursor.fetchall()
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        try:
            if len(results1[0]) == 0:
                results1 = None
        except:
            results1=None
        try:
            if len(results2[0]) == 0:
                results2 = None
        except:
            results2=None
    except:
        logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    author_list=[]
    title_list=[]
    if results1:
        for db_result in results1:
            data = {'db_id': db_result[0],
                    'title': db_result[1],
                    'author': db_result[2],
                    'dynasty': db_result[3],
                    'content': db_result[4],
                    'poem_image': db_result[5],
                    'typeid': db_result[6]
                    }
            author_list.append(data)
    else:
        pass
    if results2:
        for db_result in results2:
            data = {'db_id': db_result[0],
                    'title': db_result[1],
                    'author': db_result[2],
                    'dynasty': db_result[3],
                    'content': db_result[4],
                    'poem_image': db_result[5],
                    'typeid': db_result[6]
                    }
            title_list.append(data)
    else:
        pass
    return json.dumps({
        "author_num":len(author_list),
        "title_num":len(title_list),
        "author_list":author_list,
        "title_list":title_list
    },ensure_ascii=False)

def get_poet_info(word):
    db = pymysql.connect("119.29.173.14", "root", "756896214", "xunshi")
    cursor = db.cursor()
    sql = "SELECT * FROM Poet WHERE author = '{}';".format(word)
    try:
        cursor.execute(sql)
        results = cursor.fetchone()
        if len(results) == 0:
            print('no results')
            results = None
        # print(len(results))
    except:
        logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    return results
if __name__ == '__main__':
    a=get_poet_info("shit")
    print(a)


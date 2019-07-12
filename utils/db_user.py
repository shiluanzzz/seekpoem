# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import operator
import random
import traceback
from configparser import ConfigParser
import logging
import pymysql, time
# from func import jwd_to_site
import requests


conf = ConfigParser()
conf.read('db.cfg')
section = conf.sections()[0]
host = conf.get(section, 'host')
db_name = conf.get(section, 'db')
user = conf.get(section, 'user')
passwd = conf.get(section, 'passwd')

logger = logging.getLogger(__name__)  # 设置日志名称
logger.setLevel(logging.INFO)  # 设置日志打印等级
handler = logging.FileHandler("log_db_user.log")  # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志的打印格式
handler.setFormatter(formatter)  #
logger.addHandler(handler)

def jwd_to_site(j,w):
    """
    经纬度转地名
    :param j:  经度
    :param w: 纬度
    :return:  返回地名
    """
    parameters = {'location': "{},{}".format(str(j),str(w)), 'key': 'cfedb9207134ba8128b62a0c171c3de2'}
    base = 'https://restapi.amap.com/v3/geocode/regeo?'
    response = requests.get(base, parameters)
    print(response.url)
    answer = response.json()
    try:
        city=answer['regeocode']['addressComponent']['city']
        return str(city).strip('市')
    except:
        province=answer['regeocode']['addressComponent']['province']
        return str(province).strip('省')



def get_poems(image):
    """
    根据意向获取匹配的所有诗
    :param image: 意向
    :return: 所有诗 如果这个意向在数据库不存在 则返回空。
    """
    # print(image)
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    sql = 'SELECT * FROM Image WHERE image="{}" limit 5'.format(image)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results[0]) == 0:
            print('no results')
            results = None
        else:
            pass
    except:
        # logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    return results


def get_poem(image):
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    sql = 'SELECT * FROM Image WHERE image="{}"'.format(image)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        result = results[random.randint(0, len(results) - 1)]
    except:
        logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    return result


def GetPoems_Random():
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    sql = "SELECT * FROM Image WHERE id mod {}=0".format(random.randint(50, 60))
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
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    sql1 = 'SELECT * FROM Image WHERE author ="{}"'.format(key)
    sql2 = 'SELECT * FROM Image WHERE title like "%{}%"'.format(key)
    sql3 = 'SELECT * FROM Image WHERE content like "%{}%"'.format(key)
    try:
        cursor.execute(sql1)
        results1 = cursor.fetchall()
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        cursor.execute(sql3)
        results3 = cursor.fetchall()
        try:
            if len(results1[0]) == 0:
                results1 = None
        except:
            results1 = None
        try:
            if len(results2[0]) == 0:
                results2 = None
        except:
            results2 = None
        try:
            if len(results3[0]) == 0:
                results3 = None
        except:
            results3 = None
    except:
        logger.error(traceback.format_exc())
        db.close()
        return None
    db.close()
    author_list = []
    title_list = []
    content_list = []
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
    if results3:
        for db_result in results3:
            data = {'db_id': db_result[0],
                    'title': db_result[1],
                    'author': db_result[2],
                    'dynasty': db_result[3],
                    'content': db_result[4],
                    'poem_image': db_result[5],
                    'typeid': db_result[6]
                    }
            content_list.append(data)
    else:
        pass
    # 将查询的诗人次数添加到数据库中
    if results1:
        InsertSearchPoet(key)

    return json.dumps({
        "author_num": len(author_list),
        "title_num": len(title_list),
        "content_num": len(content_list),
        "author_list": author_list,
        "title_list": title_list,
        "content_list": content_list
    }, ensure_ascii=False)

def get_poet_info(word):
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
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

def jisuan(w, j):
    '''
    从数据库中查找最近的位置
    :param w: 维度
    :param j: 经度
    :return:返回area_code
    '''
    sql2 = '''
    
    SELECT area_code,city,j,w,ROUND(6378.138*2*ASIN(SQRT(POW(SIN(({}*PI()/180-w*PI()/180)/2),2)+COS({}*PI()/180)*COS(w*PI()/180)*POW(SIN(({}*PI()/180-j*PI()/180)/2),2)))*1000) AS distant
    FROM Map
    ORDER BY distant
    '''.format(w, w, j)
    # 经纬度转化
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql2)
    result = cursor.fetchone()
    db.close()
    return result
    # <class 'tuple'>: ('CN6529', '阿克苏地区', 80.2606, 41.1688, 5272281.0)

def get_poem_by_position(j, w):
    jisuan_result = jisuan(w, j)
    area_code = jisuan_result[0]
    sql = "SELECT * FROM Poem where area_code='{}' ;".format(area_code)
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    data_list = []
    for each in result:
        dd = {
            'title': each[0],
            'author': each[1],
            'dynasty': each[2],
            'content': each[3],
            'area_code': each[4],
            'city': jisuan_result[1]
        }
        data_list.append(dd)
    return json.dumps(data_list, ensure_ascii=False)
# 1
def SaveHeadingImg(url, nickname, openid,poem_title,user_img):
    try:
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sql = 'INSERT into Homepage_img (url,like_num,creat_time,nickname,openid,poem_title,headImage) value ("{}","{}","{}","{}","{}","{}","{}")'.format(url, '0', now_time, nickname, openid,poem_title,user_img)
        db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
        db.close()
        print(sql)
        return 'success'
    except:
        traceback.print_exc()
        print(sql)
        logger.error(traceback.format_exc())
        return 'error'

# 点赞
def favor_img(id,openid):
    flag=1 # flag标志是点赞还是取消点赞 1表示点赞 0表示取消点赞
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    try:
        sql="select flag from user_favor where homeimg_id='{}' and open_id='{}'".format(id,openid)
        cursor.execute(sql)
        result=cursor.fetchone()
        if result:
            if int(result[0]) is 1:
                # 取消点赞
                flag=0
                sql="update user_favor set flag='{}' where homeimg_id='{}' and open_id='{}'".format(flag,id,openid)
            else:
                flag=1
                sql = "update user_favor set flag='{}' where homeimg_id='{}' and open_id='{}'".format(flag, id, openid)
            cursor.execute(sql)

        else:
            # 没结果表示用户没对这个图片进行过操作
            flag=1
            sql="insert into user_favor(open_id,homeimg_id,flag)values('{}','{}','{}');".format(openid,id,flag)
            cursor.execute(sql)
            db.commit()
    except:
        print("查询用户点赞记录表出错")
        traceback.print_exc()
        pass


    try:
        sql = "SELECT like_num FROM Homepage_img where id={}".format(id)
        cursor.execute(sql)
        like_num = cursor.fetchall()[0][0]
        if flag:
            like_num += 1
        else:
            like_num-=1
        sql2 = 'UPDATE Homepage_img set like_num={} where id ={}'.format(like_num, id)
        cursor.execute(sql2)
        db.commit()
        if flag:
            return '点赞成功'
        else:
            return "取消点赞成功"
    except:
        traceback.print_exc()
        return 'error'

# 获取首页图片
def GetHeadImg(openid,flag=1):
    """
    获取诗迹
    :param flag: flag=1表示按照图片点赞数量排序 flag=2按时间排序
    :return:
    """
    favor_list=json.loads(GetUserFavor(openid))
    sql = "SELECT * FROM Homepage_img"
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for each in result:
        a = str(each[3]) in favor_list
        dd = {'url': each[0],
              'like_num': each[1],
              'creat_time': str(each[2]),
              'id': each[3],
              'nikename': each[4],
              'openid': each[5],
              'poem_title': each[6],
              'favor': a,
              'url_backpack':each[7],
              'headImage':each[8],
              'headImage_backpack':each[9]
              }
        data.append(dd)
    # 根据flag返回需要排序的value
    def return_item(item):
        if int(flag) is 2:
            return item['creat_time']
        else:
            return item['like_num']

    data.sort(key=return_item,reverse=True)
    return json.dumps(data, ensure_ascii=False)

def GetImgByOpenId(openid):
    """
    用户查询自己的诗迹
    :param openid: 用户id
    :return:
    """
    openid = str(openid)
    sql = "SELECT * FROM Homepage_img where openid='{}'".format(openid)
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for each in result:
        dd = {'url': each[0],
              'like_num': each[1],
              'creat_time': str(each[2]),
              'id': each[3],
              'nikename': each[4],
              'openid': each[5],
              'poem_title': each[6]}
        data.append(dd)
    return json.dumps(data, ensure_ascii=False)

def FindPoemByIdAndAreaCode(position, image_id_list):
    image_id_list=list(image_id_list)
    position=position
    image_in=""
    for each in image_id_list:
        image_in+="({}),".format(each)
    image_in=image_in[:len(image_in)-1]
    print(image_id_list,type(image_id_list))
    sql='select * from Image_Poem where ip_areacode="{}" and image_id in ({})'.format(position,image_in)
    print(sql)
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    data=[]
    for each in result:
        dd={'title':each[0],
            'author':each[1],
            'dynasty':each[2],
            'content':each[3],
            'image':each[4],
            'areacode':each[5],
            'typeid':each[6],
            'image_id':each[7]}
        data.append(dd)
    return json.dumps(data,ensure_ascii=False)

def InsertSearchPoet(poet):

    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    try:
        result = json.loads(GetHotPoet_time(poet))
        print(result)
        time=int(result['time'])
        sql='update hot_poet set time="{}" where poet="{}"'.format(time+1,poet)
        cursor.execute(sql)
        db.commit()
    except:
        time=1
        sql='insert into hot_poet (poet,time) values ("{}","{}")'.format(poet,time)
        cursor.execute(sql)
        db.commit()

def GetHotPoet_time(poet):
    try:
        sql='select * from hot_poet where poet="{}"'.format(poet)
        db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        result=cursor.fetchone()
        data={'poet':result[0],'time':result[1]}
        return json.dumps(data,ensure_ascii=False)

    except:
        return False

def SaveUserSites(j, w, openid):
    site=jwd_to_site(j,w)
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    try:
        time=1
        try:
            temp_date=json.loads(GetHotUserSite(openid))
            for each in temp_date:
                if each['site']==site:
                    time=int(each['time'])
        except:
            pass
        if time!=1:
            sql='update user_site set time="{}" where site="{}"'.format(time+1,site)
        else:
            sql="INSERT INTO user_site (open_id,site,time) VALUES ('{}','{}','{}')".format(openid,site,time)
        cursor.execute(sql)
        db.commit()
        return 'success site:{}'.format(site)
    except:
        traceback.print_exc()
        return 'error'

def GetHotUserSite(openid):
    try:
        db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
        cursor = db.cursor()
        sql = "SELECT * FROM user_site WHERE open_id='{}'".format(openid)
        cursor.execute(sql)
        result=cursor.fetchall()
        date=[]
        for each in result:
            dd={'openid':each[0],'site':each[1],'time':each[2]}
            date.append(dd)

        def return_item(item):
            return int(item['time'])
        data=date.sort(key=return_item,reverse=True)
        return json.dumps(date,ensure_ascii=False)
    except:
        return 'error'

def GetHotPoet():
    try:
        sql='select * from hot_poet'
        db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        results=cursor.fetchall()
        data=[]
        for each in results:
            dd={'poet':each[0],'time':each[1]}
            data.append(dd)

        def return_item(item):
            return int(item['time'])
        data.sort(key=return_item,reverse=True)
        return json.dumps(data,ensure_ascii=False)
    except:
        traceback.print_exc()
        return False

def GetUserFavor(openid):
    try:
        sql = 'select homeimg_id from user_favor where open_id="{}" and flag="1"'.format(openid)
        db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
        cursor = db.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        data = [each[0] for each in results]
        return json.dumps(data, ensure_ascii=False)
    except:
        traceback.print_exc()
        return False

def SearchComplete(key):
    sql1 = "SELECT author FROM Poet WHERE author like '%{}%' limit 3".format(key)
    sql2 = "SELECT title FROM Image WHERE title like '%{}%' limit 2 " .format(key)
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    cursor = db.cursor()
    cursor.execute(sql1)
    result1=cursor.fetchall()
    cursor.execute(sql2)
    result2=cursor.fetchall()
    data1=[each[0] for each in result1]
    data2=[each[0] for each in result2]
    data=data1+data2
    return json.dumps(data,ensure_ascii=False)



if __name__ == '__main__':

    # a=GetHeadImg('off5G48e9E7YYBLj2XQkZT5QXtQM',1)
    # a=SaveHeadingImg("www.baidu.com","shitou","shitouopenid","测试标题","www.aa.com")
    # a=favor_img('1','shitouopenid')
    # a=GetHeadImg("shitouopenid",1)

    # a=GetImgByOpenId("shitouopenid")
    # a=InsertSearchPoet("李白")
    # a=GetHotPoet_time("李白")
    # a=SaveUserSites('113.61','23.58','shitouopenid')
    # a=GetHotUserSite("shitouopenid")

    SearchComplete("石")

    # print(a)


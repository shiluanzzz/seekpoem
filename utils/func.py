# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import logging
import random
import traceback

import requests
# from synonyms import compare

from utils import db_user, db_connect

logger = logging.getLogger(__name__)  # 设置日志名称
logger.setLevel(logging.INFO)  # 设置日志打印等级
handler = logging.FileHandler("log_func.log")  # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志的打印格式
handler.setFormatter(formatter)  #
logger.addHandler(handler)



def find_jyc(word,num=0.9):
    try:
        try:
            with open('image.json', 'r')as f:
                data = json.load(f)
            num=float(num)# 相似度值
        except:
            print("image.json 文件不存在 正在重新下载")
            db_connect.get_image_json()
            return find_jyc(word,num)
        if num<0.4:
            return {'poem_image':'花','num':'0.001'}
        else:
            copy=list(data)
            while len(copy):
                data_word=copy[random.randint(0,len(copy)-1)]
                copy.remove(data_word)
                r=compare(word,data_word,seg=False)
                if r>num:
                    return {'poem_image':data_word,'num':r}
            return find_jyc(word,num=num-0.1)
    except:
        pass

def GetPoetInfo(word):
    result= db_user.get_poet_info(word)
    if result:
        data={
            'author':result[0],
            'dynasty':result[1],
            'introduction':result[2]
        }
        return json.dumps(data,ensure_ascii=False)
    else:
        return json.dumps({},ensure_ascii=False)

def get_poems_by_image(word):
    """
    根据意向查询所有匹配的诗句
    :param word:
    :return:
    """
    try:
        db_results = db_user.get_poems(word)
        if db_results:
            data_list = []
            for db_result in db_results:
                data = {'db_id': db_result[0],
                        'poem_title': db_result[1],
                        'poem_author': db_result[2],
                        'poem_chaodai': db_result[3],
                        'poem_content': db_result[4],
                        'poem_image': db_result[5],
                        'typeid': db_result[6],
                        'xiangsidu': '1'}
                data_list.append(data)
            return json.dumps(data_list, ensure_ascii=False)
        else:
            word2=find_jyc(word,0.8)["poem_image"]
            return get_poems_by_image(word2)
    except:
        logger.error(traceback.format_exc())

def chuli(word):
    """
    根据意向查询一个匹配的诗
    :param word:
    :return:
    """
    try:
        try:
            db_result = db_user.get_poem(word)
            if db_result != None:
                data = {'db_id': db_result[0],
                        'poem_title': db_result[1],
                        'poem_author': db_result[2],
                        'poem_chaodai': db_result[3],
                        'poem_content': db_result[4],
                        'poem_image': db_result[5],
                        'typeid': db_result[6],
                        'xiangsidu': '1'}
                return json.dumps(data, ensure_ascii=False)
            else:
                logger.error(traceback.format_exc())
        except:
            logger.error(traceback.format_exc())

        try:
            word1 = word
            data1 = find_jyc(word1, 0.8)
        except:
            logger.error(traceback.format_exc())
            word1 = None
            return None

        rt_data = {'num': data1['num'], 'poem_data': db_user.get_poem(data1['poem_image'])}
        poem = rt_data['poem_data']
        data = {'db_id': poem[0],
                'poem_title': poem[1],
                'poem_author': poem[2],
                'poem_chaodai': poem[3],
                'poem_content': poem[4],
                'poem_image': poem[5],
                'typeid': poem[6],
                'xiangsidu': rt_data['num']}
        return json.dumps(data, ensure_ascii=False)
    except:
        logger.error(traceback.format_exc())
        return None

def GetPoems():
    """
    查询所有诗
    :return:
    """
    try:
        db_results = db_user.GetPoems_Random()
        if db_results:
            data_list = []
            count=0
            single_list=[]
            for db_result in db_results:
                count+=1
                data = {
                        'db_id': db_result[0],
                        'title': db_result[1],
                        'author': db_result[2],
                        'dynasty': db_result[3],
                        'content': db_result[4],
                        'poem_image': db_result[5],
                        'typeid': db_result[6]
                        }
                single_list.append(data)
                if count==20:
                    data_list.append(single_list)
                    single_list=[]
                    count=0
            return json.dumps(data_list, ensure_ascii=False)
    except:
        logger.error(traceback.format_exc())


def FindPoemByImageAndPosition(image,j,w):
    position= db_user.jisuan(j=j, w=w)[0] #ip_areacode
    print(position)
    image_data=json.loads(get_poems_by_image(image))
    image_id_list=[each['db_id'] for each in image_data]
    return db_user.FindPoemByIdAndAreaCode(position, image_id_list)

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




if __name__ == '__main__':
    a=GetPoems()
    print(a)

# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import logging
import traceback

import db_user
from syonoym_chuli import find_jyc

logger = logging.getLogger(__name__)  # 设置日志名称
logger.setLevel(logging.INFO)  # 设置日志打印等级
handler = logging.FileHandler("func.log")  # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志的打印格式
handler.setFormatter(formatter)  #
logger.addHandler(handler)


def GetPoetInfo(word):
    result=db_user.get_poet_info(word)
    if result:
        data={
            'author':result[0],
            'dynasty':result[1],
            'introduction':result[2]
        }
        return json.dumps(data,ensure_ascii=False)
    else:
        return 0

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
            for db_result in db_results:
                data = {'db_id': db_result[0],
                        'title': db_result[1],
                        'author': db_result[2],
                        'dynasty': db_result[3],
                        'content': db_result[4],
                        'poem_image': db_result[5],
                        'typeid': db_result[6]
                        }
                data_list.append(data)
            return json.dumps(data_list, ensure_ascii=False)
    except:
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    a = get_poems_by_image('山')
    b = chuli('花')
    c = GetPoems()


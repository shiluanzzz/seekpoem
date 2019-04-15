# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import random
import traceback
import db_connect
import synonyms
import time

import logging
logger=logging.getLogger(__name__) # 设置日志名称
logger.setLevel(logging.INFO) #设置日志打印等级
handler=logging.FileHandler("syonoym.log") # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')# 设置日志的打印格式
handler.setFormatter(formatter) #
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
                r=synonyms.compare(word,data_word,seg=False)
                if r>num:
                    return {'poem_image':data_word,'num':r}
            return find_jyc(word,num=num-0.1)
    except:
        pass

#
# def find_it(word,num):
#
#     try:
#         num=float(num)
#         with open('image.json', 'r')as f:
#             data = json.load(f)
#         for data_word in data:
#             r = synonyms.compare(word, data_word, seg=False)
#             if r>num:
#                 return {'poem_image':data_word,'num':r}
#             else:
#                 pass
#         return {'poem_image':'花','num':0.0001}
#     except:
#         logger.error(traceback.format_exc())
#         return {'poem_image':'花','num':0.0001}


if __name__ == '__main__':
    a=find_jyc("枫树",0.9)
    print(a)
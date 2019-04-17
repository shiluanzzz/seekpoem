# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import logging
import traceback
from flask import Flask, request
import func
from db_user import FindPoemByKey

app=Flask(__name__)

logger = logging.getLogger(__name__)  # 设置日志名称
logger.setLevel(logging.INFO)  # 设置日志打印等级
handler = logging.FileHandler("func.log")  # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志的打印格式
handler.setFormatter(formatter)  #
logger.addHandler(handler)

@app.route('/GetPoemsByImage',methods=['GET'])
def GetPoemsByImage():
    word = request.args.get('word')
    logging.info("GetPoemsByImage {}".format(word))
    return func.get_poems_by_image(word)


@app.route('/test_return',methods=['GET'])
def return_word():
    word=request.args.get('word')
    logging.info("return_word {}".format(word))
    return json.dumps({'word':word})


@app.route('/img',methods=['GET'])
def params():
    word = request.args.get('word1')
    logging.info("params {}".format(word))
    return func.chuli(word)


@app.route('/GetPoems',methods=['GET'])
def GetPoems():
    logging.info("GetPoems")
    return func.GetPoems()

@app.route('/FindPoem',methods=['GET'])
def FindPoem():
    word=request.args.get('key')
    logging.info("FindPoem {}".format(word))
    return FindPoemByKey(key=word)

@app.route("/GetPoetInfo",methods=['GET'])
def GetPoetInfo():
    word = request.args.get('name')
    return func.GetPoetInfo(word)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8000",debug=False)
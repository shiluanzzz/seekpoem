# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import logging
import traceback
from flask import Flask, request

import db_user
import func
from db_user import FindPoemByKey

logger = logging.getLogger(__name__)  # 设置日志名称
logger.setLevel(logging.INFO)  # 设置日志打印等级
handler = logging.FileHandler("func.log")  # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志的打印格式
handler.setFormatter(formatter)  #
logger.addHandler(handler)
app=Flask(__name__)



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

@app.route("/GetPoemByPosition",methods=['GET'])
def GetPoemByPosition():
    w=request.args.get('w')
    j=request.args.get('j')
    return db_user.get_poem_by_position(j=j,w=w)

@app.route('/GetHeadImg',methods=['GET'])
def GetHeadImg():
    flag=request.args.get('flag')
    return db_user.GetHeadImg(int(flag))

@app.route('/favor',methods=['GET'])
def favor():
    id=request.args.get('id')
    openid=request.args.get('openid')
    return db_user.favor_img(id,openid)

@app.route('/SaveHeadingImg',methods=['GET'])
def SaveHeadingImg():
    url=request.args.get('url')
    nickname=request.args.get('nickname')
    openid=request.args.get('openid')
    poem_title=request.args.get('poem_title')
    return db_user.SaveHeadingImg(url=url,nickname=nickname,openid=openid,poem_title=poem_title)

@app.route("/FindPoemByImageAndPosition",methods=['GET'])
def FindPoemByImageAndPosition():
    image=request.args.get('i')
    j=request.args.get('j')
    w=request.args.get('w')
    return func.FindPoemByImageAndPosition(image=image,j=j,w=w)

@app.route("/FindMyPoem",methods=['GET'])
def FindMyPoem():
    id=request.args.get('id')
    return db_user.GetImgByOpenId(id)

#获取热门关键词
@app.route("/GetHotPoet",methods=['GET'])
def GetHotPoet():
    return db_user.GetHotPoet()

#保持用户地理位置
@app.route('/SaveUserSites',methods=['GET'])
def SaveUserSites():
    j=request.args.get('j')
    w=request.args.get('w')
    openid=request.args.get('openid')
    return db_user.SaveUserSites(j,w,openid)

#获取用户去过的地方
@app.route('/GetUserSites',methods=['GET'])
def GetUserSites():
    openid=request.args.get('openid')
    return db_user.GetHotUserSite(openid)

@app.route('/GetUserFavor',methods=['GET'])
def GetUserFavor():
    openid=request.args.get('openid')
    return db_user.GetUserFavor(openid)
if __name__ == '__main__':

    app.run(host="0.0.0.0",port="8000",debug=True)
# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import logging
import traceback

from flask import Flask, request
from utils import db_user, func

logger = logging.getLogger(__name__)  # 设置日志名称
logger.setLevel(logging.INFO)  # 设置日志打印等级
handler = logging.FileHandler("func.log")  # 创建日志文件
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 设置日志的打印格式
handler.setFormatter(formatter)  #
logger.addHandler(handler)
app = Flask(__name__)


@app.route('/GetPoemsByImage', methods=['GET'])
def GetPoemsByImage():
    word = request.args.get('word')
    logging.info("GetPoemsByImage {}".format(word))
    return func.get_poems_by_image(word)


@app.route('/test_return', methods=['GET'])
def return_word():
    word = request.args.get('word')
    logging.info("return_word {}".format(word))
    return json.dumps({'word': word})


@app.route('/img', methods=['GET'])
def params():
    word = request.args.get('word1')
    logging.info("params {}".format(word))
    return func.chuli(word)


# 获取诗库
@app.route('/GetPoems', methods=['GET'])
def GetPoems():
    logging.info("GetPoems")
    return func.GetPoems()


# 根据关键词寻诗
@app.route('/FindPoem', methods=['GET'])
def FindPoem():
    word = request.args.get('key')
    logging.info("FindPoem {}".format(word))
    return db_user.FindPoemByKey(key=word)


# 获取诗人信息
@app.route("/GetPoetInfo", methods=['GET'])
def GetPoetInfo():
    word = request.args.get('name')
    return func.GetPoetInfo(word)


# 地理位置寻诗
@app.route("/GetPoemByPosition", methods=['GET'])
def GetPoemByPosition():
    w = request.args.get('w')
    j = request.args.get('j')
    return db_user.get_poem_by_position(j=j, w=w)


# 获取主页图片
@app.route('/GetHeadImg', methods=['GET'])
def GetHeadImg():
    flag = request.args.get('flag')
    openid = request.args.get('openid')
    return db_user.GetHeadImg(openid, int(flag))


# 点赞
@app.route('/favor', methods=['GET'])
def favor():
    id = request.args.get('id')
    openid = request.args.get('openid')
    return db_user.favor_img(id, openid)


# 保存主页图片
@app.route('/SaveHeadingImg', methods=['GET'])
def SaveHeadingImg():
    url = request.args.get('img_url')
    nickname = request.args.get('nickname')
    openid = request.args.get('openid')
    poem_title = request.args.get('poem_title')
    user_img = request.args.get('userimg_url')
    return db_user.SaveHeadingImg(url=url, nickname=nickname, openid=openid, poem_title=poem_title,
                                  user_img=user_img)


# 根据地理位置、意向 寻找诗
@app.route("/FindPoemByImageAndPosition", methods=['GET'])
def FindPoemByImageAndPosition():
    image = request.args.get('i')
    j = request.args.get('j')
    w = request.args.get('w')
    return func.FindPoemByImageAndPosition(image=image, j=j, w=w)


# 获取用户的诗迹
@app.route("/FindMyPoem", methods=['GET'])
def FindMyPoem():
    id = request.args.get('id')
    return db_user.GetImgByOpenId(id)


# 获取热门关键词
@app.route("/GetHotPoet", methods=['GET'])
def GetHotPoet():
    return db_user.GetHotPoet()


# 保持用户地理位置
@app.route('/SaveUserSites', methods=['GET'])
def SaveUserSites():
    j = request.args.get('j')
    w = request.args.get('w')
    openid = request.args.get('openid')
    return db_user.SaveUserSites(j, w, openid)


# 获取用户去过的地方
@app.route('/GetUserSites', methods=['GET'])
def GetUserSites():
    openid = request.args.get('openid')
    return db_user.GetHotUserSite(openid)


# 获取用户点赞过的图片
@app.route('/GetUserFavor', methods=['GET'])
def GetUserFavor():
    openid = request.args.get('openid')
    return db_user.GetUserFavor(openid)

# 搜索自动补全
@app.route('/SearchComplete',methods=['GET'])
def SearchComplete():
    key=request.args.get('k')
    return db_user.SearchComplete(key)

@app.route('/get_openid',methods=['GET'])
def get_openid():
    code=request.args.get('code')
    data=func.get_openid(code)
    try:
        return data['openid'],200
    except:
        return traceback.format_exc(),500

@app.route('/delete_user_img',methods=['GET'])
def del_user_img():
    key=request.args.get('id')
    try:
        db_user.del_user_img(key)
        return "success",200
    except:
        return traceback.format_exc(),500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000", debug=False ,use_reloader=False)

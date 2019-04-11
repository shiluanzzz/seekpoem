# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
from syonoym_chuli import find_jyc
from db_user import get_poem
from flask import Flask, request

app=Flask(__name__,static_url_path='')

@app.route("/test_api")
def test_api():
    headers={
        'content-type':'application/json'
    }
    data=[
        {'name':'第一个字典','tag':'111'},
        {'name':'第二个字典','tag':'222'}
    ]
    return json.dumps(data),200,headers




@app.route('/img',methods=['GET'])
def params():
    # 获取三个word意向查找到的匹配值
    try:
        word1 = request.args.get('word1')
        data1=find_jyc(word1,0.9)
    except:
        word1=None
        data1={'num':0}
    try:
        word2 = request.args.get('word2')
        data2=find_jyc(word2,0.9)
    except:
        word2=None
        data2 = {'num': 0}
    try:
        word3 = request.args.get('word3')
        data3=find_jyc(word3,0.9)
    except:
        word3=None
        data3 = {'num': 0}

    if data1['num']>data2['num']:
        if data1['num']>data3['num']:
            # 1最大
            rt_data={'num':data1['num'],'poem_data':get_poem(data1['poem_image'])}
        else:
            rt_data = {'num': data3['num'], 'poem_data': get_poem(data3['poem_image'])}
    else:
        if data2['num']>data3['num']:
            # 2最大
            rt_data={'num':data2['num'],'poem_data':get_poem(data2['poem_image'])}
        else:
            rt_data = {'num': data3['num'], 'poem_data': get_poem(data3['poem_image'])}

    poem=rt_data['poem_data']
    data={'db_id':poem[0],
          'poem_title':poem[1],
          'poem_author':poem[2],
          'poem_chaodai':poem[3],
          'poem_content':poem[4],
          'poem_image':poem[5],
          'typeid':poem[6],
          'xiangsidu':rt_data['num']}
    return json.dumps(data,ensure_ascii=False)
    """
        return 
        <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{}</title>
    </head>
    <body>
    <h1>{}</h1>
    <h3>{}-{}</h3>
    {}
    </body>
    </html>
    .format(poem[1],poem[1],poem[2],poem[3],poem[4])
    """

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="8000",debug=True)
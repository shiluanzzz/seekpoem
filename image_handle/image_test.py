# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import time
import db_user
from PIL import Image, ImageFont, ImageDraw
import json
import random
import traceback
import pymysql,logging
from configparser import ConfigParser
conf=ConfigParser()
conf.read('db.cfg')
section = conf.sections()[0]
host=conf.get(section,'host')
db_name=conf.get(section,'db')
user=conf.get(section,'user')
passwd=conf.get(section,'passwd')

def draw_poet(file,title,text,author,user_name):
    text=text.strip('①').strip('②').strip('③').strip('④')
    lines=text.split('。')
    lens=len(lines)
    if lines[lens-1] == "":
        lines.remove(lines[lens-1])
    
    im = Image.open(file)
    height=im.size[1]
    width=im.size[0]
    new_width=1000
    new_height=int(height/width*new_width)
    poem_height=len(lines)*50+60+20
    new_img=Image.new(im.mode,(new_width,new_height+poem_height),'#FFFFFF')##FFFFFF
    new_img.paste(im.resize((new_width,new_height),Image.ANTIALIAS),(0,0))


    font_60=ImageFont.truetype('C:\Windows\Fonts\STKAITI.TTF',60)
    font_50=ImageFont.truetype('C:\Windows\Fonts\STKAITI.TTF',50)
    font_20=ImageFont.truetype('C:\Windows\Fonts\STKAITI.TTF',20)
    font_30 = ImageFont.truetype('C:\Windows\Fonts\STKAITI.TTF', 30)
    draw = ImageDraw.Draw(new_img)
    # print(new_height+50)
    draw.text((1,new_height+5),title,fill='#000000',font=font_60)
    draw.text((4+60*len(title),new_height+40),author,fill='#808080',font=font_30)
    for each in lines:
        draw.text((1, 20+new_height + (lines.index(each)+1)*50), each+'。', fill='#000000', font=font_50)

    draw.text((1000-len(user_name)*20-50,new_height+poem_height-25),"Design By {}".format(user_name),fill='#000000',font=font_20)
    # new_img.show()
    save_path='F:\\PyProject\\seekpoem\\image_handle\\img\\'
    new_img.save('{}{}.png'.format(save_path,title))

def GetPoems_Random():
    db = pymysql.connect(host=host, user=user, passwd=passwd,db=db_name)
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
        db.close()
        return None
    db.close()
    return results


def get_poem():
    result=GetPoems_Random()
    for each in result:
        print(each[4])
        try:
            lines=each[4].split('。')
            lines.remove(lines[len(lines)-1])
            for each in lines:
               print("{} : {}".format(lines.index(each),each+'。'))
        except:
            print('error')
            traceback.print_exc()
            break

def test():
    a='分根金谷里，移植广庭中。新枝含浅绿，晚萼散轻红。影入环阶①水，香随度隙风。路远无由寄，徒念③春闺空②。'
    lines=a.split('。')

    if lines[len(lines)-1]=="":
        lines.remove(lines[4])
    print(lines)
if __name__ == '__main__':
    result=GetPoems_Random()
    img_list=[
        'img.png','img1.png','img2.jpg'
    ]
    for each in result[:20]:
        print(each)
        # break
        begin_time=time.time()
        draw_poet(img_list[random.randint(0,2)],title=each[1],author="[{}]".format(each[3])+each[2],text=each[4],user_name='SHILUAN')
        print('times:{}',time.time()-begin_time)
        # a=input()
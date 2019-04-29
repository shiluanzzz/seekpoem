# -*- coding:utf-8 -*-
# __author__ = "shitou6"
from PIL import Image, ImageFont, ImageDraw
def draw_poet(file,title,text,author):
    text1=text.split('。')[0]
    text2=text.split('。')[0]
    im = Image.open(file)
    height=im.size[1]
    width=im.size[0]
    new_width=1000
    new_height=int(height/width*new_width)
    new_img=Image.new(im.mode,(new_width,new_height+200),'#FFFFFF')##FFFFFF
    new_img.paste(im.resize((new_width,new_height),Image.ANTIALIAS),(0,0))

    draw = ImageDraw.Draw(new_img)
    print(new_height+50)
    draw.text((1,new_height+5),title,fill='#000000',font=ImageFont.truetype(r'Arial.tff',60))
    draw.text((4+60*len(title),new_height+30),author,fill='#808080',font=ImageFont.truetype(r'Arial.tff',50))
    draw.text((1,new_height+80),text1,fill='#000000',font=ImageFont.truetype(r'Arial.tff',50))
    draw.text((1,new_height+140),text2,fill='#000000',font=ImageFont.truetype(r'Arial.tff',50))
    draw.text((800,new_height+180),"Design By Shiluanzzz",fill='#000000',font=ImageFont.truetype(r'Arial.tff',20))
    new_img.show()

if __name__ == '__main__':
    draw_poet('img.png','题西林壁','横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。','石滦')
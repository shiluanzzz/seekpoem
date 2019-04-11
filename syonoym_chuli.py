# -*- coding:utf-8 -*-
# __author__ = "shitou6"
import json
import random

import synonyms
import time



def find_jinyici(word):
    with open('image2.json', 'r')as f:
        data = json.load(f)
    time1=time.time()
    count=0
    file1=open('temp.txt','w')
    file2=open('xiangsi.txt','w+')
    for each in data:
        r=synonyms.compare(word,each,seg=False)
        if r>0.8:
            str1=str("{} , {} 相似度：{}".format(word,each,str(r)))
            file2.write(str1+'\n')
        sst=str(str(count)+"time: {}".format(str(time.time()-time1)))
        file1.write(sst+'\n')
        count+=1
    file1.close()
    file2.close()

def find_jyc(word,num):
    with open('image2.json', 'r')as f:
        data = json.load(f)
    num=float(num)# 相似度值
    copy=list(data)
    while len(copy):
        data_word=copy[random.randint(0,len(copy)-1)]
        copy.remove(data_word)
        r=synonyms.compare(word,data_word,seg=False)
        if r>num:
            return {'poem_image':data_word,'num':r}
    return find_jyc(word,num=num-0.1)

if __name__ == '__main__':

    a=find_jyc('石头',0.9)['num']
    print(a)
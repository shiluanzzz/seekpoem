import os
import traceback
from threading import Thread

import requests,pymysql
from configparser import ConfigParser
import oss2
from utils.oss_upload import AutoRequests


conf = ConfigParser()
conf.read('db.cfg')
section = conf.sections()[0]
host = conf.get(section, 'host')
db_name = conf.get(section, 'db')
user = conf.get(section, 'user')
passwd = conf.get(section, 'passwd')



def replace_homepageUrl(url1,url2):
    """
    在oss异步上传图片之后替换url
    :param url:
    :return:
    """
    db = pymysql.connect(host=host, user=user, passwd=passwd, db=db_name)
    try:
        cursor = db.cursor()
        sql = "UPDATE Homepage_img SET url='{}',url_backpack='{}' WHERE url='{}'".format(url2,url1,url1)
        cursor.execute(sql)
        db.commit()
        return True
    except:
        traceback.print_exc()
        return False

def async_call(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

@async_call
def replace_url(url1):
    # 下载图片
    print("开始调用 replace_url 函数")
    if 'https://i.loli.net' in url1:
        r=AutoRequests.GetUrlContent(url1,2)
        l=url1.split('/')
        file_name=l[6]
        oss_file_path='user_image/{}-{}-{}/{}'.format(l[3],l[4],l[5],l[6])
        with open(file_name,'wb')as f:
            f.write(r)
            f.close()
        # print("下载完毕")
        auth=oss2.Auth('LTAIGNTlWKY4MRBe','WcpBavqxlYPkPWILvPup3TGxnXubho')
        bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'poempic')
        bucket.put_object_from_file(oss_file_path,file_name)
        # print('上传完毕！')
        os.remove(file_name)
        url="https://poempic.oss-cn-hangzhou.aliyuncs.com/{}".format(oss_file_path)
        print(url)
        replace_homepageUrl(url1,url)
        print("end")
    else:
        pass

if __name__ == '__main__':
    # replace_url('','')
    replace_homepageUrl('https://i.loli.net/2019/05/26/5cea4f894b1b981237.png','https://poempic.oss-cn-hangzhou.aliyuncs.com/user_image/2019-05-26/5cea4f894b1b981237.png')

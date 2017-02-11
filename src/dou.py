# encoding=utf-8
import json
import re
import time

import requests
from lxml import html


# URL= sys.argv[1]

def req(startUrl,s,pageList):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': 'bid=8k8BpBJD9qU; gr_user_id=8d230d99-3838-4008-8d2f-f14f840f447c; ll="108296"; _ga=GA1.2.1368108966.1474689230; viewed="26835090_3864073_1064275"; _vwo_uuid_v2=5C41C62A962FA7C09560D37353FBEBDD|2f07091c6519fd1e3d7a9a3c91a6f4b4; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1486186346%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; __utmt=1; _pk_id.100001.8cb4=8e0d16baa5edde37.1474689230.33.1486186468.1485749796.; _pk_ses.100001.8cb4=*; __utma=30149280.1368108966.1474689230.1485749803.1486186347.40; __utmb=30149280.6.9.1486186468743; __utmc=30149280; __utmz=30149280.1485749803.39.18.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=30149280.15547',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    }

    data = {

    }
    print 'starturl:' + startUrl
    r = requests.get(
        startUrl,
        headers=header, data=data)

    tree = html.fromstring(r.content)
    pageListHtml = tree.xpath('//*[@id="content"]/div/div[1]/div[3]/a/@href')   # 选取分页
    if len(pageList) == 0:
        for val in pageListHtml:
            pageList.append(val)

    buyers = tree.xpath('//*[@id="comments"]/li/div[2]/p/text()')   # 主要的内容
    # print buyers
    regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)

    off = False
    for item in buyers:
        result = str(re.findall(regex, item)).replace("']", '').replace("['", '').replace("[]", '').replace("', '", '').replace("[u'",'')
        if result != '':
            if(result not in s):
                s.add(result)
            else:
                off = True

    return off

def main(startUrl):
    s = set()  # 存放结果的集合
    i = 0
    pageList = []  # 分页的url

    result = req(startUrl,s,pageList)
    print pageList
    if len(pageList) >0:
        for val in pageList:
            req(val,s,pageList)


    print '一共爬取了' + str(len(s)) + '个'
    data_email = []
    now = int(time.time())

    for item in s:
        dict = {
            "_email": item,
            "time": now,
            "url": startUrl,
            "status":0,
            "source": 'douban'
        }

        data_email.append(dict)

   # dou_db.mInsert(data_email['emailList'])

    return data_email


# main()

import tornado.web


class getEmailHandler(tornado.web.RequestHandler):
    def post(self):

        url = self.get_argument("url")
        print 'GET:URL' + url
        emailList = main(url)

        obj = {
            "emailList": emailList
        }
        j = json.dumps(obj)
        print j
        self.write(obj)
        # self.write(input_word[::-1])
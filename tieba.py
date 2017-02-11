# encoding=utf-8
import re
import sys
import time
import json
import requests
from lxml import html

from src import dou_db



def req(startUrl,s,pageList):
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': 'TIEBA_USERTYPE=23fdbb361380878070691806; bdshare_firstime=1474861285905; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1482850292,1482850327,1482850532,1482850569; BDUSS=lBURmlySTdock5UclFLLU85ZE54NVp5bklBSy1yflhBQTZVUGtFbkh4b2ZoSmxZSVFBQUFBJCQAAAAAAAAAAAEAAADBLM4WwMPSttfT0rvGrAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB~3cVgf93FYM; STOKEN=557107e8dd3128a8347e7d06d0c7cb09df019f2b9c8c8db9830ee13a6abab4f4; TIEBAUID=83f4b7179f8aeee39cb626b5; BAIDUID=C17787A1E42B2D4EF1ACF2655D088176:FG=1; PSTM=1485230263; BIDUPSID=E4C79AC24E4807BC0807F3ABE82BD396; MCITY=-289%3A; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=1; H_PS_PSSID=1429_21094_21942_21801_22026; wise_device=0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
    }

    data = {

    }
    print 'url:'
    print startUrl
    r = requests.get(
        startUrl,
        headers=header, data=data)

    tree = html.fromstring(r.content)

    pageListHtml = tree.xpath('//*[@id="thread_theme_7"]/div[1]/ul/li[1]/a/@href')   # 选取分页
    pageNumHtml = tree.xpath('//*[@id="thread_theme_7"]/div[1]/ul/li[2]/span[2]/text()')   # 选取分页数，贴吧太变态，选取分页数才是最明智的

    pageNum = int (pageNumHtml[0])

    if len(pageList) == 0:
        if pageNum > 1:
            startUrl_model = startUrl.split('=')
            _startUrl_model = startUrl_model[0]

            while pageNum:
                continueUrl = _startUrl_model + '?pn=' + str(pageNum)
              #  print continueUrl
                pageList.append(continueUrl)
                pageNum = pageNum - 1

    buyers = tree.xpath('//*[@id="j_p_postlist"]/div[6]/div[2]/div[1]/cc/text()')   # 主要的内容
   # print buyers
    # print buyers
    regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.IGNORECASE)

    result = str(re.findall(regex, r.content)).replace("']", '').replace("['", '').replace("[]", '').replace("', '", ',').replace("[u'", '').replace("u", '')

    # print result
    res = result.split(',')
    print res

    for val in res:
        if(val not in s):
            s.add(val)


def main(startUrl):
    surl = startUrl.split('?')
    startUrl = surl[0]
    print startUrl
    s = set()  # 存放结果的集合
    pageList = []  # 分页的url
    result = req(startUrl,s,pageList)

    if len(pageList) >0:
        for val in pageList:
            req(val,s,pageList)

  #  print s
    print 'count:' + str(len(s)) + ''
    data_email = []
    now = int(time.time())

    for item in s:
        dict = {
            "_email": item,
            "time": now,
            "status": 0,
            "source": 'tieba'
        }

        data_email.append(dict)

    return data_email

# main('http://tieba.baidu.com/p/4877116887')

import tornado.web

class getTiebaEmail(tornado.web.RequestHandler):
    def post(self):

        url = self.get_argument("url")
        print 'GET:URL:' + url
        emailList = main(url)

        obj = {
            "emailList": emailList
        }
        j = json.dumps(obj)
        self.write(obj)

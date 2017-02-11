# encoding=utf-8
import requests
import json

import db

header = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=on9ogme6ejp3rj9s3luc3ngvk4; ses=98dace65701794d9d1ea494357443944; t=1485410423; uca=6f30a17595285f7a65b7cbba57506c6f; uid=48628065; _mly_lang=cn; app_install_62=1; ldi=071d92ca9f25460528c05aad6cc684ac',
    'user-agent':'meiliyue/6.4.0 (iPhone; iOS 10.2; Scale/2.00)',

}

data = {
    'loc_prov':u"上海",
    'loc_city':u"上海",
    'country_short':'CN',
    'ios_push_status':0,
    'default_search_type':'online',
    'is_first':0,
    'page':1
}

# r = requests.post(
#     "http://mapi.miliyo.com/search/online?_ua=i%7C10.2%7C0%7C80%7Cappstore%7C071d92ca9f25460528c05aad6cc684ac%7C750%7C1334%7C0%7Ccn%7C443a45fbf4fedbe9e3a4bb59726c9e1e&__clttzaeiou=48628065",
#     headers=header, data=data)
#
# rr = json.loads(r.text)
#
# print rr['last_id']

i=813
while i<1000:
    data['page']= i
    print data
    r = requests.post("http://mapi.miliyo.com/search/online?_ua=i%7C10.2%7C0%7C80%7Cappstore%7C071d92ca9f25460528c05aad6cc684ac%7C750%7C1334%7C0%7Ccn%7C443a45fbf4fedbe9e3a4bb59726c9e1e&__clttzaeiou=48628065",headers=header,data=data)
    rr = json.loads(r.text)
 #  print r.text
    db.mInsert(rr['list'])
   ## print rr['last_id']
    data['last_id'] = rr['last_id']
    i=i+1

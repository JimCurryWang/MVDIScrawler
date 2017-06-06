#資料庫連線
#import pymysql

import urllib
import requests
import http.cookiejar
from bs4 import BeautifulSoup
from bs4.element import Tag

from datetime import timedelta
import time

# row2 & row15-24 & row96-98 註記為資料庫連線版本
##資料庫連線
#conn= pymysql.connect(
#        host='1xx.1xx.2xx.1xx',
#        port = 3307,
#        user='root',
#        passwd='xxx',
#        db ='DriverInformationService',
#        charset='utf8',
#        )     

#cur = conn.cursor()



#創建cookie
filename = 'BusWebcookie.txt'

cookie = http.cookiejar.MozillaCookieJar(filename)  #聲明一個MozillaCookieJar對象實例来保存cookie，之後寫入文件
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)


postdata = urllib.parse.urlencode({ "method":"queryDriverDetail",
                                    "seq":"13975",
                                    "companyName":"統聯汽車客運股份有限公司",
                                    "countyName":"新北市",
                                    "town":"三重區",
                                    "address":"光復路２段７３號",
                                    "tel":"02-29957799"  }).encode('utf-8')

headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }

loginUrl = "https://www.mvdis.gov.tw/m3-emv-mk3/freeway/query" #登錄初始頁面的URL


#導入ssl 關閉驗證 監理服務網是非信任網站
import ssl  
#context = ssl._create_unverified_context()
ssl._create_default_https_context = ssl._create_unverified_context 
#request = urllib.request.Request(loginUrl,data=postdata,headers=headers,unverifiable= False)

request = urllib.request.Request(loginUrl,data=postdata,headers=headers)
result = opener.open(request) #模擬登錄，並把cookie保存到變量
cookie.save(ignore_discard=True, ignore_expires=True) #保存cookie到cookie.txt中


#p1-p146 == range(1,147)
for i in range(1,147):
    for error in range(5):
        try:
            #利用cookie請求訪問另一個網址 此網址是駕駛者資料網址
            driverUrl = 'https://www.mvdis.gov.tw/m3-emv-mk3/freeway/query?d-444630-p='+str(i)+'&method=queryDriverDetailByDisplaytag' 
            r = opener.open(driverUrl)  #請求訪問查詢網址
            #r = requests.post(Url, postdata ,verify=False)
            break;
        except Exception as e:
            print(e)
            continue;

    #print(r.read().decode('utf-8'))

    soup = BeautifulSoup(r.read().decode("utf-8"), "lxml")
    html = soup.findAll('tr',{'class':{'odd','even'}})               
    #print(r.text)


    for h in html:
        #print(h)
        try:
            company = '統聯'
            
            value = h.findAll('td',{'style':'text-align:center;'})
            name = value[0].string
            
            Date = value[1].string.replace("年","-").replace("月","-").replace("日","")  #時間轉換
            Date = Date.split('-')
            LicensingDate = str(int(Date[0])+1911)+"-"+Date[1]+"-"+Date[2]
            
            violation = value[2].string
            DrunkDriving = value[3].get_text().replace("\t","").replace("\r\n","").replace("\n","").replace("　","").replace(" ","") #消除空格
            print(company,name,LicensingDate,violation,DrunkDriving)
            
            #資料庫連線
            #cur.execute("INSERT IGNORE INTO Driver (company,name,LicensingDate,violation,DrunkDriving) VALUES ('"+company+"','"+name+"','"+LicensingDate+"','"+violation+"','"+DrunkDriving+"')")
            #conn.commit()   #提交數據 
        
        except Exception as e:
            print(e)   
     
    
    print("page "+ str(i) + " done")

            




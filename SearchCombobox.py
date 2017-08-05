#!/usr/local/bin/python
#-*-coding:utf-8-*-
# 2015-6-26 DaoXin
import pycurl
import StringIO
import urllib
import urllib2
from random import choice
import re
import sys
import string
from bs4 import BeautifulSoup
import requests
import sys
import csv
import xlrd
import xlwt

reload(sys)
sys.setdefaultencoding('utf-8')

# useragent 列表，大家可以自行去收集。不过在本例中似乎不需要这个
AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:2.0b4pre) Gecko/20100815 Minefield/4.0b4pre",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
    "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; zh-CN) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; zh-CN) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; zh-CN) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; fr-fr) AppleWebKit/312.5 (KHTML, like Gecko) Safari/312.3",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Camino/2.2.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0b6pre) Gecko/20100907 Firefox/4.0b6pre Camino/2.2a1pre",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML like Gecko) Chrome/22.0.1229.79 Safari/537.4",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0.112941",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6; zh-CN) AppleWebKit/528.16 (KHTML, like Gecko, Safari/528.16) OmniWeb/v622.8.0",
]


class CrawlBaidukeyword:

    def __init__(self):
        self.UserAgent = choice(AGENTS)

    # def curl(self, url):
    #     while 1:
    #         try:
    #             b = StringIO.StringIO()
    #             c = pycurl.Curl()
    #             c.setopt(pycurl.URL, url)  # 打开URL
    #             c.setopt(pycurl.FOLLOWLOCATION, 2)  # 允许跟踪来源，有参数：1和2
    #             c.setopt(pycurl.ENCODING, 'gzip')  # 开启gzip压缩提高下载速度
    #             c.setopt(pycurl.NOSIGNAL, True)  # 开启后多线程不会报错
    #             c.setopt(pycurl.MAXREDIRS, 1)  # 最大重定向次数，0表示不重定向
    #             c.setopt(pycurl.CONNECTTIMEOUT, 60)  # 链接超时
    #             c.setopt(pycurl.TIMEOUT, 30)  # 下载超时
    #             c.setopt(pycurl.USERAGENT, self.UserAgent)
    #             # pycurl.USERAGENT  模拟浏览器
    #             c.setopt(pycurl.WRITEFUNCTION, b.write)  # 回调写入字符串缓存
    #             c.perform()  # 执行上述访问网址的操作
    #             # print c.getinfo(pycurl.HTTP_CODE)
    #             c.close()
    #             html = b.getvalue() 
    #             # if 'http://verify.baidu.com/' in html:
    #             #     print "验证码"
    #             #     time.sleep(500)
    #             #     continue
    #             # else:
    #             return html  
    #         except:
    #             continue
    def requesturl(self,url):
        headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        # 'Cookie':BAIDUID=28DFC37089FDC6934485B1762084FD7B:FG=1; BIDUPSID=28DFC37089FDC6934485B1762084FD7B; PSTM=1493369082; BDUSS=M2MVN1V341bXFPUkV2aWp0ZjE5Tk4tVnlLOEYtbVYtaFFmbFZCdlExbUJDalZaSVFBQUFBJCQAAAAAAAAAAAEAAABsySg3tdrSu8e5QjJCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIF9DVmBfQ1ZQ0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; PSINO=6; H_PS_PSSID=22832_1446_13290_21121_21931_22159
        'Host':'sp0.baidu.com',
        # Referer:https://www.baidu.com/s?wd=%E9%92%93%E9%B1%BC%E8%88%B9&rsv_spt=1&rsv_iqid=0xb67d1b26000b9dbe&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&oq=http%253A%252F%252Fluoli770.d17.cc&rsv_t=6d2avGCd%2BCGSUKFPd6xkBMTchgRQf%2FnLl661i4m%2BRrDd%2BHI5TNwBKKhufeLXFMBBorRk&rsv_pq=837c5b1c000a7b0f&inputT=664&rsv_sug3=6&rsv_n=2&rsv_sug1=3&rsv_sug7=100&rsv_sug4=7607
        'User-Agent':self.UserAgent

        }
        while 1:
            r = requests.get(url,headers=headers)
            if 'http://verify.baidu.com/' in r.text:
                print "验证码"
                time.sleep(500)
                continue  
            else: 
                return r.text

    def baiduindexcombobox(self, guanjianmuci):
        baiduindex_data = []
        baiduurl = "http://nssug.baidu.com/su?prod=index&wd=" + \
            urllib.quote(guanjianmuci)
        pagehtml = self.curl(baiduurl)
        if "p:false," in pagehtml:
            cwguanjiancilist = re.findall(r"\"(.*?)\"", pagehtml)
            del cwguanjiancilist[0]
            for cwguanjianci in cwguanjiancilist:
                baiduindex_data.append(cwguanjianci)

        return baiduindex_data

    def baiducombobox(self, guanjianmuci):
        baiducombobox_data = []
        baiducomboboxurl = "https://sp0.baidu.com/5a1Fazu8AA54nxGko9WTAnF6hhy/su?wd=%s" % guanjianmuci
        baiducomboboxpagehtml = self.requesturl(baiducomboboxurl)
        if "p:false," in baiducomboboxpagehtml:
            bdcbguanjiancilist = re.findall(r"\"(.*?)\"", baiducomboboxpagehtml)
            del bdcbguanjiancilist[0]
            for bdcbguanjianci in bdcbguanjiancilist:
                baiducombobox_data.append(bdcbguanjianci)

        return baiducombobox_data

    def baidurightrelatedsearch(self, cppagehtml):
        rightrelatedsearch_data = []

        baidurightsoup = BeautifulSoup(cppagehtml, "lxml")
        zchtml = baidurightsoup.find_all(
            "div", class_="opr-recommends-merge-panel opr-recommends-merge-mbGap")

        for chanpinbt in zchtml:
            zchtml1 = chanpinbt.select(
                "[class~=c-gap-top-small] a")
            for chanpinbt in zchtml1:
                rightrelatedsearch_data.append(chanpinbt.string)

        return rightrelatedsearch_data

    def index5118(self, pagehtml):
        keywordindex_data = []
        keywordssnum_data = []

        soup = BeautifulSoup(pagehtml, "lxml")
        keywordindexhtml = soup.select(
            "[class~=Fn-ui-list] dl:nth-of-type(2) dd:nth-of-type(2)")
        for keywordindex in keywordindexhtml:
            keywordindex_data.append(keywordindex.string)

        keywordssnumhtml = soup.select(
            "[class~=Fn-ui-list] dl:nth-of-type(2) dd:nth-of-type(3)")
        for keywordssnum in keywordssnumhtml:
            keywordssnum_data.append(keywordssnum.string)

        data5118_data = [keywordindex_data, keywordssnum_data]

        return keywordindex_data

    def socombobox(self, guanjianmuci):
        socombobox_data = []
        baiduurl = "https://sug.so.360.cn/suggest?callback=suggest_so&encodein=utf-8&encodeout=utf-8&format=json&fields=word,obdata&word=" + \
            urllib.quote(guanjianmuci)
        pagehtml = self.curl(baiduurl)
        if "\"result\":[]" not in pagehtml:
            cwguanjiancilist = re.findall(r"\"word\":\"(.*?)\"}", pagehtml)
            for cwguanjianci in cwguanjiancilist:
                socombobox_data.append(cwguanjianci)

        return socombobox_data

    def sogoucombobox(self, guanjianmuci):
        sogoucombobox = []
        baiduurl = "https://www.sogou.com/suggnew/ajajjson?key=" + \
            urllib.quote(guanjianmuci) + "&type=web"
        pagehtml = self.curl(baiduurl)
        if "[],[],[]," not in pagehtml:
            cwguanjiancilist = re.findall(
                r"sug\([\".*\",[(.*)\"],[\"0;", pagehtml)
            for cwguanjianci in cwguanjiancilist:
                sogoucombobox.append(cwguanjianci)

        return sogoucombobox

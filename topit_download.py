#-*- coding:UTF-8 -*-
import urllib2 , urllib
import sys,os
import re,cookielib
from BeautifulSoup import BeautifulSoup
from time import sleep

default_encoding = 'utf-8'
if sys.getdefaultencoding != default_encoding:  #解决out range[128]
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def opener(url):
    cookie = cookielib.CookieJar()
    hand = urllib2.HTTPCookieProcessor(cookie)
    opener=urllib2.build_opener(hand)
    opener.open('http://www.topit.me/event/warmup/welcome/views/index.html')
    opener.addheaders.append(('Cookie','is_click=1'))
    return opener.open(url)

def report(count,blocksize,totalsize):
    per = int(100*count*blocksize/totalsize)
    if per > 100:
        per = 100
    sys.stdout.write("\r%%%d complete"%per)
    sys.stdout.flush()

class topit():
    def __init__(self):
        self.page_list = []
        self.item_list=[]
        self.download_list = []
        self.title_list = []
        self.path = ''
        self.base_url = 'http://www.topit.me/?p='
        self.enable = True
        self.count = 1

    def get_item_url(self, url):  # 得到http://www.topit.me/item/29449582
        # print url
        print "正在获取资源……"
        response=opener(url).read()
        # print opener(url).info()
        # print response
        soup = BeautifulSoup(response)
        for p in soup.findAll(href=re.compile(r'.*?/item/[0-9]+?$')):
            self.item_list.append(p['href'])
            self.item_list=list(set(self.item_list))

    def get_download_url(self,item_url):  # get download_url
        response=opener(item_url).read()
        # print opener(item_url).info()
        soup = BeautifulSoup(response)
        self.download_list.append(soup.find('a',download='')['href'])
        self.title_list.append(soup.h2.string)
        #print "寻找到资源"

    def download_pic(self):  # 下载图片
        path = self.path+'/'+self.title_list[0]+'.jpg'
        if os.path.exists(path):
            print "第%d张图片已经存在"%self.count
            self.count += 1
            del self.download_list[0]
            del self.title_list[0]
            if len(self.item_list):
                self.downloading()
            else:
                self.enable = False
                self.downloading()
        # print opener(self.download_list[0]).info
        urllib.urlretrieve(self.download_list[0], path,reporthook=report)
        print ""
        print "第%d张图片下载完成"%self.count
        self.count+=1
        #    sleep(60)
        del self.download_list[0]
        del self.title_list[0]
        if len(self.item_list):
            sleep(10)

    def before_down(self):
        start_page = int(raw_input('请输入起始页数:'))
        end_page = int(raw_input('请输入结束页数:'))
        self.path=raw_input('请输入存储位置:')
        while start_page <= end_page:
            self.page_list.append(self.base_url+str(start_page+1))
            start_page+=1
        print "开始下载图片"

    def downloading(self):
        while self.enable:
            # print "TEST"
            if len(self.item_list)<=3 and len(self.page_list):  # 判断是需要加载下一页
                self.get_item_url(self.page_list[0])
                del self.page_list[0]
            self.get_download_url(self.item_list[0])
            del self.item_list[0]
            self.download_pic()
            if len(self.item_list) == 0:
                self.enable =False
            # print len(self.item_list)
        print "下载完成"
        self.after_down()

    def after_down(self):
        choice = raw_input("输入R返回下载页面，输入Q退出程序:")
        if choice in ['R','r','Q','q']:
            if choice == 'R' or choice == 'r':
                self.Start()
            else :
                sys.exit(0)
        else :
            print"请输入正确选择"
            self.after_down()

    def Start(self):
        self.before_down()
        self.downloading()


if __name__ =='__main__':
    print"""************************
程序：topit.me图片爬虫
作者：DHS
时间：2015.10.2
问题：输入检查未完成
************************"""
    s = topit()
    s.Start()







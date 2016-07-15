#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author: nothing -*-
# Pw @ 2016-01-22 14:57:34

import requests
import re
import sys
import time
reload(sys)
sys.setdefaultencoding("utf-8")
import os
class spider(object):
    def __init__(self):
        print "spider start work...."

#获取网页源码
    def getsource(self,url):
        html = requests.get(url)
        return html.text

#产生不同页数的链接
    def changepage(self,url,total_page):
        now_page = int(re.search('pageNum=(\d+)',url,re.S).group(1))
        page_group = []
        for i in range(now_page,total_page+1):
            link = re.sub('pageNum=\d+','pageNum=%s'%i,url,re.S)
            page_group.append(link)
        return page_group

#抓取每个课程块的信息
    def geteveryclass(self,source):
        everyclass = re.findall('deg="0"(.*?)</li>',source,re.S)
        return everyclass

#提取信息
    def getinfo(self,eachclass):
        info = {}
        info['title'] = re.search('alt="(.*?)">',eachclass,re.S).group(1)
        info['address'] = re.search('<a href="(.*?)\.html" target="_blank"',eachclass,re.S).group(1)
        info['content'] = re.search('none;">(.*?)</p>',eachclass,re.S).group(1).strip()
        timeandlevel = re.findall('<em>(.*?)</em>',eachclass,re.S)
        info['classtime'] = timeandlevel[0]
        info['classlevel'] = timeandlevel[1]
        info['learnnum'] = re.search('number">(.*?)</em>',eachclass,re.S).group(1)
        return info
    #保存
    def saveinfo(self,classinfo):
        f = open('jikexueyuan2.txt','w')
        fobj = open('linkssss.txt','w')
        for each in classinfo:
            f.writelines('title:' + each['title'] + '\n')
            f.writelines('address:' + each['address'] + '\n')
            f.writelines('content:' + each['content'] + '\n')
            f.writelines('classtime:' + each['classtime'] + '\n')
            f.writelines('classlevel:' + each['classlevel'] + '\n')
            f.writelines('learnnum:' + each['learnnum'] + '\n\n')
            fobj.writelines(each['address'] + '\n')
        f.close()
        fobj.close()

#生成课时和题目文件夹，注意：可是文件夹需要执行一步替换操作
    def title_time(self,classinfo):
        keshi = open('keshi.txt','w')
        for each in classinfo:
            keshi.writelines(each['classtime'][0:2] + '\n')
        keshi.close()
#生成所有链接
    def all_links(self):
        link = open('linkssss.txt','r')
        keshi = open('keshi2.txt','r')
        fobj = open('links.txt','w')
        while True:
            num = keshi.readline().strip('\n')
            jk_link = link.readline().strip('\n')
            if num and jk_link:        
                for i in range(1,int(num)+1):
                    jk_url = jk_link + '_' + str(i) + '.html?ss=1'
                    fobj.writelines(jk_url + '\n')
            else:
                break
        link.close()
        keshi.close()
        fobj.close()
#生成课时数字
    def keshi(self):
        f = open('keshi.txt','r')
        fo = open('keshi2.txt','w')
        while True:
            num = f.readline().strip('\n')
            if num:
                try:
                    fo.writelines(str(int(num)) + '\n')
                except:
                    for i in num:
                        if i.isdigit():
                            fo.writelines(str(int(i)) + '\n')
                        else:
                            break
            else:
                break
        f.close()
        fo.close()
if __name__ == '__main__':
    classinfo = []
    url = 'http://www.jikexueyuan.com/course/?pageNum=1'
    jikespider = spider()
    all_links = jikespider.changepage(url,85)
    for link in all_links:
        print u'正在处理页面：' + link
        time.sleep(5)
        html = jikespider.getsource(link)
        everyclass = jikespider.geteveryclass(html)
        for each in everyclass:
            #print '/**************************************/'
            #print each
            info = jikespider.getinfo(each)
            classinfo.append(info)
        #print classinfo
    jikespider.saveinfo(classinfo)
    jikespider.title_time(classinfo)
    jikespider.keshi()
    jikespider.all_links()
print u'全部处理完成！'
print u'开始删除多余文件。。。。'
os.system('rm jikexueyuan2.txt keshi.txt keshi2.txt linkssss.txt')
print u'删除完毕。。。'
print u'开始爬取标题'
os.system('python menu.py')

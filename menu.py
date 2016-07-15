#coding=utf-8
import requests
import re
import os
import traceback
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
s = requests.Session()
link = open('links.txt','r')
menu = open('menu.txt','w')
mysql = open('mysql.txt','w')
error = open('error.txt','w')
print '开始读取url。。。'
while True:
    links = link.readline().strip('\n')
    if links:
        try:
            jike = requests.get(links)
            html = jike.text
            try:
                title_all = re.findall(re.compile('.jpg">(.*?)<'),html)[0]
                title = re.findall(re.compile('.jpg">(.*?)<'),html)[1]
                print u'开始写入总标题: ' + title_all
                menu.writelines(title_all.encode('utf8') + '\n')
                print u'开始写入标题: ' + title
                menu.writelines('----' + title.encode('utf8') + '***:' + links +'\n')
                mysql.writelines(title.encode('utf8')+';'+links+'\n')
            except IndexError:
                try:
                    title = re.findall(re.compile('.jpg">(.*?)<'),html)[0]
                    print u'开始写入标题: ' + title
                    menu.writelines('----' + title.encode('utf8') + '***:' + links +'\n')
                    mysql.writelines(title.encode('utf8')+';'+links+'\n')
                except IndexError:
                    try:
                        title_all = re.findall(re.compile('.png">(.*?)<'),html)[3]
                        title = re.findall(re.compile('.png">(.*?)<'),html)[4]
                        print u'开始写入总标题: ' + title_all
                        menu.writelines(title_all.encode('utf8') + '\n')
                        print u'开始写入标题: ' + title
                        menu.writelines('----' + title.encode('utf8') + '***:' + links +'\n')
                        mysql.writelines(title.encode('utf8')+';'+links+'\n')
                    except IndexError:
                        title = re.findall(re.compile('.png">(.*?)<'),html)[3]
                        print u'开始写入标题: ' + title
                        menu.writelines('----' + title.encode('utf8') + '***:' + links +'\n')
                        mysql.writelines(title.encode('utf8')+';'+links+'\n')
        except Exception,ex:
            print u'连接错误: '+links
            traceback.print_exc(file=error)
            error.writelines("\nerror: " + links + '\n\n')
            pass
    else:
        break
print "Everything is OK!"
link.close()
menu.close()
error.flush()
error.close()
mysql.close()

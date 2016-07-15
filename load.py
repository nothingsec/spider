#coding=utf-8
import requests
import re
import os
import time
import traceback

s = requests.session()
#requests.adapters.DEFAULT_RETRIES = 5
s.config['keep_alive'] = False

def login():
    login_url = "http://passport.jikexueyuan.com/sso/login"
    post_url = "http://passport.jikexueyuan.com/submit/login?is_ajax=1"
    verifyCode_url = "http://passport.jikexueyuan.com/sso/verify"

    request = s.get(login_url)
    html = request.text
    #获取登录数据
    expire = re.search(r"(?s)value='(.*?)' name='expire",html)
    #开始下载验证码
    verifyCodeGifPath = '/root/jikexueyuan.gif'
    verify_code = s.get(verifyCode_url)
    data = verify_code.content
    code_pic = open(verifyCodeGifPath,'w')
    code_pic.write(data)
    code_pic.flush()
    code_pic.close()
    #读取保存到本地的验证码
    os.system('eog ' + verifyCodeGifPath)
    verify = raw_input("请输入图中的验证码:")  
    postdata = {
            'expire': expire.group(1),
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
            'referer': 'http%3A%2F%2Fwww.jikexueyuan.com%2F',
            'uname': 'wenjuan.lian@126.com',
            'password': '2016skdwlaqxz', 
            'verify': verify,                                   
            }
    post_data = s.post(post_url,postdata)
    print "登陆成功"

login()
index_url = 'http://www.jikexueyuan.com/course/2479_1.html?ss=1'
r = s.get(index_url)
cookies = r.request.headers['Cookie']
print cookies

link = open('links.txt','r')
mp4_url = open('url.txt','w')
error = open('error.txt','w')
print '开始读取url。。。'
while True:
    links = link.readline().strip('\n')
    if links:
        jike = s.get(links)
        html = jike.text
        try:
            #123
            name = re.search(r'(?s)<title>(.*?)-',html,re.S).group(1)
            mp4 = re.search('<source src="(.*?)" type',html,re.S).group(1)
            print name
            print u'开始写入mp4: ' + mp4
            mp4_url.write(mp4 + ' : ' + links + '\n')            
            os.system("wget -c %s" % mp4)
            s.config['keep_alive'] = False
        except:
            print "出现异常！跳过: " + links
            traceback.print_exc(file=error)
            error.writelines('error: ' + links + '\n')
            pass            
        time.sleep(10)
    else:
        break
link.close()
mp4_url.close()
error.close()

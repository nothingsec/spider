#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author: nothing -*-
# Pw @ 2016-03-25 12:40:09

import requests
import re
import os
import time

s = requests.Session()

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
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36',
            'referer': 'http%3A%2F%2Fwww.jikexueyuan.com%2F',
            'uname': 'wenjuan.lian@126.com',                   
            'password': '2016skdwlaqxz',                                    
            'verify': verify,                                   
            }
    post_data = s.post(post_url,postdata)
    print "登陆成功"

login()
index_url = 'http://www.jikexueyuan.com/course/2633.html'
r = s.get(index_url)
cookies = r.request.headers['Cookie']
print cookies

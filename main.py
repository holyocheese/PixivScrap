#-*- coding:utf-8 -*-
import os
import urllib
from bs4 import BeautifulSoup as Bs
import sys
import requests
import demjson

reload(sys)
sys.setdefaultencoding('utf-8')
# 统一访问session
se = requests.session()
# 变更工作空间
os.chdir(r'd:\\cheese python\\pixiv_img')
path = r'd:\\cheese python\\pixiv_img'
filename = 'cookie.txt'

class Pixiv(object):
    '''pixiv请求类'''

    def __init__(self):
        # 主页
        self.indexurl = "https://www.pixiv.net/"
        # 登录请求连接
        self.loginurl = "https://accounts.pixiv.net/api/login?lang=zh"
        # 图片搜索列表
        self.img_list_url = "https://www.pixiv.net/search.php"
        # 作者页
        self.inner_url = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id="
        # 请求头
        self.headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        # 登录所需数据
        self.logindata = {
            'pixiv_id': 'j8436346@gmail.com',
            'password': '123456',
            'return_to': r"https://www.pixiv.net/",
            'post_key': []
        }
        # 搜索关键词、页数
        self.searchdata = {
            'word': '',
            'order': 'date_d',
            'p': 1,
        }
        # 作者页搜索结果列表
        self.img_list = []
        # 下载连接和标题
        self.down_list = []

    def login(self):
        """模拟登录请求"""
        postkey = self.getpostkey()
        if(postkey == None):
            print "postkey为空！"
            return
        else:
            self.logindata['post_key'] = postkey
        #登录
        try:
            se.post(self.loginurl, data=self.logindata, headers=self.headers)
            print "Login Done!"
        except Exception as e:
            print e

    def get_img_list(self, keyword="10000users", page= 1):
        """搜索所有图片，跳转页"""
        count = 1
        postdata = self.searchdata
        postdata['word'] = keyword
        # 循环获取图片搜索页到目标页数为止
        # 添加进pixiv.inner_url列表
        while count <= page:
            print "Page " +str(count)
            postdata['p'] = count
            searchdata = urllib.urlencode(postdata)
            html = se.get(self.img_list_url+"?"+searchdata, headers=self.headers)
            bsObj = Bs(html.text, 'lxml')
            href = bsObj.findAll("div",{"id":"js-mount-point-search-result-list"})
            # 获取作品ID拼接跳转连接
            for dataitem in href:
                if 'data-items' in dataitem.attrs:
                    print dataitem.attrs['data-items'].decode("unicode-escape")
                    toObj = demjson.decode(dataitem.attrs['data-items'])
                    for item in toObj:
                        if item not in self.img_list:
                            self.img_list.append(self.inner_url+item["illustId"])
            print "page " + str(count) + " add DONE!"
            # 获取当前页所有图片 （下载）
            for link in self.img_list:
                html = se.get(link, headers=self.headers)
                bsObj = Bs(html.text, 'lxml')
                try:
                    src = bsObj.find("img", {"class": "original-image"})
                    if src:
                        print filename + "is Downloading"
                        self.down_list.append({"src": src.attrs['data-src'].decode("unicode-escape"),
                                               "title": src.attrs['alt']})
                        filetype = src.attrs['data-src'].split('.')[-1]
                        url = 'http://www.baidu.com'
                        local = r'd://google.html'
                        urllib.urlretrieve(url, local)
                        urllib.urlretrieve(src.attrs['data-src'], os.path.join(path, filename + "." + filetype))
                except AttributeError as e:
                    print "NOT Found"
                except Exception as e:
                    print e
            for item in self.down_list:
                for key in item:
                    print key + ":" + item[key]

            self.download(self.down_list)
            # self.saveimg()
            # 页数+1
            count = count + 1
            # 清空图片连接
            self.img_list = []

    def download(dict, threadnum=1):
        os.mkdir("geigei")
        for i in dict:
            for link in i:
                src = link['src']
                filetype = link['src'].split('.')[-1]
                filename = link['title']
                try:
                    print filename + "is Downloading"
                    urllib.urlretrieve(src, os.path.join(path, filename + "." + filetype))
                except:
                    print '\tError retrieving the URL:'

    def main(self):
        self.login()
        self.get_img_list()

    def getpostkey(self):
        """获取登录所需要的postkey"""
        url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
        try:
            html = se.get(url, headers=self.headers).text
        except Exception as e:
            print "VPN"
            return ""
        bsObj = Bs(html, "lxml")
        postkey = bsObj.find('input')['value']
        return postkey

if __name__ == "__main__":
    pixiv = Pixiv()
    pixiv.main()

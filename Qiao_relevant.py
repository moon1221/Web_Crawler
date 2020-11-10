# -*- coding:utf-8 -*-
from selenium import webdriver
from lxml import etree
import pymysql
import re
from pyquery import PyQuery as pq
def insert(table,value):
    db = pymysql.connect("localhost", "root", "root", "qiao")
    cursor = db.cursor()
    sql = 'INSERT INTO {} (title,content,image) VALUES ("{}","{}","{}")'.format(table,value[0],value[1],value[2])
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()
def get_first_link():
    url=[]
    browser = webdriver.Chrome()
    url_index = 'http://www.fj-archives.org.cn/dazt/qpzt/qpcg/kzqp/#'
    browser.get(url=url_index)
    parse_html = etree.HTML(browser.page_source)
    url.append('http://www.fj-archives.org.cn/dazt/qpzt/qpcg/kzqp/'+parse_html.xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/ul/li[1]/a/@href')[0])
    url.append('http://www.fj-archives.org.cn/dazt/qpzt/qpcg/kzqp/' + parse_html.xpath('/html/body/div[2]/div/div[2]/div[1]/div[2]/ul/li[2]/a/@href')[0])
    # print(url)
    return url
def kangzhan(url):
    browser = webdriver.Chrome()
    browser.get(url=url)
    parse_html = etree.HTML(browser.page_source)
    str = parse_html.xpath('/html/body/div[2]/div/div[2]/div[2]/div/ul/li/a/@href')
    for i in range(0, 3):
        imf = []
        li_url = 'http://www.fj-archives.org.cn/dazt/qpzt/qpcg/kzqp' + str[i]
        # print(li_url)
        browser.get(li_url)
        # print(browser.page_source)
        parse_html1 = etree.HTML(browser.page_source)
        imf.append(parse_html1.xpath('//h3/text()')[0])
        imf.append(parse_html1.xpath('//*[@id="detailCon"]//p/text()'))
        img = parse_html1.xpath('//*[@id="detailCon"]//img/@src')
        for j in range(0, len(img)):
            # result = li_url.split('/')
            # print(result, result[7])
            img[j] = 'http://www.fj-archives.org.cn/' + img[j]
            print(img[j])
        imf.append(img)
        print(imf)
        # insert('qiao_kang_zhan',imf)

def gushi(url):
    # print(url)
    browser = webdriver.Chrome()
    browser.get(url=url)  #获取传入网址的网页内容
    # print(browser.page_source)
    parse_html = etree.HTML(browser.page_source) #通过lxml中的etree中的xpath来获取元素属性或者元素内容
    str = parse_html.xpath('/html/body/div[2]/div/div[2]/div[2]/div/ul/li/a/@href')  #列表的url，不过这样只能获取到一部分，需要后面进行拼接
    # print(str)
    for i in range(0, len(str)):
        imf_gushi = []
        li_url = url + str[i]   #进行url拼接
        print(li_url)
        browser.get(li_url)     #抓取li_url的内容
        # print(browser.page_source)
        parse_html1 = etree.HTML(browser.page_source)
        imf_gushi.append(parse_html1.xpath('//h3/text()')[0])   #获取到标题
        imf_gushi.append(parse_html1.xpath('/html/body/div[2]/div/div[2]/div//span/text()'))   #获取到文本内容
        img = parse_html1.xpath('/html/body/div[2]/div/div[2]/div//img/@src')     #获得图片的地址，但是只有后半部分（用JS可以通过src属性获取到完全的地址，还待解决），目前用字符串拼接的方法
        for j in range(0, len(img)):
            result=li_url.split('/')     #首先进行字符串切割
            print(result,result[10])
            img[j] ='http://www.fj-archives.org.cn/dazt/qpzt/qpcg/qpgs_1452/'+result[10] +img[j]    #拼接地址
            # print(img[j]) 输出图片url
        imf_gushi.append(img)   #图片字段追加到插入信息
        insert('qiao_kang_zhan',imf_gushi)  #调用插

if __name__=='__main__':
    url=get_first_link()  #首页获取到桥批抗战和桥批故事的url
    # gushi(url[1])
    kangzhan(url[0])
    # insert('qiao_kang_zhan',kangzhan(url[0]))   #调用插入函数以及qiao_kang_zhan函数
    # insert('qiao_gu_shi',gushi(url[1]))

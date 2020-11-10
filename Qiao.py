# -*- coding:utf-8 -*-
from lxml import etree
import json
import pymysql
import requests
def xiaoshuo():
    # 不添加请求头，浏览器会识别到，请求错误

    target = 'http://www.fj-archives.org.cn/dazt/qpzt/qpcg/kzqp/#'
    req = requests.get(target)
    headers = {
        'user-agent': 'Mozilla/5.0'  # 加上请求头,
    }
    req = requests.get(target, headers=headers)
    req.encoding = req.apparent_encoding
    print(req.status_code)
    print('尝试：',req.text)

def rsp():
    proxies = {
        "HTTP": "http://221.224.136.211",   #使用代理
    }
    target = 'http://app.lib.stu.edu.cn/qiaopi/list_2'
    req = requests.get(target)
    headers = {
        'user-agent': 'Mozilla/5.0'  # 加上请求头,
    }
    req = requests.get(target, headers=headers,proxies=proxies)
    req.raise_for_status()
    req.encoding='utf-8-sig'
    parse_html = etree.HTML(req.text)
    links = parse_html.xpath('//*[@id="articleList"]/ul/li[1]/a')
    # print(links)
    for index in range(len(links)):
    #     # links[index]返回的是一个字典
    #     print(links[index].tag)
        print(links[index].attrib)
    #     print(links[index].text)

def insert(value):
    db = pymysql.connect("localhost", "root", "root", "qiao")
    cursor = db.cursor()
    sql = "INSERT INTO qiao_search_json (json) VALUES ({})".format(value)
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()

def getData():
    from selenium import webdriver
    from html.parser import HTMLParser
    browser = webdriver.Chrome()
    for i in range(2,5):
        url='https://qiaopisjk.sysu.edu.cn/api/item/{}'.format(i)
        print(url)
        browser.get(url=url)
        htm=browser.page_source
        parse_html=etree.HTML(htm)
        # parse_html.xpath('//*[@id="root"]/pre/text()')
        # / html / body
        data=parse_html.xpath('/html/body/pre/text()')
        print(data[0])
        data_json="'"+data[0]+"'"
        print(data_json)
        # data_list=json.loads(data[0])
        # print(data_list['data'])
        return data_json
        # print(parse_html.xpath('/html/body/pre/text()'))
    browser.close()

if __name__=='__main__':
    getData()
    insert(getData())

# -*- coding:utf-8 -*-
from selenium import webdriver
from lxml import etree
import pymysql
import time,re
import requests
from selenium.webdriver.common.action_chains import ActionChains
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

def get_link():
    links=[]
    url='http://app.lib.stu.edu.cn/qiaopi/list_2'
    browser = webdriver.Chrome()
    browser.get(url=url)
    parse_html=etree.HTML(browser.page_source)
    # print(parse_html)
    link=parse_html.xpath('//*[@id="templatemo_menu"]/ul/li/a')
    # print(link)
    for index in range(len(link)):
        links.append('http://app.lib.stu.edu.cn'+link[index].attrib['href'])
        # print(links[index])
    return links

def get_all_link(ur):
    link_list=[]
    browser = webdriver.Chrome()
    for next in range(1, 2):
        url=ur+'{}'.format(next)
        print(url)
        browser.get(url=url)
        parse_html = etree.HTML(browser.page_source)
        link=(parse_html.xpath('//*[@id="articleList"]/ul/li/a'))  # 获取每一页中的链接
        for i in range(len(link)):
            list_url1=link[i].attrib['href']
            print(list_url1)
            list_url = 'http://app.lib.stu.edu.cn' + link[i].attrib['href']
            link_list.append(list_url)
        # a = browser.find_element_by_link_text('>')
        # a.click()
        # time.sleep(60)
    browser.quit()
    print(link_list)
    return link_list

def qiao_zixun(link_list):
    # link_list=['http://app.lib.stu.edu.cn/qiaopi/article/1777']
    browser = webdriver.Chrome()
    for i in range(0,1):
        value=[]
        str = '  '
        image=[]
        browser.get(url=link_list[i])
        dom_html=etree.HTML(browser.page_source)
        title=dom_html.xpath('//*[@id="ContentPlaceHolder1_title"]')[0].text
        value.append(title)
        content = dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]//p')
        for j in range(len(content)):
            str=str+content[j].xpath('string(.)')
        value.append(str)
        img=dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]//img')
        for k in range(len(img)):
            image.append(dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]//img')[k].attrib['src'])
        value.append(image)
        time.sleep(30)
        # print(value)
        insert('qiao_zi_xun',value)
    browser.quit()

def qiao_gushi(link_list):
    browser = webdriver.Chrome()
    for i in range(0, 1):
        value = []
        str = '  '
        image = []
        browser.get(url=link_list[i])
        dom_html = etree.HTML(browser.page_source)
        title = dom_html.xpath('//*[@id="ContentPlaceHolder1_title"]')[0].text
        value.append(title)
        content = dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]')
        for j in range(len(content)):
            str = str + content[j].xpath('string(.)')
        value.append(str)
        img = dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]//img')

        for k in range(len(img)):
            temp=img[k].attrib['src']
            if img[k]:  #利用正则表达式判断是不是真的地址
                image.append(temp)
            else:
                image.append('http://app.lib.stu.edu.cn'+temp)
        value.append(image)
        time.sleep(30)
        print(value)
        # insert('qiao_gu_shi', value)
    browser.quit()

def qiao_resources(link_list):
    browser = webdriver.Chrome()
    for i in range(0, 1):
        value = []
        str = '  '
        image = []
        browser.get(url=link_list[i])
        dom_html = etree.HTML(browser.page_source)
        title = dom_html.xpath('//*[@id="ContentPlaceHolder1_title"]')[0].text
        value.append(title)
        content = dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]')
        for j in range(len(content)):
            str = str + content[j].xpath('string(.)')
        value.append(str)
        img = dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]//img')

        for k in range(len(img)):
            if img[k]:  # 利用正则表达式判断是不是真的地址
                image.append(img[k])
            else:
                image.append('http://app.lib.stu.edu.cn' + img[k])
            image.append(dom_html.xpath('//*[@id="ContentPlaceHolder1_context"]//img')[k].attrib['src'])
        value.append(image)
        time.sleep(30)
        print(value)
        # insert('qiao_gu_shi', value)
    browser.quit()

if __name__=='__main__':
    get_all_link('http://app.lib.stu.edu.cn/qiaopi/list_2?page=')
    get_all_link('http://app.lib.stu.edu.cn/qiaopi/list_8?page=')
    # qiao_gushi(result)
    # qiao_zixun(result)
    # qiao_zixun()
    # urls=get_link()
    # qiao_zixun(urls[1])
    # qiao_resources(urls[3])

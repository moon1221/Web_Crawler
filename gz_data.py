db = None
cursor = None
broswer = None
md_grid_list = None
one = None
title = None
tt = None
fromx = None
f1 = None
f2 = None
ff1 = None
ff2 = None
countx = None
c1 = None
c2 = None
cc1 = None
cc2 = None
formats = None
fm = None
detail = None
tags = None
tag = None
sql = None
rs = None
oo = None
pp =None
topicx=None
scorex=None
mask_numx=None
data_hzx=None
man_numx=""
man_scorex=""
man_repalyx=""
abs_contentx =""

def openWin(broswer,detail):

    ActionChains(broswer).move_to_element(detail).perform()
    broswer.execute_script('arguments[0].scrollIntoView(false);', detail)
    time.sleep(5)
    broswer.execute_script("arguments[0].target = '_blank';", detail) #浏览器执行一个JS代码
    time.sleep(3);
    ActionChains(broswer).move_to_element(detail).click().perform()
    time.sleep(5)
    if(len(broswer.window_handles)<=1):
        openWin(broswer, detail);

    return


def  read_page(broswer,cursor):
    md_grid_list = broswer.find_elements_by_class_name("openDataListSubBg") #获取数据总条数
    _l = len(md_grid_list)
    for num in range(0, _l):
        md_grid_list = broswer.find_elements_by_class_name('openDataListSubBg')
        time.sleep(5);
        one = md_grid_list[num]
        title = one.find_element_by_class_name('cardTitle')
        tt = title.text
        print(tt)
        fromx = one.find_elements_by_css_selector('.groupTime span')
        f1 = fromx[0]
        f2 = fromx[1]
        ff1 = f1.text
        ff2 = f2.text
        print(ff1)
        print(ff2)
        countx = one.find_elements_by_css_selector('.dataCounts span')
        c1 = countx[0]
        c2 = countx[1]
        cc1 = c1.text
        cc2 = c2.text
        print(cc1)
        print(cc2)
        formats = one.find_element_by_class_name('fileFormat')
        fm = formats.text
        print(fm)

        topicxx = one.find_element_by_css_selector(".titleIcon label")
        topicx = topicxx.text
        print(fm)

        score = one.find_element_by_class_name("score")
        scorex = score.text
        print(scorex)

        detail = one.find_element_by_tag_name('a')
        # print(detail.text)

        openWin(broswer, detail) #打开了一个新窗口，之前的窗口就不存在了，重点地方
        time.sleep(20);
        broswer.switch_to.window(broswer.window_handles[1])
        # print(broswer.page_source)
        time.sleep(5);
        urlx = broswer.current_url
        print(urlx)

        tags = broswer.find_elements_by_css_selector('.dataLabel .tag-item')
        tag = ",".join(t.text for t in tags)
        print(tag)

        try:
            detailMask = broswer.find_elements_by_class_name("detailMask")
            print(len(detailMask))
            mask_numx = len(detailMask)
        except:
            print("Error: cant find 项目数")

        dataDetailInfoContentBox = broswer.find_element_by_css_selector(".dataDetailInfoContentBox > .content >.ng-binding")
        abs_contentx = dataDetailInfoContentBox.text
        print(abs_contentx)

        dataP = broswer.find_elements_by_css_selector(".dataDetailInfoContentBox  .flex-100")

        try:
            dataOpenP2 = dataP[0].find_elements_by_class_name("flex-20")
            dataHz = dataOpenP2[2].find_elements_by_tag_name("span");
            print(dataHz[1].text)
            data_hzx = dataHz[1].text
        except:
            print("Error: cant find 更新频率")

        dataOpenP = dataP[0].find_elements_by_class_name("flex-20")
        dataOpen = dataOpenP[3].find_elements_by_tag_name("span");
        oo=dataOpen[1].text
        print(oo)
        dataOpenTime = dataP[1].find_elements_by_class_name("flex-20")
        dataTime = dataOpenTime[1].find_elements_by_tag_name("span");
        pp=dataTime[1].text
        print(pp)

        try:
            man = broswer.find_elements_by_class_name("dataDetailReplyName")
            man_numx = len(man)
            print(man_numx)
            dataDetailReplyContent = broswer.find_elements_by_class_name("dataDetailReplyContent")
            man_repalyx = '|'.join(i.text for i in dataDetailReplyContent)
            print(man_repalyx)

            # 评判星级
            s = []
            dataDetailReplyStar = broswer.find_elements_by_class_name("dataDetailReplyStar")
            for stars in dataDetailReplyStar:
                star = stars.find_elements_by_class_name("material-icons")
                print(len(star))
                s.append(len(star))
            man_scorex = ','.join(str(i) for i in s)
            print(man_scorex)
        except:
            print("Error: cant find reply")

        create_datex = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        sql = "insert into opendata_gz (title,source,update_date,download,view,formats,tag,open_type,public_date,score,topic,mask_num,data_hz,man_num,man_score,man_reply,abs_content,create_date,url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        cursor.execute(sql, [tt, ff1, ff2, cc1, cc2, fm, tag, oo, pp,scorex,topicx,mask_numx,data_hzx,man_numx,man_scorex,man_repalyx,abs_contentx,create_datex,urlx]);
        rs = db.commit()
        # 浏览器返回
        broswer.close()
        broswer.switch_to.window(broswer.window_handles[0])
        time.sleep(5)
    # 翻页
    next2 = broswer.find_elements_by_css_selector('.pageBox .pagination ul li')
    nextx = next2[int(len(next2) - 1)]
    classname = nextx.get_attribute("class")
    index = classname.find('disabled')
    print(index)
    if (index == -1):
        next = broswer.find_element_by_link_text("下一页")
        ActionChains(broswer).move_to_element(next).click().perform();
        time.sleep(15)
        # 递归
        read_page(broswer,cursor)
    return

import pymysql;
import time;
from selenium import webdriver;
from selenium.webdriver import ActionChains;


db = pymysql.connect("localhost","root","root","blockly_db",cursorclass = pymysql.cursors.DictCursor)
cursor = db.cursor()
broswer = webdriver.Chrome()  #启动浏览器
broswer.get('http://data.guizhou.gov.cn/#!/dataDirectory');
time.sleep(15);

read_page(broswer,cursor)


db.close();
broswer.close();
broswer.quit();

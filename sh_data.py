tt = None
ff1 = None
ff2 = None
cc1 = None
cc2 = None
fm = None
tag = None
oo = None
pp = None
scorex = None
topicx = None
mask_numx = None
data_hzx = None
man_numx = None
man_scorex = None
man_repalyx = None
abs_contentx = None
create_datex = None
urlx = None
manList = None
typexxx = None
xIndex = 0
pIndex = 0

#读留言
def  read_replay(broswer,listx): #递归读下一页，数据一对多（理论上应该新建一个表）
    ton_lis = broswer.find_elements_by_css_selector("#list-view .ton_li")
    _lx = len(ton_lis)
    listx[0] = listx[0] + len(ton_lis) #数组为参数，递归
    print(len(ton_lis))

    for numx in range(0,_lx):
        ton_lis = broswer.find_elements_by_css_selector("#list-view .ton_li")
        li = ton_lis[numx]
        p = li.find_elements_by_tag_name("p")
        print(p[2].text)
        listx[1].append(p[2].text)

        rate = li.find_elements_by_css_selector(".layui-rate .layui-icon-rate-solid")
        print(len(rate))
        listx[2].append(str(len(rate)))

    #翻页
    page  =  broswer.find_element_by_css_selector("#ton_page")
    ax = page.find_element_by_link_text('下一页')
    classname = ax.get_attribute("class")
    print(classname)
    index = classname.find('layui-disabled');
    print(index)
    if(index ==-1):
        ActionChains(broswer).move_to_element(ax).click().perform();
        time.sleep(15)
        read_replay(broswer, listx)
    return

def  read_page(broswer,cursor):
    md_grid_list = broswer.find_elements_by_class_name("result-item")
    time.sleep(5)
    i = 0
    j = 0
    print("##########")
    print(j)
    print("##########")
    _l = len(md_grid_list)
    for num in range(0,_l):
        md_grid_list = broswer.find_elements_by_class_name("result-item")
        one = md_grid_list[num]
        title = one.find_element_by_css_selector(".every-item .title")
        topic = one.find_element_by_css_selector(".every-item  .type .domain-type")

        typex = one.find_element_by_css_selector(".every-item  .type span")

        typexxx = typex.text
        typexxx = typexxx.strip()
        typexxx = typexxx[1:3]
        txx = "数据"
        print(typexxx)
        print(txx)
        print(typexxx==txx)
        print(typexxx , txx)
        print(len(txx))
        print(len(typexxx))

        if(typexxx == "数据"):
            print("type=",typexxx)

        datex = one.find_element_by_css_selector(".every-item  .date span")
        formats = one.find_elements_by_css_selector(".every-item .file-type-btn")
        countsx = one.find_elements_by_css_selector(".every-item  .number span i")

        score = one.find_elements_by_css_selector(".every-item .rate div .layui-icon-rate-solid")

        print(title.text)
        tt= title.text
        print(topic.text)
        topicx = topic.text

        print(datex.text)
        ff2 = datex.text
        print(countsx[0].text)
        cc2 = countsx[0].text
        print(countsx[1].text)
        cc1 =countsx[1].text

        fm = ",".join(t.text for t in formats)
        xIndex = 0
        pIndex = 0
        if(typexxx=="接口"):
            xIndex = -1
            pIndex = -2
            fm = typexxx
        print(fm)
        scorex = len(score)
        print(scorex)
        i = i + 1
        print("********************************************")
        print(i)
        print("********************************************")


        ActionChains(broswer).move_to_element(title).click().perform();
        time.sleep(25)
        broswer.switch_to.window(broswer.window_handles[1])
        urlx = broswer.current_url
        print(urlx)
        #print(broswer.page_source)

        deep = None
        deep = broswer.find_elements_by_css_selector("#table-result-wrap .deep")
        #print(deep)
        tds = broswer.find_elements_by_css_selector("#table-result-wrap td")

        dataDetailInfoContentBox = tds[0]
        print(dataDetailInfoContentBox.text)
        abs_contentx = dataDetailInfoContentBox.text

        try:
            tags = deep[1].find_element_by_css_selector("td")
            print(tags.text)
            tag = tags.text
        except:
            print("Error: cant find tags")

        if (typexxx == "数据"):
            try:
                detailMask = broswer.find_elements_by_css_selector(".layui-table-body tr")
                print(len(detailMask))
                mask_numx = len(detailMask)
            except:
                print("Error: cant find 项目数")
        else:
            try:
                detailMaskxxx = broswer.find_elements_by_css_selector(".return-value-table")
                detailMaskx = detailMaskxxx[1]
                print(detailMaskx.text)
                detailMask=detailMaskx.find_elements_by_css_selector("tbody tr")
                #print(detailMask.text)
                print(len(detailMask))
                mask_numx = len(detailMask)
            except:
                print("Error: cant find 项目数")

        try:
            dataOpen = tds[7+xIndex]
            #print(dataOpen[0].text)
            print(dataOpen.text)
            oo = dataOpen.text
        except:
            print("Error: cant find 开放属性")

        print(typexxx)
        if (typexxx == "数据"):
            try:
                dataHz = tds[8+xIndex]
                print(dataHz .text)
                data_hzx = dataHz .text
            except:
                print("Error: cant find 更新频率")
        else:
            data_hzx = "实时接口"
            print(data_hzx)

        try:
            dataDepart = deep[6+xIndex].find_element_by_css_selector("td")
            print(dataDepart.text)
            ff1 = dataDepart.text
        except:
            print("Error: cant find 数据提供方")

        try:
            dataOpenTime = tds[9+pIndex]
            print(dataOpenTime.text)
            pp=dataOpenTime.text
        except:
            print("Error: cant find 创建时间")

        manList = [0,[],[]];
        read_replay(broswer, manList)
        print(manList)
        man_numx = manList[0]
        man_repalyx = "|".join(manList[1])
        man_scorex = ",".join(manList[2])
        create_datex = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

        sql = "insert into opendata_sh (title,source,update_date,download,view,formats,tag,open_type,public_date,score,topic,mask_num,data_hz,man_num,man_score,man_reply,abs_content,create_date,url) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)";
        cursor.execute(sql, [tt, ff1, ff2, cc1, cc2, fm, tag, oo, pp, scorex, topicx, mask_numx, data_hzx, man_numx,
                             man_scorex, man_repalyx, abs_contentx, create_datex,urlx]);
        rs = db.commit()

        # 浏览器返回

        broswer.close()
        broswer.switch_to.window(broswer.window_handles[0])
        time.sleep(5)

    #翻页
    print("下一页")
    next = broswer.find_element_by_link_text("下一页")
    print(next.tag_name)
    classname = next.get_attribute("class")
    print(classname)
    index = classname.find('layui-disabled');
    print(index)
    if (index == -1):
        ActionChains(broswer).move_to_element(next).click().perform();
        time.sleep(15)
        # 递归
        read_page(broswer,cursor)
    # 测试翻页成功
    #md_grid_list = broswer.find_element_by_class_name("openDataListSubBg")
    #print(md_grid_list.text)
    return




from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import pymysql


broswer = None
count = None

# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "db")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

broswer = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
#broswer.set_page_load_timeout(5);
#broswer.set_script_timeout(15);
broswer.get('https://data.sh.gov.cn/view/data-resource/index.html');
time.sleep(25)

read_page(broswer,cursor)
broswer.close()
# 关闭数据库连接
db.close()


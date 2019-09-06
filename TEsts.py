import time,random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from threading import Thread
login_url = "https://passport.zhihuishu.com/login?service=https://onlineservice.zhihuishu.com/login/gologin"
delay_time = 30
MONITOR=True # 启用循环弹题监控
driver = webdriver.Chrome()
def xpath_object(xpathname):# 执行某种操作
    WebDriverWait(driver, delay_time).until(ec.presence_of_all_elements_located(
        (By.XPATH, xpathname)))
    return driver.find_element_by_xpath(xpathname)

def logging(text):
    local_time = time.ctime()
    with open('刷课日志.log','a',encoding='utf-8') as p:
        need_to_write = '时间:'+str(local_time)+"   事件:"+text+"\n"
        p.write(need_to_write)


def text_object(name):
    WebDriverWait(driver, delay_time).until(ec.presence_of_all_elements_located(
        (By.LINK_TEXT, name)))
    return driver.find_element_by_link_text(name)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2', 'Accept-Encoding': 'gzip, deflate, br', 'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': '188', 'Connection': 'keep-alive', 'Referer': 'https://passport.zhihuishu.com/login?service=https%3A%2F%2Fstudy.zhihuishu.com%2FlearningNew%2FvideoList%3FrecruitAndCourseId%3D4b5c5e50475241584143505c5a', 'Cookie': 'Hm_lvt_0a1b7151d8c580761c3aef32a3d501c6=1566874037,1567238270,1567427031; acw_tc=76b20fe215668740413035231e0419829e52a1a904c08c41d1158e01aceb5a; Z_LOCALE=1; c_session_id=1B8DFCEBBC9B5C7366FCB65ED8090116; route=10de0fe0538e49816d33b636c6edf649; JSESSIONID=91ACAD65407C97628F46977A5C9BCD13; source=-1; SERVERID=4516a494fea80bcfc392e5b45dea0690|1567662784|1567662775'}
def get_movie(html,local_lesson):
    from bs4 import BeautifulSoup
    import re
    soup = BeautifulSoup(html,'lxml')
    ul = soup.find('ul',class_="nano-content")
    num = 0
    eles = []
    names = []
    ids = []
    vedio_sizes = []
    for i in ul.children:
            # 原生条件：'id="progress_0"' in str(i) or 'class="fl time_icofinish" style="display:none"' in str(i)
        if "clearfix video " in str(i):
            if 'id="progress_0"' in str(i) or 'class="fl time_icofinish" style="display:none"' in str(i):
                eles.append(i)
                name = re.findall(r'_name="(.*?)"',str(i),re.S)[0]
                names.append(name)
                vedio_id = re.findall(r'" id="(video-[0-9]{5,8})"',str(i),re.S)[0]
                ids.append(vedio_id)
                try:
                    size = re.findall(r'<span class="time fl">(.*?)</span>',str(i),re.S)[0]
                except:
                    size = re.findall(r'<span class="time">(.*?)</span>',str(i),re.S)[0]
                vedio_sizes.append(size)
            else:
                print(re.findall(r'_name="(.*?)"',str(i),re.S)[0],'==已跳过')
    print(local_lesson)
    for element in names: # 防止element不在其中（防止字符串不完全一样）
        print(element)
        if str(element) in local_lesson:

            local_lesson = element
            break
    local_num = names.index(local_lesson)
    print(local_num)
    front = names[0:local_num]
    after = names[local_num:len(names)]# list全部转换一遍
    ids = ids[local_num:len(names)]
    sizes = vedio_sizes[local_num:len(names)]
    print(front)
    print(after)
        # print(i)
    # print(len(eles))
    # print(eles[-1])
    return after,ids,sizes

def mon(xpathname):   # 弹题辅助线程  ===>   主要作用:在界面弹出题目后,自动答题并关闭弹出的题目
    num = 1
    while MONITOR:
        time.sleep(1) # 检查频率为1秒一次
        try:
            num+=1
            driver.switch_to.frame("tmDialog_iframe")  # 转换到弹题的iframe =_=终于解决了庆祝下 9/5--0:51分
            WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located(
                    (By.XPATH, xpathname)))
            # '/html/body/div/div[1]/div/div/div/div/div/div/div[1]/span[2]/p[1]/span'
            '/html/body/div/div[1]/div/div/div/div/div/div/div[3]/label'



            '/html/body/div/div[1]/div/div/div/div/div/div/div[2]/label'
            driver.find_element_by_xpath('/html/body/div/div[1]/div/div/div/div/div/div/div[2]/label').click() #
            # time.sleep(1)
            driver.switch_to.default_content() # 转换为原页面
            # text_object('关闭').click() # error
            text_object('关闭').click()
            print("处理弹题成功！" )
            logging("处理弹题成功！" )

        except:
            if num%100==0:
                logging('脚本运行正常')
def login():
    driver.get(login_url)
    #  播放按钮JS： //*[@id="playButton"]
    xpath_username = '//*[@id="lUsername"]'
    xpath_password = '//*[@id="lPassword"]'
    xpath_button = '//*[@id="f_sign_up"]/div/span'
    xpath_object(xpath_username).send_keys("13793813168")
    xpath_object(xpath_password).send_keys("swbd1234")
    xpath_object(xpath_button).click()

def main():

    login()
    shengwuhuaxue = '//*[@id="sharingClassed"]/div[2]/ul[{}]'.format(2) # 共两节课 如果是第一节就填写ul[1],

    xpath_object(shengwuhuaxue).click()
    localtime = str(time.time()).replace('.', '')[0:13]
    # time.sleep(5)
    url = driver.current_url
    driver.get('https://www.baidu.com')
    driver.get(url)
    resp = driver.execute_script("return document.documentElement.outerHTML")   # 执行Js获取页面HTML STRING
    # print(resp)

    open('view.htm', 'w', encoding='utf8').write(resp)


    # time.sleep(10)
    try:
        WebDriverWait(driver, delay_time).until(ec.presence_of_all_elements_located(
            (By.LINK_TEXT, '我知道了')))
        driver.find_element_by_link_text('我知道了').click()
    except:
        logging('ERROR')

    # element = text_object('成绩分析')
    # driver.execute_script("arguments[0].click();", element) # 处理selenium.common.exceptions.ElementClickInterceptedException异常
    # n = driver.window_handles # 获取所有界面的句柄
    # print(n)
    # driver.switch_to.window(n[1]) # 将当前界面切换至新界面
    # url1 = driver.current_url
    # print(url1)
    # time.sleep(1)
    # name1 = driver.find_element_by_link_text('生物化学的涵义和研究内容')

    input("press any key to countinue")   #
    local_lesson = xpath_object('//*[@id="lessonOrder"]').text
    print(local_lesson)
    names, ids, sizes = get_movie(resp,local_lesson)
    # driver.close()
    # driver.switch_to.window(n[0]) #切换回原界

    # 监控线程



    qusetion_xpath = '/html/body/div/div[1]/div/div/div/div/div/div/div[1]'
    Monitor = Thread(target=mon,args=(qusetion_xpath,))
    Monitor.setDaemon(True) # 守护主线程
    Monitor.start()
    print(ids,names)
    for i in ids:#简单脂质 4分30出现一个弹题目

        time.sleep(5)
        i1 = '//*[@id="{}"]/div[1]/span[1]'.format(i)
        xpath_object(i1).click()
        # input("ii") '//*[@id="tm_dialog_win_1567681948870"]/div[2]/a'

        print("...")
        print(names[ids.index(i)])
        this_time = sizes[ids.index(i)]
        print(this_time)
        seconds = int(str(this_time).split(':')[0])*60*60+int(str(this_time).split(':')[1])*60+int(str(this_time).split(':')[2])
        print(seconds,'s')
        time.sleep(seconds+30) # 10分钟一个视频





    # print(resp.text)




if __name__ == '__main__':
    main()
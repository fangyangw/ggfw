
import sys
sys.path.insert(0, r'./chromedriver-win64')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
 
# 如果ChromeDriver在系统PATH中
driver = webdriver.Chrome()
 

#url = 'https://ggfw.hrss.gd.gov.cn/gdweb/ggfw/web/pub/ggfwzyjs.do'
url = 'https://ggfw.hrss.gd.gov.cn/isso/login.html'
url = 'https://ggfw.hrss.gd.gov.cn/zxpx/auc/myCourse'
# 打开网页
driver.get(url)

def answer_question():
    elms = driver.find_elements(By.XPATH,'//div[@class="exam-subject-text-queanswar-answer"]')
    if not elms:
        print("当前没有问题弹框，等待下次检测....")
        return 0
    select = random.randint(0,1)
    elm = elms[select]
    try:
        elm.click()
    except:
        print("点击选项失败，可能是隐藏的窗口")
        time.sleep(60)
        return False

    time.sleep(1)

    element = driver.find_elements(By.XPATH,"//*[contains(text(), '提交答案')]")
    if element:
        element[0].click()
    else:
        print("Error: 没有提交答案按钮")

    time.sleep(1)
    
    error_el = driver.find_elements(By.XPATH,"//*[contains(text(), '确定')]")
    # driver.find_elements(By.XPATH,'//a[@class="l-btn l-btn-small"]') 
    if error_el:
        print("=====================捕获到确定按钮：")
        print(error_el[0].get_attribute('outerHTML'))
        try:
            error_el[0].click()
        except Exception as e:
            print("Error: %s" % str(e))
    else:
        print("Error: 没有提交答案后的确认按钮")
    
    time.sleep(1)
    error_el = driver.find_elements(By.XPATH,"//*[contains(text(), '答案错误，请继续答题')]")
    if error_el:
        select = select + 1
        error_el = driver.find_elements(By.XPATH,"//*[contains(text(), '确认')]")
        if error_el:
            
            print("====================捕获到确认按钮：")
            print(error_el[0].get_attribute('outerHTML'))
            error_el[0].click()
        answer_question()
    return 1

def check_vidio(progress):
    elms = driver.find_elements(By.XPATH,'//*[@id="realPlayVideoTime"]')
    if elms:
        elm = elms[0]
        print("学习进度： %s" % elm.text)
        #if int(elm.text) > 98:
            #driver.close()
        return int(elm.text)
    else:
        elms = driver.find_elements(By.XPATH,"//*[contains(text(), '学习进度：')]")
        if elms:
            ee = elms[0].find_elements(By.XPATH,"//*[contains(text(), '已完成')]")
            if ee:
                return -1
            else:
                print("Error: 查不到学习进度，且状态不为已完成")
        return progress
        print("视频正常运行，不需要点击启动")


def start_pause_vidio():
    elm = None
    try:
        elm = driver.find_elements(By.XPATH,'//div[@class="prism-big-play-btn"]')
    except:
        print("Error: 查不到观察进度")
    # id like player-con_component_3F0695D3-0D51-4A60-B0C6-5D8446E0A3F5
    if elm:
        elm[0].click()

    elm = driver.find_elements(By.XPATH,'//div[@class="prism-big-play-btn"]')
    if elm:
        elm[0].click()

def check_and_watch_vidio():
    select = 0
    progress = 0
    while True:
        try:
            first_handle = driver.window_handles[0]
            driver.switch_to.window(first_handle)
            if start_pause_vidio():
                break
            answer_question()
            progress = check_vidio(progress)
            if progress == -1:
                break
            if progress >= 98:
                time.sleep(60)
                break
            time.sleep(5)
        except Exception as e:
            print(str(e))

def wait_user_login():
    while True:
        try:
            driver.switch_to.window(driver.window_handles[0])
            all_class = driver.find_elements(By.XPATH, "//*[contains(text(), '点击学习')]")
            print(all_class)
            if all_class:
                return all_class
        except Exception as e:
            print(str(e))
        time.sleep(10)


# 查找元素

all_class = wait_user_login()
time.sleep(2)
current_class = all_class[0]
current_class.click()
time.sleep(2)

current_class_index = 0

while True:
    
    try:
        check_and_watch_vidio()
        all_class = driver.find_elements(By.XPATH, "//*[contains(text(), '点击学习')]")
        if len(all_class) < 1:
            break
        current_class = all_class[0]
        current_class.click()
    
    # 处理元素找不到的异常
    except Exception as e:
        print(e)     
    time.sleep(2)

# 关闭浏览器
driver.quit()
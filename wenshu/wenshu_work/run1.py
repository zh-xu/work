from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.wait import WebDriverWait
import re
import random
import time

# 配置信息
options = webdriver.ChromeOptions()

# 取消浏览器正在受到测试软件的控制
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ['enable-automation'])

prefs = {"": ""}
prefs["credentials_enable_service"] = False
prefs[
    "profile.password_manager_enabled"] = False
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

driver.get(
    'https://account.court.gov.cn/oauth/authorize?response_type=code&client_id=zgcpwsw&redirect_uri=https%3A%2F%2Fwenshu.court.gov.cn%2FCallBackController%2FauthorizeCallBack&state=cec527c6-4cac-4dba-823f-c013f2cf14bd&timestamp=1622647199816&signature=3E56CEFD78654975FDB6ACE4EF91EFE682A1E1192D1D9270415BEE72025F2FD1&scope=userinfo')

# 找到登陆按钮点击登陆
time.sleep(1)

time.sleep(3)
# driver.find_element_by_xpath("//form[@class='login-form-container']/div[@class='login-form']/div[@class='form-field']/div[@class='form-field-control']/div[@class='mobile-field has-error']/div[@class='mobile-input custom-input']/input[@class='phone-number-input']").send_keys('18531775212')
driver.find_element_by_xpath("//*[@id='root']/div/form/div/div[1]/div/div/div/input").send_keys('18531775212')

time.sleep(1)
driver.find_element_by_xpath("//*[@id='root']/div/form/div/div[2]/div/div/div/input").send_keys('AIyaya12')
time.sleep(1)
driver.find_element_by_xpath("//*[@id='root']/div/form/div/div[3]/span").click()

time.sleep(3)
driver.find_element_by_xpath("//li[@id='loginLi']/a").click()
print("登陆完毕")
time.sleep(5)

a = driver.find_elements_by_xpath("//div[@class='index_divchildcourt_arrow']/a")[1].click()

time.sleep(4)

all_handles = driver.window_handles
print(all_handles, '所有句柄id')
driver.switch_to.window(all_handles[-1])
index_windows1 = driver.current_window_handle
print(index_windows1, '当前句柄id')
driver.find_element_by_xpath('//div[@class="search-middle"]/input').send_keys('交通事故')
time.sleep(3)
driver.find_element_by_xpath("//div[@class='search-rightBtn search-click']").click()


def page_turning():
    num_w = driver.find_element_by_xpath("//div[@class='fr con_right']").text
    num_w = int(re.findall(r"\d+\.?\d*", num_w)[-1])
    if num_w % 15 == 0:
        number_pages = num_w // 15
        number_pages = number_pages - 1
        # for i in range(number_pages):
        return number_pages
    else:
        number_pages = num_w // 15
        return number_pages


def download_weit():
    global url_writ_list
    all_handles = driver.window_handles
    driver.switch_to.window(all_handles[1])

    for writ in url_writ_list:

        writ.click()
        print("进入文书详情页")
        time.sleep(10)
        all_handles = driver.window_handles
        print(all_handles, '所有句柄id')
        driver.switch_to.window(all_handles[-1])
        index_windows1 = driver.current_window_handle
        print(index_windows1, '当前句柄id')
        writ_html = driver.page_source
        title = driver.find_element_by_xpath('//div[@class="PDF_title"]').text

        print('正在下载-----%s' % (title))
        try:
            with open('F:\work\wenshu\download_wenshu\%s.html' % (title), 'wb') as f:
                f.write(writ_html.encode('utf-8'))
        except Exception as e:
            print('错误', Exception)
            print('%s重复下载' % (title))

        driver.close()
        driver.switch_to.window(all_handles[1])
        if writ == url_writ_list[-1]:
            del url_writ_list


def func_amend():
    global url_writ_list

    if len(url_writ_list) != 0:
        download_weit()
        number_pages = page_turning()
        for i in range(number_pages):
            if 'url_writ_list' not in locals().keys():  # 判断文书列表变量是否存在
                driver.find_elements_by_xpath("//div[@class='left_7_3']/a")[-1].click()
                time.sleep(10)
                url_writ_list = driver.find_elements_by_xpath(
                    "//div[@class='LM_right item_table']//div[@class='LM_list']/div[@class='list_title clearfix']/h4/a")
                download_weit()


def time_random():
    '''
    随机睡5到9
    :return:
    '''
    t = random.randint(5, 10)
    time.sleep(t)


# 判断检索条件下文件数目
def file_number(number):
    number = int(re.findall(r"\d+\.?\d*", number)[0])
    return number


# 民事案由点击事件

def relating_civil():
    global url_writ_list
    current_text = driver.find_element_by_xpath(
        "//div[@class='LM_left item_table']//li[@id='9000']/a[contains(text(),'民事案由')]").text
    number = file_number(current_text)
    print('当前处理分类是%s' % (current_text))
    if number > 2000:
        driver.find_element_by_xpath(
            "//div[@class='LM_left item_table']//li[@id='9000']/i[@class='jstree-icon jstree-ocl']").click()
        time.sleep(2)
        print("打开了分类元素")
        li_list = driver.find_elements_by_xpath(
            "//div[@class='LM_left item_table']//li[@id='9000']/ul[@class='jstree-children']/li")
        print(len(li_list))
        a_list = ["/a[@id='9001_anchor']", "/a[@id='9012_anchor']", "/a[@id='9047_anchor']", "/a[@id='9130_anchor']",
                  "/a[@id='9299_anchor']", "/a[@id='9461_anchor']", "/a[@id='9542_anchor']", "/a[@id='9705_anchor']",
                  "/a[@id='9771_anchor']", "/a[@id='8000_anchor']"]
        close_options = "//div[@class='LT_Filter_right clearfix']/p[3]/i[@class='fa fa-close']"
        li_a_dic = {}
        for k, v in zip(li_list, a_list):
            li_a_dic[k] = v

        for k, v in li_a_dic.items():

            """
                range（10） 获取页面ui由返回值的list确定长度 将ui连接与对应的xp进行字典格式的存储
            """
            current_text = driver.find_element_by_xpath(
                "//div[@class='LM_left item_table']//li[@id='9000']/ul[@class='jstree-children']/li%s" % (v)).text
            number = file_number(current_text)
            print('当前处理分类是%s' % (current_text))
            if number > 2000:
                # driver.find_element_by_xpath(
                #     "//div[@class='LM_left item_table']//li[@id='9000']/ul[@class='jstree-children']/%s/i[@class='jstree-icon jstree-ocl']" % (
                #         v))
                # time.sleep(2)
                #
                # """
                # 后期处理上是否可以将每一组的a_url与文本text进行字典存储，形成一个全网页的分组的字典集合方便进行判断处理
                # """
                # group_a_list = ["//a[@id='9708_anchor']", "//a[@id='9710_anchor']", "//a[@id='9711_anchor']",
                #                 "//a[@id='9713_anchor']", "//a[@id='9716_anchor']", "//a[@id='9717_anchor']",
                #                 "//a[@id='9722_anchor']", "//a[@id='9723_anchor']", "//a[@id='9741_anchor']",
                #                 "//a[@id='9742_anchor']", "//a[@id='9750_anchor']", "//a[@id='9751_anchor']",
                #                 "//a[@id='9757_anchor']", "//a[@id='9766_anchor']"
                #                 ]
                #
                # for a in group_a_list:
                #     driver.find_element_by_xpath(a).click()
                #     time.sleep(3)
                #     """
                #     每次分类点击都有可能出现页面没有数据的情况
                #     """
                pass

            else:
                driver.find_element_by_xpath(
                    "//div[@class='LM_left item_table']//li[@id='9000']/ul[@class='jstree-children']/li%s" % (
                        v)).click()
                time.sleep(3)
                writ_counts = driver.find_element_by_xpath("//div[@class='fr con_right']/span").text
                each_page = driver.find_element_by_xpath("//select[@class='pageSizeSelect']/option[3]")
                print(each_page, '显示十五个')
                time.sleep(0.5)
                each_page.click()
                time.sleep(10)
                url_writ_list = driver.find_elements_by_xpath(
                    "//div[@class='LM_right item_table']//div[@class='LM_list']/div[@class='list_title clearfix']/h4/a")
                print(url_writ_list, "文书列表页urllist")
                while len(url_writ_list) == 0:
                    driver.refresh()
                    writ_counts = driver.find_element_by_xpath("//div[@class='fr con_right']/span").text
                    each_page = driver.find_element_by_xpath("//select[@class='pageSizeSelect']/option[3]")
                    print(each_page, '显示十五个')
                    time.sleep(0.5)
                    each_page.click()
                    time.sleep(10)
                    url_writ_list = driver.find_elements_by_xpath(
                        "//div[@class='LM_right item_table']//div[@class='LM_list']/div[@class='list_title clearfix']/h4/a")
                    print(url_writ_list, "文书列表页urllist")
                    time.sleep(3)

                if len(url_writ_list) != 0:
                    func_amend()
                    if 'url_writ_list' not in locals().keys():
                        driver.find_element_by_xpath(close_options)
                        time.sleep(5)

    else:
        pass
        """
        下载函数相关
        """


relating_civil()

"""
每下载一篇后都要改页面的文书显示数量



"""

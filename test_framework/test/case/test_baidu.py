import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils.config import Config ,DRIVER_PATH,DATA_PATH,REPORT_PATH
from utils.log import Logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner_PY3 import HTMLTestRunner
from utils.mail import Email
from test.page.baidu_result_page import BaiDuMainPage,BaiDuResultPage

class TestBaiDu(unittest.TestCase):
    #URL ='https://www.baidu.com'
    config = Config()
    URL = config.get("URL")
    excel = DATA_PATH +'/baidu.xlsx'
    #driver_path = os.path.dirname(os.getcwd()) + r'\driver\chromedriver.exe'
    logger = Logger().get_logger()

    #locator_kw = (By.ID,'kw')
    #locator_su = (By.ID,'su')
    #locator_result = (By.XPATH,'//div[contains(@class,"result")]/h3/a')
    def sub_setUp(self):    #测试固件,执行代码之前的准备
       # self.driver = webdriver.Chrome(executable_path=DRIVER_PATH+r'\chromedriver.exe')
       #self.driver.get(self.URL)
       """初始页面为mainpage"""
       self.page = BaiDuMainPage(browser_type='chrome').get(self.URL,maximize_window=False)
    def sub_tearDown(self): #测试固件，执行代码之后的清扫
        self.page.quit()
        """
        进行参数化
        """
    def test_search_one(self):
        datas = ExcelReader(self.excel).excel_data  #返回数据
        for d in datas:
            with self.subTest(data=d):
                self.sub_setUp()
                #self.page.find_element(*self.locator_kw).send_keys(d['search'])
                self.page.search(d['search'])
                #self.page.find_element(*self.locator_su).click()
                time.sleep(3)
                #结果页
                self.page.save_screen_shot()
                self.page=BaiDuResultPage(self.page)
                links = self.page.result_links
                for link in links:
                    self.logger.info(link.text)
                self.sub_tearDown()
    # def test_search_two(self):
    #     self.driver.find_element(*self.locator_kw).send_keys("python")
    #     self.driver.find_element(*self.locator_su).click()
    #     time.sleep(3)
    #     links = self.driver.find_elements(*self.locator_result)
    #     for link in links:
    #         self.logger.info(link.text)
    #         #print(link.text)

# if __name__=='__main__':
#     report = REPORT_PATH+r'\report.html'
#     print(report)
#     with open(report,'wb') as f:
#         runner = HTMLTestRunner(stream=f,verbosity=2 ,title='xxx测试',description='测试详情')
#         runner.run(TestBaiDu('test_search_one'))
#     e = Email(server='smtp.qq.com',
#               sender='1404482005@qq.com',
#               receiver="'1404482005@qq.com';'1901854026@qq.com'",
#               message='百度搜索测试报告',
#               title='测试报告结果',
#               password='pfoozuyovftobaca',
#               path=report)
#     e.send()
    #unittest.main(verbosity=2)
    """
这里的verbosity是一个选项,表示测试结果的信息复杂度，有三个值
0 (静默模式 ): 你只能获得总的测试用例数和总的结果 比如 总共100个 失败20 成功80
1 (默认模式): 非常类似静默模式 只是在每个成功的用例前面有个“.”  每个失败的用例前面有个 “F”
2 (详细模式):测试结果会显示每个测试用例的所有相关的信息
    """
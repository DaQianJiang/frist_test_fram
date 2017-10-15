import os
from utils.HTMLTestRunner_PY3 import HTMLTestRunner
from utils.mail import Email
from utils.config import REPORT_PATH
import unittest

report = REPORT_PATH+'report.html'
fp = open(report,'wb')
case_path = os.path.dirname(os.path.abspath('.'))+'\case'
print(case_path)
suite = unittest.TestLoader().discover(case_path)

if __name__=='__main__':
    runner = HTMLTestRunner(stream=fp,verbosity=2,title='xxx测试报告',description='百度搜索测试报告')
    runner.run(suite)
    e = Email(server='smtp.qq.com',
              sender='1404482005@qq.com',
              receiver='1404482005@qq.com', #;'1901854026@qq.com'
              message='百度搜索测试报告',
              title='测试报告结果',
              password='pfoozuyovftobaca',
              path=report)
    e.send()

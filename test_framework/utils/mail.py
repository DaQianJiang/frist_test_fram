import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror,error
from utils.log import Logger
import re

logger = Logger().get_logger()
class Email(object):
    def __init__(self,server,sender,password,receiver,title,message=None,path = None):
        """初始化Email

        :param server: smtp 服务器，必填
        :param sender: 邮件发件人，必填
        :param password: 发件人密码，必填
        :param receiver: 收件人，多收件人用“；”隔开，必填
        :param title: 邮件标题，必填
        :param message: 邮件正文，非必填
        :param path: 附件路径，可传入list（多附件）或str（单附件），非必填
        """
        self.title = title
        self.message = message
        self.path = path

        self.sender = sender
        self.receive = receiver
        self.server = server
        self.passward = password

        self.msg = MIMEMultipart('related')#创建MIMEMultipart对象，因为不止text还会有其他内容
    def _attach_file(self,att_file):
        """ 将单个文件添加到附件列表中"""
        att = MIMEText(open('%s'%att_file,'rb').read(),'plain','utf-8')
        att['Content-Type']= 'application/octet-stream'
        file_name = re.split(r'[\\|/]',att_file)
        att["Content-Disposition"]='attachment;filename="%s"'%file_name[-1]
        self.msg.attach(att)
        logger.info('attach file{}'.format(att_file))
    def send(self):
        self.msg['From']=self.sender
        self.msg['To']=self.receive
        self.msg['Subject']=self.title

        if self.message:
            self.msg.attach(MIMEText(self.message))
        if self.path:
            if isinstance(self.path,list):
                for f in self.path:
                    self._attach_file(f)
            elif isinstance(self.path,str):
                self._attach_file(self.path)

        #链接服务器发送
        try:
            stmp_server = smtplib.SMTP_SSL(self.server,465)
        except (gaierror and error)as e:
            logger.info('发送邮件失败，请检查SMTP服务器%s',e)
        else:
            try:
                stmp_server.login(self.sender,self.passward)
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败%s',e)
            else:
                stmp_server.sendmail(self.sender,self.receive.split(';'),self.msg.as_string())
            finally:
                stmp_server.quit()
                logger.info('发送邮件"{0}"成功！收件人"{1}".如果没有收到邮件请检查垃圾箱，'
                            '同时检查地址是否正确'.format(self.title,self.receive))
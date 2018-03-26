#coding=utf8
import requests,json,sys,config,time
from requests.auth import HTTPBasicAuth
from baseTestCase import ParametrizedTestCase
import filescom


# 执行测试的类
class TestAuthed(ParametrizedTestCase):
    def setUp(self):
        self.logger.info("setUp begin")
        '''
        你需要在每个case运行开始初始化的东西（case结束时会清除）：例如数据库，累加值，case公用参数等
        '''
        self.logger.info("setUp end")
    
    def testStatus(self):
        self.logger.info("%s.%s"%(self.__class__.__name__,sys._getframe().f_code.co_name))
        self.logger.info("测试:xxxxxxxxxxxx")
        '''
        case的具体脚本，随便写，爱怎么写怎么写，需要分装方法可以自己写。pyimport或者直接接下方  def XXX（self），
        '''
        time.sleep(5)
        
    def testCode(self):
        self.logger.info("测试:xxxxxxxxxxxxxx")
        '''
        case的具体脚本，随便写，爱怎么写怎么写，需要分装方法可以自己写。pyimport或者直接接下方  def XXX（self），
        '''

       
    def tearDown(self):
        self.logger.info("tearDown begin")
        '''每个case运行结束后想清清除的操作，比如断开数据库链接，公共参数重新分值等等'''
        self.logger.info("tearDown end")
#coding=utf8
import requests,json,sys,xlrd,config,os,re,traceback
from requests.auth import HTTPBasicAuth
from baseTestCase import ParametrizedTestCase
from lib import prama_helper
from lib.prama_helper import pramas_sava
from data import com_pramas
reload(sys)
sys.setdefaultencoding( "utf-8" )
host=config.host

# 执行测试的类
class TestSimple(ParametrizedTestCase):
    def setUp(self):
        self.logger.info("setUp begin")
        self.logger.info("setUp end")
    
    @staticmethod
    def gettestfun(case_num,case_url,case_method,case_prama,case_ex,case_dis,case_rely,case_berely):
        def func(self):
            self.logger.info("%s.test_func_%s"%(self.__class__.__name__,case_num))
            self.logger.info("测试:%s"%str(case_dis))
            if case_rely:
                print case_rely 
                pro_re = re.compile("%\((.*?)\)")
                for i in case_prama.keys():
                    con = pro_re.search(case_prama[i])
                    if con:
                        print con.group(1)
                        print con.group()
                        values=getattr(com_pramas, con.group(1))
                        case_prama[i]=case_prama[i].replace(con.group(),values)
                for i in case_ex.keys():
                    con = pro_re.search(case_ex[i])
                    if con:
                        print con.group(1)
                        print con.group()
                        values=getattr(com_pramas, con.group(1))
                        case_ex[i]=case_ex[i].replace(con.group(),values)
                    
            httprequest=getattr(requests, case_method)
            self.logger.info("请求地址为：%s"%case_url)
            self.logger.info("请求内容为：%s"%case_prama)
            respon=httprequest(case_url,case_prama).content.decode("unicode_escape").encode("UTF-8")
            r_response=json.loads(respon)
            self.logger.info("返回结果为：%s"%respon)
            for i in case_ex.keys():
                key='r_response["'+i.replace(".",'"]["')+'"]'
                expression=case_ex[i].replace(i,key)
                try:
                    truevalue=eval(key)
                except:
                    raise AssertionError("判定字段%s 错误，接口返回不存在该字段或字段名称错误，读取不到该字段！"%truevalue)   
                self.logger.info("断言：%s"%expression)
                try:
                    assert eval(expression)
                except:  
                    raise AssertionError("该断言表达式：%s 结果为flase,实际response的校验参数：%s 的值为 %s"%(expression,key,truevalue))
            if case_berely:
                print case_berely 
                for i in case_berely.keys(): 
                    value=eval(case_berely[i].split(".",1)[0]+'["'+case_berely[i].split(".",1)[1].replace(".",'"]["')+'"]')
#                     exec("self."+i+"=value") in TestSimple
                    pramas_sava(i,value)
        return func
       
    def tearDown(self):
        self.logger.info("tearDown begin")
        self.logger.info("tearDown end")
        
def __generateTestCases():
    '''打开excel'''
    excel_path=os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0],os.path.pardir,"data","api_data.xlsx"))
    datas=xlrd.open_workbook(excel_path)
    table=datas.sheet_by_index(0)
    nrow=table.nrows
    '''读取case信息集合成列表'''
    case_lists=[]
    for i in range(nrow-1):
        case_num=int(table.cell(i+1,0).value)
        case_url=table.cell(i+1,1).value.split(",")[config.test_or_line]
        m=re.findall("i.service.live.weibo.com",case_url)
        if len(m)>0:
            case_url=case_url.replace(m[0],host)
        case_method=table.cell(i+1,2).value
        case_prama=json.loads(table.cell(i+1,3).value)
        case_ex=json.loads(table.cell(i+1,4).value)
        case_switch=int(table.cell(i+1,5).value)
        case_dis=table.cell(i+1,6).value
        case_rely=json.loads(table.cell(i+1,8).value)
        case_berely=json.loads(table.cell(i+1,9).value)
        if case_switch==1:
            case_lists.append([case_num,case_url,case_method,case_prama,case_ex,case_dis,case_rely,case_berely])
    print case_lists
        
    for args in case_lists:
        setattr(TestSimple, 'test_func_%s'%args[0],TestSimple.gettestfun(*args))
__generateTestCases()
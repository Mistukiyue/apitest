#coding=utf-8
import os,sys,re,time
import unittest
import config
import filescom
import baseTestCase
import logger
import mail_send
from sys import argv
from multiprocessing import Process,Pool


cur_file_dir = os.path.split(os.path.realpath(__file__))[0]
if not cur_file_dir+'/testcases' in sys.path:
    sys.path.append(os.path.split(os.path.realpath(__file__))[0]+'/testcases')
    if os.path.isdir(config.cases_dir):
        floder,files_name,files_path=filescom.walk_files(config.cases_dir)
        for dir_path in floder:
            sys.path.append(dir_path)

case_list=config.cases_dir 
run_project=config.run_project
run_case=config.run_case


def suite(cases_list):
    modules = []
    case_list_tmp = []
    newpro=''
    if len(run_project):
        if len(run_case):
            newpro='[\\\\|/]('+'|'.join(run_project)+')'+'[\\\\|/]'+'('+'|'.join(run_case)+')'+'.py$'
        else:
            newpro='[\\\\|/]('+'|'.join(run_project)+')'+'[\\\\|/]test(\w+)\.py$'
    else:
        if len(run_case):
            newpro='[\\\\|/]('+'|'.join(run_case)+')'+'.py$'
        else:
            newpro='[\\\\|/]test(\w+)\.py$'
    print "newpro---------------:",newpro       
    test_search = re.compile(newpro, re.IGNORECASE)
    print "cases_list------------------------:",cases_list
    for tmp in cases_list:
        if os.path.isdir(tmp):
            floder,files_name,files_path=filescom.walk_files(case_list)
            case_list_tmp=case_list_tmp+filter(test_search.search, files_path)
        else:
            if tmp[-3:] == ".py" :
                case_list_tmp.append(tmp)
    
    print case_list_tmp
    files = filter(test_search.search, case_list_tmp)
    filenametomodulename = lambda f:os.path.splitext(os.path.basename(f))[0]
    print "filenametomodulenam--------------:",filenametomodulename, files
    modulenames = map(filenametomodulename, files) 
    print "modulenames--------------:",modulenames 
    #导入测试模块  
    modules = map(__import__,modulenames)
    print "modules--------------:",modules 
    testcase_list = []
    module_class_list = []
    for module in modules:
        for attr_name in dir(module):
            #便利模块下所有的类
            attr = getattr(module, attr_name)
            try:
                if issubclass(attr, unittest.TestCase) and attr.__name__.startswith("Test"):
                    #判断类为unittest的子类，并且已Test开头
                    testcase_list.append(attr_name)
                    module_class_list.append(attr)
            except Exception:
                continue     
    print "testcase_list--------------",testcase_list
    print "module_class_list--------------",module_class_list
    return module_class_list
    
def one_thread(cases_list):
    module_class_list=suite(cases_list)
    send_mail=mail_send.Reporter()
    log_path=[logger.log_path()]
    log_test = logger.StreamToLogger(log_path[0])
    runner = unittest.TextTestRunner(stream=log_test)
#     runner=HTMLTestRunner.HTMLTestRunner(stream=log_test,title=u'my unit test',description=u'This is a report test')
    allTests = unittest.TestSuite()
    for attr in module_class_list:
        allTests.addTest(baseTestCase.ParametrizedTestCase.parametrize(attr,logger=log_test))                  
    runner.run(allTests)
    send_mail.send(log_path)


log_path_list=[]
def run_proc(attr,log_path):        ##定义一个函数用于进程调
    log_test = logger.StreamToLogger(log_path)
    runner = unittest.TextTestRunner(stream=log_test)
    allTests = unittest.TestSuite()
    allTests.addTest(baseTestCase.ParametrizedTestCase.parametrize(attr,logger=log_test))                  
    runner.run(allTests)
        
def dul_thread(cases_list):
    send_mail=mail_send.Reporter()
    module_class_list=suite(cases_list)
    send_mail=mail_send.Reporter()
    if len(module_class_list)>0:
        print 'Run the main process (%s).' % (os.getpid())
        mainStart = time.time()
        p = Pool(8)
        for attr in module_class_list:
            classname=attr.__name__
            print classname
            log_path=logger.log_path(classname)
            log_path_list.append(log_path)
            p.apply_async(run_proc,args=(attr,log_path,))
        print 'Waiting for all subprocesses done ...'
        p.close() #关闭进程池
        p.join()  #等待开辟的所有进程执行完后，主进程才继续往下执行
        print 'All subprocesses done'
        mainEnd = time.time()  #记录主进程结束时间
        print log_path_list
        send_mail.send(log_path_list)

if __name__ == "__main__":
    #分线程运行
    if config.thread_m==0:
        one_thread(config.case_list)
    elif config.thread_m==1:
        dul_thread(config.case_list) 
    filescom.output_delete(20)
    
    
    
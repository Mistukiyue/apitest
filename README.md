# apitest
基于unittest的接口测试demo（分级+log+html+重试+按class多进程运行）
==

运行config配置：
--
apitest/config.py

分级运行配置如下：
--
    cur_file_dir = os.path.split(os.path.realpath(__file__))[0]
    cases_dir=cur_file_dir
    case_list=[os.path.abspath(os.path.join(cur_file_dir,"testcases/"))]
    host="i.xxxxxxx.live.xxxxx.com"     #我们的项目测试环境接口有不同的域名，做了域名配置，生效需要接口地址管理文件上使用这个配置（我这边有一个单独的。py文件管理各种业务接口数据）如果不需要你也可以不用
    test_or_line=0                      #同上接口case中我们都配置两个环境的url，通过0，1切换线上线下环境，如果不需要你也可以不用
    thread_m=1 #0为单线程，1为多线程

    run_project=[]    #执行运行一个文件夹下所有case（文件夹需要在testcase文件下）例如：run_project=[“文件夹名”] 运行文件夹下所有case
    run_case=[]       #指定运行一个具体的case
run： run_case.py
--
运行入口，如名

output：
--
业务型的接口在case编写中有前后耦合性，需要一定的顺序，但是为了提速我们需要多线程运行这些耦合的case，所以要有些前后运行，有些并行运行。

#我选择按照类的单位级别多线程运行：
1.不同类同时运行
2.同类下的case按照顺序串行运行
3.日志按照类来存储，避免多进程日志输出乱序
4.汇总到html报告输出
![image_text](https://github.com/Mistukiyue/apitest/blob/master/img/1.png)
#html：
运行完会生成一个output文件，按照执行日期存储每次的运行结果：
网页展示如下，支持按钮筛选“全部”“正确”“失败”：
![image_text](https://github.com/Mistukiyue/apitest/blob/master/img/2.png)
![image_text](https://github.com/Mistukiyue/apitest/blob/master/img/3.png)
#log：
log连接指向每个测试类的完整log（多线程日志乱序做了处理，不会混乱）
![image_text](https://github.com/Mistukiyue/apitest/blob/master/img/4.png)

重试：
--
使用filescom.py的装饰器 @dubl_num(num) num指定重试次数

非业务行接口（仅字段判断型）
--
针对非业务性接口，单独编写脚本case很浪费时间，便使用excel进行管理（可以选择db等其他存储工具皆可），python脚本自动生成脚本代码；
#api_data.xlsx
--
如图，支持1.参数传递，
        2.测试跳过
        3.python语法断言
        
![image_text](https://github.com/Mistukiyue/apitest/blob/master/img/5.png)

#testsimpleapi.py
--

api_data.xlsx数据读取 xlrd库

自动生成脚本代码（和脚本case一致的日志输出等级，方便debug）：

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
                
 对应日志参考（更多可见ouput样例）
 ![image_text](https://github.com/Mistukiyue/apitest/blob/master/img/7.png)






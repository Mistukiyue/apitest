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

    run_project=[]    #执行运行一个文件夹下所有case（文件夹需要在testcase文件下）
    run_case=[]       #制定运行一个具体的case
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
![image_text](https://github.com/Mistukiyue/apitest/blob/master/img/5.png)

#testsimpleapi.py
--
自动生成脚本代码：





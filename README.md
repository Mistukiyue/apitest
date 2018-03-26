# apitest
基于unittest的接口测试demo（分级+log+html+重试+按class多进程运行）
==

运行config配置：
--
apitest/config.py

分级运行配置如下：
--
run_project=[]            #执行运行一个文件夹下所有case（文件夹需要在testcase文件下）
run_case=["testexample"]  #制定运行一个具体的case
thread_m=1                #0为单线程，1为多线程

run： run_case.py
--

output：
--
运行完会生成一个output文件，按照执行日期存储每次的运行结果：
网页展示如下，支持按钮筛选“全部”“正确”“失败”：

log连接指向每个测试类的完整log（多线程日志乱序做了处理，不会混乱）





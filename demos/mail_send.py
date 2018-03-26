#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib,os,re
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart


# 第三方 SMTP 服务
mail_host=""  #设置服务器
mail_user=""    #用户名(有的邮箱用户名是邮箱地址，有些不是)
mail_pass=""   #口令（密码）
send_mail="" #邮箱地址

receivers = ['954667698@qq.com'] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱;,'954667698@qq.com'

class Reporter :
    def __init__(self):
        self.mail_host = mail_host
        self.mail_user = mail_user
        self.mail_user = mail_pass
        self.run_log=None
        self.failnum=0
        self.all_time=[0,0]
        self.case_name=[]
        self.def_name=[]
       
        '''获取本次运行的log路径地址'''
    def log_file(self,run_log):
        print "------------------run_log split",run_log.split('/')
        filename=run_log.split('/')[-1]
        files=run_log
        print files,filename
        return files,filename
    
    '''获取所有的描述信息'''
    def case_dis(self,line):
        dis_re = re.compile(":测试.*")
        dis = dis_re.search(line)
        if dis:
            return dis.group()
        else:
            return "no dis"
        
    '''获取case失败与否'''
    def fail_succ(self,line):
        check_re=re.compile("\[INFO\]:(F|E)\n")
        check=check_re.search(line)
        if check:
            return "fail"
        else:
            return "success"
        
    '''表一—------单个case处理——名称and状态and描述信息'''
    def case_list(self,line,runlog):
        cases_re = re.compile("test.*?\]\[INFO\]:Test.*")
        cases = cases_re.search(line)
        dis = self.case_dis(line)
        succ = self.fail_succ(line)
        if succ=="fail":
            self.failnum=self.failnum+1
        self.fail_succ(line)
#         for case in self.case_name:
#             print "-----------------",case
        if cases:
#             casesname = cases.group().split("][")[-2].split(".")[-2]
            casesname = runlog.split(os.path.sep)[-2]
            defname=cases.group().split("][")[-1].split(":")[-1]
            ex,i=self.check_exit(casesname, self.case_name)
#             print casesname,ex,i
            if ex:
                self.case_name.append([succ,dis,defname,"/".join(runlog.split(os.path.sep)[-2:])])
                self.case_name[i][5]=self.case_name[i][5]+1
            else:
                self.case_name.append([succ,dis,defname,"/".join(runlog.split(os.path.sep)[-2:]),casesname,1])

            
#         print len(self.case_name)
        
    '''判断字符串是否存在一个二级列表中''' 
    def check_exit(self,strs,lists):
        num=[]
        if len(lists)==0:
            return False,None
        for i in range(len(lists)):
            if strs in lists[i]:
                num.append(i)
        if len(num)>=1:
            return True,num[0]
        else:
            return False,None
                  
    '''获取所有的报错信息'''
    def error_msg(self,run_log):
        def_name=[]
        with open(run_log,'r') as files:
            fileline=files.read()
        '''获取本次log耗时'''
        re_text=re.compile("((tests|test) in (\d|.)*s)")
        re_case=re_text.findall(fileline)
#         print re_case
        times=float(re_case[0][0].split(" ")[-1][:-1])
        '''如果log运行时间大于上次log运行时间则更新运行时间'''
        if times>self.all_time[0]*60+self.all_time[1]:
            if times/60<=0:
                self.all_time=[0,times]
            elif times/60>0:
                self.all_time=[int(times)/60,times-int(times)/60*60]
        '''表一list   获取单个case的日志信息'''
        re_text=re.compile("([(\d|\W){29,40}].*?\[INFO\]:setUp begin(.|\n)*?\[INFO\]:tearDown begin)")
        re_case=re_text.findall(fileline)
        for re_text in re_case:
            self.case_list(re_text[0],run_log)
#         for i in self.case_name:
#             print i
            
        '''表二list'''
        error_re=re.compile("(:(ERROR|FAIL): test(.|\n)*?\[INFO\]:--(.|\n)*?\[INFO\]:Traceback(.|\n)*?\[INFO\]:\n)")
        error_def=error_re.findall(fileline)
        print "len(error_def)",len(error_def)

        for error in error_def:
            res=re.compile("((ERROR|FAIL): test.*?\))")
            res_text=res.findall(error[0])[0][0]
#             print "------error[0]",error
#             print "------re_text",res_text
            classname,defname=res_text.split(" ")[2][1:-2].split(".")[0],res_text.split(" ")[1]
#             print "------classname,defname", classname,defname
            error_re=re.compile("([(\d|\W){29,40}].*?\[INFO\]:Traceback(.|\n)*?\[(2017|2018))")
#             print error_re.findall(error[0])
            error_msg=error_re.findall(error[0])[0][0]
#             print "------errormsg",error_msg
            def_name.append([classname,defname,error_msg[:-5].replace("\n","<br>")])
        for err in def_name:
            status,i=self.check_exit(err[1], self.def_name)
#             print "status,i",status,i
            if status !=True:
                self.def_name.append(err)
            if status == True:
#                 print "----------第几位重复",i
                self.def_name[i][2]=self.def_name[i][2]+err[2]
#         for i in self.def_name:
#             print i
        
    def get_header(self):
        header = '''
                <!DOCTYPE html>
                <html>
                <head>
                <meta charset="utf-8" />
                <style type="text/css">
                table
                  {
                    border-collapse:collapse;
                    width:90%;
                    text-align:center;
                    }
                table,td,th
                  {
                    border:1px solid black;
                  }
                th
                  {
                    height:40px;
                    background-color:#2F4F4F;
                    color:white;
                  }
                .hiddenRow  { display: none; }
                
                </style>
                </head>
                <body >
                <script type="text/javascript"> 
                                
                                function getElementByAttr(tag,attr,value)
                                {
                                    var aElements=document.getElementsByTagName(tag);
                                    var aEle=[];
                                    for(var i=0;i<aElements.length;i++)
                                    {
                                        if(aElements[i].getAttribute(attr)==value)
                                            aEle.push( aElements[i] );
                                    }
                                    return aEle;
                                }
                                window.onload=function()
                                {
                                    var atd=getElementByAttr('td','status','bn');
                                    for(var i=0;i<atd.length;i++){
                                        rowObj = atd[i];                        
                                        var s = rowObj.innerHTML;            
                                        if(s=="fail"){
                                        rowObj.style.backgroundColor="#FF4500";
                                        }else if(s=="success"){rowObj.style.backgroundColor="#00FA9A";}
                                　　}
                                }
                                
                                function show(number){ 
                                    var table = document.getElementById("discript");
                                    //console.log(table);
                                    var tr = document.getElementsByClassName("btr");
                                    //console.log(tr);
                                    for (var i = 0; i < tr.length; i ++){ 
                                        //console.log(tr[i]);
                                        var tds=tr[i]
                                        var tds=tds.getElementsByTagName("td")
                                        var s = tds[tds.length-3].innerHTML;
                                        if(number==1 ){
                                            for (var x = 0; x < 4; x ++){
                                                tds[tds.length-x-1].className= "";}
                                            table.className= "";
                                            }
                                        if(number==2 ){
                                            if(s=="success"){
                                            for (var x = 0; x < 4; x ++){
                                                tds[tds.length-x-1].className= "";}
                                            }else if(s=="fail"){
                                            for (var x = 0; x < 4; x ++){
                                                tds[tds.length-x-1].className= "hiddenRow";}
                                            }
                                            table.className= "hiddenRow";
                                            }
                                            
                                        if(number==3 ){
                                            if(s=="success"){
                                            for (var x = 0; x < 4; x ++){
                                                tds[tds.length-x-1].className= "hiddenRow";}
                                            }else if(s=="fail"){
                                            for (var x = 0; x < 4; x ++){
                                                tds[tds.length-x-1].className= "";}
                                            }
                                            table.className= "";
                                            }
                                    
                                        } 
                                    }
                                function drawCircle(pass, fail){ 
                                    var color = ["#00FA9A","#FF4500"];  
                                    var data = [pass,fail]; 
                                    var text_arr = ["通过", "失败"];
                                
                                    var canvas = document.getElementById("circle");  
                                    var ctx = canvas.getContext("2d");  
                                    var startPoint=0;
                                    var width = 20, height = 10;
                                    var posX = 112 * 2 + 20, posY = 30;
                                    var textX = posX + width + 5, textY = posY + 10;
                                    for(var i=0;i<data.length;i++){  
                                        ctx.fillStyle = color[i];  
                                        ctx.beginPath();  
                                        ctx.moveTo(150,100);   
                                        ctx.arc(150,100,84,startPoint,startPoint+Math.PI*2*(data[i]/(data[0]+data[1])),false);  
                                        ctx.fill();  
                                        startPoint += Math.PI*2*(data[i]/(data[0]+data[1]));  
                                        ctx.fillStyle = color[i];  
                                        ctx.fillRect(posX, posY + 20 * i, width, height);  
                                        ctx.moveTo(posX, posY + 20 * i);  
                                        ctx.font = 'bold 14px';
                                        ctx.fillStyle = color[i];
                                        var percent = text_arr[i] + ":"+data[i];  
                                        ctx.fillText(percent, textX, textY + 20 * i);  
                                }
                            }
                </script>
                <div style ="float:left" class=heading >
                <h2>AutoTestapi 测试报告：耗时'''+str(self.all_time[0])+'''分'''+str(self.all_time[1])+'''秒</h2>
                <p>本次执行用例数：'''+str(len(self.case_name))+'''</p>
                <p style="color:red;">错误数量数：'''+str(self.failnum)+'''</p>
                <button onclick="show(1)">全部</button>
                <button onclick="show(2)">成功</button>
                <button onclick="show(3)">失败</button>
                </div>
                <div style ="float:left" class=piechart >
                <canvas id="circle" width="400" height="250" <canvas>
                </div>
                </canvas>
                <script>
                drawCircle('''+str(len(self.case_name)-self.failnum)+''', '''+str(self.failnum)+''')
                </script>
                <table id=t1>
                <tr>
                <th>用例名</th>
                <th>case名</th>
                <th>执行结果</th>
                <th>用例描述</th>
                <th>log链接</th>
                </tr>
                    '''
        td2=''
        if len(self.def_name)>=1:
            td2+='''
                    </table ><P>具体失败信息：</p>
                    <table id=discript>
                    <tr>
                    <th>用例名称</th>
                    <th>出错方法</th>
                    <th>错误信息</th>
                    </tr>'''
        td2start=td2
        td2end="</table></body></html>"
        return header,td2start,td2end
                    
    def get_table(self):
        td1=''
        for tr in self.case_name:
            if len(tr)==4:
                td1 +='''<tr class=btr>
                        <td >'''+tr[2]+'''</td>
                        <td status=bn>'''+tr[0]+'''</td>
                        <td >'''+tr[1]+'''</td>
                        <td ><a href="'''+tr[3]+'''">log</a></td>
                        </tr>'''
            elif len(tr)==6:
                td1 +='''<tr class=btr>
                        <td rowspan="'''+str(tr[5])+'''">'''+tr[4]+'''</td>
                        <td >'''+tr[2]+'''</td>
                        <td status=bn>'''+tr[0]+'''</td>
                        <td >'''+tr[1]+'''</td>
                        <td ><a href="'''+tr[3]+'''">log</a></td>
                        </tr>'''
        td2=''
        for tr in self.def_name:
            if len(tr)==3:
#                 print tr
                td2+='''
                            <tr >
                            <td>'''+tr[0]+'''</td>
                            <td>'''+tr[1]+'''</td>
                            <td>'''+tr[2]+'''</td>
                            </tr>
                    '''
        return td1,td2
    
    def get_html(self,runlog):
        path,filename=os.path.split(runlog)
        path=os.path.abspath(os.path.join(path,os.path.pardir))
        filename=filename.split('.')[0]
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)
        report_path=os.path.join(path,filename+".html")
        f=file(report_path,"w+")
        heater,tb2start,tb2end=self.get_header()
        tb1,tb2=self.get_table()
        msg=heater+tb1+tb2start+tb2+tb2end
        f.writelines(msg)
        f.close()
        print path,filename
        return msg,report_path
        
    def send(self,run_log_list):
        for run_log in run_log_list:
            print run_log
            self.error_msg(run_log)
            print "___________________________________________________________"
            print self.case_name
        msg,report_path=self.get_html(run_log)
        return msg,report_path
    
    def send_mail(self,run_log,text=None,report_path=None):
        #创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] =send_mail
        message['To'] = receivers[0]
        subject = 'AutoTestapi用例执行报错信息'
        message['Subject'] = Header(subject, 'utf-8')
        
        #构造附件，传送runtestcase的log文件
        files,filename=self.log_file(run_log)
        att1 = MIMEText(open(files, 'rb').read(), 'base64', 'utf-8')
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Type"] = 'application/octet-stream'
        print filename
        att1["Content-Disposition"] = 'attachment; filename=%s'%filename
        message.attach(att1) 
        if report_path!=None:
            #构造附件2 html报告
            files,filename=self.log_file(report_path)
            att2 = MIMEText(open(files, 'rb').read(), 'base64', 'utf-8')
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att2["Content-Type"] = 'application/octet-stream'
            print filename
            att2["Content-Disposition"] = 'attachment; filename=%s'%filename
            message.attach(att2) 
        #邮件正文内容
        msg = text
        message.attach(MIMEText(msg, 'html', 'utf-8'))
        


        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(host=mail_host,port=25)
            #ssl认证的邮箱类型使用 
    #         smtpObj = smtplib.SMTP_SSL(host=mail_host,port=465) 
            #登录用户名
            smtpObj.login(str(mail_user),mail_pass)  
            #发件邮箱
            smtpObj.sendmail(send_mail, receivers, message.as_string())
            print "邮件发送成功"
        except smtplib.SMTPException:
            print smtplib.SMTPException
            print "Error: 无法发送邮件"
   

if __name__ == '__main__':
    send=Reporter()
    log_list=[]
    run_log_list=log_list
    msg,report_path=send.send(run_log_list)
#     send.send_mail(run_log_list[0], msg, report_path)
    
 
    
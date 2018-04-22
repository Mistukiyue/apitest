#coding=utf-8  
import os,hashlib,traceback,time,re,platform
import shutil

def walk_files(path):
    floder=[]
    files_name=[]
    files_path=[]
    for dirpath, dirs, files in os.walk(path): 
        floder.append(dirpath)
        for fil in files:
            files_name.append(fil)
            files_path.append(os.path.join(dirpath,fil))
    return floder,files_name,files_path


def dubl_num(num):
    def dubl(func):
        def wrapper(self,num=num):
            for i in range(1,num+1):
                print "当前 i 的值为  %s ————————————————————————————————————"%i
                try:
                    func(self)
                    print "重试case运行成功啦"
                    print "重试case结束啦"
                    break
                except Exception,e:
                    if i!=num:
                        print "重试case第  %s  次运行失败了————————————————————————————————————失败情况如下"%i
                        print 'str(Exception):\t', str(Exception)
                        print 'traceback.format_exc():\n%s' % traceback.format_exc()
                    else:
                        raise Exception(traceback.format_exc()) 

        return wrapper
    return dubl

            
def output_delete(num):
    cur_file_dir = os.path.split(os.path.realpath(__file__))[0]
    log_path=os.path.abspath(os.path.join(cur_file_dir,"output"))
    print log_path
    for dirpath, dirs, files in os.walk(log_path):
        floder=dirs
        break
    print floder
    
    report_file=walk_files(log_path)[0]
    report_file=[[i,os.stat(i).st_ctime] for i in report_file if i.split(os.path.sep)[-1][:4]==time.strftime("%Y-%m-%d%X", time.localtime())[:4]]
    report_file=sorted(report_file, key=lambda student: student[1])
    floder_path=[i[0] for i in report_file]
    print floder_path
    print len(floder_path)
    if len(floder_path)>num:
        print "ouput日志过多%s  删除中。。。。。"%len(floder_path)
        for i in range(len(floder_path)-10):
            shutil.rmtree(floder_path[i])


    
if __name__ =="__main__": 
    pass
    

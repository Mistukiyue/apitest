#coding=utf-8  
import logging,os,time

runtime=(time.strftime("%Y-%m-%d%X", time.localtime())).replace(":","")
print runtime

def log_path(floder="onetheard"):
    logDir=os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0],os.path.pardir,"output",runtime,floder))
    if os.path.exists(logDir):
        pass
    else:
        os.makedirs(logDir)
    print logDir
    log_path=os.path.join(logDir,runtime+".log")
    print log_path
    return log_path



class StreamToLogger:
    def __init__(self, path,clevel = logging.DEBUG,Flevel = logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter("[%(asctime)s][%(process)d][%(filename)s:%(lineno)d][%(levelname)s]:%(message)s")  
        #设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        #设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)
        
    def write(self,msg):
        self.logger.info(msg)
         
    def flush(self):
        return

    
if __name__ =="__main__":  
    logger=StreamToLogger()
    logger.logger.debug('一个debug信息')
    logger.logger.info('一个info信息')
    logger.logger.warn('一个warning信息')
    logger.logger.error('一个error信息')
    logger.logger.critical('一个致命critical信息')
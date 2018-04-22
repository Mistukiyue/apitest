import os,sys,re
from data import com_pramas
pramas_path=os.path.abspath(os.path.join( os.path.split(os.path.realpath(__file__))[0],os.path.pardir,"data","com_pramas.py"))
print pramas_path 

def pramas_sava(name,value):
    f=open(pramas_path,'r')
    text=f.readlines()
    if name not in dir(com_pramas):
        text.append(name+'="'+value+'"\n')
    else:
        for i in range(len(text)):
            pro_re = re.compile(name+'="(.*)"')
            con = pro_re.search(text[i])
            if con:
                text[i]=text[i].replace(con.group(1),value)
    f=open(pramas_path,'w+')
    f.writelines(text)
    f.close()
    
def pramas_delete(name):
    f=open(pramas_path,'r')
    text=f.read()
    con = re.compile(name+'="(.*)"\n').search(text)
    print con.group()
    print text
    text=text.replace(con.group(),"")
    print text
    f=open(pramas_path,'w+')
    f.writelines(text)
    f.close()
    
def pramas_saves(lists):
    f=open(pramas_path,'r')
    text=f.readlines()
    for i in lists:
        name=i[0]
        value=i[1]
        if name not in dir(com_pramas):
            text.append(name+'="'+value+'"\n')
        else:
            for i in range(len(text)):
                pro_re = re.compile(name+'="(.*)"')
                con = pro_re.search(text[i])
                if con:
                    text[i]=text[i].replace(con.group(1),value)
    f=open(pramas_path,'w+')
    f.writelines(text)
    f.close()

def pramas_deletes(names):
    f=open(pramas_path,'r')
    text=f.read()
    for name in names:
        con = re.compile(name+'="(.*)"\n').search(text)
        print con.group()
        print text
        text=text.replace(con.group(),"")
        print text
    f=open(pramas_path,'w+')
    f.writelines(text)
    f.close()


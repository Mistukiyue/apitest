#coding=utf-8
import os 

cur_file_dir = os.path.split(os.path.realpath(__file__))[0]
cases_dir=cur_file_dir
case_list=[os.path.abspath(os.path.join(cur_file_dir,"testcases/"))]

thread_m=1 #0为单线程，1为多线程

run_project=[]
run_case=[]



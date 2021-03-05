# -*- codeing= utf-8 -*-
# @Time :2021/2/8 12:28
# @Author:黄国彬
# @Update:佟宏元
# @File:PaChinese.py
# @Software:PyCharm
import os
import re
import sys

import pandas as pd
import xlwt
import linecache
import string

unpattern_k = 0  # 无规则次数
unpattern_i = 0  # 无规则次数
# 匹配中文规则
prompt = re.compile(r'prompt=".*[\u4e00-\u9fa5].*"')
text = re.compile(r'text=".*[\u4e00-\u9fa5].*"')
require = re.compile(r'requiredMessage=".*[\u4e00-\u9fa5].*"')
emptyText = re.compile(r'emptyText=".*[\u4e00-\u9fa5].*"')
title = re.compile(r'title=".*[\u4e00-\u9fa5].*"')
label = re.compile(r'label=".*[\u4e00-\u9fa5].*"')
chinese = re.compile(r'[\u4e00-\u9fa5]*')
chinese2 = re.compile(r'[\u4e00-\u9fa5]+')

#反向匹配
# remove1=re.compile(r'^<!--(.*)-->')
remove_single=re.compile(r"(//+[\u4e00-\u9fa5]*)")#取反匹配//+中文
remove_note=re.compile(r"<!--(.*)-->")
remove_max=re.compile(r'/\\*(.*?)(\n*)\\*/')#匹配多行注释
remove_max1=re.compile(r'\/\*(\s|.)*?\*\/')#匹配多行注释

pattern1=re.compile(r'/\*')#匹配\*
pattern2=re.compile(r'\*/')#匹配*/

chinese = re.compile(r'[\u4e00-\u9fa5]*')
# 全局变量
dict = {}
datapattern = []
removepattern=[]
datapattern.append(prompt)
datapattern.append(text)
datapattern.append(require)
datapattern.append(emptyText)
datapattern.append(title)
datapattern.append(label)
#反向匹配
removepattern.append(remove_single)
removepattern.append(chinese)
# print(removepattern[0])

dict['chinese'] = chinese
dictunpattern=[]
# 设置输出集合
alldataSet = set()
randomdata=[]
# 初始化excle
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet4 = book.add_sheet('无规则词条', cell_overwrite_ok=True)  # 创建工做表
def main():
    master()


# 主方法
def master():
    # path = ".\\a.java"
    # path=sys.argv[1]
    print("<=========开始检索=========>")
    path = r"E:\code\shixun\work\test"  # 文件路径
    pathlist = OSfilename(path)  # 获取目录下全部文件名用list存储
    alldata(pathlist)  # 获取词条
    savepath = r"E:\code\shixun\work\爬取中文.xls"  # 保存在当前路径下的xls文件中
    saveDate(alldataSet, savepath)  # 输出excle
    print("<=========检索完成=========>")


# 获取路径集合
def OSfilename(filepath):  # 返回路径的集合
    All_Filename = []
    for (dirpath, dirnames, filenames) in os.walk(filepath):
        for i in filenames:
            All_Filename += [os.path.join(dirpath, i)]
    return All_Filename

# 获取词条
def alldata(pathlist):
    sheet3 = book.add_sheet('无法检测路径', cell_overwrite_ok=True)  # 创建工做表
    i = 0
    for path in pathlist:
        try:
            findChinese(path)
        except:
            sheet3.write(i, 0, path)
            i += 1
            continue
    return alldata

#匹配到中文  bd=re.sub('/'," ",bd)
def findChinese(path):
    # 返回结果
    file = open(path, encoding="UTF-8")
    strfile = file.read()
    # 遍历字符串，一次处理一行
    global unpattern_i
    global unpattern_k
    line_num = 0
    for line in strfile.splitlines():
        line_num+=1
        time = 0  # 记录正则匹配次数
        for i in range(len(datapattern)):
            re = datapattern[i].findall(line)
            if len(re) != 0:
                for j in range(len(re)):
                    time += 1
                    alldataSet.add(re[j])
        if time == 0:
            str = chinese2.findall(line)
            if len(str) != 0:
                strun=linecache.getline(path,line_num)#获取指定文件（path）的行号（line_num）

                if unpattern_i == 800 * (unpattern_k+1):#一列满足800个则列数加一
                    unpattern_k += 1
                sheet4.write(unpattern_i - 800 * (unpattern_k), (unpattern_k) , path)#
                sheet4.write(unpattern_i - 800 * (unpattern_k), (unpattern_k)+1 , line_num)
                sheet4.write(unpattern_i - 800 * (unpattern_k),  (unpattern_k)+2,strun)
                unpattern_i+=1
    file.close()
    return

# 输出excle
def saveDate(datalist, savepath):
    k = 0
    sheet = book.add_sheet('有规则词条', cell_overwrite_ok=True)  # 创建工做表
    sheet2 = book.add_sheet('纯汉字词条', cell_overwrite_ok=True)  # 创建工做表
    i = 0
    for e in iter(datalist):
        if i == 800 * (k + 1):
            k += 1
        str = dict.get('chinese').findall(e)
        # print(str)
        if len(str) != 0:
            sheet.write(i - 800 * (k), 2 * (k), e)
            sheet2.write(i - 800 * (k), 2 * (k), str)
        i += 1
    book.save(savepath)

if __name__ == '__main__':
    main()

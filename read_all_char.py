#coding=utf-8
#
# read all charactor from a file
# 读取所有的文字
# 这里主要是通过, unicode来对一个字符串进行编码成utf8这样就正确读取个数和获取信息了

import os

def read_all_char(filename):
    local_filename = unicode(filename, 'utf8');
    f = open(local_filename, "r");
    ctx = f.readlines();
    t = {};
    for line in ctx:
        local_line = unicode(line, 'utf8');
        num = len(local_line);
        for l in local_line:
            t[l] = True;

    lstr = "";
    for d in t:
        lstr = lstr + d;
    print(lstr);
    return;

read_all_char("G/TEST.txt");

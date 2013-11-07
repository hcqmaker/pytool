# -*- coding:utf8 -*-

import os,codecs

#--------------------------
# param path 要搜索文件的目录
# param t 保存文件的列表
def findfiles(path, t):
    files = os.listdir(path);
    for f in files:
        npath = path + '/' + f;
        if(os.path.isfile(npath)):
            t.append(npath);
        if(os.path.isdir(npath)):
            if (f[0] == '.'):
                pass;
            else:
                findfiles(npath, t);
    return;
            
            
t = [];
#path = "F:/test_lua/Resources/hd/Images";
path = "G:/练手区";
findfiles(unicode(path, 'utf8'), t);

for fn in t:
    print(fn);

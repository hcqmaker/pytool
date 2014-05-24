#!/usr/bin/env python
#-*-coding:utf8-*-
# 这个是服务器进行程序发布的后台程序
# 主要用于服务器方面的管理
# 注意机子上必须先安装 wget,unzip 这两个包

import socket, select, thread, os, struct

host='127.0.0.1'
port=8901

help_data = [
  "unpack {unzip path} {zip url}",       
  "download {zip url or other url}",
  "unzip {zip file} {unzip path}",
  "kill {com.Main}",
  "shell {ls}",
        ];

#========================================
# 获取url中的文件名字
def get_url_filename(url):
    index = url.rfind('/');
    if (index == -1):
        return url;
    zip_name = url[index + 1:]; 
    return zip_name;

#========================================
# 关闭一个进程
def kill_cmd(pro_name):
    ss = os.popen("kill -9 `ps -ef|grep " + pro_name + " | grep -v \"grep\"|awk '{print $2} '`").read();
    return ss;

#========================================
# 添加shell 命令
def shell_cmd(cmd):
    print("data",cmd);
    ss = os.popen(cmd).read();
    return ss;

#========================================
# 调用shell wget下载 zip文件 
def handle_download(url, zip_name, obj):
    cmd_str = "wget -O " + zip_name + " " + url;
    print(cmd_str);
    ss = os.popen(cmd_str).read();
    obj.end_download(ss);
    thread.exit_thread();
    return;

#========================================
#  解压zip文件
def handle_unzip(filename, path, obj):
    cmd_str = "unzip -d " + path + " " + filename;
    print(cmd_str);
    ss = os.popen(cmd_str).read();
    obj.end_unzip(ss);
    thread.exit_thread();
    return;

#========================================
# 
class client_pack():
    def __init__(self):
        self.bytes = '';
        self.data_len = 0;
        return;

    def push(self, bytes):
        self.bytes += bytes;
        self.parse_len();
        return;

    def parse_len(self):
        if (self.data_len <= 0 and len(self.bytes) >= 4):
            (self.data_len,) = struct.unpack("i", self.bytes[:4]);
            print("len:", self.data_len);
            self.bytes = self.bytes[4:];
        return;

    def has_msg(self):
        if (len(self.bytes) >= self.data_len and self.data_len > 0):
            return True;
        return False;

    def get_msg(self):
        msg = self.bytes[:self.data_len];
        print("msg:",msg);
        self.bytes = self.bytes[self.data_len:];
        self.data_len = 0;
        self.parse_len();
        return msg;

#========================================
#
class client_data():
    def __init__(self, s):
        self.s = s;
        self.zip_name = '';
        self.path = '.';
        self.url = '';
        self.dning = 0;
        self.uping = 0;
        self.dn_only = False;
        self.msg = client_pack();
        return;

    def get_socket(self):
        return self.s;

    def recv_data(self, bytes):
        self.msg.push(bytes);
        self.parse_data();
        return;

    def parse_data(self):
        while True:
            if (not self.msg.has_msg()):
               break; 
            pack_data = self.msg.get_msg();
            str_ss = pack_data.split(" ");
            num = len(str_ss);
            print("data parse len:",num);
            if (num > 1):
                self.handle_data(str_ss[0], str_ss, num);
            else:
                self.send_data("Invalid command ");
        return;

    def handle_data(self, cmd, data, num):
        if (cmd == "unpack"):
            if (self.dning == 1):
                self.send_data("download something");
                return;
            if (num < 3):
                self.send_data("Invalid command like[" + help_data[0] + "]");
            else:
                self.dn_only = False;
                self.path = data[1];
                self.url = data[2];
                if (self.url.find("http://") == -1 and self.url.find("https://") == -1):
                    self.send_data("Invalid command like [ " + help_data[0] + "] ");
                    return;
                if (self.path == ""):
                    self.path = '.';
                self.zip_name = get_url_filename(self.url);
                self.start_download();
        elif (cmd == "download"):
            if (num < 2):
                self.send_data("Invalid command like ["+help_data[1]+"] ");
            else:
                self.dn_only = True;
                self.url = str_ss[1];
                self.zip_name = get_url_filename(self.url);
                self.start_download();
        elif (cmd == "unzip"):
            if (num < 3):
                self.send_data("Invalid command like [" + help_data[2] + "] ");
            else:
                self.zip_name = data[1];
                self.path = data[2];
                self.start_unzip();
        elif (cmd == "kill"):
            if (num < 2):
                self.send_data("Invalid command [" + help_data[3] + "]");
            else:
                ss = kill_cmd(data[1]);
                self.send_data("ok" + ss);
        elif (cmd == "shell"):
            if (num < 2):
                self.send_data("Invalid command like ["+help_data[4]+"]");
            else:
                cmd_data = '';
                xn = len(data);
                for i in range(1, xn):
                    cmd_data = cmd_data + data[i] + " ";
                if (cmd_data == ""): 
                    self.send_data("Invalid command like [" + help_data[4] + "]");
                    return;

                ss = shell_cmd(cmd_data);
                self.send_data(ss);
        elif (cmd == "help"):
            ss = '\n'.join(help_data);
            self.send_data(ss);
        else:
            self.send_data("Invalid command ");
        return;

    def send_cmd(self, cmd, data):
        pack_data = cmd + " " + data;
        self.s.send(struct.pack("i", len(pack_data)) + pack_data);
        return;

    def send_data(self, data):
        self.send_cmd("data", data);
        return;

    def start_download(self):
        self.dning = 1;
        thread.start_new_thread(handle_download, (self.url, self.zip_name, self));
        return;

    def start_unzip(self):
        self.uping = 1;
        thread.start_new_thread(handle_unzip, (self.zip_name, self.path, self));
        return;

    def end_download(self, ss):
        self.dning = 0;
        if (self.dn_only):
            self.send_data("download finish : " + self.zip_name + " od:" + ss);
            return;
        self.start_unzip();
        print("download finish");
        return;

    def end_unzip(self, ss):
        self.uping = 0;
        self.send_data("unzip finish : " + self.zip_name + " od:" + ss);
        print("unzip filename");
        return;

#========================================
class server_help():
    def ___init___(self):
        return;

    def start(self,host,port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host,port));
        self.s.listen(1);
        self.s.setblocking(0);
        self.epoll = select.epoll();
        self.epoll.register(self.s.fileno(), select.EPOLLIN);
        self.run();        
        return;

    def run(self):
        try:
            cs = {};
            client_list = {};
            while True:
                events = self.epoll.poll(1);
                for fileno, event in events:
                    if (fileno == self.s.fileno()):
                        c, address = self.s.accept();
                        print("[client connect]",address,"");
                        c.setblocking(0);
                        self.epoll.register(c.fileno(), select.EPOLLIN)
                        cs[c.fileno()] = c;
                        client_list[c.fileno()] = client_data(c);
                    elif event & select.EPOLLIN:
                        cc = client_list[fileno];
                        if (c and cc):
                            try:
                                bytes = c.recv(1024);
                                cc.recv_data(bytes);
                            except socket.error, e:
                                print("[client except:]", e);
                                self.epoll.unregister(fileno);
                                cs[fileno].close();
                                del client_list[fileno];
                                del cs[fileno];

                        #client_list[c.fileno()].push(cs[fileno].recv(1024));
                    elif event & select.EPOLLOUT:
                        #bytes_out = cs[fileno].send(resps[fileno]);
                        print("ou");
                    elif event & select.EPOLLHUP:
                        print("[client close]");
                        self.epoll.unregister(fileno);
                        cs[fileno].close();
                        del client_list[fileno];
                        del cs[fileno];
        finally:
            self.epoll.unregister(self.s.fileno());
            self.epoll.close();
            self.s.close();


if __name__ == "__main__":
    print("==== start server ===");
    sh = server_help();
    sh.start(host,port);
    #test_data();
                        

            
            

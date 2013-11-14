import sys
import memcache
import socket

def memcached_command():
    mc = None;
    is_connect = False;
    cmd = None;
    while(True):
        input_data = raw_input("cmd:");
        t = input_data.split(" ");
        num = len(t);
        if (num > 0):
            cmd = t[0];
        if (cmd == "quit"):
            break;
        elif (cmd == "mc"):
            mc = memcache.Client(['127.0.0.1:11211'], debug=0);
            print("connect: memcached: 127.0.0.1:11211");
            is_connect = True;
        elif (cmd == "telnet"):
            mc = memcache.Client([t[1] + ":" + t[2]], debug=0);
            print("connect: memcached: " + t[1] + t[2]);
            is_connect = True;
        elif (cmd == "close"):
            if (is_connect):
                mc.disconnect_all();
                is_connect = False;
        elif (cmd == "stats"):
            if (is_connect):
                data = None;
                if (num > 1):
                    data = mc.get_stats(t[1]);
                else:
                    data = mc.get_stats();
                #print(data);
                if (len(data) > 0):
                    data_tuple = data[0];
                    data_name = data_tuple[0];
                    data_list = data_tuple[1];
                    data_keys = data_list.keys();
                    data_keys.sort();
                    print(name);
                    for v in data_keys:
                         print("%-30s:%-20s" %(v, data_list[v]));
        elif (cmd == "dump"):
            if (is_connect):
                print("dump something");
        elif (cmd == "set"):
            if (is_connect):
                key = t[1];
                val = t[2];
                if (num > 3):
                    time = int(t[3]);
                else:
                    time = 0;
                mc.set(key, val, time);
                #print(data);
        elif (cmd == "slabs"):
            if (is_connect):
                data = mc.get_slabs();
                print(data);
        elif (cmd == "dump_keys"):
            """ dump_keys [path] # dump all key to a files """
            if (is_connect and num > 1):
                file_name = t[1];
                file_handler = open(file_name, "wb");
                data_out,info_out = mc.get_dump_key();
                for data_tuple in data_out:
                    data_name = data_tuple[0];
                    data_dict = data_tuple[1];
                    data_keys = data_dict.keys();
                    
                    #print("==================");
                    #print(data_keys);
                    for key in data_keys:
                        data_item = data_dict[key];
                        file_str = "%s,%s,%s\n" %(key, data_item['size'], data_item['end_time']);
                        file_handler.write(file_str);
                        #print("item_key:",key);
                        #print("%-30s:%-s" %(v, data_list[v]));
                file_handler.flush();
                file_handler.close();
                # out info
                info_duple = info_out[0];
                info_vname = info_duple[0];
                info_vdict = info_duple[1];
                info_num = 0;
                for info_k in info_vdict:
                    info_item = info_vdict[info_k];
                    info_item_num = info_item["number"];
                    info_num = info_num + int(info_item_num);
                    print("ITEM:" + info_k +":number " + info_item["number"]);
                print("item key total num:", info_num);
                print("finish dump");
            else:
                print("dump_keys [filename]");
                
        #print(cmd);
    return;



memcached_command();

#encoding=utf-8
import sys
import string
import MySQLdb as mydb

def do_find():
    #mysql -h192.168.101.29 -P7725 -uroot -p"^sttt&7725*()"
    con = mydb.connect(host='192.168.101.29', user='root', passwd='^sttt&7725*()',db='phone_tkd_public',port=7725);
    cur = con.cursor();
    #con:execute("set names utf8;")
    sql = "SELECT user_id FROM g_user WHERE `level` >=4 AND `level` <= 9;";
    cur.execute(sql);
    rows = cur.fetchall();
    ll = [];
    for row in rows:
        ll.append(row[0]);

    head = "INSERT INTO g_task(user_id, task_id, task_type, currCount, state) VALUES";
    num = len(ll);
    dtstr = '';
    for i in range(num):
        if ((num-1)== i):
            dtstr = dtstr + "(" + str(ll[i]) + ", 20012, 3, 0, 0);";
        else:
            dtstr = dtstr + "(" + str(ll[i]) + ", 20012, 3, 0, 0),";

    fn = open("task_do.sql", "w");
    fn.write(head);
    fn.write(dtstr);
    fn.close();
    
    #print(dtstr);
    cur.close();
    con.close();
    return;

do_find();

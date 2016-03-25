#encoding=utf-8
import sys
import string
import MySQLdb as mydb

"""

"""

def do_find():
    con = mydb.connect(host='127.0.0.1', user='root', passwd='root',db='game');
    cur = con.cursor();
    sql = "SELECT COUNT(*) FROM game_user WHERE login_time >= '2014-12-01 00:00:00';";
    cur.execute(sql);
    row = cur.fetchone();
    print(row);
    cur.close();
    con.close();
    return;

def do_act():
    l = [1,2,3,4,5,6];
    print(','.join(str(i)for i in l));

def do_all():
    con = mydb.connect(host='127.0.0.1', user='root', passwd='root',db='game',port=3306);
    cur = con.cursor();
    #con:execute("set names utf8;")
    sql = "SELECT user_id FROM game_user WHERE `level` >=4 AND `level` <= 9;";
    cur.execute(sql);
    rows = cur.fetchall();
    ll = [];
    for row in rows:
        ll.append(row[0]);

    head = "INSERT INTO game_task(user_id, task_id, task_type, currCount, state) VALUES";
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

#do_act();

def get_cupl(num):
        t = [];
        for i in range(1, num + 1):
            for j in range(i, num + 1):
                t.append([i,j]);
        return t;

#print(get_cupl(3));
lk = [1,3,6,7,9];
for i in lk:
    print(i);


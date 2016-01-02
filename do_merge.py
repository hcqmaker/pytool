#encoding=utf-8
import sys
import MySQLdb as mydb

"""
合服处理

1. 创建数据库和表 phone_monsterxx.sql
2. 合并数据库到指定的数据库
3. 更新需要重新设置的服务器id
4. 更新一些需要每次更新的次数
5. 设置服务器的的合服列表phone_share.g_server_combine
6. 重新设置服务服的ip和端口phone_share.g_server_list
7. 重启对应的tomcat

"""
USER='root';

PASSWD='zuzhang202';
HOST='192.168.1.222';

TIME_STR = '2014-12-01 00:00:00';
SERVER_ID = 1

STO_DB = 'phone_monster_mix_12';
SFROM_DBS = ['phone_monster','phone_monster_2'];
SDO_SQL = 'mix_sql.sql';

#============================================================

FIND_USER_SQL = "SELECT `user_id` FROM `%s`.`g_user` WHERE login_time >= '%s';"
DO_INSERT_SQL = "insert into `%s`.`%s`(%s) (select %s from `%s`.`%s` where user_id in (%s));";
DO_INSERT_FIELD_SQL = "insert into `%s`.`%s`(%s) (select %s from `%s`.`%s` where %s in (%s));";
DO_USER_SQL = "insert into `%s`.`g_user`(%s) (select %s from `%s`.`g_user` where user_id in (%s));";

DO_FIELD_T={
    #g_user
    "g_user":"`user_id`,`user_name`,`level`,`profession`,`x`,`y`,`screen_id`,`user_exp`,`call_id`,\
`camp`,`union_id`,`union_name`,`party`,`spirit`,`gold`,`bill`,`prestige`,`baby_bill`,`gender`,`state`,\
`area_id`,`step`,`time`,`renew_time`,`url`,`node_star_sum`,`package_num`,`follow_id`,`vip`,`max_form_mr_num`,\
`com_att_hard`,`com_def_hard`,`spe_att_hard`,`spe_def_hard`,`speed_hard`,`server_id`,`generater_lv`,`generater_exp`,\
`generater_upgrade_giftbag`,`train_hall_rob_num`,`is_enter_train_hall`,`enter_train_hall_time`,`has_training_get_exp`,\
`dream_spirit`,`dcave_exchanged`,`celebrity_difficult`,`celebrity_status`,`daoguan_pve_has`,`daoguan_pve_difficult`,\
`series_prestige_level`,`series_prestige`,`series_emblem`,`daoguan_pvp_num`,`unlock`,`salutation_rewards`,`vip_buy`,\
`active_score`,`rob_fragment_num`,`login_time`,`amity`,`open_treasure_num`,`last_update_spirit`,`spirit_item_use_num`, \
`goldbar_use_num`,`frecharge`,`follow_login`,`add_login`,`ware_house_num`,`arena_medal`,`dreamcave_clean`,`robFragBuyNum`,`platform`",
    #g_cheer
    "g_cheer":"`user_id`,`location1_state`,`location1_level`,`location1_mid`,\
`location2_state`,`location2_level`,`location2_mid`,`location3_state`,`location3_level`,\
`location3_mid`,`location4_state`,`location4_level`,`location4_mid`,`location5_state`,\
`location5_level`,`location5_mid`,`location6_state`,`location6_level`,`location6_mid`,\
`location7_state`,`location7_level`,`location7_mid`,`location8_state`,`location8_level`,\
`location8_mid`,`location9_state`,`location9_level`,`location9_mid`,`create_time`",
    #g_compound
    "g_compound":"`user_id`,`compound_num`,`buy_num`,`enter_last_time`",
    #g_dr_task_info
    "g_dr_task_info":"`user_id`,`refresh_num`,`task_monster_id`,`remind_num`,`reset_num`,\
`first_pos`,`day_first_pass`,`other_id`,`other_monster_id`,`other_monster_status`,\
    `use_spirit`,`last_update_time`",
    #g_dr_task_ms
    "g_dr_task_ms":"`user_id`,`monster_id`,`level`,`expire_time`",
    #g_equip
    "g_equip":"`id`,`user_id`,`mid`,`equip_id`,`equip_part`,`equip_type`,`level`,`monster_id`,`quality`,\
`up_time`,`qup_time`,`openHole`,`inlay`,`xlInfo`,`strengthenInfo`",
    #g_formation
    "g_formation":"`user_id`,`fmt_id`,`state`,`mid1`,`mid2`,`mid3`,`mid4`,`mid5`,`mid6`,`mid7`,`mid8`,`mid9`,`lv`,`experience`",
    #g_fragment
    "g_fragment":"`user_id`,`fragment_id`,`pos_num`",
    #g_friend
    "g_friend":"`user_id`,`friend_id`,`intimacy`",
    #g_friend_gift
    "g_friend_gift":"`user_id`,`game_friends`,`community_friends`,`give_num`,\
`receive_num`,`give_time`,`give_users`,`give_items`,\
`can_receive_from`,`can_receive_type`,`can_receive_id`,`friend_request`,\
`amity_rewards`,`last_enter_time`,`receive_last_time`",
    #g_generater_luck_event
    "g_generater_luck_event":"`user_id`,`event_id`,`reward_item_type`,`reward_item_id`,`reward_item_num`,`status`,`time`,`finish_num`",
    #g_ios_push_token
    "g_ios_push_token":"`user_id`,`ios_push_token`,`platform`",
    #g_leave_words
    "g_leave_words":"`from_user_id`,`from_user_name`,`to_user_id`,`words`",
    #g_mail
    "g_mail":"`type`,`to_uid`,`from_uid`,`from_name`,`state`,`attachment`,`subject`,`content`,`rewards`,`other`,`time`",
    #g_mail_common
    "g_mail_common":"`type`,`to_uid`,`from_uid`,`from_name`,`state`,`attachment`,`subject`,`content`,`rewards`,`other`,`time`",
    #g_map
    "g_map":"`user_id`,`map_id`,`difficult`,`is_get_full_star_rewards`,`is_full_star`,`last_enter_time`",
    #g_map_exploit
    "g_map_exploit":"`server_id`,`map_id`,`manager_id`,`manager_name`,`measure_id`,\
`begin_manage_time`,`begin_measure_time`,`ministrant`,`protected_users`",
    #g_monster
    "g_monster":"`id`,`user_id`,`monster_id`,`com_att`,`com_def`,`spe_att`,`spe_def`,`speed`,\
`hp`,`crit_ratio`,`dcrit_ratio`,`hit_ratio`,`escape_ratio`,`parry_ratio`,`against_ratio`,`intimate`,\
`_character`,`genes`,`gender`,`lv`,`follow`,`exp`,`com_att_lv`,`com_def_lv`,`spe_att_lv`,\
`spe_def_lv`,`speed_lv`,`hp_lv`,`total_lv`,`str_lv`,`com_skill`,`spe_skill`,`quality`,\
`up_quality_exp`,`teamIndex`,`passives`,`learn_skills`,`com_att_aptitude`,`com_def_aptitude`,\
`spe_att_aptitude`,`spe_def_aptitude`,`speed_aptitude`,`total_aptitude`,`apt_comatt_upnum`,\
`apt_comdef_upnum`,`apt_speatt_upnum`,`apt_spedef_upnum`,`apt_speed_upnum`,`apt_total_upnum`,\
`consume_comatt_hard`,`consume_comdef_hard`,`consume_speatt_hard`,`consume_spedef_hard`,\
`consume_speed_hard`,`com_att_cult`,`com_def_cult`,`spe_att_cult`,`spe_def_cult`,`speed_cult`,\
`com_att_cult_num`,`com_def_cult_num`,`spe_att_cult_num`,`spe_def_cult_num`,\
`speed_cult_num`,`strengthen_lv`,`pass_pos`,`treasures`,`is_ware_house`,`is_mat`,`generation`,`cheer_teamIndex`",
    #g_monster_capture
    "g_monster_capture":"`user_id`,`map_id`,`monster_id`,`cur_capture_num`,`reset_capture`,`cur_refresh_num`,`reset_refresh`,\
`use_ball`,`last_update_time`,`recovery_num`,`recovery_time`",
    #g_monster_generater
    "g_monster_generater":"`user_id`,`gen_type`,`day_free_count`,`temp_drop_count`,`perm_count`,`last_time`,`gen_is_get_luck`,`is_spend_money`,`last_enter_time`",
    #g_monster_handbook
    "g_monster_handbook":"`user_id`,`monster_ids`,`collect_rank_num`,`collect_reward_next_num`,`special_collect_reward`",
    #g_monster_mating_message
    "g_monster_mating_message":"`apply_id`,`apply_name`,`apply_monster_uid`,`apply_monster_cfg_id`,`apply_gender`,\
`apply_generation`,`apply_genes`,`user_id`,`user_name`,`user_monster_uid`,\
`user_monster_cfg_id`,`user_gender`,`user_generation`,`user_genes`,`expiredTime`,`isInvalid`,`type`",
    #g_monster_mating_register
    "g_monster_mating_register":"`server_id`,`user_id`,`user_name`,`monster_uid`,`monster_cfg_id`,`gender`,`generation`,`genes`,`is_auto_mating`,`expired_time`",
    #g_moon_card
    "g_moon_card":"`user_id`,`expired_time`,`reward_status`,`reward_id`,`last_reward_time`",
    #g_mysticmap
    "g_mysticmap":"`user_id`,`create_time`,`refresh_time`",
    #g_mysticnode
    "g_mysticnode":"`user_id`,`node_id`,`fight_time`,`refresh_num`",
    #g_node
    "g_node":"`user_id`,`map_id`,`node_id`,`difficult`,`battle_cnt`,`star`,`first`,`resetNum`",
    #g_package
    "g_package":"`user_id`,`cell_index`,`item_id`,`item_num`,`item_type`",
    #g_passive
    "g_passive":"`user_id`,`passive_id`,`level`,`mid`,`exp`",
    #g_rest
    "g_rest":"`user_id`,`enter_time`,`status`",
    #g_shop_guest
    "g_shop_guest":"`user_id`,`guest_point`,`exp_card_valid_time`,`luck_card_valid_time`,`buy_shop_id`,`buy_num`,`enter_last_time`,`guest_card_valid_time`,\
`seiko_card_valid_time`,`war_card_valid_time`,`skill_card_valid_time`,`compound_card_valid_time`",
    
    #看代码有没有直接生成的
    #g_shop_limit
    "g_shop_limit":"`server_id`,`shop_id`,`item_type`,`item_id`,`remain_num`",
    #g_shop_user
    "g_shop_user":"`user_id`,`buy_shop_id`,`last_time`",
    #g_sign
    "g_sign":"`user_id`,`status`,`sign_days`,`month_reward`,`last_update_time`,`sign_num`,`vip_sign_num`,\
`vip_month_reward`,`vip_sign_status`,`curr_month_resign_num`,`curr_month_vip_resign_num`",
    #g_system_reward
    "g_system_reward":"`user_id`,`reward_item`,`type`,`other_data`,`time`",
    #g_task
    "g_task":"`user_id`,`task_id`,`curr_count`,`task_type`,`state`,`time`,`last_enter_time`",
    #g_treasure
    "g_treasure":"`id`,`user_id`,`treasure_id`,`level`,`exp`,`mid`",
    #g_user_limit_num
    "g_user_limit_num":"`user_id`,`formation_upgrade_num`,`skill_upgrade_num`,`last_update_time`",
    #log_activecode
    "log_activecode":"`user_id`,`index`,`time`",
    #log_activity
    "log_activity":"`user_id`,`activity_id`,`condition_id`,`time`",
    #log_activity_buycraze_record
    "log_activity_buycraze_record":"`user_id`,`activity_id`,`value`",
    #log_activity_capture_record
    "log_activity_capture_record":"`user_id`,`activity_id`,`value`",
    #log_activity_egg_record
    "log_activity_egg_record":"`user_id`,`activity_id`,`value`",
    #log_activity_fight_win
    "log_activity_fight_win":"`user_id`,`activity_id`,`value`",
    #log_activity_mating_record
    "log_activity_mating_record":"`user_id`,`activity_id`,`value`",
    #log_activity_mixpet_record
    "log_activity_mixpet_record":"`user_id`,`activity_id`,`value`",
    #log_activity_openchest_record
    "log_activity_openchest_record":"`user_id`,`activity_id`,`value`",
    #log_activity_strongpet_record
    "log_activity_strongpet_record":"`user_id`,`activity_id`,`value`",
    #log_mail_common
    "log_mail_common":"`uid`,`mail_id`,`time`",
    
    };

#========================================================================
#========= 更新server_id的
DO_UPDATE = {
    "g_monster_mating_register":"update `%s`.`g_monster_mating_register` set server_id = %d;",
    #"g_monster_mating_message":"update `%s`.`g_monster_mating_message` set server_id = %d;",
    "g_map_exploit":"update `%s`.`g_map_exploit` set server_id = %d;",
    "g_exploit_user":"update `%s`.`g_exploit_user` set server_id = %d;",
    };
#========================================================================

class DBClass():
    def __init__(self):
        return;
    def setup(self, fromdbs, todb, fn):
        self.fromdbs = fromdbs;
        self.todb = todb;
        self.user_t = {};
        self.fn = fn;
        self.writedb = None;
        return;
    def open_sql(self):
        self.sqlfile = open(self.fn, 'wb');
        return;
    def close_sql(self):
        self.sqlfile.close();
        return;
    def do_write_sql(self, sql, msg):
        self.sqlfile.write('/* ' + msg + ' */\n');
        self.sqlfile.write(sql + "\n\n");
        self.sqlfile.flush();
        return;
    def do_select_user(self):
        for dbName in self.fromdbs:
            con = mydb.connect(host=HOST, user=USER, passwd=PASSWD,db=dbName);
            cur = con.cursor();
            sql = FIND_USER_SQL % (dbName,TIME_STR);
            cur.execute(sql);
            rows = cur.fetchall();
            ll = [];
            for row in rows:
                ll.append(row[0]);
            self.user_t[dbName] = ll;
            cur.close();
            con.close();
        return;
    def do_field_dbName_DB(self, dbName, field):
        field_str = DO_FIELD_T[dbName];
        for key,val in self.user_t.items():
            lstr = ','.join(str(i)for i in val);
            sql = DO_INSERT_FIELD_SQL % (self.todb, dbName, field_str, field_str, key, dbName, field, lstr);
            self.do_write_sql(sql, key + "==>" + dbName);
        return;
    def do_field_dbName(self, dbName):
        field_str = DO_FIELD_T[dbName];
        for key,val in self.user_t.items():
            lstr = ','.join(str(i)for i in val);
            sql = DO_INSERT_SQL % (self.todb, dbName, field_str, field_str, key, dbName, lstr);
            self.do_write_sql(sql, key + "==>" + dbName);
        return;
    
    def do_user(self):
        self.do_field_dbName("g_user");
        self.do_field_dbName("g_cheer");
        self.do_field_dbName("g_compound");
        self.do_field_dbName("g_dr_task_info");
        self.do_field_dbName("g_dr_task_ms");
        self.do_field_dbName("g_formation");
        self.do_field_dbName("g_fragment");
        self.do_field_dbName("g_friend");
        self.do_field_dbName("g_friend_gift");
        self.do_field_dbName("g_generater_luck_event");
        self.do_field_dbName("g_ios_push_token");
        self.do_field_dbName("g_map");
        self.do_field_dbName("g_equip");
        #self.do_field_dbName("g_map_exploit");
        self.do_field_dbName("g_monster");
        self.do_field_dbName("g_monster_capture");
        self.do_field_dbName("g_monster_generater");
        self.do_field_dbName("g_monster_handbook");
        self.do_field_dbName("g_monster_mating_message");
        self.do_field_dbName("g_monster_mating_register");
        self.do_field_dbName("g_moon_card");
        self.do_field_dbName("g_mysticmap");
        self.do_field_dbName("g_mysticnode");
        self.do_field_dbName("g_node");
        self.do_field_dbName("g_package");
        self.do_field_dbName("g_passive");
        self.do_field_dbName("g_rest");
        self.do_field_dbName("g_shop_guest");
        self.do_field_dbName("g_shop_user");
        self.do_field_dbName("g_sign");
        self.do_field_dbName("g_system_reward");
        self.do_field_dbName("g_task");
        self.do_field_dbName("g_treasure");
        self.do_field_dbName("g_user_limit_num");
        self.do_field_dbName("log_activecode");
        self.do_field_dbName("log_activity");
        self.do_field_dbName("log_activity_buycraze_record");
        self.do_field_dbName("log_activity_capture_record");
        self.do_field_dbName("log_activity_egg_record");
        self.do_field_dbName("log_activity_fight_win");
        self.do_field_dbName("log_activity_mating_record");
        self.do_field_dbName("log_activity_mixpet_record");
        self.do_field_dbName("log_activity_openchest_record");
        self.do_field_dbName("log_activity_strongpet_record");

        self.do_field_dbName_DB('g_leave_words','to_user_id');
        self.do_field_dbName_DB('g_mail','to_uid');
        self.do_field_dbName_DB('g_mail_common','to_uid');
        self.do_field_dbName_DB('log_mail_common','uid');
        
        # 把需要修改服务器ID的进行一下修改
        #g_monster_mating_register,g_monster_mating_message,g_map_exploit,g_exploit_user
        for (k,v) in DO_UPDATE.items():
            sql = v % (self.todb, SERVER_ID);
            self.do_write_sql(sql, self.todb + "==>" + k);
        return;
    # 获取所有的组合方式
    def get_cupl(self,num):
        t = [];
        for i in range(0, num):
            for j in range(i+1, num):
                t.append([i,j]);
        return t;
    # 查看多个表中是否有相同的user_id
    def check_same_user(self):
        print("========= start check same user =======");
        self.do_select_user();
        data_t = [];
        name_t = [];
        #print(self.user_t);
        for (k,v) in self.user_t.items():
            tt = {};
            for d in v:
                tt[d] = True;
            data_t.append(tt);
            name_t.append(k);
        # 获取可能的组合进行比较
        num = len(data_t);
        ct = self.get_cupl(num);
        for i in ct:
            i1 = i[0];
            i2 = i[1];
            key1 = name_t[i1];
            key2 = name_t[i2];
            ks = data_t[i1];
            vs = data_t[i2];
            print("key1,key2=>",key1,key2);
            for k in ks:
                if (vs.has_key(k)):
                    print("same user_id:" + str(k));
            
        return;
    
    def run(self):
        self.do_select_user();
        self.open_sql();
        self.do_user();
        self.close_sql();
        return;


app = DBClass();
app.setup(SFROM_DBS,STO_DB,SDO_SQL);
#app.check_same_user();
app.run();


#-*-coding:utf8-*-
from xml.etree.ElementTree import ElementTree
import os;

# 一个通用的类针对xml进行分解并获得一个表


"""
{node:"monster", k:, v:[]}
node：节点的名字
k: 作为字典的key的数据
v: 字典数据中需要存储的数据
"""
def doXmlParse(fn, t):
    out_dict = {};
    tree = ElementTree();
    tree.parse(fn);
    tree_nodes = tree.findall(t["node"]);
    for rnode in tree_nodes:
        sv = {};
        for k in t["v"]:
            sv[k] = rnode.get(k);
        out_dict[rnode.get(t["k"])] = sv;
    return out_dict;

def test_monster_fetter():
    to_monster = {"node":"monster", "k":"id", "v":["passive","comSkill","speSkill","fetters","name"]};
    to_fetter = {"node":"p", "k":"id", "v":["monsters"]};

    dic_monster = doXmlParse("monster.xml", to_monster);
    dic_fetter = doXmlParse("fetter.xml", to_fetter);

    # 检查精灵的被动技能
    for (k,v) in dic_monster.items():
        l_fetters = v.get("fetters");
        # 羁绊不存在
        if (l_fetters != None and l_fetters != ""):
            fs = l_fetters.split(",")
            for kk in fs:
                tmp = dic_fetter.get(kk);
                if (tmp == None or tmp == ""):
                    print("宠物 ID:" + k + " 羁绊 ID:" + kk + " 不存在");
                    
    return;
def test_monster_passive():
    to_monster = {"node":"monster", "k":"id", "v":["passive","comSkill","speSkill","fetters","name"]};
    to_passive = {"node":"passive", "k":"id", "v":["name","skillRank"]};

    dic_monster = doXmlParse("monster.xml", to_monster);
    dic_passive = doXmlParse("monster_passives.xml", to_passive);
    
    # 检查精灵的被动技能
    for (k,v) in dic_monster.items():
        l_passive = v.get("passive");
        # 被动技能不存在
        if (l_passive == None or l_passive == ""):
            print("宠物 ID:" + k + " 被动技能没有设置");
        else:
            if (dic_passive.get(l_passive) == None):
                print("宠物 ID:" + k + " 设置的被动技能 ID:" + l_passive + " 不存在");
    return;

def test_monster_skill():
    to_monster = {"node":"monster", "k":"id", "v":["passive","comSkill","speSkill","fetters","name"]};
    to_skill = {"node":"skill", "k":"id", "v":["monsters","name"]};

    dic_monster = doXmlParse("monster.xml", to_monster);
    dic_skill = doXmlParse("monster_skill.xml", to_skill);
    
    # 检查精灵的被动技能
    for (k,v) in dic_monster.items():
        l_comSkill = v.get("comSkill");
        l_speSkill = v.get("speSkill");
        # 主动技能不存在
        if (l_comSkill == None or l_comSkill == ""):
            print("宠物 ID:" + k + " 普攻或者特功技能没有设置");
        else:
            tmp = dic_skill.get(l_comSkill);
            if (tmp == None or tmp == ""):
                print("宠物 ID:" + k + " 设置的技能 ID:" + l_comSkill + " 不存在");
        if (l_speSkill == None or l_speSkill == ""):
            print("宠物 ID:" + k + " 普攻或者特功技能没有设置");
        else:
            tmp = dic_skill.get(l_speSkill);
            if (tmp == None or tmp == ""):
                print("宠物 ID:" + k + " 设置的技能 ID:" + l_speSkill + " 不存在");
    return;
    
#test_monster_passive_skill_fetter();
test_monster_passive();


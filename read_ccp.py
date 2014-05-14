#-*-coding:utf8-*-
from xml.etree.ElementTree import ElementTree
import os;

#
# {}
#
#
#
def tprint(r):
    print(r.tag,r.attrib);
    return;

class ParseCCB():
    def __init__(self):
        self.tree = ElementTree();
        self.mp = [];
        return;

    def parse(self,url):
        self.tree.parse(url);
        self.root = self.tree.getroot();
        root_dic = self.root.find('dict');
        frist_dic = root_dic.find('dict');
        self.parse_dict(frist_dic, self.mp);
        #tprint(frist_dic);
        return;
    
    def parse_children(self, root, mp):
        ndics = root.findall("dict");
        for dic in ndics:
            self.parse_dict(dic, mp);
        return;
    
    def parse_one_properties_array(self, r):
        array = r.find("array");
        ar = [];
        if (array == None):
            return ar;
        for a in array:
            ar.append(a.text);
        return ar;
    
    def parse_one_properties(self, r, n):
        ar = self.parse_one_properties_array(r);
        #print("pro=",r[1].text);
        rtext = r[1].text;
        if (rtext == "contentSize"):
            n["contentSize"] = {"x":float(ar[0]), "y":float(ar[1])};
        elif (rtext == "anchorPoint"):
            n["anchorPoint"] = {"x":float(ar[0]), "y":float(ar[1])};
        elif (rtext == "scale"):
            n["scale"] = {"x":float(ar[0]), "y":float(ar[1])};
        elif (rtext == "position"):
            n["position"] = {"x":float(ar[0]), "y":float(ar[1])};
        elif (rtext == "displayFrame"):
            for s in ar:
                if (s != "" and s != None):
                    n["displayFrame"] = s;
                    break;
        return;
    
    def parse_properties(self, root, n):
        dicts = root.findall("dict");
        for dic in dicts:
            self.parse_one_properties(dic, n);   
        return;
    
    def parse_dict(self, root, mp):
        array = root.findall("array");
        ns = {"prop":{}, "tp":root[1].text};
        mp.append(ns);
        ch = array[0];
        if (len(ch) > 0):
            ns["child"] = [];
            self.parse_children(ch, ns["child"]);
        self.parse_properties(array[1], ns["prop"]);
        return;
    def toJson(self):
        return;
    def toprint(self):
        print(self.mp);
        return;
      
ccb_file = 'C:\\Python27\\monster_map.ccb';

ccb = ParseCCB();
ccb.parse(ccb_file);
ccb.toprint();

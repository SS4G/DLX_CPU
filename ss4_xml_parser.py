# -*- coding: utf-8 -*-
class xml_parser:
    def __init__(self):
        pass
    def get_xml_file_as_str(self,file_name):
        try :
            f=open(file_name,"r")
            lines=f.readlines()
            new_list=[]
            for k in lines:
                new_list.append(k.strip())
            f.close()
            return "".join(new_list)
        except FileNotFoundError:
            print(file_name+" not found")
    def get_tag_block_list(self,tag,string):
        list0=[]
        start_index=0
        end_index=0
        tag_len=len(tag)+2
        while True:
            #print("debug ",string)
            start=string.find("<"+tag+">")
            if start==-1:
                break
            end=string.find("</"+tag+">")
            #print("DEBUG 10:",string[start+len(tag)+2:end])
            list0.append(string[start+len(tag)+2:end])
            
            string=string[end+len("</"+tag+">"):]        
        return list0             
        


  





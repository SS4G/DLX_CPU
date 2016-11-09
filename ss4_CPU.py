# -*- coding: utf-8 -*-
import os
import sys
import copy
from ss4_instruction import *
from ss4_xml_parser import *
from ss4_Cpu_hw_wiget import*
class CPU:         
    def __init__(self):
        # fu list       
        self.glb_clk_cycle=0 
        self.single_type_reg_num=10 #单独一种寄存器的数量               
        self.creat_hw_wiget()
        self.creat_instruction_set()
        self.get_instruction_queue()  
        
       
    
    def creat_hw_wiget(self):
        """
            生成CPU中所包含的单元部件
        """
        #创建fu组
        self.fu_group=[
        Fu(fu_type="alu_add",fu_index_in_type=0),
        Fu(fu_type="alu_mul",fu_index_in_type=0),
        #Fu(fu_type="alu_mul",fu_index_in_type=1),
        Fu(fu_type="alu_div",fu_index_in_type=0),
        Fu(fu_type="ld_unit",fu_index_in_type=0),
        Fu(fu_type="st_unit",fu_index_in_type=0)        
        ]
        #创建寄存器组
        self.reg_group=[Reg(reg_type="int",reg_index_in_type=i) for i in range(self.single_type_reg_num)]+[Reg(reg_type="float",reg_index_in_type=i) for i in range(self.single_type_reg_num)]

    def creat_instruction_set(self):
        """
            根据指令集定义xml生成指令集
        """
        self.inst_queue_len=0
        self.xml_parser0=xml_parser()
        self.inst_set={}#include instruction set dirctory 
                        #type dict{ dict{},dict{}, }
        self.inst_queue=[]#include instructions object        

        inst_set_xml_str=self.xml_parser0.get_xml_file_as_str(os.getcwd()+"\instruction.xml")

        inst_set_str_list=self.xml_parser0.get_tag_block_list(tag="instruction",string=inst_set_xml_str)
         
        self.inst_set_list=[self.creat_1_type_inst(i) for i in inst_set_str_list]
            
        #为CPU定义指令集
        for i in self.inst_set_list:
            self.inst_set[i["name"]]=i 
    
    def get_instruction_queue(self):
        """
        获取源文件中的指令序列
        """
        (self.inst_queue,self.inst_queue_len)=self.construct_inst_queue(os.getcwd()+"\src.s")

    def creat_1_type_inst(self,inst_set_str):
        """
            根据从xml中解析出来的字符串来生成一个新的指令类型
            返回一个包含指令 名称 使用的FU 以及执行时间的字典
        """
        tmp_inst_dict={
            "name":"",#instruction name 
            "exe_cycle":"",# cycles need for instruction execute
            "fu":""# function unit used by instruction 
            }      
        names=self.xml_parser0.get_tag_block_list(tag="name",string=inst_set_str)
        tmp_inst_dict["name"]=names[0]  
        
        execute_cycles=self.xml_parser0.get_tag_block_list(tag="execute_cycle",string=inst_set_str)
        tmp_inst_dict["exe_cycle"]=int(execute_cycles[0])      
        
        fus=self.xml_parser0.get_tag_block_list(tag="function_unit",string=inst_set_str)
        tmp_inst_dict["fu"]=fus[0]      
        return tmp_inst_dict
            
    def construct_inst_queue(self,src_file):
        """
        从.s源文件中获取指令序列
        """
        inst_queue=[]
        queue_len=0
        try :
            #----------construct instruction set ------
            src_handle=open(src_file,"r")
            for  i in src_handle:
                striped_line=i.strip()                
                if striped_line!="":                    
                    param_list=striped_line.split()
                    inst_type=param_list[0]
                    
                    #call constructor of  class instruction
                    inst_queue.append(Instruction(
                        inst_ID=queue_len                                  ,                   
                        full_instruction=striped_line                           ,
                        exe_state="UN_LOAD"                                    ,
                        full_exe_cycles=self.inst_set[inst_type]["exe_cycle"]   ,         
                        current_exe_cycles=0                                    ,
                        fu=self.inst_set[inst_type]["fu"]                       ,
                        dst_reg =param_list[1]                                  ,
                        src_reg1=param_list[2]                                  ,
                        src_reg2=param_list[3]                
                    ))
                    queue_len+=1  
                else:
                    continue
            src_handle.close()                    
            return (inst_queue,queue_len)       
        except FileNotFoundError:
            print("assmble languange source file not found")
   
    def get_fu_obj(self,fu_type="No_FU",fu_index=0,which="old"):
        """
            获取Fu对象的引用
        """
        if which=="old":
            for i in  self.old_state_fu_group:
                if (i.fu_type==fu_type) and (i.fu_index_in_type==fu_index):
                    return i 
        elif which=="new":  
            for i in  self.fu_group:
                if (i.fu_type==fu_type) and (i.fu_index_in_type==fu_index):
                    return i 
        # if code reach here some error occured
        print("ERROR 002: %s%d fu not found" % (fu_type,fu_index))
        input("Pause")   
   
    def get_reg_obj(self,reg_type="No_r",reg_index=0,which="new"):
        if which=="old":
            for i in  self.old_state_reg_group:
                if (i.reg_type==reg_type) and (i.reg_index_in_type==reg_index):
                    return i 
        elif which=="new":
            for i in  self.reg_group:
                if (i.reg_type==reg_type) and (i.reg_index_in_type==reg_index):
                    return i 
                    
        # if code reach here some error occured
        print("ERROR 002: %s%d reg not found" % (reg_type,reg_index))
        #self.debug_print_inst_queue(show_reg_group=True)
        input("Pause")
               
    def copy_fu_group(self,fu_list):
        """
        将fu对象完全拷贝一次 使用浅拷贝 因为fu对象中没有其他的可变对象
        只有常量属性
        """
        copied_list=[]
        for obj in fu_list:
            copied_list.append(copy.deepcopy(obj))
        return copied_list  
    
    def copy_reg_group(self,reg_list):
        """
        将reg对象完全拷贝一次 使用浅拷贝 因为fu对象中没有其他的可变对象
        只有常量属性
        """
        copied_list=[]
        for obj in reg_list:
            copied_list.append(copy.deepcopy(obj))
        return copied_list  
       
    def change_instruction_state(self,cur_inst):
        """
        参数：cur_inst 当前的指令对象
        返回：下一条指令是否需要进入IF态（本条指令是否腾出了IF的位置） info
        """
        #get related wiget in CPU first
        fu_inuse_type=cur_inst.fu["type"]
        fu_inuse_index=cur_inst.fu["index"]
        dst_reg_inuse_type =cur_inst.dst_reg["type"]
        dst_reg_inuse_index=cur_inst.dst_reg["index"]  
        
        src_reg1_inuse_type =cur_inst.src_reg1["type"]
        src_reg1_inuse_index=cur_inst.src_reg1["index"]         

        src_reg2_inuse_type =cur_inst.src_reg2["type"]
        src_reg2_inuse_index=cur_inst.src_reg2["index"]            
        
        #fu_inuse is fu obj related with this instruction 
        fu_inuse_old=self.get_fu_obj(fu_type=fu_inuse_type,fu_index=fu_inuse_index,which="old")
        fu_inuse_new=self.get_fu_obj(fu_type=fu_inuse_type,fu_index=fu_inuse_index,which="new")
        
        dst_reg_inuse_old=self.get_reg_obj(reg_type=dst_reg_inuse_type,reg_index=dst_reg_inuse_index,which="old")
        dst_reg_inuse_new=self.get_reg_obj(reg_type=dst_reg_inuse_type,reg_index=dst_reg_inuse_index,which="new")
 
        src_reg1_inuse_old=self.get_reg_obj(reg_type=src_reg1_inuse_type,reg_index=src_reg1_inuse_index,which="old")
        src_reg1_inuse_new=self.get_reg_obj(reg_type=src_reg1_inuse_type,reg_index=src_reg1_inuse_index,which="new")
        
        src_reg2_inuse_old=self.get_reg_obj(reg_type=src_reg2_inuse_type,reg_index=src_reg2_inuse_index,which="old")
        src_reg2_inuse_new=self.get_reg_obj(reg_type=src_reg2_inuse_type,reg_index=src_reg2_inuse_index,which="new")
        
        
        if cur_inst.exe_state=="UN_LOAD":# instruction at state UN_LOAD
            return ""
        elif cur_inst.exe_state=="IF":         
            if fu_inuse_old.is_busy:
                #print("stall at IF due to fu busy")
                return "" #keep instruction in IF state , do nothing to this instruction 
            elif dst_reg_inuse_old.tobe_write:
                print("stall at IF due to dst reg  busy")
                return  "" #keep instruction in IF state , do nothing to this instruction 
            else:
                
                #set write state
                dst_reg_inuse_new.tobe_write=True
                dst_reg_inuse_new.tobe_write_inst_ID.append(cur_inst.inst_ID)
                dst_reg_inuse_new.reg_user_inst=cur_inst.inst_ID
                
                #set read state
                src_reg1_inuse_new.tobe_read=True 
                src_reg1_inuse_new.tobe_read_inst_ID.append(cur_inst.inst_ID)
                src_reg2_inuse_new.tobe_read=True 
                src_reg2_inuse_new.tobe_read_inst_ID.append(cur_inst.inst_ID)
                
                #set realted FU
                fu_inuse_new.busy_inst_ID=cur_inst.inst_ID
                fu_inuse_new.is_busy=True
                fu_inuse_new.op=cur_inst.full_instruction

                cur_inst.exe_state="ID1" 
                
                #记录指令各个状态完成的时间 为后续记分牌的显示做准备
                cur_inst.update_inst_exe_record("Issu",self.glb_clk_cycle+1)
                return "next_inst_state_go_IF"#return info
                
        elif cur_inst.exe_state=="ID1":# instruction at state ID1   
            #根据tobe_write的列表判断是读写相关(WAR)还是写读相关(RAW) 如果是读写相关，那么
            #本状态可以读 如果是写读相关 那么就得等
            is_RAW=False
            for i in src_reg1_inuse_old.tobe_write_inst_ID:
                if i<cur_inst.inst_ID:
                    is_RAW=True
                    
            for i in src_reg2_inuse_old.tobe_write_inst_ID:
                if i<cur_inst.inst_ID:
                    is_RAW=True    
                           
            if is_RAW:#确定是写读相关(RAW) 停止一个周期                
                return "" #keep instruction in ID1 state , do nothing to this instruction
            else:#可以执行
                cur_inst.exe_state="ID2"    
                if len(src_reg1_inuse_new.tobe_read_inst_ID)==1:
                    src_reg1_inuse_new.tobe_read=False
                src_reg1_inuse_new.tobe_read_inst_ID.remove(cur_inst.inst_ID)#remove ID from toberead_list
                
                if len(src_reg2_inuse_new.tobe_read_inst_ID)==1:
                    src_reg2_inuse_new.tobe_read=False
                src_reg2_inuse_new.tobe_read_inst_ID.remove(cur_inst.inst_ID)#remove ID from toberead_list
                
                #记录指令各个状态完成的时间 为后续记分牌的显示做准备
                cur_inst.update_inst_exe_record("Read_operand",self.glb_clk_cycle+1)
                return ""
        elif cur_inst.exe_state=="ID2":
            cur_inst.exe_state="EX0"
            return ""
            
        elif cur_inst.exe_state=="EX0":

            cur_inst.current_exe_cycles+=1

            if cur_inst.current_exe_cycles >= cur_inst.full_exe_cycles:
                cur_inst.exe_state="WB0"
                #记录指令各个状态完成的时间 为后续记分牌的显示做准备
                cur_inst.update_inst_exe_record("Exe_complete",self.glb_clk_cycle+1)
                return ""
            else:
                return ""                
                
        elif cur_inst.exe_state=="WB0": 
            #根据tobe_read的列表判断是读写相关(WAR)还是写读相关(RAW) 如果是写读相关，那么
            #本状态可以写 如果是读写相关(WAR) 那么就得等
            is_WAR=False
                
            for i in dst_reg_inuse_old.tobe_read_inst_ID:
                if i<cur_inst.inst_ID:
                    is_WAR=True
                    
            if is_WAR:
                return ""
            else:
                cur_inst.exe_state="FIN"                
                #clear all marks in reg          
                if len(dst_reg_inuse_new.tobe_write_inst_ID)==1:
                    dst_reg_inuse_new.tobe_write=False
                dst_reg_inuse_new.tobe_write_inst_ID.remove(cur_inst.inst_ID)

                #set realted FU
               
                fu_inuse_new.busy_inst_ID=-1
                fu_inuse_new.is_busy=False
                fu_inuse_new.op="No_opration"
                
                #记录指令各个状态完成的时间 为后续记分牌的显示做准备
                cur_inst.update_inst_exe_record("Write_back",self.glb_clk_cycle+1)
               
                return "instruction_fin" #this instruction has been executed     
        elif cur_inst.exe_state=="FIN":
            return "" #this instruction has been executed        
        else :
            print("ERROR 000 : unknow state of instruction")            
            input("process exit ")
            return None
    
    def instruction_state_parser(self):
        """
        对指令的状态进行解析 并修改相应的CPU资源状态
        """
        if self.glb_clk_cycle==0:
            #初次运行的准备
            #装载第一条指令
            self.inst_queue[0].exe_state="IF"
            #第一次复制fu的状态
            self.old_state_fu_group=self.copy_fu_group(self.fu_group)
            #第一次复制reg的状态
            self.old_state_reg_group=self.copy_reg_group(self.reg_group)
            #首次设置运行返回信息为空
            self.info="next_inst_state_go_IF"
            self.load_new_inst=True
            self.IF_empty=False
            self.to_load_inst=0
        else :
            
            # 下面是一个时钟周期内所有指令的检索
            #print(self.load_new_inst)
            #print(self.IF_empty)
            
            if self.load_new_inst and (self.to_load_inst<self.inst_queue_len):
                self.inst_queue[self.to_load_inst].exe_state="IF"
                self.to_load_inst+=1
                self.load_new_inst=False
            
            for instruction in self.inst_queue:
                #保存旧的fu状态 保证不会因为指令序列的顺序引发逻辑上的错误
                #在进行指令状态转移时 所有的指令都要参考的状态是old_fu_list
                #修改时修改的是fu_group
                #然后每次在所有指令的状态更新完成后 最后再更新self.old_state_fu_group
                self.info=self.change_instruction_state(instruction)   
                if self.info=="next_inst_state_go_IF":
                    self.IF_empty=True 
                #更新旧的状态至新的状态
            if self.IF_empty==True:            
                self.load_new_inst=True 
            else :
                self.load_new_inst=False
            self.IF_empty=False

            
            #更新最新状态至旧的状态中 作为下一个时钟周期的参考    
            self.old_state_fu_group=self.copy_fu_group(self.fu_group)       
            self.old_state_reg_group=self.copy_reg_group(self.reg_group)

            #在迭代完成所有的指令后判断是否所有的指令状态都为FIN 若是则返回进程退出指令
            process_terminate_flag=True 
            for instruction in self.inst_queue:
                if instruction.exe_state!="FIN":
                    process_terminate_flag=False 
            if process_terminate_flag:
                return "Terminate"
            else :
                return "Continue"
    
    def clock_cycle(self): 
        if len(self.inst_queue)==0:
            return "empty_inst_queue"
    
        run_state=self.instruction_state_parser()

        #self.debug_print_inst_queue(show_inst_queue=True,show_fu_group=True)
        
        self.glb_clk_cycle+=1
       
        return run_state
    
    def cpu_run(self):
        while True:
            run_state=self.clock_cycle()
            #disp
            states=self.get_CPU_inner_state()
            self.debug_disp_3_table(states)
            #disp
            print("DEBUG:--------at clock %d cycles--------" % (self.glb_clk_cycle))
            input("1 clock Pause")
            if run_state=="Terminate":
                print("DEBUG all instruction has been executed")
                break 
    
    def get_CPU_inner_state(self):
        fu_state=[]
        for i in self.fu_group:
            tmp={}
            tmp["type"]=i.fu_type
            tmp["busy"]="Yes" if i.is_busy else "No"
            if i.busy_inst_ID!=-1:#some instruction is running on fu
                Fu_instruction=self.inst_queue[i.busy_inst_ID].full_instruction
                tmp["Op"]=Fu_instruction.split()[0]
                tmp["Fi"]=Fu_instruction.split()[1]
                tmp["Fj"]=Fu_instruction.split()[2]
                tmp["Fk"]=Fu_instruction.split()[3]
                
                #从指令对应的字符串中获取寄存器的类型以及索引1
                src_reg_j_index=Instruction.convert_str_to_wiget(None,tmp["Fj"])
                src_reg_k_index=Instruction.convert_str_to_wiget(None,tmp["Fk"])
                
                #根据上一步获取的索引来获取对应的寄存器对象
                src_reg_j=self.get_reg_obj(reg_type=src_reg_j_index["type"],reg_index=src_reg_j_index["index"],which="new")
                src_reg_k=self.get_reg_obj(reg_type=src_reg_k_index["type"],reg_index=src_reg_k_index["index"],which="new")
                
                #从对应的寄存器对象中获取相关的信息
                reg_j_busy_id=src_reg_j.get_writing_inst_ID()
                reg_k_busy_id=src_reg_k.get_writing_inst_ID()
                
                if reg_j_busy_id!=-1:
                    tmp["Qj"]=self.inst_queue[reg_j_busy_id].full_instruction.split()[0]
                    if i.busy_inst_ID<reg_j_busy_id:
                        tmp["Rj"]="Yes"
                    else:
                        tmp["Rj"]="No"
                else :
                    tmp["Qj"]=" "
                    tmp["Rj"]="Yes"
                if reg_k_busy_id!=-1:
                    tmp["Qk"]=self.inst_queue[reg_k_busy_id].full_instruction.split()[0] 
                    if i.busy_inst_ID<reg_k_busy_id:
                        tmp["Rk"]="Yes"
                    else:
                        tmp["Rk"]="No"
                else :
                    tmp["Qk"]=" "
                    tmp["Rk"]="Yes"
                    
            else:
                tmp["Op"]=" "
                tmp["Fi"]=" "
                tmp["Fj"]=" "
                tmp["Fk"]=" "
                tmp["Qj"]=" "
                tmp["Qk"]=" "
                tmp["Rj"]=" "
                tmp["Rk"]=" "
            
            fu_state.append(tmp)
        #获取指令执行步骤状态
        inst_state=[]
       
        for inst in self.inst_queue:
            tmp={}
            tmp["name"]=inst.full_instruction
            tmp["Issu"]=inst.Issu
            tmp["Read_operand"]=inst.Read_operand
            tmp["Exe_complete"]=inst.Exe_complete
            tmp["Write_back"]=inst.Write_back
            inst_state.append(tmp)
        #获取寄存器占用状态
        reg_state=[]
        for reg in self.reg_group:
            tmp={}
            busy_id=reg.get_writing_inst_ID()
            tmp["name"]=("R" if reg.reg_type=="int" else "F")+str(reg.reg_index_in_type)
            if busy_id!=-1:
                tmp["fu"]=self.inst_queue[busy_id].fu["type"]+str(self.inst_queue[busy_id].fu["index"])
            else:
                tmp["fu"]=" "
            reg_state.append(tmp)
        
        return (fu_state,inst_state,reg_state)      
    
    def debug_print_inst_queue(self,show_inst_queue=False,show_fu_group=False,show_reg_group=False):
        print("---------debug show begin---------")
        if show_inst_queue:
            print("***instruction state below***")
            print("instruction          | state | cur_cycles | full_cycles ")
            for i in self.inst_queue:
                print("------------------------")
                print(i.full_instruction,"|",i.exe_state,"|",i.current_exe_cycles,"      |",i.full_exe_cycles)
                #print("state:",i.exe_state)
                #print("fu:",i.fu)
                ##print("dst_reg",i.dst_reg)
                ##print("src_reg1",i.src_reg1)
                ##print("src_reg2",i.src_reg2)
                #print("cur_cycles",i.current_exe_cycles)
                #print("full_cycles",i.full_exe_cycles)
                
        if  show_fu_group:                
            print("***fu state below***")
            print("fu_name|"," busy | ","inst_id")
            for i in self.fu_group:
                print("------------------------")                
                print(i.fu_type,i.is_busy,i.busy_inst_ID)
                
            print("***reg state below ***")     
        
        if show_reg_group:
            for i in self.reg_group:
                pass
                #print("reg_name:",i.reg_type,i.reg_index_in_type)
                print("reg_read_inst_ID",i.tobe_read_inst_ID)            
                print("reg_write_inst_ID",i.tobe_write_inst_ID)            
            
        print("*****debug show end*******")

    
    def debug_disp_3_table(self,states):
        """
            显示算法所需要的三个表格
        """
        print("Instruction state table")
        print("---------------------------------------------------")
        print("INst Name | Issu  | Read_op | Exe_complete |  WB  |")
        for inst_state in states[1]:
            print(inst_state["name"]," | ",inst_state["Issu"]," | ",
            inst_state["Read_operand"]," | ",inst_state["Exe_complete"]," | ",
            inst_state["Write_back"])
        
        print("---------------------------------------------------")
        print("Fu state table")
        print("---------------------------------------------------")
        print("Fu Name    | Busy    |  Op   |   Fi    |   Fj    |    Fk   |   Qj   |   Qk   |   Rj  |   Rk  |")    
        for i in states[0]:
            print(i["type"],"  |  ",i["busy"],"   |  ",i["Op"],"   |  " ,i["Fi"],"   |  ",i["Fj"],"   |  ",i["Fk"],"   |  ",i["Qj"],"   |  ",i["Qk"],"   |  ",i["Rj"],"   |  ",i["Rk"],"   |   ")
        
        print("---------------------------------------------------")
        print("reg state table")
        print("---------------------------------------------------")
        print("reg Name | Fu |")
        print("---------------------------------------------------")
        for i in states[2]:    
            print(i["name"],i["fu"])
        print("---------------------------------------------------")
    
    
        
        
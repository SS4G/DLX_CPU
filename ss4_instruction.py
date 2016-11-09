# -*- coding: utf-8 -*-
class Instruction:
        def __init__(self,
            inst_ID=0                     ,
            full_instruction="LD F1 M0 R1",
            exe_state="UN_LOAD"           ,
            full_exe_cycles=10            ,
            current_exe_cycles=0          ,
            fu="alu_add" ,
            dst_reg= "F0",
            src_reg1="F0",
            src_reg2="F0"                 
        ):
            #指令自有变量
            self.inst_ID=inst_ID #指令的唯一标号
            self.full_instruction=full_instruction#源文件中的原始指令
            self.exe_state=exe_state#执行状态 
            #UN_LOAD(未执行) 
            #IF (已取指) 
            #ID1(已发射到功能部件等待操作数) 
            #ID2(已等到所有操作数待执行) 
            #EX0(正在执行)
            #WB0(已达到执行周期表明已经执行完毕等待写回)
            #FIN(执行完毕 可以从指令状态表中清除)
            self.full_exe_cycles=full_exe_cycles#完成EX步骤所需要的总的周期数
            self.current_exe_cycles=current_exe_cycles#当前已经执行的周期
            
            #记分牌相关变量
            
            self.fu=self.convert_str_to_wiget(fu) #需要使用的功能部件            
            self.dst_reg=self.convert_str_to_wiget(dst_reg) #结果的目标寄存器
            #type tuple (type,in_type_index)
            
            self.src_reg1=self.convert_str_to_wiget(src_reg1)#操作数寄存器1
            self.src_reg2=self.convert_str_to_wiget(src_reg2)#操作数寄存器2
            
            #执行状态记录 用来记录每条指令执行完成的周期
            self.Issu=-1
            self.Read_operand=-1 
            self.Exe_complete=-1
            self.Write_back=-1 
        
        def update_inst_exe_record(self,update_to_state,cur_clk):
            if update_to_state=="Issu":
                self.Issu=cur_clk
            elif update_to_state=="Read_operand":
                self.Read_operand=cur_clk
            elif update_to_state=="Exe_complete":
                self.Exe_complete=cur_clk
            elif update_to_state=="Write_back":
                self.Write_back=cur_clk
            else:
                input("ERROR 003 : unknow state Pause")
            
                        
            
            
        def show(self):
            print("-----An instructio------")
            print("inst_ID:",self.inst_ID)
            print("full_instruction:",self.full_instruction)
            print("exe_state:",self.exe_state)         
            print("full_exe_cycles:",self.full_exe_cycles)            
            print("current_exe_cycles:",self.current_exe_cycles)          
            print("fu:",self.fu)           
            print("dst_reg:",self.dst_reg)                  
            print("src_reg1:",self.src_reg1)                
            print("src_reg2:",self.src_reg2) 
        
        def convert_str_to_wiget(self,str0):
            fu_list=["alu_add","alu_add","alu_mul","alu_mul","alu_div","ld_unit","st_unit"]
            if str0 in fu_list :
                return {"type":str0,"index":0}# in this version the one type fu is only 1 entity
            elif "F" in str0:
                return {"type":"float","index":int(str0[1:])}
            elif ("R" in str0) or ("M" in str0):    
                return {"type":"int","index":int(str0[1:])}
        
        
        
        
        
        
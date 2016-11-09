# gui  shell of project
import tkinter as tk
from functools import partial as pto
from ss4_CPU import *

class GUI_shell:
    def __init__(self):
        self.SUPPORTED_MAX_INSTRUCTIONS=10 #显示支持的最大的指令数
        self.CPU_SINGLE_TYPE_REG_NUMBER=10
        self.history_clock=-1
        self.cpu_inner_state_history=[]
        print("main execute")
        self.cpu=CPU()
        
    def write_lable(self,lable_obj=None,content_str=" ",forground_color="black"):
        lable_obj.config(text=content_str)
    
    def creat_std_lable(self,top=None,fg="black",bg="white",height=1,width=15,text=" ",x_pos=0,y_pos=0,style_type=0,defaut_style=False):  
        
        if style_type==0:
            fg='black'
            bg='gray'
        elif style_type==1:
            fg='green'
            bg='white'
        elif style_type==2:
            fg='black'
            bg='gray'
        elif style_type==3:
            fg='red'
            bg='white'
        elif style_type==4:
            fg='black'
            bg='gray'
        elif style_type==5:
            fg='blue'
            bg='white'

        if not defaut_style:
            tmp=tk.Label(top,height = height,width = width,relief="ridge",borderwidth=3,
                    #文本
                    text = text,
                    font = 'Consolas -12 ',
                    background=bg,
                    foreground = fg,
                    )
            tmp.grid(row=y_pos,column=x_pos)         
            return tmp
        else:
            tmp=tk.Label(top,height = height,width = width,
                    #文本
                    text = text,
                    font = 'Consolas -12 ',
                    )
            tmp.grid(row=y_pos,column=x_pos)         
            return tmp
    
    def init_table_in_grids(self):
        #inst_tlb_y_offset=0 #inst tlb length=14
        #reg_state_y_offset=23 #reg_state_length=7
        #fu_state_y_offset=14  #fu_state_length=9
        
        self.inst_tlb_y_offset=0 #inst tlb length=14
        self.reg_state_y_offset=14 #reg_state_length=7
        self.fu_state_y_offset=21  #fu_state_length=9       
        
        inst_tlb_y_offset =self.inst_tlb_y_offset
        reg_state_y_offset=self.reg_state_y_offset
        fu_state_y_offset =self.fu_state_y_offset
        
        self.top = tk.Tk()
        
        #creat instruction statue table 
        self.inst_tlb_title=      self.creat_std_lable(top=self.top,text="记分牌算法",x_pos=0,y_pos=inst_tlb_y_offset+0,defaut_style=True)
        self.inst_tlb_title=      self.creat_std_lable(top=self.top,text="指令状态",x_pos=0,y_pos=inst_tlb_y_offset+1,defaut_style=True)
        self.inst_tlb_item=[]                         
        self.inst_tlb_item.append(self.creat_std_lable(top=self.top,text="name",        x_pos=0,y_pos=inst_tlb_y_offset+2,style_type=0))
        self.inst_tlb_item.append(self.creat_std_lable(top=self.top,text="Issu",        x_pos=1,y_pos=inst_tlb_y_offset+2,style_type=0))
        self.inst_tlb_item.append(self.creat_std_lable(top=self.top,text="Read_oprand", x_pos=2,y_pos=inst_tlb_y_offset+2,style_type=0))
        self.inst_tlb_item.append(self.creat_std_lable(top=self.top,text="Exe_complete",x_pos=3,y_pos=inst_tlb_y_offset+2,style_type=0))
        self.inst_tlb_item.append(self.creat_std_lable(top=self.top,text="Write_back",  x_pos=4,y_pos=inst_tlb_y_offset+2,style_type=0))
        
        #存储所有指令栅格的列表
        self.all_inst=[]
        #eg :all_inst[0][1] 列表的第一行第二列
        for i in range(10):
            one_inst_items=[]
            for j in range(5):
                one_inst_items.append(self.creat_std_lable(top=self.top,text="   ",x_pos=j,y_pos=i+inst_tlb_y_offset+3,style_type=1))
            self.all_inst.append(one_inst_items)    
        
        #
        self.emptyline0=        self.creat_std_lable(top=self.top,text="     ",       x_pos=0,y_pos=inst_tlb_y_offset+13,defaut_style=True)
        self.fu_tlb_title=      self.creat_std_lable(top=self.top,text="功能单元状态",x_pos=0,y_pos=fu_state_y_offset+0,defaut_style=True)
        self.fu_tlb_item=[]     
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Fu_name",          x_pos=0,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Busy",             x_pos=1,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Operation",        x_pos=2,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Fi(dst)",          x_pos=3,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Fj(src1)",         x_pos=4,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Fk(src2)",         x_pos=5,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Qj",               x_pos=6,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Qk",               x_pos=7,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Rj(src1_ready)",   x_pos=8,y_pos=fu_state_y_offset+1,style_type=2))
        self.fu_tlb_item.append(self.creat_std_lable(top=self.top,text="Rk(src2_ready)",   x_pos=9,y_pos=fu_state_y_offset+1,style_type=2))
        
        #fu条目构成的列表
        self.all_fu=[]
        for i in range(5):
            one_fu_items=[]
            for j in range(10):
                one_fu_items.append(self.creat_std_lable(top=self.top,text="   ",x_pos=j,y_pos=i+fu_state_y_offset+2,style_type=3))
            self.all_fu.append(one_fu_items)    
        #print(self.all_fu)
        
        self.emptyline1=self.creat_std_lable(top=self.top,text="     ",       x_pos=0,y_pos=fu_state_y_offset+7,defaut_style=True)
        self.emptyline2=self.creat_std_lable(top=self.top,text="     ",       x_pos=0,y_pos=fu_state_y_offset+8,defaut_style=True)
        
        self.reg_r_tlb_title=self.creat_std_lable(top=self.top,text="寄存器状态",x_pos=0,y_pos=reg_state_y_offset+0,defaut_style=True)
        
        #整数型寄存器构成的列表 横向排列 该列表是一维列表
        self.reg_r_item=[]
        self.reg_r_name=[]
        for i in range(self.CPU_SINGLE_TYPE_REG_NUMBER):
            self.reg_r_name.append(self.creat_std_lable(top=self.top,text="R"+str(i),x_pos=i,y_pos=reg_state_y_offset+1,style_type=4))
        for i in range(self.CPU_SINGLE_TYPE_REG_NUMBER):
            self.reg_r_item.append(self.creat_std_lable(top=self.top,text="   ",x_pos=i,y_pos=reg_state_y_offset+2,style_type=5))
        
        #浮点型寄存器构成的列表 横向排列 该列表是一维列表
        self.reg_f_item=[]
        self.reg_f_name=[]
        for i in range(self.CPU_SINGLE_TYPE_REG_NUMBER):
            self.reg_f_name.append(self.creat_std_lable(top=self.top,text="F"+str(i),x_pos=i,y_pos=reg_state_y_offset+3,style_type=4))
        for i in range(self.CPU_SINGLE_TYPE_REG_NUMBER):
            self.reg_f_item.append(self.creat_std_lable(top=self.top,text="   ",x_pos=i,y_pos=reg_state_y_offset+4,style_type=5))
        
        self.blank0=self.creat_std_lable(top=self.top,text="   ",x_pos=10,y_pos=reg_state_y_offset+5,defaut_style=True)
        self.blank1=self.creat_std_lable(top=self.top,text="   ",x_pos=10,y_pos=reg_state_y_offset+6,defaut_style=True)
        self.clock=self.creat_std_lable(top=self.top,text="0 clock_cycles"  ,x_pos=10,y_pos=inst_tlb_y_offset+1,defaut_style=True)
        self.exit_mention0=self.creat_std_lable(top=self.top,text="   "     ,x_pos=7 ,y_pos=inst_tlb_y_offset+3,defaut_style=True)
        self.exit_mention1=self.creat_std_lable(top=self.top,text="   "     ,x_pos=8 ,y_pos=inst_tlb_y_offset+3,defaut_style=True)
        self.exit_mention2=self.creat_std_lable(top=self.top,text="   "     ,x_pos=9 ,y_pos=inst_tlb_y_offset+3,defaut_style=True)
    
    def write_cpu_inner_state_to_gui(self,states):
        """
            将获取的CPU的内部状态映射到图形化的表格中
        """
          
        #all_inst=[]
        #all_fu=[]
        
        inst_index=0
        for inst_state in states[1]:
            self.write_lable(self.all_inst[inst_index][0]," " if inst_state["name"]        ==-1 else str(inst_state["name"]        ))
            self.write_lable(self.all_inst[inst_index][1]," " if inst_state["Issu"]        ==-1 else str(inst_state["Issu"]        ))
            self.write_lable(self.all_inst[inst_index][2]," " if inst_state["Read_operand"]==-1 else str(inst_state["Read_operand"]))
            self.write_lable(self.all_inst[inst_index][3]," " if inst_state["Exe_complete"]==-1 else str(inst_state["Exe_complete"]))
            self.write_lable(self.all_inst[inst_index][4]," " if inst_state["Write_back"]  ==-1 else str(inst_state["Write_back"]  ))
            inst_index+=1
        
        fu_index=0         
        for fu_state in states[0]:
            self.write_lable(self.all_fu[fu_index][0],str(fu_state["type"]))
            self.write_lable(self.all_fu[fu_index][1],str(fu_state["busy"]))
            self.write_lable(self.all_fu[fu_index][2],str(fu_state["Op"]  ))
            self.write_lable(self.all_fu[fu_index][3],str(fu_state["Fi"]  ))
            self.write_lable(self.all_fu[fu_index][4],str(fu_state["Fj"]  ))
            self.write_lable(self.all_fu[fu_index][5],str(fu_state["Fk"]  ))
            self.write_lable(self.all_fu[fu_index][6],str(fu_state["Qj"]  ))
            self.write_lable(self.all_fu[fu_index][7],str(fu_state["Qk"]  ))
            self.write_lable(self.all_fu[fu_index][8],str(fu_state["Rj"]  ))
            self.write_lable(self.all_fu[fu_index][9],str(fu_state["Rk"]  ))
            
            
            fu_index+=1

        r_reg_index=0
        for r_reg in states[2][0:self.CPU_SINGLE_TYPE_REG_NUMBER]:
            self.write_lable(self.reg_r_item[r_reg_index],str(r_reg["fu"]))
            r_reg_index+=1
            
        f_reg_index=0    
        for f_reg in states[2][self.CPU_SINGLE_TYPE_REG_NUMBER:2*self.CPU_SINGLE_TYPE_REG_NUMBER]:
            self.write_lable(self.reg_f_item[f_reg_index],str(f_reg["fu"]))
            f_reg_index+=1
    
    def flush_table(self):
        """
            将获取的CPU的内部状态映射到图形化的表格中
        """

        for i in range(10):
            self.write_lable(self.all_inst[i][0]," ")
            self.write_lable(self.all_inst[i][1]," ")
            self.write_lable(self.all_inst[i][2]," ")
            self.write_lable(self.all_inst[i][3]," ")
            self.write_lable(self.all_inst[i][4]," ")
        
         
        for i in range(5):
            self.write_lable(self.all_fu[i][0],"  ")
            self.write_lable(self.all_fu[i][1],"  ")
            self.write_lable(self.all_fu[i][2],"  ")
            self.write_lable(self.all_fu[i][3],"  ")
            self.write_lable(self.all_fu[i][4],"  ")
            self.write_lable(self.all_fu[i][5],"  ")
            self.write_lable(self.all_fu[i][6],"  ")
            self.write_lable(self.all_fu[i][7],"  ")
            self.write_lable(self.all_fu[i][8],"  ")
            self.write_lable(self.all_fu[i][9],"  ")

        r_reg_index=0
        for r_reg in range(self.CPU_SINGLE_TYPE_REG_NUMBER):
            self.write_lable(self.reg_r_item[i],"  ")
            r_reg_index+=1
            
        f_reg_index=0    
        for f_reg in range(self.CPU_SINGLE_TYPE_REG_NUMBER):
            self.write_lable(self.reg_f_item[f_reg_index],"  ")
            f_reg_index+=1
    
    def run_GUI_shell_loop(self):
        
        self.init_table_in_grids()
        
        ##设置下一步按钮
        #self.btn_next=tk.Button(self.top,height=1,width=15,text="next",font = 'Consolas -12 ',
        #fg="red",bg="yellow",
        #command=self.update,relief="ridge",borderwidth=1)
        #self.btn_next.grid(row=self.inst_tlb_y_offset+2,column=10)
        
        #设置下一步按钮
        self.btn_next=tk.Button(self.top,height=1,width=15,text="next",font = 'Consolas -12 ',
        fg="red",bg="yellow",
        command=self.next_cycle,relief="ridge",borderwidth=1)
        self.btn_next.grid(row=self.inst_tlb_y_offset+2,column=10)
        
        #设置下一步按钮
        self.btn_last=tk.Button(self.top,height=1,width=15,text="last",font = 'Consolas -12 ',
        fg="red",bg="yellow",
        command=self.last_cycle,relief="ridge",borderwidth=1)
        self.btn_last.grid(row=self.inst_tlb_y_offset+3,column=10)
        
        #设置复位按钮
        self.btn_reset=tk.Button(self.top,height=1,width=15,text="reset",font = 'Consolas -12 ',
        fg="green",bg="yellow",
        command=self.reset_system,relief="ridge",borderwidth=1)
        self.btn_reset.grid(row=self.inst_tlb_y_offset++4,column=10)
        
        #设置退出按钮
        self.btn_reset=tk.Button(self.top,height=1,width=15,text="exit",font = 'Consolas -12 ',
        fg="blue",bg="yellow",
        command=self.top.quit,relief="ridge",borderwidth=1)
        self.btn_reset.grid(row=self.inst_tlb_y_offset+6,column=10)
        
        self.btn_input=tk.Button(self.top,height=1,width=15,text="input code",font = 'Consolas -12 ',
        fg="blue",bg="yellow",
        command=self.input_src_code,relief="ridge",borderwidth=1)
        self.btn_input.grid(row=self.inst_tlb_y_offset+8,column=10)
        
        self.reset_system()
        #
        self.top.mainloop()
        print("Process terminate successfully!!")
    
    def reset_system(self):
        self.history_clock=-1
        self.cpu_inner_state_history=[]
        self.cpu=CPU()
        self.flush_table()
        cpu_inner_states=self.cpu.get_CPU_inner_state()
        self.write_cpu_inner_state_to_gui(cpu_inner_states)
        self.write_lable(self.clock,str(self.cpu.glb_clk_cycle)+" cycles",forground_color="green")
        self.write_lable(self.exit_mention0," ",forground_color="red")
        self.write_lable(self.exit_mention1," ",forground_color="red")
        self.write_lable(self.exit_mention2," ",forground_color="red")
        while True:
            run_state=self.cpu.clock_cycle()
            if run_state=="empty_inst_queue":
                self.write_lable(self.exit_mention0,"         No",forground_color="red")
                self.write_lable(self.exit_mention1,"Instruction!",forground_color="red")
                self.write_lable(self.exit_mention2,"Please input!",forground_color="red")
                return 
            elif run_state=="Terminate":
                cpu_inner_states=self.cpu.get_CPU_inner_state()
                self.cpu_inner_state_history.append(cpu_inner_states)
                break
            else:
                cpu_inner_states=self.cpu.get_CPU_inner_state()
                self.cpu_inner_state_history.append(cpu_inner_states)
      
    def update(self):
        #run_state=self.cpu.clock_cycle()
        #if run_state=="empty_inst_queue":
        #    self.write_lable(self.exit_mention0,"         No",forground_color="red")
        #    self.write_lable(self.exit_mention1,"Instruction!",forground_color="red")
        #    self.write_lable(self.exit_mention2,"Please input!",forground_color="red")
        #    return None
        #
        #
        #cpu_inner_states=self.cpu.get_CPU_inner_state()
        #
        #if run_state=="Terminate":
        #    self.write_lable(self.exit_mention0,"no more ",forground_color="red")
        #    self.write_lable(self.exit_mention1,"Instruction!",forground_color="red")
        #    self.write_lable(self.exit_mention2,"Press reset!",forground_color="red")
        #    self.write_cpu_inner_state_to_gui(cpu_inner_states)
        #else:   
        #    self.write_cpu_inner_state_to_gui(cpu_inner_states)
        #    self.write_lable(self.clock,str(self.cpu.glb_clk_cycle)+" cycles",forground_color="green")
        
        self.write_cpu_inner_state_to_gui(self.cpu_inner_state_history[self.history_clock])    
        self.write_lable(self.clock,str(self.history_clock)+" cycles")
        self.history_clock+=1
            
    def next_cycle(self):
        if self.history_clock<len(self.cpu_inner_state_history)-1:
            self.history_clock+=1
            self.write_cpu_inner_state_to_gui(self.cpu_inner_state_history[self.history_clock])    
            self.write_lable(self.clock,str(self.history_clock)+" cycles")
            
        else:
            self.write_lable(self.exit_mention0,"no more ",forground_color="red")
            self.write_lable(self.exit_mention1,"Instruction!",forground_color="red")
            self.write_lable(self.exit_mention2,"Press reset!",forground_color="red")
         
    def last_cycle(self):
        if self.history_clock>0:
            self.history_clock-=1
            self.write_cpu_inner_state_to_gui(self.cpu_inner_state_history[self.history_clock])    
            self.write_lable(self.clock,str(self.history_clock)+" cycles")
        else:
            self.write_lable(self.exit_mention0,"no previous",forground_color="red")
            self.write_lable(self.exit_mention1,"Instruction!",forground_color="red")
            self.write_lable(self.exit_mention2,"Press reset!",forground_color="red")
       
    def input_src_code(self):
        self.top2=tk.Tk()
        self.label_title=tk.Label(self.top2,height=1,width=40,text="input your instruction below:",font = 'Consolas -12 ',relief="ridge",borderwidth=1)          
        
        self.label_title.pack()
        self.ent_list=[]
        for i in range(10):
            self.ent_list.append(tk.Entry(self.top2,width=40))
        for i in range(10):
            self.ent_list[i].pack()
            
        self.btn_save=tk.Button(self.top2,height=1,width=15,text="save",font = 'Consolas -12 ',fg="blue",bg="yellow",
        command=self.save,relief="ridge",borderwidth=1)
        self.label_save=tk.Label(self.top2,height=1,width=40,text="   ",font = 'Consolas -12 ',relief="ridge",borderwidth=1)          

        self.btn_save.pack()
        self.label_save.pack()
        
        self.top2.mainloop()
    
    def save(self):
        lines=[]
        for i in self.ent_list:
            lines.append(i.get())
        
        false_flag=False
        for line in lines:
            if self.line_check(line)==False:
                self.label_save.config(text="syntax Error!")
                false_flag=True
                break 
        if not false_flag:
            self.rewrite_src(lines)
            self.label_save.config(text="save complete!")
             
    def rewrite_src(self,lines):
        try :
            f=open(os.getcwd()+"\src.s","w")
            for i in lines:
                f.write(i+"\n")
                print("rewrite file finished!")
        except FileNotFoundError:
            print("assmble languange source file not found")
                        
    def line_check(self,line):
        """
            return True if the line is legal
            else return  False 
        """
        inst_set_list=[]
        reg_name_list=[]
        for name in self.cpu.inst_set:
            inst_set_list.append(name)
        for reg in self.cpu.reg_group:
            reg_name_list.append(reg.reg_name)
        if line == "":
            return True
        line_list=line.split()
        
        if len(line_list)!=4:
            return False
        else:
            if line_list[0] not in inst_set_list:
                return False 
            elif (line_list[1] not in reg_name_list) or (line_list[2] not in reg_name_list) or (line_list[3] not in reg_name_list):
                return False
            else :
                return True
            
gui=GUI_shell()
gui.run_GUI_shell_loop()

print("process end")



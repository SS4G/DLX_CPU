class Fu:
    def __init__(self,fu_type="No_type",fu_index_in_type=0):
        self.fu_type=fu_type
        self.fu_index_in_type=fu_index_in_type
        self.is_busy=False
        self.busy_inst_ID=-1# 指明是那一条指令占用了该FU
        self.op="No_op"
        self.dst_r="No_r"
        self.src_r1="No_r"
        self.src_r2="No_r"
        self.fu_for_s1="No_FU"       
        self.fu_for_s2="No_FU"
        self.s1_is_ready=True
        self.s2_is_ready=True 
class Reg:
    def __init__(self,reg_type="No_type",reg_index_in_type=0):
        self.reg_type=reg_type#int or float or mem or imm
        #mem is  memory ,imm is  offset 
        self.reg_index_in_type=reg_index_in_type
        self.reg_name=("R" if self.reg_type=="int" else "F")+str(reg_index_in_type)

        self.tobe_read=False
        self.tobe_read_inst_ID=[]
        self.tobe_write=False
        self.tobe_write_inst_ID=[]
        
    def get_writing_inst_ID(self):
        if self.tobe_write_inst_ID==[]:
            return -1 
        else :
            return min(self.tobe_write_inst_ID)
     
        
    def show_reg(self):
        print("name=",self.reg_type,"index=",self.reg_index_in_type)
        print("tobe_write",self.tobe_write_inst_ID)
        print("tobe_read",self.tobe_read_inst_ID)
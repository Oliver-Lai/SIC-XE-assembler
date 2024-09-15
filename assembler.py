import json
with open('optable.json') as f:
    optab = json.load(f)
path = 'Figure2.15.txt'
path_w = 'Figure2.16.txt'
path_t = 'Figure2.16_t.txt'
f_w = open(path_w,'w')
f = open(path, 'r')
cs_sympt = {"global_var":[]}
cs = 0
#Pass 1
while True:
        file_eof = f.readline()
        if('.' in file_eof):
            f_w.write("\t\t%s"%file_eof)
            continue
        if file_eof == "":
            print("PASS 1 Done!")
            break
        a = file_eof.split()
        if("START" in a):
            #初始化critical section 的內容
            sympt = {} 
            locc = int(a[2])
            littpool = []
            sympt.update({a[0]:locc})
            f_w.write("%.4x\t%s"%(locc,file_eof))
        if(len(a)==3):
            #處理START
            if(a[1]=="EQU"):
                if(a[2]=="*"):      #處理*代表loc
                    sympt.update({a[0]:locc})
                    f_w.write("%.4x\t%s"%(locc,file_eof))
                else:
                    express = [a[2]]
                    if("+"in a[2]):
                        express = a[2].split("+")
                        i = 0
                        for x in express:
                            if(x in sympt.keys()):
                                express[i] = sympt[x]
                                i += 1
                            else:
                                i+=1
                    j=0
                    for x in express:
                        if("-"in x):
                            x = x.split("-")
                            i = 0
                            for c in x:
                                if(c in sympt.keys()):
                                    if(i==0):
                                        x[i] = sympt[c]
                                        i += 1
                                    else:
                                        x[i] = -sympt[c]
                                        i += 1
                            express[j] = x
                        j+=1
                    sum = 0
                    for x in express[0]:
                        sum += x
                    sympt.update({a[0]:sum})
                    f_w.write("%.4x\t%s"%(sum,file_eof))
                continue
            elif(a[1]=="RESW"):
                sympt.update({a[0]:locc})
                f_w.write("%.4X\t%s"%(locc,file_eof))
                locc += 3 * int(a[2])
            elif(a[1]=="RESB"):
                sympt.update({a[0]:locc})
                f_w.write("%.4X\t%s"%(locc,file_eof))
                locc += 1 * int(a[2])
            elif(a[1]=="BYTE"):
                f_w.write("%.4X\t%s"%(locc,file_eof))
                sympt.update({a[0]:locc})
                if(a[2][0]=='X'):
                    locc += len(a[2][2:-1])//2
                elif(a[2][0]=='C'):
                    locc += len(a[2][2:-1])
            elif(a[1]=="WORD"):
                f_w.write("%.4X\t%s"%(locc,file_eof))
                sympt.update({a[0]:locc})
                locc += 3
            elif(a[1].replace("+","") in optab.keys()):
                f_w.write("%.4X\t%s"%(locc,file_eof))
                sympt.update({a[0]:locc})
                if(optab[a[1].replace("+", "")][1]==2):
                    locc += 2
                elif(optab[a[1].replace("+", "")][1]==3):
                    if(a[2][0]=="="):
                        littpool.append(a[2])
                    if(a[1][0]=="+"):
                        locc += 4
                    else:
                        locc += 3



        if(len(a)==2):
            if(a[0]=="EXTREF"):
                #將要引用外部的變數放入symblotable
                EXTREF_list = a[1].split(",")
                sympt.update({"EXTREF":EXTREF_list})
                f_w.write("\t\t%s"%file_eof)
            elif(a[0]=="EXTDEF"):
                #將對外部共用的變數放到global_var裡
                exdef_list = a[1].split(",")
                cs_sympt["global_var"].append(exdef_list)
                f_w.write("\t\t%s"%file_eof)
            elif(a[1]=="CSECT"):
                #初始化critical section 的內容
                sympt.update({"Totallen":locc})
                cs_sympt.update({str(cs):sympt})
                cs += 1
                sympt = {}
                locc = 0
                littpool = []
                sympt.update({a[0]:locc})
                f_w.write("%.4X\t%s"%(locc,file_eof))
            elif(a[0]=="END"): 
                f_w.write("\t\t%s\n"%file_eof)
                #處理還沒宣告littpool裡的變數
                if(littpool!=None):
                    for x in set(littpool):
                        if(x[1]=="C"):
                            f_w.write("%.4X\t*\t\t%s\n"%(locc,x))
                            sympt.update({x:locc})
                            locc += len(x)-4
                        elif(x[1]=="X"):
                            f_w.write("%.4X\t*\t\t%s\n"%(locc,x))
                            sympt.update({x:locc})
                            locc += 1
                    littpool = []
                    sympt.update({"Totallen":locc})
                    cs_sympt.update({str(cs):sympt})
            elif(a[0].replace("+", "") in optab.keys()):
                f_w.write("%.4X\t%s"%(locc,file_eof))
                if(optab[a[0].replace("+", "")][1]==2):
                    locc += 2
                elif(optab[a[0].replace("+", "")][1]==3):
                    if(a[1][0]=="="):
                        littpool.append(a[1])
                    if(a[0][0]=="+"):
                        locc += 4
                    else:
                        locc += 3
                elif(optab[a[1].replace("+", "")][1]==1):
                    locc += 1



        if(len(a)==1):
            if(a[0]=="LTORG"):
                f_w.write("\t\t%s"%file_eof)
                if(littpool!=None):
                    for x in set(littpool):
                        if(x[1]=="C"):
                            f_w.write("%.4X\t*\t\t%s\n"%(locc,x))
                            sympt.update({x:locc})
                            locc += len(x)-4
                        elif(x[1]=="X"):
                            f_w.write("%.4X\t*\t\t%s\n"%(locc,x))
                            sympt.update({x:locc})
                            locc += (len(x)-4)*3
                    littpool = []
            elif(a[0].replace("+","") in optab.keys()):
                f_w.write("%.4X\t%s"%(locc,file_eof))
                if(optab[a[0].replace("+", "")][1]==1):
                    locc += 1
                elif(optab[a[0].replace("+", "")][1]==2):
                    locc += 2
                else:
                    locc += 3
sytab = open("symtable.json","w")
json.dump(cs_sympt,sytab)      
sytab.close()
f.close()
f_w.close()


#Pass 2

def format4(opcode,sympt,n,i,x,var):
    opcode = optab[opcode.replace("+","")][0]
    tmp =int(opcode[1],16)
    tmp = "{0:b}".format(tmp)
    m = False
    if(len(tmp)<4):
        while(len(tmp)<4):
            tmp = "0%s"%tmp
    tmp = "%s%s%s"%(tmp[0:2],n,i)
    opcode = "%s%X"%(opcode[0],int(tmp,2))
    tmp = "%s001"%x
    opcode = "%s%X"%(opcode,int(tmp,2))
    if(var[0]=='#'):
        if(int(var[1:])==range(10)):
            opcode = "%s%.5X"%(opcode,(int(var[1:])))
            
        else:
            if(var[1:] in sympt["EXTREF"]):
                opcode = "%s00000"%(opcode)
                m = True
            else:
                opcode = "%s%.5X"%(opcode,hex(sympt[var[1:]]))
    else:
        if(var in sympt["EXTREF"]):
                opcode = "%s00000"%(opcode)
                m = True
        else:
            opcode = "%s%.3X"%(opcode,hex(sympt[var]))
    return opcode,m

def twos_complement(hex_num):
    b_num = bin(int(hex_num, 16))[2:]
    while(len(b_num)<12):
        b_num = "0%s"%b_num
    if b_num[0] == '1':
        b_num = bin(int(b_num, 2) - 1)[2:]
    inverted_num = ''.join('1' if bit == '0' else '0' for bit in b_num)
    decimal_num = int(inverted_num, 2)
    return decimal_num

def format3(opcode,loc,sympt,n,i,x,var,b=0):
    pc = loc + 3
    opcode = optab[opcode][0]
    tmp =int(opcode[1],16)
    tmp = "{0:b}".format(tmp)
    m = False
    if(len(tmp)<4):
        while(len(tmp)<4):
            tmp = "0%s"%tmp
    tmp = "%s%s%s"%(tmp[0:2],n,i)
    opcode = "%s%X"%(opcode[0],int(tmp,2))
    if(var[0]=='#'):
        tmp = "%s000"%x
    else:
        tmp = "%s010"%x
    opcode = "%s%X"%(opcode,int(tmp,2))
    if(var[0]=='#'):
        if(int(var[1:]) in range(10)):
            opcode = "%s%.3X"%(opcode,(int(var[1:])))
            
        else:
            if(var[1:] in sympt["EXTREF"]):
                opcode = "%s000"%(opcode)
                m = True
            else:
                opcode = "%s%.3X"%(opcode,hex(sympt[var[1:]]))
    else:
        if(var in sympt["EXTREF"]):
                opcode = "%s000"%(opcode)
                m = True
        else:
            num = sympt[var.replace("@","")]-pc
            if num<0:
                pc = twos_complement("%.2X"%pc)
                num = sympt[var.replace("@","")] + pc + 1
            opcode = "%s%.3X"%(opcode,num)
    return opcode,m
def format2(opcode,var):
    r_s = {'A':0,'X':1,'L':2,'B':3,'S':4,'T':5,'F':6}
    opcode = optab[opcode][0]
    if(","in var):
        var = var.split(",")
        for x in var:
            opcode = "%s%s"%(opcode,r_s[x])
    else:
        opcode = "%s%s0"%(opcode,r_s[var])
    return opcode

def format1():
    pass
path_op = 'Figure2.17.txt'
with open('symtable.json') as f:
    sytab = json.load(f)   
          
f_w = open(path_t,'w')   
f_r = open(path_w,'r')
op = open(path_op,'w')
cs = -1
M = []
start_loc = []
T = [0,0]
while True:
        file_eof = f_r.readline().upper()
        if('.' in file_eof):
            f_w.write("%s"%file_eof)
            continue
        if file_eof == "":
            if(T != [0,0]):
                op.write("T00%s%.2X"%(T[0],T[1]))
                for x in T[2:]:
                    op.write("%s"%x)
                op.write("\n")
            T = [0,0]
            cs += 1
            for x in M:
                op.write(x)
                op.write("\n")
            op.write("E\n")
            print("PASS 2 Done!")
            break
        a = file_eof.split()
        if(a[0]in["LTORG","END"]):
            f_w.write("%s"%file_eof)
        elif(a[0]=="EXTREF"):
            f_w.write("%s"%file_eof)
            op.write("R")
            a[1] = a[1].split(",")
            for x in a[1]:
                op.write("%s "%x)
            op.write("\n")
        elif(a[0]=="EXTDEF"):
            f_w.write("%s"%file_eof)
            op.write("D")
            a[1] = a[1].split(",")
            for x in a[1]:
                op.write("%s%.6X"%(x,sympt[x]))
            op.write("\n")
        elif(("RESW" in a)or("RESB" in a)):
            f_w.write("%s"%file_eof)
            if(T!=[0,0]):
                op.write("T00%s%.2X"%(T[0],T[1]))
                for x in T[2:]:
                    op.write("%s"%x)
                op.write("\n")
                T = [0,0]
        elif("EQU" in a):
            f_w.write("%s"%file_eof)
        elif("START" in a) or ("CSECT" in a):
            if(T != [0,0]):
                op.write("T00%s%.2X"%(T[0],T[1]))
                for x in T[2:]:
                    op.write("%s"%x)
                op.write("\n")
            T = [0,0]
            cs += 1
            for x in M:
                op.write(x)
                op.write("\n")
            if("CSECT" in a):
                if(start_loc):
                    op.write("E%s\n"%start_loc.pop())
                else:
                    op.write("E\n")
            M = []
            sympt = sytab[str(cs)]
            locc = 0
            if("START" in a):
                start_loc.append("%.6X"%locc)
            f_w.write("%s"%file_eof)
            op.write("H%s %.6X%.6X\n"%(a[1],locc,sympt["Totallen"]))


        elif(len(a)==4):
            if(a[2].replace('+','') in optab.keys()):
                if(optab[a[2].replace('+','')][1]==3):
                    if(a[2][0]=='+'):
                        n = 1
                        i = 1
                        x = 0
                        if(a[3][0]=="@"):
                            i = 0
                        if(",X" in a[3]):
                            x = 1
                        if("#" in a[3]):
                            n = 0
                        opcode,m = format4(a[2],sympt,n,i,x,a[3].replace(",X",""))
                        if(m==True):
                            M.append("M%.6X05+%s"%(int(a[0],16)+1,a[3].replace(",X","")))
                        f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                        if((T[1]+4)<=30):
                            if(T[1]==0):
                                T[0]=a[0]
                            T.append(opcode)
                            T[1] += 4
                        else:
                            op.write("T00%s%.2X"%(T[0],T[1]))
                            for x in T[2:]:
                                op.write("%s"%x)
                            op.write("\n")
                            T = [a[0],0,opcode]
                            T[1] += 4
                    else:
                        n = 1
                        i = 1
                        x = 0
                        if(a[3][0]=="@"):
                            i = 0
                        if(",X" in a[3]):
                            x = 1
                        if("#" in a[3]):
                            n = 0
                        opcode,m = format3(a[2],int(a[0],16),sympt,n,i,x,a[3].replace(",X",""))
                        if(m==True):
                            M.append("M%.6X05+%s"%(int(a[0],16)+1,a[3]))
                        f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                        if((T[1]+3)<=30):
                            if(T[1]==0):
                                T[0]=a[0]
                            T.append(opcode)
                            T[1] += 3
                        else:
                            op.write("T00%s%.2X"%(T[0],T[1]))
                            for x in T[2:]:
                                op.write("%s"%x)
                            op.write("\n")
                            T = [a[0],0,opcode]
                            T[1] += 3
                elif(optab[a[2]][1]==2):
                    opcode = format2(a[2],a[3])
                    f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                    if((T[1]+2)<=30):
                        if(T[1]==0):
                            T[0]=a[0]
                        T.append(opcode)
                        T[1] += 2
                    else:
                        op.write("T00%s%.2X"%(T[0],T[1]))
                        for x in T[2:]:
                            op.write("%s"%x)
                        op.write("\n")
                        T = [a[0],0,opcode]
                        T[1] += 2
            elif(a[2]=="WORD"):
                if(a[3] not in range(10)):
                    f_w.write("%s\t000000\n"%file_eof.replace("\n",""))
                    if((T[1]+3)<=30):
                        if(T[1]==0):
                            T[0]=a[0]
                        T.append("000000")
                        T[1] += 3
                    else:
                        op.write("T00%s%.2X"%(T[0],T[1]))
                        for x in T[2:]:
                            op.write("%s"%x)
                        op.write("\n")
                        T = [a[0],0,"000000"]
                        T[1] += 3
                    a[3] = a[3].split("+")
                    i = 0
                    for x in a[3]:
                        a[3][i] = "+%s"%x
                        i += 1
                    
                    j=0
                    for x in a[3]:
                        if("-"in x):
                            x = x.split("-")
                            i = 0
                            for c in x:
                                if(i==0):
                                    i += 1
                                else:
                                    x[i] = "-%s"%c
                                    i += 1
                            a[3][j] = x
                        j+=1
                    for x in a[3][0]:
                        M.append("M00%s06%s"%(a[0],x))
            elif(a[2]=="BYTE"):
                opcode = a[3][2:4]
                f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                if((T[1]+1)<=30):
                        if(T[1]==0):
                            T[0]=a[0]
                        T.append("%s"%opcode)
                        T[1] += 1
                else:
                    op.write("T00%s%.2X"%(T[0],T[1]))
                    for x in T[2:]:
                        op.write("%s"%x)
                    op.write("\n")
                    T = [a[0],0,opcode]
                    T[1] += 1


        elif(len(a)==3):
            if(a[1].replace('+','') in optab.keys()):
                if(optab[a[1].replace('+','')][1]==3):
                    if(a[1][0]=='+'):
                        n = 1
                        i = 1
                        x = 0
                        if(a[2][0]=="@"):
                            i = 0
                        if(",X" in a[2]):
                            x = 1
                        if("#" in a[2]):
                            n = 0
                        opcode,m = format4(a[1],sympt,n,i,x,a[2].replace(",X",""))
                        if(m==True):
                            M.append("M%.6X05+%s"%(int(a[0],16)+1,a[2].replace(",X","")))
                        f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                        if((T[1]+4)<=30):
                            if(T[1]==0):
                                T[0]=a[0]
                            T.append(opcode)
                            T[1] += 4
                        else:
                            op.write("T00%s%.2X"%(T[0],T[1]))
                            for x in T[2:]:
                                op.write("%s"%x)
                            op.write("\n")
                            T = [a[0],0,opcode]
                            T[1] += 4
                    else:
                        n = 1
                        i = 1
                        x = 0
                        if(a[2][0]=="@"):
                            i = 0
                        if(",X" in a[2]):
                            x = 1
                        if("#" in a[2]):
                            n = 0
                        opcode,m = format3(a[1],int(a[0],16),sympt,n,i,x,a[2].replace(",X",""))
                        if(m==True):
                            M.append("M%.6X05+%s"%(int(a[0],16)+1,a[2]))
                        f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                        if((T[1]+3)<=30):
                            if(T[1]==0):
                                T[0]=a[0]
                            T.append(opcode)
                            T[1] += 3
                        else:
                            op.write("T00%s%.2X"%(T[0],T[1]))
                            for x in T[2:]:
                                op.write("%s"%x)
                            op.write("\n")
                            T = [a[0],0,opcode]
                            T[1] += 3
                elif(optab[a[1]][1]==2):
                    opcode = format2(a[1],a[2])
                    f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                    if((T[1]+2)<=30):
                        if(T[1]==0):
                            T[0]=a[0]
                        T.append(opcode)
                        T[1] += 2
                    else:
                        op.write("T00%s%.2X"%(T[0],T[1]))
                        for x in T[2:]:
                            op.write("%s"%x)
                        op.write("\n")
                        T = [a[0],0,opcode]
                        T[1] += 2
            elif(a[1]=='*'):
                if(a[2][1]=='C'):
                    string = a[2][3:-1]
                    opcode = ""
                    ascii_values = []
                    i = 0
                    for character in string:
                        opcode = "%s%X"%(opcode,ord(character))
                    f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                    if((T[1]+len(string))<=30):
                        if(T[1]==0):
                            T[0]=a[0]
                        T.append(opcode)
                        T[1] += len(string)
                    else:
                        op.write("T00%s%.2X"%(T[0],T[1]))
                        for x in T[2:]:
                            op.write("%s"%x)
                        op.write("\n")
                        T = [a[0],0,opcode]
                        T[1] += len(string)
                elif(a[2][1]=='X'):
                    opcode = a[2][3:-1]
                    f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                    if((T[1]+1)<=30):
                        if(T[1]==0):
                            T[0]=a[0]
                        T.append(opcode)
                        T[1] += 1
                    else:
                        op.write("T00%s%.2X"%(T[0],T[1]))
                        for x in T[2:]:
                            op.write("%s"%x)
                        op.write("\n")
                        T = [a[0],0,opcode]
                        T[1] += 1


        elif(len(a)==2):
            if(a[1] in optab.keys()):
                if(optab[a[1]][1]==3):
                    opcode = optab[a[1]][0]
                    tmp =int(opcode[1],16)
                    tmp = "{0:b}".format(tmp)
                    m = False
                    if(len(tmp)<4):
                        while(len(tmp)<4):
                            tmp = "0%s"%tmp
                    tmp = "%s%s%s"%(tmp[0:2],1,1)
                    opcode = "%s%X0000"%(opcode[0],int(tmp,2))
                    f_w.write("%s\t%s\n"%(file_eof.replace("\n",""),opcode))
                    if((T[1]+3)<=30):
                        if(T[1]==0):
                            T[0]=a[0]
                        T.append(opcode)
                        T[1] += 3
                    else:
                        op.write("T00%s%.2X"%(T[0],T[1]))
                        for x in T[2:]:
                            op.write("%s"%x)
                        op.write("\n")
                        T = [a[0],0,opcode]
                        T[1] += 3


f_w.close()
f_r.close()
op.close()
    





encoder_dic={# R TYPE INSTRUCTION                           #OPCODE DICTIONARY
             "ADD":["R","0110011","000","0000000"],
             "SUB":["R","0110011","000","0100000"],
             "SLL":["R","0110011","001","0000000"],
             "XOR":["R","0110011","100","0000000"],
             "SRL":["R","0110011","101","0000000"],
             "SRA":["R","0110011","101","0010000"],
             "OR":["R","0110011","110","0000000"],
             "AND":["R","0110011","111","0000000"],

             # I TYPE INSTRUCTION
            #type1
            "LB":["I","0000011","000","NA"],
            "LH":["I","0000011","001","NA"],
            "LW":["I","0000011","010","NA"],
            "LBU":["I","0000011","100","NA"],
            "LHU":["I","0000011","101","NA"],
            #type2
            "ADDI":["I","0010011","000","NA"],
            "SLLI":["I","0010011","001","0000000"],
            "XORI":["I","0010011","100","NA"],
             "SRAI":["I","0010011","101","0100000"],
             "SLLI":["I","0010011","001","0000000"],
             "ORI":["I","0010011","110","NA"],
             "ANDI":["I","0010011","111","NA"],
             #type3
             "JALR":["I","1100111","000","NA"],

             #S TYPE INSTRUCTION

             "SB":["S","0100011","000","NA"],
             "SH":["S","0100011","001","NA"],
             "SW":["S","0100011","010","NA"],

             #SB TYPE INSTRUCTION

             "BEQ":["SB","1100011","000","NA"],
             "BNE":["SB","1100011","001","NA"], #CONFIRM WITH SIR 1100111 OR 1100011
             "BLT":["SB","1100011","100","NA"],
             "BGE":["SB","1100011","101","NA"],
             "BLTU":["SB","1100011","110","NA"],
             "BGEU":["SB","1100011","111","NA"],

             #U TYPE INSTRUCTION

             "LUI":["U","0110111","NA","NA"],

             #UJ TYPE INSTRUCTION

             "JAL":["UJ","1101111","NA","NA"],

             }


register_dic={"X0":"00000",       #REGISTER DICTIONARY
              "X1":"00001",
              "X2":"00010",
              "X3":"00011",
              "X4":"00100",
              "X5":"00101",
              "X6":"00110",
              "X7":"00111",
              "X8":"01000",
              "X9":"01001",
              "X10":"01010",
              "X11":"01011",
              "X12":"01100",
              "X13":"01101",
              "X14":"01110",
              "X15":"01111",
              "X16":"10000",
              "X17":"10001",
              "X18":"10010",
              "X19":"10011",
              "X20":"10100",
              "X21":"10101",
              "X22":"10110",
              "X23":"10111",
              "X24":"11000",
              "X25":"11001",
              "X26":"11010",
              "X27":"11011",
              "X28":"11100",
              "X29":"11101",
              "X30":"11110",
              "X31":"11111",
              }

def two_complement(immediate_bitcode): # 2'S COMPLEMENT FUNCTIONS
    immediate_bitcode_list=list(immediate_bitcode)[::-1]
    for i in range(0,len(immediate_bitcode_list)):
      if immediate_bitcode_list[i]=='1':
          for j in range(i+1,len(immediate_bitcode_list)):
              if immediate_bitcode_list[j]=='0':
                    immediate_bitcode_list[j]='1'
              else:
                  immediate_bitcode_list[j]='0'
          break
    immediate_bitcode="".join(immediate_bitcode_list[::-1])
    return immediate_bitcode

def zero_padding(val,size):       # PADDING FUNCTION
  bit_size=len(val)
  for i in range(size-bit_size):
    val="0"+val
  return val

def binary_hex_32_bit(binarycode):   #BINARY TO HEXADECIMAL CONVERTOR FUNCTION
  hex=""
  for i in range(0,31,4):
    code=binarycode[i:i+4]
    int_val=0
    for j in range(4):
      int_val+=(2**(3-j))*int(code[j])
    if int_val>9:
      if int_val==10:
              hex_code='A'
      if int_val==11:
              hex_code='B'
      if int_val==12:
              hex_code='C'
      if int_val==13:
              hex_code='D'
      if int_val==14:
              hex_code='E'
      if int_val==15:
              hex_code='F'
    else:
      hex_code=str(int_val)
    hex+=hex_code
  return hex


def risc5assembler(code_arr):
  #R TYPE INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="R":
    print("Instruction Type--",encoder_dic[code_arr[0]][0])
    print(code_arr)
    print("opcode--",encoder_dic[code_arr[0]][1])
    print("destination code--",register_dic[code_arr[1]])
    print("func3 code--",encoder_dic[code_arr[0]][2])
    print("func7 code--",encoder_dic[code_arr[0]][3])
    print("source1 code--",register_dic[code_arr[2]])
    print("source2 code--",register_dic[code_arr[3]])
    bitcode=encoder_dic[code_arr[0]][3]+register_dic[code_arr[3]]+register_dic[code_arr[2]]+encoder_dic[code_arr[0]][2]+register_dic[code_arr[1]]+encoder_dic[code_arr[0]][1]
    print("BITCODE VALUE --",bitcode)
    hex=binary_hex_32_bit(bitcode)
    print("32 B hexadecimal Code---","0x",hex)

    #I TYPE INSTRUCTION

  #TYPE 1 INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="I" and encoder_dic[code_arr[0]][1]=="0000011":
    last_arr=code_arr[-1].split('(')
    code_arr=code_arr[:-1]+[last_arr[0],last_arr[-1][0:-1]]
    print(code_arr)
    opcode=encoder_dic[code_arr[0]][1]
    des_address=register_dic[code_arr[1]]
    func3=encoder_dic[code_arr[0]][2]
    s_address=register_dic[code_arr[-1]]
    print("opcode--",opcode)
    print("destination address--",des_address)
    print("func3 code--",func3)
    print("source address--",s_address)
    immediate=int(code_arr[-2]) #uses 2's complement system
    immediate_bitcode=zero_padding(bin(abs(immediate))[2:],12) #  positive number's 2's complement calculation
    # negative number's 2's complement calculation
    if immediate<0:
      immediate_bitcode=two_complement(immediate_bitcode)
    print("immediate_bitcode--",immediate_bitcode)
    bitcode=immediate_bitcode+s_address+func3+des_address+opcode
    print("BITCODE value--",bitcode)
    hex=binary_hex_32_bit(bitcode)
    print("32 B hexadecimal Code---","0x",hex)

  #TYPE 2 INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="I" and encoder_dic[code_arr[0]][1]=="0010011":
    print("Instruction Type--",encoder_dic[code_arr[0]][0])
    print(code_arr)
    opcode=encoder_dic[code_arr[0]][1]
    des_address=register_dic[code_arr[1]]
    func3=encoder_dic[code_arr[0]][2]
    func7=encoder_dic[code_arr[0]][3]
    s_address=register_dic[code_arr[-2]]
    print("opcode--",opcode)
    print("destination code--",des_address)
    print("func3 code--",func3)
    print("source1 code--",s_address)
    immediate=int(code_arr[-1]) #uses 2's complement system
    immediate_bitcode=zero_padding(bin(abs(immediate))[2:],12) #  positive number's 2's complement calculation
    # negative number's 2's complement calculation
    if immediate<0:
      immediate_bitcode=two_complement(immediate_bitcode)
    print("immediate_bitcode--",immediate_bitcode)
    if(code_arr[0]=="SRAI"):
              immediate_bitcode=immediate_bitcode[0]+"1"+immediate_bitcode[2:] #confirm with sir
    bitcode=immediate_bitcode+s_address+func3+des_address+opcode
    print("BITCODE value--",bitcode)
    hex=binary_hex_32_bit(bitcode)
    print("32 B hexadecimal Code---","0x",hex)

  #TYPE 3 INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="I" and encoder_dic[code_arr[0]][1]=="1100111":
    last_arr=code_arr[-1].split('(')
    code_arr=code_arr[:-1]+[last_arr[0],last_arr[-1][0:-1]]
    print(code_arr)
    opcode=encoder_dic[code_arr[0]][1]
    des_address=register_dic[code_arr[1]]
    func3=encoder_dic[code_arr[0]][2]
    s_address=register_dic[code_arr[3]]
    print("opcode--",opcode)
    print("destination address--",des_address)
    print("func3 code--",func3)
    print("source address--",s_address)
    immediate=int(code_arr[-2]) #uses 2's complement system
    immediate_bitcode=immediate_bitcode=zero_padding(bin(abs(immediate))[2:],12) #  positive number's 2's complement calculation
    # negative number's 2's complement calculation
    if immediate<0:
      immediate_bitcode=two_complement(immediate_bitcode)
    print("immediate_bitcode--",immediate_bitcode)
    bitcode=immediate_bitcode+s_address+func3+des_address+opcode
    print("BITCODE value--",bitcode)
    hex=binary_hex_32_bit(bitcode)
    print("32 B hexadecimal Code---","0x",hex)


  # U tYPE INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="U":
    print("opcode--",encoder_dic[code_arr[0]][1])
    print("destination address--",register_dic[code_arr[1]])
    immediate=int(code_arr[-1]) #uses 2's complement system
    immediate_bitcode=zero_padding(bin(abs(immediate))[2:],20) # positive number's 2's complement calculation
    # negative number's 2's complement calculation
    if immediate<0:
      immediate_bitcode=two_complement(immediate_bitcode)
    print("immediate_bitcode--",immediate_bitcode)

    bitcode=immediate_bitcode+register_dic[code_arr[1]]+encoder_dic[code_arr[0]][1]
    print("BITCODE value--",bitcode)
    hex=binary_hex_32_bit(bitcode)
    print("32 B hexadecimal Code---","0x",hex)

  # UJ TYPE INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="UJ":
        print("opcode--",encoder_dic[code_arr[0]][1])
        print("destination address--",register_dic[code_arr[1]])
        immediate=int(code_arr[2]) #uses 2's complement system
        immediate_bitcode=zero_padding(bin(abs(immediate))[2:],21) # positive number's 2's complement calculation
        # negative number's 2's complement calculation
        if immediate<0:
          immediate_bitcode=two_complement(immediate_bitcode)
        print("immediate_bitcode--",immediate_bitcode)
        bitcode=immediate_bitcode[0]+immediate_bitcode[10:20]+immediate_bitcode[9]+immediate_bitcode[1:9]+register_dic[code_arr[1]]+encoder_dic[code_arr[0]][1]

        print("BITCODE value--",bitcode)
        hex=binary_hex_32_bit(bitcode)
        print("32 B hexadecimal Code---","0x",hex)

  # S TYPE INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="S":
        last_arr=code_arr[-1].split('(')
        code_arr=code_arr[:-1]+[last_arr[0],last_arr[-1][0:-1]]
        print(code_arr)
        opcode=encoder_dic[code_arr[0]][1]
        sou1=register_dic[code_arr[3]]
        sou2=register_dic[code_arr[1]]
        func3=encoder_dic[code_arr[0]][2]
        print("opcode--",opcode)
        print("source1 address--",sou1)
        print("source2 address--",sou2)
        print("func3 code--",func3)
        immediate=int(code_arr[-2]) #uses 2's complement system
        immediate_bitcode=zero_padding(bin(abs(immediate))[2:],12) # positive number's 2's complement calculation
        # negative number's 2's complement calculation
        if immediate<0:
          immediate_bitcode=two_complement(immediate_bitcode)
        print("immediate_bitcode--",immediate_bitcode)

        bitcode=immediate_bitcode[0:7]+sou2+sou1+func3+immediate_bitcode[7:12]+opcode
        print("BITCODE value--",bitcode)
        hex=binary_hex_32_bit(bitcode)
        print("32 B hexadecimal Code---","0x",hex)
  #SB TYPE INSTRUCTION
  if encoder_dic[code_arr[0]][0]=="SB":
    print("Instruction Type--",encoder_dic[code_arr[0]][0])
    print(code_arr)
    opcode=encoder_dic[code_arr[0]][1] #need to confirm opcode
    sou1_address=register_dic[code_arr[1]]
    func3=encoder_dic[code_arr[0]][2]
    func7=encoder_dic[code_arr[0]][3]
    sou2_address=register_dic[code_arr[-2]]
    print("opcode--",opcode)
    print("source1 code--",sou1_address)
    print("func3 code--",func3)
    print("source2 code--",sou2_address)
    immediate=int(code_arr[-1]) #uses 2's complement system
    immediate_bitcode=zero_padding(bin(abs(immediate))[2:],13) #  positive number's 2's complement calculation
    # negative number's 2's complement calculation
    if immediate<0:
      immediate_bitcode=two_complement(immediate_bitcode)
    print("immediate_bitcode--",immediate_bitcode)
    bitcode=immediate_bitcode[0]+immediate_bitcode[2:8]+sou2_address+sou1_address+func3+immediate_bitcode[8:12]+immediate_bitcode[1]+opcode
    print("BITCODE value--",bitcode)
    hex=binary_hex_32_bit(bitcode)
    print("32 B hexadecimal Code---","0x",hex)


code=input("PLEASE ENTER ASSEMBLY CODE PNEMONICS-- \n")
code=code.upper();
code_arr=code.split(',')
code_arr=code_arr[0].split(' ')+code_arr[1:]
print("Details of your pnemonics are as follows---")
risc5assembler(code_arr)
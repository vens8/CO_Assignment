from sys import float_repr_style, stdin
opcodes = {
    'add': '00000',
    'sub': '00001',
    'mov1': '00010',
    'mov2': '00011',
    'ld': '00100',
    'st': '00101',
    'mul': '00110',
    'div': '00111',
    'rs': '01000',
    'ls': '01001',
    'xor': '01010',
    'or': '01011',
    'and': '01100',
    'not': '01101',
    'cmp': '01110',
    'jmp': '01111',
    'jlt': '10000',
    'jgt': '10001',
    'je': '10010',
    'hlt': '10011'
}

# opcodes along with the number of registers to take the values from
types = {
    '00000': 3,
    '00001': 3,
    '00010': 1,
    '01000': 1,
    '01001': 1,
    '00011': 2,
    '00111': 2,
    '01101': 2,
    '01110': 2,
    '00101': 1,
    '01111': 0,
    '10000': 0,
    '00100': 1,
    '10001': 0,
    '10010': 0,
    '00110': 3,
    '01010': 3,
    '01011': 3,
    '01100': 3,
    '10011': 0,
}

registers = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111'
}

# Initial register values
registers_values = {
    'R0': '0000000000000000',
    'R1': '0000000000000000',
    'R2': '0000000000000000',
    'R3': '0000000000000000',
    'R4': '0000000000000000',
    'R5': '0000000000000000',
    'R6': '0000000000000000',
    'FLAGS': '0000000000000000',
}
line_number=1
mem_address=0
# Dictionary to store the values of the memory addresses
variables={}  #its key will be the variable name or label name and value will be the memory address
labels={}       #key will be the label name and value will be the memory address
halt_instructions=[]#this will store the various number of halt statements encountered stored according to line number
errors={}
def parse(line):
    global line_number
    global mem_address
    lst=list(line.split())
    if(line=='\n'):
        pass
    else:
        line_number+=1
        if(lst[0][-1]==':'):
            parse(line[len(lst[0])+1:])
            labels[lst[0][:len(lst[0])-1]]=mem_address
            mem_address+=1

        elif(lst[0]=='var'):
            if(len(lst)==2):
                if(lst[1] in variables.keys() or lst[1] in labels.keys()):
                    errors[line_number]="Wrong syntax used for instructions"
                elif(lst[1] not in variables.keys() and lst[1] not in labels.keys()):
                    variables[lst[1]]=mem_address
                    mem_address+=1
                    flag=True
                else:
                    errors[line_number]="wrong synatx used for instructions"
            else:
                errors[line_number]="wrong syntax used for instructions(wrong number of arguments are present)"
        
        elif(lst[0] in opcodes.keys()):  
            if(lst[0]=='add' or lst[0]=='sub' or lst[0]=='mul' or lst[0]=='xor' or lst[0]=='or' or lst[0]=='and'):
                if(len(lst)==4):   #to check the number of argumenst are correct or not
                    if(lst[1] in registers.keys() and lst[2] in registers.keys() and lst[3] in registers.keys()):
                        mem_address+=1
                        flag=True
                    else:
                        errors[line_number]="wrong syntax used for instructions"
                else:
                    errors[line_number]="wrong syntax used for instructions(wrong number of arguments are present)"    
                   
            elif(lst[0]=='rs' or lst[0]=='ls'):
                if(len(lst)==3):
                    if(lst[1] in registers.keys() and lst[2] not in registers.keys()):
                        if(lst[2][0]=='$' and lst[2][1:]>=0 and lst[2][1:]<=225):
                            mem_address+=1
                            flag=True
                        else:
                            errors[line_number]="wrong value of immidiate used or wrong syntax used for instructions"
                    else:
                        errors[line_number]="wrong syntax used for instructions"
                else:
                    errors[line_number]="wrong syantax used for instructions(wrong number of arguments are present" 
                    
            elif(lst[0]=='mov'):
                if(len(lst)==3):
                    if((lst[1] in registers and lst[2][0]=='$') or (lst[1] in registers and lst[2] in registers)):            
                        if(lst[1] in registers and lst[2][0]=='$'):
                            if(lst[2][1:]>=0 and lst[2][1:]<=225):
                                mem_address+=1
                                flag=True
                            else:
                                errors[line_number]="Illegal immidieate value is used"
                        
                        else:
                            mem_address+=1
                            flag=True
                    else:
                        errors[line_number]="Wrong type of arguments are used"
                else:
                    errors[line_number]="Wrong number of argumenst are used"
            
            elif(lst[0]=='ld' or lst[0]=='st'):
                if(len(lst)==3):
                    if(lst[1] in registers.keys() and lst[2] in labels.keys() and lst[2] not in variables.keys()):
                        mem_address+=1
                        flag=True
                    else:
                        errors[line_number]="wrong type of arguments are used"
                else:
                    errors[line_number]="wrong number of arguments are present"
            
            elif(lst[0]=='jmp' or lst[0]=='jlt' or lst[0]=='jgt' or lst[0]=='je'):
                if(len(lst)==2):
                    if(lst[1] not in labels.keys()):
                        labels[lst[1]]=mem_address
                    if(lst[1] in variables.keys()):
                        errors[line_number]="wrong syntax used for instructions"
                    else:
                        mem_address+=1
                        flag=True
                else:
                    errors[line_number]="wrong synatx for isntruction(Wrong number of argumensta are used"

            elif(lst[0]=='hlt'):
                if(len(lst)==1):
                    halt_instructions.append(line_number)
                    mem_address+=1
                    flag=True
                else:
                    errors[line_number]="Wrong syntax used(incorrect number of arguments)"

        else:
            errors[line_number]='typos in instruction name'
    return flag


# Convert a string decimal into the equivalent binary of custom bits
def binary(number, bit):
    binary = bin(int(number)).replace('0b', '')[::-1]
    if len(binary) > bit:
        binary = binary[0:bit]
        return binary[::-1]

    while len(binary) < bit:
        binary += '0'
    return binary[::-1]

def process(command):
    s = ""
    words = list(command.split())
    registers_values['FLAGS']='0000000000000000'
    
    if words[0] != 'mov':
        if words[0] == 'var':  # Create a new variable and store a default value as 0.
            variables[words[1]] = 0000000000000000
        elif words[0][-1] == ':':
            pass
            # Add code for labels
        else:  # try to use 'try/except' for catching dictionary key errors for error generation test cases.
            s += opcodes[words[0]]
            if types[opcodes[words[0]]] > 0:  # generate the machine code
                s += '0' * (16 - 5 - 3 * types[opcodes[words[0]]])
                for i in range(1, types[opcodes[words[0]]] + 1):
                    s += registers[words[i]]
            
            if words[0] == 'add':  # addition
                if int(registers_values[words[2]], 2) + int(registers_values[words[3]], 2) > 65535:
                    registers_values['FLAGS']='0000000000001000'
                    registers_values[words[1]] = binary(int(registers_values[words[2]], 2) + int(registers_values[words[3]], 2), 16)  # Store only 16 bits even for overflow
                    print(s)

            elif words[0] == 'sub':  # subtraction
                if int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2) < 0:
                    registers_values['FLAGS']='0000000000001000'
                    registers_values[words[1]] = binary(int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2), 16)
                    print(s)

            elif words[0] == 'ld':  # load
                registers_values[words[1]] = words[2][1::]
                print(s)

            elif words[0] == 'st':  # store
                variables[words[2]] = registers_values[words[1]]
                print(s)

            elif words[0] == 'mul':  # multiply
                if int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2) > 65535:
                    registers_values['FLAGS']='0000000000001000'
                    registers_values[words[1]] = binary(int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2), 16)
                    print(s)
            
            elif words[0] == 'not':
                str=''
                registers_values['FLAGS']='0000000000000000'
                for i in registers_values[words[2]]:
                    if(i=='1'):
                        str+='0'
                    else:
                        str+='1' 
                registers_values[words[1]]=str.copy() 
                print(s)
            elif words[0] == 'cmp':
                if(int(registers_values[words[1]])>int(registers_values[words[2]]) ):
                    registers_values['FLAGS']='0000000000000010'
                elif(int(registers_values[words[1]])<int(registers_values[words[2]]) ):
                    registers_values['FLAGS']='0000000000000100'
                else:
                    registers_values['FLAGS']='0000000000000001'
            elif words[0] == 'jmp':
                pass
            elif words[0] == 'jlt':
                if(registers_values['FLAGS']=='0000000000000100'):
                    print(s)
            elif words[0] == 'jgt':
                if(registers_values['FLAGS']=='0000000000000010'):
                    print(s)
            elif words[0] == 'je':
                if(registers_values['FLAGS']=='0000000000000001'):
                    print(s)
            elif words[0] =='hlt':
                print(s)
            
    else:
        if words[2][0] == '$':
            s += opcodes['mov1']
            s += registers[words[1]]
            s += binary(words[2][1::], 8)
        else:
            s += opcodes['mov2']
            if types[opcodes['mov2']] > 0:
                s += '0' * (16 - 5 - 3 * types[opcodes['mov2']])
                for i in range(1, types[opcodes['mov2']] + 1):
                    s += registers[words[i]]

            registers_values[words[1]] = registers_values[words[2]]

    print(s)  # print the machine code for every command
    # print(registers_values)
    # print(variables)

for line in stdin:
    if line == '':  # If empty string is read then stop the loop
        break
    else:
        parse(line)  # perform some operation(s) on given string

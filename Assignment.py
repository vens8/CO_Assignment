from sys import stdin
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
variables = {}
mem_address={}
variables_and_labels={}  #its key will be the variable name and value will be the memoery address
errors={}
def check_errors(line):
    global line_number
    line_number+=1
    global mem_address
    lst=list(line.split(" "))
    if(line=='\n'):
        pass
    else:
        flag=0
        if(lst[0]=='var'):
            if(len(lst)!=2):
                flag+=1
                errors[line_number]='Wrong syntax used for instruction(wrong number of arguments'
            elif(lst[1][0]=='$'):
                flag+=1
                errors[line_number]='Wrong syntax used for instructions(wrong type of argument is used'
            elif(lst[1] in variables_and_labels):
                flag+=1
                errors[line_number]='Value has already been initialised earlier(both label and variable have same name)'
            elif(lst[1] in registers):
                flag+=1
                errors[line_number]='Wrong syntax used for instruction(wrong type of argument is used'
            elif(lst[1] in opcodes):
                flag+1
                errors[line_number]='Wrong syntax used for instruction(wrong type of argument is used'                    
        
        elif(lst[0]=='add' or lst[0]=='sub' or lst[0]=='mov' or lst[0]=='ld' or lst[0]=='st' or lst[0]=='mul' or lst[0]=='div' or lst[0]=='rs' or lst[0]=='ls' or lst[0]=='xor' or lst[0]=='or' or lst[0]=='and' or lst[0]=='not' or lst[0]=='cmp' or lst[0]=='jmp' or lst[0]=='jlt' or lst[0]=='jgt' or lst[0]=='je' or lst[0]=='hlt'):
            if(len(lst)!=4):   #to check the number of argumenst are correct or not
                flag+=1
                errors[line_number]='Wrong syntax used for instructions(wrong number of arguments)'
            elif(lst[0]=='add' or lst[0]=='sub' or lst[0]=='mul' or lst[0]=='xor' or lst[0]=='or' or lst[0]=='and'):
                if(lst[1][0]=='$' or lst[2][0]=='$' or lst[3][0]=='$' or lst[1] in opcodes or lst[2] in opcodes or lst[3] in opcodes):
                    flag+=1
                    errors[line_number]='Wrong syntax used for instructions'
            else:
                if(flag==0):
                    mem_address+=1           
        
        elif(lst[0]=='rs' or lst[0]=='ls'):
            if(len(lst)!=3):
                flag+=1
                errors[line_number]='Wrong syntax used for instructions(wrong number of arguments)'
            elif(lst[2][0]=='$'):
                if(int(lst[2][1:])<=225 and int(lst[2][1:])>0):
                    pass
                else:
                    flag+=1
                    errors[line_number]='Illegal immidiate values'
            elif(lst[2] in opcodes or lst[2] in registers or lst[1][0]=='$' or lst[1] in opcodes):
                flag+=1
                errors[line_number]='Wrong syntax used for instructions'
            else:
                if(flag==0):
                    mem_address+=1
            
        elif(lst[0]=='mov'):
            if(len(lst)!=3):
                flag+=1
                errors[line_number]='Wrong syntax used for instructions(wrong number of arguments)'
            elif(lst[2][0]=='$' and lst[1][0]=='$'):
                flag+=1
                errors[line_number]="wrong syntax used for instructions"
            elif(lst[2][0]!='$' and lst[1][0]=='$'):
                flag+=1
                errors[line_number]="wrong syntax used for instructions"
            elif(lst[2] not in opcodes and lst[1] not in opcodes):
                if(flag==0):
                    mem_address+=1
                else:
                    errors[line_number]="wrong syntax used for instructions"
        
        elif(lst[0]=='ld' or lst[0]=='st'):
            if(len(lst)!=3):
                flag+=1
                errors[line_number]="wrong sysntax used for isntructions(wrong number of arguments are used"
            if(lst[1] not in registers):
                flag+=1
                errors[line_number]="wrong syntax used for instructions"
            if(lst[2] in variables_and_labels):
                flag+=1
                errors[line_number]="Value has already been initialised earlier"
            if(lst[1][0]=='$' or lst[2][0]=='$' or lst[1] in opcodes or lst[2] in opcodes or lst[2] in registers):
                flag+=1
                errors[line_number]="Wrong syntax used for instructions"
            else:
                if(flag==0):
                    mem_address+=1
        
        elif(lst[0]=='jmp' or lst[0]=='jlt' or lst[0]=='jgt' or lst[0]=='je'):
            if(len(lst)!=2):
                flag+=1
                errors[line_number]="wrong sysntax used for isntructions(wrong number of arguments are used"
            if(lst[1] in registers or lst[1][0]=='$' or lst[1] in opcodes):
                flag+=1
                errors[line_number]="wrong syntax used for instructions"
            else:
                if(flag==0):
                    mem_address+=1
        
        elif(lst[0]=='hlt'):
            if(len(lst)==1):
                mem_address+=1
            else:
                errors[line_number]="Wrong syntax used(incorrect number of arguments)"
        
        else:
            errors[line_number]='typos in instruction name'
        


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
                    flags = list(registers_values['FLAGS'])
                    flags[12] = '1'
                    registers_values['FLAGS'] = "".join(flags)
                registers_values[words[1]] = binary(int(registers_values[words[2]], 2) + int(registers_values[words[3]], 2), 16)  # Store only 16 bits even for overflow

            elif words[0] == 'sub':  # subtraction
                if int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2) < 0:
                    flags = list(registers_values['FLAGS'])
                    flags[12] = '1'
                    registers_values['FLAGS'] = "".join(flags)
                else:
                    registers_values[words[1]] = binary(int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2), 16)

           
            elif words[0] == 'ld':  # load
                registers_values[words[1]] = words[2][1::]
           
            elif words[0] == 'st':  # store
                variables[words[2]] = registers_values[words[1]]
           
            elif words[0] == 'mul':  # multiply
                if int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2) > 65535:
                    flags = list(registers_values['FLAGS'])
                    flags[12] = '1'
                    registers_values['FLAGS'] = "".join(flags)
                registers_values[words[1]] = binary(int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2), 16)
           
            elif words[0] == 'not':
                str=''
                registers_values['FLAGS']='0000000000000000'
                for i in registers_values[words[2]]:
                    if(i=='1'):
                        str+='0'
                    else:
                        str+'1' 
                registers_values[words[1]]=str.copy() 

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
                if(registers_values['FLAGS']!='0000000000000100'):
                    # THIS LINE MUST PRODUCE AN ERROR>>>> I CAN'T UNDERSTAND, this error comes when we are getting a jlt statement and value of flag is not appropriate... so will that be an error or do we sim ply have to ignore this case 
                    pass
            elif words[0] == 'jgt':
                pass
            elif words[0] == 'je':
                pass
            elif words[0] =='hlt':
                pass
            
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
    check_errors(line)  # perform some operation(s) on given string

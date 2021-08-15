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
line_number = 1
mem_address = 0
# Dictionary to store the values of the memory addresses
variables = {}  # its key will be the variable name and value will be the memory address
labels = {}  # key will be the label name and value will be the memory address
halt_instructions = []  # this will store the various number of halt statements encountered stored according to line number
errors = {}
flag_parse = False
flag_process = False
temp_labels={}
temp_variables={}

def parse(line):
    global line_number, mem_address, flag_parse, errors, variables
    words = list(line.split())
    if line != '\n':
        if ':' in line and words[0][-1] == ':':
            if flag_parse:
                line_number += 1
            if words[0][:len(words[0]) - 1] not in labels and words[0][:len(words[0]) - 1] not in variables:
                if(words[0][:len(words[0])-1] in temp_labels):
                    del temp_labels[words[0][:len(words[0])-1]]
                labels[words[0][:len(words[0]) - 1]] = mem_address
            else:
                errors[line_number] = "Label name already in use."
            if ':' in line:
                flag_parse = False
                parse(line[len(words[0]) + 1:])
            else:
                flag_parse = True
                parse(line[len(words[0]) + 1:])
                mem_address += 1
                line_number += 1

        elif words[0] == 'var':
            line_number += 1
            if len(words) == 2:
                if words[1] in variables.keys() or words[1] in labels.keys():
                    errors[line_number] = "Wrong syntax used for instructions"
                elif words[1] not in variables.keys() and words[1] not in labels.keys():
                    if(words[1] in temp_variables):
                        del temp_variables[words[1]]
                    variables[words[1]] = -1
                else:
                    errors[line_number] = "wrong syntax used for instructions"
            else:
                errors[line_number] = "wrong syntax used for instructions(wrong number of arguments are present)"

        elif words[0] == 'mov' or words[0] in opcodes.keys():
            line_number += 1
            if words[0] == 'add' or words[0] == 'sub' or words[0] == 'mul' or words[0] == 'xor' or words[0] == 'or' or words[0] == 'and':
                if len(words) == 4:  # to check the number of arguments are correct or not
                    if words[1] in registers.keys() and words[2] in registers.keys() and words[3] in registers.keys():
                        mem_address += 1
                    else:
                        errors[line_number] = "wrong syntax used for instructions"
                else:
                    errors[line_number] = "wrong syntax used for instructions (wrong number of arguments are present)"

            elif words[0] == 'rs' or words[0] == 'ls':
                if len(words) == 3:
                    if words[1] in registers.keys() and words[2] not in registers.keys():
                        if words[2][0] == '$' and int(words[2][1:]) >= 0 and int(words[2][1:]) <= 255:
                            mem_address += 1
                        else:
                            errors[line_number] = "wrong value of immediate used or wrong syntax used for instructions"
                    else:
                        errors[line_number] = "wrong syntax used for instructions"
                else:
                    errors[line_number] = "wrong syntax used for instructions (wrong number of arguments are present"

            elif words[0] == 'mov':
                if len(words) == 3:
                    if (words[1] in registers and words[2][0] == '$') or (
                            words[1] in registers and words[2] in registers):
                        if words[1] in registers and words[2][0] == '$':
                            if int(words[2][1:]) >= 0 and int(words[2][1:]) <= 255:
                                mem_address += 1
                            else:
                                errors[line_number] = "Illegal immediate value is used"
                        else:
                            mem_address += 1
                    else:
                        errors[line_number] = "Wrong type of arguments are used"
                else:
                    errors[line_number] = "Wrong number of arguments are used"

            elif words[0] == 'ld' or words[0] == 'st':
                if len(words) == 3:
                    if words[1] in registers.keys():
                        if words[2] not in variables.keys() and words[2][0]!='$' and words[2] not in registers.keys() and words[2] not in labels.keys() and words[2] not in temp_labels.keys():
                            temp_variables[words[2]]=-1 #this is done to check if the defination of variable exists or not
                            mem_address+=1
                        elif words[2] in variables.keys():
                            mem_address+=1              
                    else:
                        print(line)
                        errors[line_number] = "wrong type of arguments are used"
                else:
                    errors[line_number] = "wrong number of arguments are present"

            elif words[0] == 'jmp' or words[0] == 'jlt' or words[0] == 'jgt' or words[0] == 'je':
                if len(words) == 2:
                    if words[1] not in labels.keys():
                        temp_labels[words[1]] = mem_address
                    if words[1] in variables.keys():
                        errors[line_number] = "wrong syntax used for instructions"
                    else:
                        mem_address += 1
                else:
                    errors[line_number] = "wrong syntax for instruction (Wrong number of arguments are used)"

            elif words[0] == 'hlt':
                if len(words) == 1:
                    halt_instructions.append(line_number)
                    mem_address += 1
                else:
                    errors[line_number] = "Wrong syntax used (incorrect number of arguments)"
        else:
            line_number += 1
            errors[line_number] = 'Typos in instruction name'


# Convert a string decimal into the equivalent binary of custom bits
def binary(number, bit):
    binary = bin(int(number)).replace('0b', '')[::-1]
    if len(binary) > bit:
        binary = binary[0:bit]
        return binary[::-1]

    while len(binary) < bit:
        binary += '0'
    return binary[::-1]


def process(line):
    global mem_address, line_number, variables, labels
    s = ""
    words = list(line.split())
    registers_values['FLAGS'] = '0000000000000000'

    if words[0] != 'mov':
        if words[0] == 'var':  # Create a new variable and store a default value as 0.
            pass
        elif ':' in line:
            process(line[len(words[0]) + 1:])
        else:
            s += opcodes[words[0]]

            if words[0] == 'add':  # addition
                if int(registers_values[words[2]], 2) + int(registers_values[words[3]], 2) > 65535:
                    registers_values['FLAGS'] = '0000000000001000'
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) + int(registers_values[words[3]], 2),
                        16)  # Store only 16 bits even for overflow
                s += '0' * 2
                for i in range(1, 4):
                    s += registers[words[i]]
                print(s)

            elif words[0] == 'sub':  # subtraction
                if int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2) < 0:
                    registers_values['FLAGS'] = '0000000000001000'
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2), 16)
                s += '0' * 2
                for i in range(1, 4):
                    s += registers[words[i]]
                print(s)

            elif words[0] == 'ld':  # load
                registers_values[words[1]] = words[2][1::]
                s += registers[words[1]]
                s += binary(variables[words[2]], 8)
                print(s)

            elif words[0] == 'st':  # store
                variables[words[2]] = registers_values[words[1]]
                s += registers[words[1]]
                s += binary(variables[words[2]], 8) 
                print(s)

            elif words[0] == 'mul':  # multiply
                if int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2) < 65535:
                    registers_values['FLAGS'] = '0000000000001000'
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2), 16)
                    print(s)

            elif words[0] == 'div': #division
                if (registers_values[words[2]])!='0000000000000000' and int(int(registers_values[words[1]], 10) / int(registers_values[words[2]], 10)) < 65535 :
                    registers_values['R0'] = binary(int(registers_values[words[1]], 2) / int(registers_values[words[2]], 2), 16)
                    registers_values['R1'] = binary(int(registers_values[words[1]], 2) % int(registers_values[words[2]], 2), 16)
                else:
                    print("Error: Division by zero (not defined)")

            elif words[0] == 'ls': #left shift
                if int(registers_values[words[1]], 2) << int(words[2][1:]) < 65535:
                    registers_values[words[1]]=binary(int(registers_values[words[1]],2) << int(words[2][1:],10) ,16 )
                    print(s)

            elif words[0] == 'rs': #right shift
                if int(registers_values[words[1]], 2) >> int(words[2][1:]) < 65535:
                    registers_values[words[1]]=binary(int(registers_values[words[1]],2) >> int(words[2][1:],10) ,16 )
                    print(s)

            elif words[0] == 'xor': #Exclusive OR
                if int(registers_values[words[2]], 2) ^ int(registers_values[words[3]], 2) < 65535:
                    registers_values[words[1]] = binary(int(registers_values[words[2]], 2) ^ int(registers_values[words[3]], 2), 16)
                    print(s)

            elif words[0] == 'or': #Bitwise OR
                if int(registers_values[words[2]], 2) | int(registers_values[words[3]], 2) < 65535:
                    registers_values[words[1]] = binary(int(registers_values[words[2]], 2) | int(registers_values[words[3]], 2), 16)
                    print(s)

            elif words[0] =='and': #Bitwise AND
                if int(registers_values[words[2]], 2) & int(registers_values[words[3]], 2) < 65535:
                    registers_values[words[1]] = binary(int(registers_values[words[2]], 2) & int(registers_values[words[3]], 2), 16)
                    print(s)

            elif words[0] == 'not':
                str = ''
                registers_values['FLAGS'] = '0000000000000000'
                for i in registers_values[words[2]]:
                    if i == '1':
                        str += '0'
                    else:
                        str += '1'
                registers_values[words[1]] = str + ""
                print(s)
            
            elif words[0] == 'cmp':
                s += '0' * 5
                for i in range(1, 3):
                    s += registers[words[i]]
                print(s)
                if int(registers_values[words[1]]) > int(registers_values[words[2]]):
                    registers_values['FLAGS'] = '0000000000000010'
                elif int(registers_values[words[1]]) < int(registers_values[words[2]]):
                    registers_values['FLAGS'] = '0000000000000100'
                else:
                    registers_values['FLAGS'] = '0000000000000001'
            
            elif words[0] == 'jmp':
                s += '000'
                if words[1] in labels.keys():
                    s+=binary("% s" % labels[words[1]],8)

                   #   elif words[1] in variables.keys():
             #       s += variables[words[1]]
                    print(s)

            elif words[0] == 'jlt':
                if registers_values['FLAGS'] == '0000000000000100':
                    print(s)
            
            elif words[0] == 'jgt':
                if registers_values['FLAGS'] == '0000000000000010':
                    print(s)
            
            elif words[0] == 'je':
                if registers_values['FLAGS'] == '0000000000000001':
                    print(s)
            elif words[0] == 'hlt':
                s += '00000000000'
                print(s)

    else:
        if words[2][0] == '$':
            s += opcodes['mov1']
            s += registers[words[1]]
            s += binary(words[2][1::], 8)
            registers_values[words[1]] = binary(words[2][1::], 16)
            print(s)
        else:
            s += opcodes['mov2']
            if types[opcodes['mov2']] > 0:
                s += '0' * (16 - 5 - 3 * types[opcodes['mov2']])
                for i in range(1, types[opcodes['mov2']] + 1):
                    s += registers[words[i]]
            registers_values[words[1]] = registers_values[words[2]]
            print(s)


    # print(s)  # print the machine code for every command
    # print(registers_values)
    # print(variables)


for line in stdin:
    if line == '':  # If empty string is read then stop the loop
        break
    else:
        parse(line)  # perform some operation(s) on given string
'''
with open('input.txt', 'rt') as inputfile:
    command = inputfile.readline()
    while command:
        parse(command)
        # parse(command)
        command = inputfile.readline()
'''
# print(line_number)
if len(halt_instructions) == 0:
    print("Error: Halt instruction not found")
elif len(halt_instructions) > 1:
    print("Error: Multiple halt instructions found")
elif halt_instructions[0] != line_number:
    print("Error: Halt instruction not found at the end")
else:
    if len(errors) == 0:
        for i in variables:
            variables[i]=mem_address
            mem_address+=1
        if len(temp_variables)==0:
            if len(temp_labels)==0: # this will ensure that there are no undefined labels 
            #print(mem_address)
                for line in stdin:
                    if line == '':  # If empty string is read then stop the loop
                        break
                    else:
                        process(line)  # perform some operation(s) on given string
                '''
                with open('input.txt', 'rt') as inputfile:
                    command = inputfile.readline()
                    while command:
                        process(command)
                        # parse(command)
                        command = inputfile.readline()
                '''
            else:
                for i in temp_labels:
                    print(f"Error: {i} is not defined")
        else:
            for i in temp_variables:
                print(f"Error: {i} is not defined")
    else:
        for key in errors:
            print(f'Error in line {key}: {errors[key]}')

# Test working of binary() for overflow values
# print(binary(int(binary('65000', 16), 2) * int(binary('64000', 16), 2), 16))
# print(len(binary(int(binary('65000', 16), 2) + int(binary('64000', 16), 2), 16)))

# print(labels)
# print(registers_values)
# print(variables)

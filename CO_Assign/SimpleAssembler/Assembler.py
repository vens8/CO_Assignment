 # Sumit Soni 2020136
 # Aayush Kumar 2020008
 # Venkata Sai Rahul Maddula 2020149


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
line_number = 0
mem_address = 0
# Dictionary to store the values of the memory addresses
variables = {}  # Variable name as key memory address as value
labels = {}  # Label name as key and memory address as value
halt_instructions = []  # Line numbers of all occurring halt statements
errors = {}  # Line number as key and Error statement as value
flag_parse = False
temp_labels = {}  # temporary labels for accessing labels before definition
temp_variables = {}  # temporary variables for accessing labels before definition
undefined_labels = {}
undefined_variables = {}


def parse(line):
    global line_number, mem_address, flag_parse, errors, variables
    words = list(line.split())
    if len(words) != 0 and line != '\n':
        if ':' in line and words[0][-1] == ':':
            if len(words) < 2:
                line_number += 1
                errors[line_number] = "Error: Instruction not found"
            if flag_parse:
                line_number += 1
                flag_parse = False
            if words[0][:len(words[0]) - 1] not in labels and words[0][:len(words[0]) - 1] not in variables:
                if words[0][:len(words[0]) - 1] in temp_labels:
                    del temp_labels[words[0][:len(words[0]) - 1]]
                labels[words[0][:len(words[0]) - 1]] = mem_address
            else:
                errors[line_number] = "Label name already in use."
            if ':' in line:
                flag_parse = False
                parse(line[len(words[0]) + 1:])
            else:
                flag_parse = True
                mem_address += 1
                line_number += 1
                parse(line[len(words[0]) + 1:])

        elif words[0] == 'var':
            line_number += 1
            if len(words) == 2:
                if words[1] in variables.keys() or words[1] in labels.keys():
                    errors[line_number] = "Variable name already in use."
                elif words[1] not in variables.keys() and words[1] not in labels.keys():
                    if words[1] in temp_variables:
                        del temp_variables[words[1]]
                    variables[words[1]] = -1
                else:
                    errors[line_number] = "Wrong syntax used for instructions"
            else:
                errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"

        elif words[0] == 'mov' or words[0] in opcodes.keys():
            line_number += 1
            if words[0] == 'add' or words[0] == 'sub' or words[0] == 'mul' or words[0] == 'xor' or words[0] == 'or' or words[0] == 'and':
                if len(words) == 4:  # to check the number of arguments are correct or not
                    if words[1] in registers.keys() and words[2] in registers.keys() and words[3] in registers.keys():
                        mem_address += 1
                    else:
                        errors[line_number] = "Wrong syntax used for instructions"
                else:
                    errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"

            elif words[0] == 'rs' or words[0] == 'ls':
                if len(words) == 3:
                    if words[1] in registers.keys() and words[2] not in registers.keys():
                        if words[2][0] == '$' and int(words[2][1:]) >= 0 and int(words[2][1:]) <= 255:
                            mem_address += 1
                        else:
                            errors[line_number] = "Wrong value of immediate used or wrong syntax used for instructions"
                    else:
                        errors[line_number] = "Wrong syntax used for instructions"
                else:
                    errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"

            elif words[0] == 'mov':
                if len(words) == 3:
                    if (words[1] in registers and words[2][0] == '$') or (
                            words[1] in registers and words[2] in registers):
                        if words[1] in registers and words[2][0] == '$':
                            if int(words[2][1:]) >= 0 and int(words[2][1:]) <= 255:
                                mem_address += 1
                            else:
                                errors[line_number] = "Illegal immediate value type used"
                        else:
                            mem_address += 1
                    else:
                        errors[line_number] = "Wrong type of arguments used"
                else:
                    errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"

            elif words[0] == 'ld' or words[0] == 'st':
                if len(words) == 3:
                    if words[1] in registers.keys():
                        if words[2] not in variables.keys() and words[2][0] != '$' and words[
                            2] not in registers.keys() and words[2] not in labels.keys() and words[
                            2] not in temp_labels.keys():
                            temp_variables[
                                words[2]] = -1  # check if the variable definition exists
                            if words[2] not in undefined_variables:
                                undefined_variables[words[2]] = line_number
                            mem_address += 1
                        elif words[2] in variables.keys():
                            mem_address += 1
                    else:
                        errors[line_number] = "Wrong type of arguments used"
                else:
                    errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"

            elif words[0] == 'cmp' or words[0] == 'not':
                if len(words) == 3:
                    if words[1] in registers.keys() and words[2] in registers.keys():
                        mem_address += 1
                    else:
                        errors[line_number] = "Wrong type of arguments used"
                else:
                    errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"

            elif words[0] == 'jmp' or words[0] == 'jlt' or words[0] == 'jgt' or words[0] == 'je':
                if len(words) == 2:
                    if words[1] not in labels.keys():
                        temp_labels[words[1]] = mem_address
                        if words[1] not in undefined_labels:
                            undefined_labels[words[1]] = line_number
                    if words[1] in variables.keys():
                        errors[line_number] = "Wrong syntax used for instructions"
                    else:
                        mem_address += 1
                else:
                    errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"

            elif words[0] == 'hlt':
                if len(words) == 1:
                    halt_instructions.append(line_number)
                    mem_address += 1
                else:
                    errors[line_number] = "Wrong syntax used for instructions (Invalid number of arguments)"
        else:
            line_number += 1
            errors[line_number] = 'Typos in instruction name'
    else:
        errors[line_number] = "No instruction found"


# Convert a decimal (any type) into the equivalent binary of custom bits
def binary(number, bit):
    binary = bin(int(number)).replace('0b', '')[::-1]
    if len(binary) > bit:
        binary = binary[0:bit]
        return binary[::-1]

    while len(binary) < bit:
        binary += '0'
    return binary[::-1]


def process(line):
    global mem_address, line_number, variables, labels, registers_values
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
                        16) + ""  # Store only 16 bits even for overflow
                s += '0' * 2
                for i in range(1, 4):
                    s += registers[words[i]]
                print(s)

            elif words[0] == 'sub':  # subtraction
                if int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2) < 0:
                    registers_values['FLAGS'] = '0000000000001000'
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) - int(registers_values[words[3]], 2), 16) + ""
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
                s += registers[words[1]]
                s += binary(variables[words[2]], 8)
                print(s)

            elif words[0] == 'mul':  # multiply
                if int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2) < 65535:
                    registers_values['FLAGS'] = '0000000000001000'
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) * int(registers_values[words[3]], 2), 16) + ""
                s += '0' * 2
                for i in range(1, 4):
                    s += registers[words[i]]
                print(s)

            elif words[0] == 'div':  # division
                if (registers_values[words[2]]) != '0000000000000000' and int(
                        int(registers_values[words[1]], 10) / int(registers_values[words[2]], 10)) < 65535:
                    registers_values['R0'] = binary(
                        int(registers_values[words[1]], 2) / int(registers_values[words[2]], 2), 16) + ""
                    registers_values['R1'] = binary(
                        int(registers_values[words[1]], 2) % int(registers_values[words[2]], 2), 16) + ""
                    s += '0' * 5
                    for i in range(1, 3):
                        s += registers[words[i]]
                    print(s)
                else:
                    print("Error: Division by zero (not defined)")

            elif words[0] == 'ls':  # left shift
                if int(registers_values[words[1]], 2) << int(words[2][1:]) < 65535:
                    registers_values[words[1]] = binary(int(registers_values[words[1]], 2) << int(words[2][1:], 10), 16)
                    s += registers[words[1]]
                    s += binary(words[2][1::], 8)
                    registers_values[words[1]] = binary(int('0000000000000100', 2) << int('3'), 16) + ""
                    print(s)

            elif words[0] == 'rs':  # right shift
                if int(registers_values[words[1]], 2) >> int(words[2][1:]) < 65535:
                    registers_values[words[1]] = binary(int(registers_values[words[1]], 2) >> int(words[2][1:], 10), 16)
                    s += registers[words[1]]
                    s += binary(words[2][1::], 8)
                    registers_values[words[1]] = binary(int('0000000000000100', 2) << int('3'), 16) + ""
                    print(s)

            elif words[0] == 'xor':  # Exclusive OR
                if int(registers_values[words[2]], 2) ^ int(registers_values[words[3]], 2) < 65535:
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) ^ int(registers_values[words[3]], 2), 16) + ""
                    s += '0' * 2
                    for i in range(1, 4):
                        s += registers[words[i]]
                    print(s)

            elif words[0] == 'or':  # Bitwise OR
                if int(registers_values[words[2]], 2) | int(registers_values[words[3]], 2) < 65535:
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) | int(registers_values[words[3]], 2), 16) + ""
                    s += '0' * 2
                    for i in range(1, 4):
                        s += registers[words[i]]
                    print(s)

            elif words[0] == 'and':  # Bitwise AND
                if int(registers_values[words[2]], 2) & int(registers_values[words[3]], 2) < 65535:
                    registers_values[words[1]] = binary(
                        int(registers_values[words[2]], 2) & int(registers_values[words[3]], 2), 16) + ""
                    s += '0' * 2
                    for i in range(1, 4):
                        s += registers[words[i]]
                    print(s)

            elif words[0] == 'not':
                string = ''
                registers_values['FLAGS'] = '0000000000000000'
                for i in registers_values[words[2]]:
                    if i == '1':
                        string += '0'
                    else:
                        string += '1'
                registers_values[words[1]] = string + ""
                s += '0' * 5
                for i in range(1, 3):
                    s += registers[words[i]]
                print(s)

            elif words[0] == 'cmp':
                if int(registers_values[words[1]]) > int(registers_values[words[2]]):
                    registers_values['FLAGS'] = '0000000000000010'
                elif int(registers_values[words[1]]) < int(registers_values[words[2]]):
                    registers_values['FLAGS'] = '0000000000000100'
                else:
                    registers_values['FLAGS'] = '0000000000000001'
                s += '0' * 5
                for i in range(1, 3):
                    s += registers[words[i]]
                print(s)

            elif words[0] == 'jmp':
                s += '000'
                if words[1] in labels.keys():
                    s += binary("% s" % labels[words[1]], 8)
                    print(s)

            elif words[0] == 'jlt':
                # if registers_values['FLAGS'] == '0000000000000100':
                s += '000'
                if words[1] in labels.keys():
                    s += binary("% s" % labels[words[1]], 8)
                    print(s)

            elif words[0] == 'jgt':
                # if registers_values['FLAGS'] == '0000000000000010':
                s += '000'
                if words[1] in labels.keys():
                    s += binary("% s" % labels[words[1]], 8)
                    print(s)

            elif words[0] == 'je':
                # if registers_values['FLAGS'] == '0000000000000001':
                s += '000'
                if words[1] in labels.keys():
                    s += binary("% s" % labels[words[1]], 8)
                    print(s)

            elif words[0] == 'hlt':
                s += '00000000000'
                print(s)

    else:
        if words[2][0] == '$':
            s += opcodes['mov1']
            s += registers[words[1]]
            s += binary(words[2][1::], 8)
            registers_values[words[1]] = binary(words[2][1::], 16) + ""
            print(s)
        else:
            s += opcodes['mov2']
            if types[opcodes['mov2']] > 0:
                s += '0' * (16 - 5 - 3 * types[opcodes['mov2']])
                for i in range(1, types[opcodes['mov2']] + 1):
                    s += registers[words[i]]
            registers_values[words[1]] = registers_values[words[2]] + ""
            print(s)

'''
with open('input.txt', 'rt') as inputfile:
    command = inputfile.readline()
    while command:
        parse(command)
        # parse(command)
        command = inputfile.readline()
'''
input_code = ['mov R0 $5','mov R1 $10','mov R2 $1','label: add R0 R0 R2','cmp R0 R1','jlt label','hlt']
'''
while True:
    try:
        line = input()
        input_code.append(line)
    except EOFError:
        break
'''
for line in input_code:
    parse(line)

# print(line_number)
if len(halt_instructions) == 0:
    print(f"Error in line {line_number}: Halt instruction not found")
elif len(halt_instructions) > 1:
    print("Error: Multiple halt instructions found. ")
    for line in halt_instructions:
        print(f"Halt statement found at line {line}")
elif halt_instructions[0] != line_number:
    print(f"Error in line {line_number}: Halt instruction not found at the end")
else:
    if len(errors) == 0:
        for i in variables:
            variables[i] = mem_address
            mem_address += 1
        if len(temp_variables) == 0:
            if len(temp_labels) == 0:  # this will ensure that there are no undefined labels
                # print(mem_address)
                '''
                with open('input.txt', 'rt') as inputfile:
                    command = inputfile.readline()
                    while command:
                        process(command)
                        # parse(command)
                        command = inputfile.readline()
                '''
                for line in input_code:
                    process(line)
            else:
                for i in undefined_labels:
                    if i in temp_labels:
                        print(f"Error in line {undefined_labels[i]}: {i} is not defined")
        else:
            for i in undefined_variables:
                if i in temp_variables:
                    print(f"Error in line {undefined_variables[i]}: {i} is not defined")
for key in errors:
    print(f'Error in line {key}: {errors[key]}')

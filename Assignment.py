#! /usr/bin/python
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

labels = {}

# Dictionary to store the values of the memory addresses
variables = {}

line_no = 0
address_no = 0
memory_addresses = {}


def parse(command):
    pass


looped = False


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
    global registers_values
    registers_values['FLAGS'] = '0000000000000000'  # Reset the value of flags after every operation
    s = ""
    words = list(command.split())
    if len(command) > 1 or words[0] != 'var' or words[0][-1] != ':':
        if words[0] != 'mov':
            # try to use 'try/except' for catching dictionary key errors for error generation test cases.
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
            # elif words[0] = ''
        else:
            if words[2][0] == '$':
                s += opcodes['mov1']
                s += registers[words[1]]
                s += binary(words[2][1::], 8)  # convert to 8 bit binary
                registers_values[words[1]] = binary(words[2][1::], 16)
            else:
                s += opcodes['mov2']
                if types[opcodes['mov2']] > 0:
                    s += '0' * (16 - 5 - 3 * types[opcodes['mov2']])
                    for i in range(1, types[opcodes['mov2']] + 1):
                        s += registers[words[i]]

                registers_values[words[1]] = registers_values[words[2]]

        # print(s)  # print the machine code for every command
    print(registers_values)


# parse()

'''for line in stdin:
    if line == '':  # If empty string is read then stop the loop
        break
    process(line)  # perform some operation(s) on given string'''


with open('input.txt', 'rt') as inputfile:
    command = inputfile.readline()
    separated = list(command.split())
    while command:
        process(command)
        # parse(command)
        command = inputfile.readline()


# Test working of binary() for overflow values
# print(binary(int(binary('65000', 16), 2) * int(binary('64000', 16), 2), 16))
# print(len(binary(int(binary('65000', 16), 2) + int(binary('64000', 16), 2), 16)))

# print(labels)
# print(registers_values)
# print(variables)

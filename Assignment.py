
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
    'R0': 0000000000000000,
    'R1': 0000000000000000,
    'R2': 0000000000000000,
    'R3': 0000000000000000,
    'R4': 0000000000000000,
    'R5': 0000000000000000,
    'R6': 0000000000000000,
    'FLAGS': 0000000000000000,
}

# Dictionary to store the values of the memory addresses
variables = {}


# Convert a string decimal into the equivalent binary of custom bits
def binary(number, bit):
    binary = bin(int(number)).replace('0b', '')[::-1]
    while len(binary) < bit:
        binary += '0'
    return binary[::-1]


def process(command):
    s = ""
    words = list(command.split())
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
            elif words[0] == 'add':  # addition
                registers_values[words[1]] = registers_values[words[2]] + registers_values[words[3]]
            elif words[0] == 'sub':  # subtraction
                registers_values[words[1]] = registers_values[words[2]] - registers_values[words[3]]
            elif words[0] == 'ld':  # load
                registers_values[words[1]] = words[2][1::]
            elif words[0] == 'st':  # store
                variables[words[2]] = registers_values[words[1]]
            elif words[0] == 'mul': # multiply
                registers_values[words[1]] = registers_values[words[2]] * registers_values[words[3]]
            elif words[0] == 'div':  # division
                registers_values[words[1]] = registers_values[words[1]] / registers_values[words[2]] 
            elif words[0] == 'rs':  # Right Shift
                registers_values[words[1]] = registers_values[words[1]] >> int(words[2][1::])
            elif words[0] == 'ls':  # left Shift
                registers_values[words[1]] = registers_values[words[1]] << int(words[2][1::])
            elif words[0] == 'xor':  # Exclusive OR
                registers_values[words[1]] = registers_values[words[2]] ^ registers_values[words[3]]
            elif words[0] == 'or':   # OR operator
                registers_values[words[1]] = registers_values[words[2]] | registers_values[words[3]]
            elif words[0] == 'and':  # AND operator
                registers_values[words[1]] = registers_values[words[2]] & registers_values[words[3]]
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


with open('input.txt', 'rt') as inputfile:
    command = inputfile.readline()
    while command:
        process(command)
        command = inputfile.readline()

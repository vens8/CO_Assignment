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
    '00101': 2,
    '01111': 1,
    '10000': 1,
    '10001': 1,
    '10010': 1,
    '00110': 3,
    '01010': 3,
    '01011': 3,
    '01100': 3,
    '10011': 0,
}

registers = {
    'R0': '001',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111'
}
R0 = R1 = R2 = R3 = R4 = R5 = R6 = R7 = None


def process(command):
    words = list(command.split())
    if words[0] != 'mov':
        



with open('input.txt', 'rt') as inputfile:
    command = inputfile.readline()
    while command:
        process(command)
        command = inputfile.readline()
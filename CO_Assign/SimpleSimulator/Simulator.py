registers = {
    '000': 'R0',
    '001': 'R1',
    '010': 'R2',
    '011': 'R3',
    '100': 'R4',
    '101': 'R5',
    '110': 'R6',
    '111': 'FLAGS'
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
registers = {
    '000': 'R0',
    '001': 'R1',
    '010': 'R2',
    '011': 'R3',
    '100': 'R4',
    '101': 'R5',
    '110': 'R6',
    '111': 'FLAGS'
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
    if line[:6] == 'add':
        registers_values[registers[line[6:9]]] = registers_values[registers[line[8:11]]] + registers_values[registers[line[10:13]]]
        print(binary(input_code.index(line), 8).join(str(value) for value in registers_values.items()))


# List to store the input binary machine codes where each machine code has its index as memory address
input_code = []

while True:
    try:
        line = input()
        input_code.append(line)
    except EOFError:
        break

for line in input_code:
    process(line)

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
    if line[:6] == 'add':
        registers_values[registers[line[6:9]]] = registers_values[registers[line[8:11]]] + registers_values[registers[line[10:13]]]
        print(binary(input_code.index(line), 8).join(str(value) for value in registers_values.items()))


# List to store the input binary machine codes where each machine code has its index as memory address
input_code = []

while True:
    try:
        line = input()
        input_code.append(line)
    except EOFError:
        break

for line in input_code:
    process(line)

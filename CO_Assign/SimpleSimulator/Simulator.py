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

variables = {}


# Convert a string decimal into the equivalent binary of custom bits
def binary(number, bit):
    binary = bin(int(number)).replace('0b', '')[::-1]
    if len(binary) > bit:
        binary = binary[0:bit]
        return binary[::-1]

    while len(binary) < bit:
        binary += '0'
    return binary[::-1]


# Store memory address for variables
def parse(line):
    pass


def process(line):
    if line[:5] == '00000':  # Add
        if int(registers_values[registers[line[10:13]]], 2) + int(registers_values[registers[line[13:16]]], 2) > 65535:
            registers_values['FLAGS'] = '0000000000001000'
        registers_values[registers[line[7:10]]] = binary(
            int(registers_values[registers[line[10:13]]], 2) + int(registers_values[registers[line[13:16]]], 2), 16)
    elif line[:5] == '00001':  # Subtract
        if int(registers_values[registers[line[10:13]]], 2) - int(registers_values[registers[line[13:16]]], 2) < 0:
            registers_values['FLAGS'] = '0000000000001000'
        registers_values[registers[line[7:10]]] = binary(
            int(registers_values[registers[line[10:13]]], 2) - int(registers_values[registers[line[13:16]]], 2), 16)
    elif line[:5] == '00010':  # Move immediate
        registers_values[registers[line[5:8]]] = binary(int(line[8:16], 2), 16)
    elif line[:5] == '00011':  # Move register
        registers_values[registers[line[10:13]]] = registers_values[registers[line[13:16]]]
    elif line[:5] == '00100':  # Load from variable to register
        registers_values[registers[line[10:13]]] = variables[line[8:16]]
    elif line[:5] == '00101':  # Store from register to variable
        variables[line[8:16]] = registers_values[registers[line[10:13]]]
    elif line[:5] == '01110':  # Compare
        if int(registers_values[registers[line[10:13]]], 2) > int(registers_values[registers[line[13:16]]], 2):
            registers_values['FLAGS'] = '0000000000000010'
        elif int(registers_values[registers[line[10:13]]], 2) < int(registers_values[registers[line[13:16]]], 2):
            registers_values['FLAGS'] = '0000000000000100'
        else:
            registers_values['FLAGS'] = '0000000000000001'
    if line[:5] != '01110':
        registers_values['FLAGS'] = '0000000000000000'  # Flags reset after every non-compare instruction
    print(binary(input_code.index(line), 8), " ".join(str(value) for value in registers_values.values()))


# List to store the input binary machine codes where each machine code has its index as memory address
input_code = [
    '0001000100000100', '0001001000000100', '0111000000001010', '0001100000011111', '0001010000000001',
    '0111000000011100', '1000100000000111', '1001100000000000']
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


for line in input_code:
    process(line)

# Memory dump
for line in input_code:
    print(line)

# Print the empty memory dumps to fill the 256 lines
for dump in range(0, 256 - len(input_code)):
    print('0000000000000000')

# Sumit Soni 2020136
# Aayush Kumar 2020008
# Venkata Sai Rahul Maddula 2020149

import matplotlib.pyplot as plt

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

variables = {}   # memory address of variables mapped to their value
mem_address, cycle = 0, 0   # initialized variables to store the number of cycles amd mem_address for every line
x, y = [], []  # a pair of lists to store the values of the above variables for the plotting of the scatter plot graph


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
    global mem_address, variables, cycle
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
        registers_values[registers[line[5:8]]] = variables[line[8:16]] + ""

    elif line[:5] == '00101':  # Store from register to variable
        variables[line[8:16]] = registers_values[registers[line[5:8]]] + ""

    elif line[:5] == '01110':  # Compare
        if int(registers_values[registers[line[10:13]]], 2) > int(registers_values[registers[line[13:16]]], 2):
            registers_values['FLAGS'] = '0000000000000010'
        elif int(registers_values[registers[line[10:13]]], 2) < int(registers_values[registers[line[13:16]]], 2):
            registers_values['FLAGS'] = '0000000000000100'
        else:
            registers_values['FLAGS'] = '0000000000000001'

    elif line[:5] == '00110':  # Multiply
        if int(registers_values[registers[line[10:13]]], 2) * int(registers_values[registers[line[13:16]]], 2) > 65535:
            registers_values['FLAGS'] = '0000000000001000'
        registers_values[registers[line[7:10]]] = binary(
            int(registers_values[registers[line[10:13]]], 2) * int(registers_values[registers[line[13:16]]], 2), 16)

    elif line[:5] == '00111':  # Divide
        if int(registers_values[registers[line[10:13]]], 2) / int(registers_values[registers[line[13:16]]], 2) <= 65535:
            registers_values['R0'] = binary(
                int(registers_values[registers[line[10:13]]], 2) / int(registers_values[registers[line[13:16]]], 2), 16)
            registers_values['R1'] = binary(
                int(registers_values[registers[line[10:13]]], 2) % int(registers_values[registers[line[13:16]]], 2), 16)
        else:
            registers_values['FLAGS'] = '0000000000001000'

    elif line[:5] == '01001':  # Left shift
        if int(registers_values[registers[line[5:8]]], 2) << int(registers_values[registers[line[8:16]]], 2) <= 65535:
            registers_values[registers[line[5:8]]] = binary(
                int(registers_values[registers[line[5:8]]], 2) << int(registers_values[registers[line[8:16]]], 2), 16)
        else:
            registers_values['FLAGS'] = '0000000000001000'

    elif line[:5] == '01000':  # Right shift
        if int(registers_values[registers[line[5:8]]], 2) >> int(registers_values[registers[line[8:16]]], 2) <= 65535:
            registers_values[registers[line[5:8]]] = binary(
                int(registers_values[registers[line[5:8]]], 2) >> int(registers_values[registers[line[8:16]]], 2), 16)
        else:
            registers_values['FLAGS'] = '0000000000001000'

    elif line[:5] == '01010':  # Exclusive OR
        registers_values[registers[line[7:10]]] = binary(
            int(registers_values[registers[line[10:13]]], 2) ^ int(registers_values[registers[line[13:16]]], 2), 16)

    elif line[:5] == '01011':  # Bitwise OR
        registers_values[registers[line[7:10]]] = binary(
            int(registers_values[registers[line[10:13]]], 2) | int(registers_values[registers[line[13:16]]], 2), 16)

    elif line[:5] == '01100':  # Bitwise AND
        registers_values[registers[line[7:10]]] = binary(
            int(registers_values[registers[line[10:13]]], 2) & int(registers_values[registers[line[13:16]]], 2), 16)

    elif line[:5] == '01101':  # Invert
        string = ''
        for i in registers_values[registers[line[13:16]]]:
            if i == '1':
                string += '0'
            else:
                string += '1'
        registers_values[registers[line[10:13]]] = string + ""

    elif line[:5] == '01111':  # Unconditional Jump
        print(binary(mem_address, 8), " ".join(str(value) for value in registers_values.values()))
        mem_address = int(line[8:16], 2)
        y.append(mem_address)
        x.append(cycle)
        cycle += 1
        return mem_address

    elif line[:5] == '10000':  # Jump if less than
        if registers_values['FLAGS'] == '0000000000000100':
            print(binary(mem_address, 8), " ".join(str(value) for value in registers_values.values()))
            mem_address = int(line[8:16], 2)
            y.append(mem_address)
            x.append(cycle)
            cycle += 1
            return mem_address

    elif line[:5] == '10001':  # Jump if greater than
        if registers_values['FLAGS'] == '0000000000000010':
            print(binary(mem_address, 8), " ".join(str(value) for value in registers_values.values()))
            mem_address = int(line[8:16], 2)
            y.append(mem_address)
            x.append(cycle)
            cycle += 1
            return mem_address

    elif line[:5] == '10010':  # Jump if equal
        if registers_values['FLAGS'] == '0000000000000001':
            print(binary(mem_address, 8), " ".join(str(value) for value in registers_values.values()))
            mem_address = int(line[8:16], 2)
            y.append(mem_address)
            x.append(cycle)
            cycle += 1
            return mem_address

    if line[:5] != '01110':
        registers_values['FLAGS'] = '0000000000000000'  # Flags reset after every non-compare instruction
    print(binary(mem_address, 8), " ".join(str(value) for value in registers_values.values()))
    x.append(cycle)
    y.append(mem_address)
    mem_address += 1
    cycle += 1
    return mem_address


# List to store the input binary machine codes where each machine code has its index as memory address
input_code = []

# Take input
while True:
    try:
        line = input()
        input_code.append(line)
    except EOFError:
        break

i = 0
while input_code[i] != '1001100000000000':
    i = process(input_code[i])

# Print for halt at the end
x.append(cycle)
y.append(mem_address)
print(binary(mem_address, 8), " ".join(str(value) for value in registers_values.values()))

# Memory dump
for line in input_code:
    print(line)

for variable in variables.values():
    print(variable)

# Fill remaining memory dump of 256 lines
for dump in range(0, 256 - len(input_code) - len(variables)):
    print('0000000000000000')

# Plot the cycles on x axis and memory addresses on y axis and saves the image in the same directory as Bonus.py
plt.scatter(x, y)
plt.savefig('bonus.png', dpi=100)

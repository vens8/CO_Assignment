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
labels={}
mem_address=-1
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
    global mem_address
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
    
    elif line[:5] == '00110':  # multiply
        if int(registers_values[registers[line[10:13]]], 2) * int(registers_values[registers[line[13:16]]], 2) > 65535:
            registers_values['FLAGS'] = '0000000000001000'
        registers_values[registers[line[7:10]]] = binary(
            int(registers_values[registers[line[10:13]]], 2) * int(registers_values[registers[line[13:16]]], 2), 16)
    
    elif line[:5] == '00111':  # division
        if (registers_values[registers[line[10:13]]] / registers_values[registers[line[13:16]]] < 65535):
            registers_values['R0'] = binary( int(registers_values[registers[line[10:13]],2] / int(registers_values[registers[line[13:16]]],2)), 16)
            registers_values['R1'] = binary( int(registers_values[registers[line[10:13]],2] % int(registers_values[registers[line[13:16]]],2)), 16)        
            
        else:
            registers_values['FLAGS']='0000000000001000'
    
    elif line[:5] == '01001':  # left shift
        if int(registers_values[registers[line[5:8]]],2) << int(registers_values[registers[line[8:16]]],2)  < 65535:
            registers_values[registers[line[5:8]]] = binary(int(registers_values[registers[line[5:8]]],2) << int(registers_values[registers[line[8:16]]],2), 16)
        else:
            registers_values['FLAGS']='0000000000001000'

    elif line[:5] == '01000':  # right shift
        if int(registers_values[registers[line[5:8]]],2) >> int(registers_values[registers[line[8:16]]],2)  < 65535:
            registers_values[registers[line[5:8]]] = binary(int(registers_values[registers[line[5:8]]],2) >> int(registers_values[registers[line[8:16]]],2), 16)
        else:
            registers_values['FLAGS']='0000000000001000'

    elif line[:5] == '01010':  # Exclusive OR
        registers_values[registers[line[7:10]]] = binary(int(registers_values[registers[line[10:13]]], 2) ^ int(registers_values[registers[line[13:16]]], 2), 16)
    
    elif line[:5] == '01011':  # Bitwise OR
        registers_values[registers[line[7:10]]] = binary(int(registers_values[registers[line[10:13]]], 2) | int(registers_values[registers[line[13:16]]], 2), 16)
    
    elif line[:5] == '01100':  # Bitwise AND
        registers_values[registers[line[7:10]]] = binary(int(registers_values[registers[line[10:13]]], 2) & int(registers_values[registers[line[13:16]]], 2), 16)
    
    elif line[:5] == '01101': #invert
        string = ''
        for i in registers_values[registers[line[13:16]]]:
            if i == '1':
                string += '0'
            else:
                string += '1'
        registers_values[registers[line[10:13]]] = string + ""
    
    elif line[:5] == '01111':  #unconditional jump
        return int(line[8:16],2)   

    elif line[:5] == '10000':   #jump if less than
        if(labels[mem_address])
            if registers_values['FLAGS'] == '0000000000000100':
                labels[mem_address]=True
                mem_address=int(line[8:16],2)
                print(binary(input_code.index(line), 8), " ".join(str(value) for value in registers_values.values()))
            #return int(line[8:16],2)
    '''        
    elif words[0] == 'jgt':
        # if registers_values['FLAGS'] == '0000000000000010'
        if words[1] in labels.keys():
            s += binary("% s" % labels[words[1]], 8)
            print(s
    elif words[0] == 'je':
        # if registers_values['FLAGS'] == '0000000000000001':
        s += '000'
        if words[1] in labels.keys():
            s += binary("% s" % labels[words[1]], 8)
            print(s)
'''
    if line[:5] != '01110':
        registers_values['FLAGS'] = '0000000000000000'  # Flags reset after every non-compare instruction
    print(binary(input_code[index(line)], 8), " ".join(str(value) for value in registers_values.values()))
    mem_address+=1
    return mem_address


# List to store the input binary machine codes where each machine code has its index as memory address
input_code = ['0001000000000101','0001000100001010','0001001000000001','0000000000000010','0111000000000001','1000000000000011','1001100000000000']
'''

while True:
    try:
        line = input()
        input_code.append(line)
    except EOFError:
        break
'''
'''
for i in range(len(input_codes)):
    if(input_codes[i][0:5]=='01111' or input_codes[i][0:5]=='10000' or input_codes[i][0:5]=='10001' or input_codes[i][0:5]=='10010'):
        loops[binary(i,8)]=False
'''
i=0
while(input_code[i]!='1001100000000000'):
    i=process(input_code[i])
    

# Memory dump
for line in input_code:
    print(line)

# Print the empty memory dumps to fill the 256 lines
for dump in range(0, 256 - len(input_code)):
    print('0000000000000000')

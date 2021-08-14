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

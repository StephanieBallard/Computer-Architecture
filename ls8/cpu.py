"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # Memory
        self.register = [0] * 8 # Registers
        self.PC = 0 # Program Counter
        
    def ram_read(self, MAR):
        ''' Return a value at memory address register (MAR) '''
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        ''' Write value memory data register to address memory address register (MAR) '''
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        # Read program data
        address = 0
        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()

                    if line == '' or line[0] == "#":
                        continue

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)

                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

        # address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
        

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        HLT = 0b00000001   # 1
        LDI = 0b10000010   # 130
        PRN = 0b01000111   # 71
        MUL = 0b10100010

        while running:
            ir = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if ir == HLT:
                running = False

            elif ir == LDI:
                self.register[operand_a] = operand_b
                self.PC += 3

            elif ir == PRN:
                print(self.register[operand_a])
                self.PC += 2
            
            elif ir == MUL:
                self.alu("MUL", operand_a,operand_b)
                self.PC += 3


# Monday:
# - [X] Inventory what is here
# - [X] Implement the `CPU` constructor
# - [X] Add RAM functions `ram_read()` and `ram_write()`
# - [X] Implement the core of `run()`
# - [X] Implement the `HLT` instruction handler
# - [X] Add the `LDI` instruction
# - [X] Add the `PRN` instruction
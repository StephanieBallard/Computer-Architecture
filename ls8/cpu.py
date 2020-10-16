"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # Memory
        self.reg = [0] * 8 # Registers
        self.PC = 0 # Program Counter
        self.FL = 0b00000000
        
    def ram_read(self, MAR):
        ''' Return a value at memory address register (MAR) '''
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
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
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 0b00000001
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
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        HLT = 0b00000001   # 1
        LDI = 0b10000010   # 130
        PRN = 0b01000111   # 71
        MUL = 0b10100010
        ADD = 0b10100000
        SUB = 0b10100001

        SP = 7
        PUSH = 0b01000101
        POP = 0b01000110

        CALL = 0b01010000
        RET  = 0b00010001
        
        CMP = 0b10100111
        JMP = 0b01010100

        JEQ = 0b01010101
        JNE = 0b01010110

        while running:
            ir = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)

            if ir == HLT:
                running = False

            elif ir == LDI:
                self.reg[operand_a] = operand_b
                self.PC += 3

            elif ir == PRN:
                print(self.reg[operand_a])
                self.PC += 2
            
            elif ir == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.PC += 3
            
            elif ir == ADD:
                self.alu("ADD", operand_a,operand_b)
                self.PC += 3
            
            elif ir == SUB:
                self.alu("SUB", operand_a,operand_b)
                self.PC += 3

            elif ir == PUSH:
                # self.trace()
                SP -= 1
                self.ram_write(SP, self.reg[operand_a])
                self.PC += 2
            
            elif ir == POP:
                # self.trace()
                self.reg[operand_a] = self.ram[SP]
                SP += 1
                self.PC += 2

            elif ir == CALL:
                value = self.PC + 2
                SP -= 1 # decrement Stack pointer bc we are pushing off thee stack
                self.ram_write(SP, value)
                self.PC = self.reg[operand_a]

            elif ir == RET:
                self.PC = self.ram[SP]
                SP += 1

            elif ir == JMP:
                self.PC = self.reg[operand_a]

            elif ir == JEQ:
                if self.FL & 0b00000001 == 1:
                    self.PC = self.reg[operand_a]
                else:
                    self.PC += 2

            elif ir == JNE:
                if self.FL & 0b00000001 != 1:
                    self.PC = self.reg[operand_a]
                else:
                    self.PC += 2
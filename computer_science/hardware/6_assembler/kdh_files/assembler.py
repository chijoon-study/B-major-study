class Parser:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.instructions = f.readlines()
        self.instructions = list(map(lambda s: s.strip(), self.instructions))
        self.input_idx = 0
        self.output_idx = 0
        self.ins_type = ''
        print(self.instructions)

    def hasMoreLines(self) -> bool:
        self.input_idx += 1
        try:
            self.instructions[self.input_idx]
            return True
        except IndexError:
            return False

    def advance(self):
        while self.instructions[self.input_idx] == '' or self.instructions[self.input_idx][:2] == '//':
            print(self.instructions[self.input_idx])
            self.input_idx += 1

    def instructionType(self) -> str:
        ins = self.instructions[self.input_idx]
        if ins[0] == '@':
            self.ins_type = 'A'
        elif ins[0] == '(':
            self.ins_type = 'L'
        else:
            self.ins_type = 'C'

        return self.ins_type

    def symbol(self) -> str:
        if self.ins_type not in ['A', 'L']:
            print("current instruction's type should be 'A' or 'L'")
            return
        elif self.ins_type == 'A':
            return self.instructions[self.input_idx][1:]
        elif self.ins_type == 'L':
            return self.instructions[self.input_idx][1:-1]

    def dest(self) -> str:
        if self.ins_type != 'C':
            print("current instruction's type should be 'C'")
            return

        dst_rest = self.instructions[self.input_idx].split('=')
        if len(dst_rest) == 1:
            return 'null'
        else:
            return dst_rest[0]

    def comp(self) -> str:
        if self.ins_type != 'C':
            print("current instruction's type should be 'C'")
            return

        is_dest_not_null = '=' in self.instructions[self.input_idx]
        is_jump_not_null = ';' in self.instructions[self.input_idx]

        if is_dest_not_null and is_jump_not_null:
            return self.instructions[self.input_idx].split('=')[1].split(';')[0]
        elif is_dest_not_null:
            return self.instructions[self.input_idx].split('=')[1]
        elif is_jump_not_null:
            return self.instructions[self.input_idx].split(';')[0]

    def jump(self) -> str:
        if self.ins_type != 'C':
            print("current instruction's type should be 'C'")
            return

        rest_jmp = self.instructions[self.input_idx].split(';')
        if len(rest_jmp) == 1:
            return 'null'
        else:
            return rest_jmp[1]


class SymbolTable:
    def __init__(self):
        self.symbols = {'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7, 'R8': 8, 'R8': 8,
                        'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15, 'SCREEN': 16384,
                        'KBD': 24576, 'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4}
        self.var_addr = 16

    def addEntry(self, symbol: str, address: int = None):
        if address is None:
            self.symbols[symbol] = self.var_addr
            self.var_addr += 1
        else:
            self.symbols[symbol] = address

    def contains(self, symbol: str) -> bool:
        return symbol in self.symbols

    def getAddress(self, symbol: str) -> int:
        return self.symbols[symbol]


def bin_A(symbol: str):
    Bin = bin(int(symbol))[2:]
    return '0' * (15 - len(Bin)) + Bin


def bin_C(dst, cmp, jmp):
    Bin = '1110'
    comp_map = {'0': '101010', '1': '111111', '-1': '111010', 'D': '001100', 'A': '110000', '!D': '001101',
                '!A': '110001', '-D': '001111', '-A': '110011', 'D+1': '011111', 'A+1': '110111', 'D-1': '001110',
                'A-1': '110010', 'D+A': '000010', 'D-A': '010011', 'A-D': '000111', 'D&A': '000000', 'D|A': '010101'}
    jump_map = {'JGT': '001', 'JEQ': '010', 'JGE': '011', 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}
    if 'M' in cmp:
        Bin = Bin.replace('0', '1')
        cmp = cmp.replace('M', 'A')

    Bin += comp_map[cmp]

    if dst == 'null':
        Bin += '000'
    else:
        Bin += '1' if 'A' in dst else '0'
        Bin += '1' if 'D' in dst else '0'
        Bin += '1' if 'M' in dst else '0'

    if jmp == 'null':
        Bin += '000'
    else:
        Bin += jump_map[jmp]

    return Bin


parser = Parser("Max.asm")
table = SymbolTable()

while parser.hasMoreLines():
    parser.advance()
    T = parser.instructionType()
    if T == 'L':
        table.addEntry(parser.symbol(), parser.output_idx)
        continue
    parser.output_idx += 1

parser.input_idx = 0
parser.output_idx = 0

with open('Rect.hack', 'w') as f:
    while parser.hasMoreLines():
        parser.advance()
        T = parser.instructionType()
        print(parser.instructions[parser.input_idx])
        if T == 'A':
            symbol = parser.symbol()
            if not symbol.isnumeric():
                if not table.contains(symbol):
                    table.addEntry(symbol)
                symbol = table.getAddress(symbol)
            f.write('0' + bin_A(symbol) + '\n')
        elif T == 'C':
            f.write(bin_C(parser.dest(), parser.comp(), parser.jump()) + '\n')

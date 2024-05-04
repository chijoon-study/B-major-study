import sys


class Parser:
    def __init__(self, path):
        self.file = open(path, 'r')
        self.line = ''
        self.command_type = ''
        self.command_type_dict = {
            'push': 'C_PUSH',
            'pop': 'C_POP',
            'add': 'C_ARITHMETIC',
            'sub': 'C_ARITHMETIC',
            'neg': 'C_ARITHMETIC',
            'eq': 'C_ARITHMETIC',
            'gt': 'C_ARITHMETIC',
            'lt': 'C_ARITHMETIC',
            'and': 'C_ARITHMETIC',
            'or': 'C_ARITHMETIC',
            'not': 'C_ARITHMETIC',
            'label': 'C_LABEL',
            'goto': 'C_GOTO',
            'if-goto': 'C_IF',
            'function': 'C_FUNCTION',
            'return': 'C_RETURN',
            'call': 'C_CALL'
        }

    def hasMoreLines(self):
        self.line = self.file.readline().strip()
        return not self.line == ''

    def advance(self):
        while True:
            if self.line.startswith('//') or self.line == '':
                self.line = self.file.readline().strip()
                continue
            return

    def commandType(self):
        self.command_type = self.command_type_dict.get(self.line.split()[0])
        return self.command_type

    def arg1(self):
        if self.command_type == 'C_ARITHMETIC':
            return self.line

        return self.line.split()[1]

    def arg2(self):
        if self.command_type == 'C_ARITHMETIC':
            return None

        return self.line.split()[2]

    def close(self):
        self.file.close()


class CodeWriter:
    def __init__(self, path):
        self.file = open(path, 'w')
        self.bool_count = 0

        self.__address_dict = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'pointer': 3,  # R3~R4. THIS == R3
            'temp': 5,  # R5~R12
            'constant': None,  # 주소 안씀
            'static': None  # 주소 대신 별개의 값
        }

    def init_sys(self):
        # Init Sys
        self.write('@256')
        self.write('D=A')
        self.write('@SP')
        self.write('M=D')

    def write(self, string) -> None:
        self.file.write(f"{string}\n")

    def writeArithmetic(self, command):
        if command not in ['neg', 'not']:
            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

        self.write('@SP')
        self.write('M=M-1')
        self.write('A=M')

        if command == 'add':
            self.write('M=M+D')
        elif command == 'sub':
            self.write('M=M-D')
        elif command == 'neg':
            self.write('M=-M')
        elif command == 'and':
            self.write('M=M&D')
        elif command == 'or':
            self.write('M=M|D')
        elif command == 'not':
            self.write('M=!M')
        elif command in ['eq', 'gt', 'lt']:
            self.write('D=M-D')
            self.write(f'@BOOL_{self.bool_count}')
            if command == 'eq':
                self.write('D;JEQ')
            if command == 'gt':
                self.write('D;JGT')
            if command == 'lt':
                self.write('D;JLT')
            self.write('D=0')
            self.write(f'@BOOL_SKIP_{self.bool_count}')
            self.write('0;JMP')
            self.write(f'(BOOL_{self.bool_count})')
            self.write('D=-1')
            self.write(f'(BOOL_SKIP_{self.bool_count})')
            self.write('@SP')
            self.write('A=M')
            self.write('M=D')
            self.bool_count += 1

        else:
            raise Exception("unregonized command. command should be in [add, sub, neg, eq, gt, lt, and, or, not]")

        self.write('@SP')
        self.write('M=M+1')

    def writePushPop(self, command_type, segment, index):
        self.write_segment_address(segment, index)
        if command_type == 'C_PUSH':
            if segment == 'constant':
                self.write('D=A')
            else:
                self.write('D=M')
            self.write('@SP')
            self.write('A=M')
            self.write('M=D')
            self.write('@SP')
            self.write('M=M+1')
        elif command_type == 'C_POP':
            self.write('D=A')
            self.write('@R13')
            self.write('M=D')

            self.write('@SP')
            self.write('M=M-1')
            self.write('A=M')
            self.write('D=M')

            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        else:
            raise Exception("unregonized command. command type should be in [C_PUSH, C_POP]")

    def write_segment_address(self, segment, index):
        address = self.__address_dict[segment]
        if segment == 'constant':
            self.write(f'@{index}')
        elif segment == 'static':
            self.write(f'@static.{index}')
        elif segment in ['pointer', 'temp']:
            self.write('@R' + str(address + int(index)))
        elif segment in ['local', 'argument', 'this', 'that']:
            self.write(f'@{address}')
            self.write('D=M')
            self.write(f'@{index}')
            self.write('A=A+D')
        else:
            raise Exception(
                "unregonized segment. segment type should be in [local, argument, this, that, pointer, temp, constant, static]")

    def close(self):
        self.file.close()


class VMTranslator:
    def __init__(self, args: list) -> None:
        if len(args) != 2:
            raise Exception('there should be one argument that present target VM file')

        self.vm_file = args[1]
        self.parser = Parser(self.vm_file)
        output_file_name  = self.vm_file[:-3] + '.asm'
        self.writer = CodeWriter(output_file_name)

    def translate(self):
        while self.parser.hasMoreLines():
            self.parser.advance()
            command_type= self.parser.commandType()
            if command_type == 'C_ARITHMETIC':
                self.writer.writeArithmetic(self.parser.arg1())
            elif command_type in ['C_POP', 'C_PUSH']:
                self.writer.writePushPop(command_type, self.parser.arg1(), self.parser.arg2())

        self.parser.close()
        self.writer.close()


VMTranslator(sys.argv).translate()



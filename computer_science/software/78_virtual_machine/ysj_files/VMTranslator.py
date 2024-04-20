import sys
import os
import glob

"""
이전 코드가 잘 안되서, 다시 구현하는 중
이번에는 유효성 검사, Enum같이 불필요한거 제외하고, 딱 필요한거만 작성할 예정
"""


# SYS 호출 안하면 성공하는데,
# SYS 호출하면 SimoleFunction 실패함


class Parser:
    def __init__(self, path) -> None:
        self.file = open(path, 'r')
        self.command_type = None
        self.argument0 = None  # 명령어
        self.argument1 = None  # arg 1
        self.argument2 = None  # arg 2

    def hasMoreLines(self) -> bool:
        """
        다음 명령어가 있는지 확인하면서 다음 결과 바로 앞까지 이동.
        변경 조회 기능이 합쳐져있기는 한데, 주석은 어차피 무시하는거고, 멱등성이 보장되니까 괜찮지 않을까?
        """
        while True:
            current_position = self.file.tell()
            line = self.file.readline()
            if line == '':
                return False
            if not (line.lstrip().startswith('//') or line.startswith('\n')):
                self.file.seek(current_position)
                return True

    def advance(self) -> None:
        """
        현재 명령을 다음 명령으로 파일 포인터를 이동.
        초기화 직후의 현재 명령은 빈 상태.
        hasMoreLines() 가 True일때만 사용되어야 함.
        """
        command = self.file.readline()
        cmd_split = command.split()
        self.command_type = self.command_dict[cmd_split[0]]

        self.argument0 = cmd_split[0]
        if self.command_type in ['C_ARITHMETIC', 'C_RETURN']:  # 인수가 없는 경우
            return
        self.argument1 = cmd_split[1]  # 그 외에는 최소 1개씩은 있음
        if self.command_type in ['C_POP', 'C_PUSH', 'C_FUNCTION', 'C_CALL']:  # 인수가 2개인 경우
            self.argument2 = cmd_split[2]
            return

    def commandType(self) -> str:
        return self.command_type

    def arg1(self) -> str:
        if self.command_type == "C_ARITHMETIC":  # C_RETURN은 arg1() 호출 안하는게 구현 시 규칙이라 굳이 검사 X
            return self.argument0
        return self.argument1

    # 인자 2개인 경우만 호출
    def arg2(self) -> int:
        return self.argument2

    # 여기까지가 API

    def close(self) -> None:
        self.file.close()

    command_dict = {
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


class CodeWriter:

    def __init__(self, path) -> None:
        self.file = open(path, 'w')

        # 비교문 구현 시에 필요한 분기 작업의 식별자 역할
        self.bool_count = 0

        # 함수 retrun문 호출 시 필요한 식별자 역할 - 한 함수가 여러번 호출될 수 있으므로
        self.call_count = 0

        # VMTranslator가 setFilename 호출해서 설정해줌
        self.curr_file = None

    def init_sys(self):
        # Init Sys
        self.write('@256')
        self.write('D=A')
        self.write('@SP')
        self.write('M=D')
        self.writeCall('Sys.init', 0)

    def writeArithmetic(self, command) -> None:
        # 근데 이거 그냥 중복 감안하고 걍 문자열로 저장해도 될거 같은데, pushpop 부분도 그렇고
        """
        역할 설명
        1. 필요한 argument가 2개면 미리 pop해서 값(주소X)을 D에 넣기
        2. 나머지 arg 값을 M에 저장하기 (= A를 주소값으로 설정)
        3. 연산 수행하기(연산 코드 작성)
        4. 스택 포인터 + 1하기
        -> 스택에 값을 집어넣어야 한다고 생각할 수 있는데,
        -> 스택 자체는 메모리 주소값을 가지고 있을 뿐임.
        -> 2번 과정이 끝나면 A에 스택이 참조하고 있는 주소값이 할당되어 있으므로
        -> 그냥 3번에서 M=OOO 같은 식으로 설정해주고,
        -> 스택 push 돼어있다고 보고 SP +1만 해주면 되는거임.
        """
        if command not in ['neg', 'not']:
            # @SP, M=M+1: sp -= 1
            self.write('@SP')
            self.write('M=M-1')
            # A=M: A = *sp
            self.write('A=M')
            # D=M: D = A(*sp)
            self.write('D=M')

        # @SP, M=M+1: sp -= 1
        self.write('@SP')
        self.write('M=M-1')
        # A=M: A = M(sp)
        self.write('A=M')

        if command == 'add':  # Arithmetic operators
            self.write('M=M+D')
        elif command == 'sub':
            self.write('M=M-D')
        elif command == 'and':
            self.write('M=M&D')
        elif command == 'or':
            self.write('M=M|D')
        elif command == 'neg':
            self.write('M=-M')
        elif command == 'not':
            self.write('M=!M')
        elif command in ['eq', 'gt', 'lt']:
            '''
            특정 조건을 만족하는 경우 @BOOLn으로 이동, M=-1(true)로 설정하고 진행
            만족하지 않으면 그대로 내려가서 M=0(false로 설정) @BOOLSKIPn으로 이동해서 @BOOLn 부분 생략하고 진행
            '''
            self.write('D=M-D')
            self.write(f'@BOOL{self.bool_count}')

            if command == 'eq':
                self.write('D;JEQ')
            elif command == 'gt':
                self.write('D;JGT')
            elif command == 'lt':
                self.write('D;JLT')

            # @SP, A=M: A = *sp
            self.write('@SP')
            self.write('A=M')

            self.write('M=0')
            self.write('@SKIPBOOL{}'.format(self.bool_count))
            self.write('0;JMP')

            self.write('(BOOL{})'.format(self.bool_count))

            # @SP, A=M: A = *sp
            self.write('@SP')
            self.write('A=M')

            self.write('M=-1')

            self.write('(SKIPBOOL{})'.format(self.bool_count))
            self.bool_count += 1
        else:
            raise Exception

        # @SP, M=M+1: sp += 1
        self.write('@SP')
        self.write('M=M+1')

    def writePushPop(self, command_type, segment, index) -> None:
        self.write_address(segment, index)
        if command_type == 'C_PUSH':
            # D에 추가하기를 원하는 값(constant) or 주소(그 외) 저장
            if segment == 'constant':
                self.write('D=A')
            else:
                self.write('D=M')

            # @SP, A=M, M=D: *sp = D
            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            # 스택에 push 되었으므로 포인터 주소 1 올리기
            # @SP, M=M+1: sp += 1
            self.write('@SP')
            self.write('M=M+1')

        elif command_type == 'C_POP':
            '''
            이해가 잘 안갔는데, 이 코드는 주소(segment, index로 구한)로 pop된 값을 넣어주는 역할을 해야 함
            A가 값을 넣은 주소고 그걸 R13에 저장
            스택 포인터 값 빼느라 기존 A값 없어짐
            R13읽어서 주소 가져오고 D에 저장한 pop된 값 저장
            '''

            # D=A, @R13, M=D: R13 = A(segment, index로 구한 주소)
            self.write('D=A')
            self.write('@R13')  # R13은 스택 구현 계획 상 할당 안된 값이라 VM 변역기가 마음대로 사용 가능
            self.write('M=D')

            # 스택 포인터는 현재 값이 있는 가장 큰 주소 + 1의 값을 가지므로
            # 현재 값을 뺴기 위해서 1 감소시키기
            # @SP, M=M-1: sp -= 1
            self.write('@SP')
            self.write('M=M-1')

            # D에 *sp 저장
            # A=M, D=M: D = *sp
            self.write('A=M')
            self.write('D=M')

            # 저장된 값 다시 가져오기
            # @R13, A=M. M=D: *R13 = D -> A = *sp
            self.write('@R13')
            self.write('A=M')
            self.write('M=D')
        else:
            raise ValueError

    def writeLabel(self, label: str):
        self.write(f'({self.curr_file}${label})')

    def writeGoto(self, label: str):
        # @label, 0;JMP: goto @label
        self.write(f'@{self.curr_file}${label}')
        self.write('0;JMP')

    def writeIf(self, label: str):
        # @SP, M=M-1: sp -= 1
        self.write('@SP')
        self.write('M=M-1')

        # A=M, D=M: D = *sp
        self.write('A=M')
        self.write('D=M')

        # @label, D;JNE: if D != 0(false) then goto @label
        self.write(f'@{self.curr_file}${label}')
        self.write('D;JNE')

    def writeFunction(self, function_name: str, n_vars: int):  # TODO 일단 여긴 문제 없음
        # ({function_name}): label function_name
        self.write(f'({function_name})')

        for _ in range(n_vars):
            # # @SP, A=M, M=0: *sp = 0
            self.write('@SP')
            self.write('A=M')
            self.write('M=0')

            # @SP, M=M+1: sp += 1
            self.write('@SP')
            self.write('M=M+1')

    def writeCall(self, function_name: str, n_vars: int):
        return_address = f'{function_name}$ret.{self.call_count}'
        self.call_count += 1

        # 동작: stack.append(return_address)
        # @return_address D=A: D = return_address
        self.write(f'@{return_address}')
        self.write('D=A')
        # @SP, A=M, M=D: *sp = D
        self.write('@SP')
        self.write('A=M')
        self.write('M=D')
        # @SP, M=M+1: sp += 1
        self.write('@SP')
        self.write('M=M+1')

        for segment in ['LCL', 'ARG', 'THIS', 'THAT']:
            # @{segment}, D=M: D = @{segment}
            self.write(f'@{segment}')
            self.write('D=M')

            # @SP, A=M, M=D: *sp = D
            self.write('@SP')
            self.write('A=M')
            self.write('M=D')

            # @SP, M=M+1: sp += 1
            self.write('@SP')
            self.write('M=M+1')

        # @SP, D=M, @LCL, M=D: LCL = sp
        self.write('@SP')
        self.write('D=M')
        self.write('@LCL')
        self.write('M=D')

        # @SP, D=M, @{arg_offset}, D=D-A, M=D: ARG = SP-5-n_args
        arg_offset = 5 + n_vars
        # 위에서 SP를 D에 넣어둔 상태라 없어도 됨
        # self.write('@SP')
        # self.write('D=M')
        self.write(f'@{arg_offset}')
        self.write('D=D-A')
        self.write('@ARG')
        self.write('M=D')

        # @{function_name}, 0;JMP: goto function_name
        self.write(f'@{function_name}')
        self.write('0;JMP')

        # (return_address): label return_address - 함수가 끝나면 여기부터 코드가 이어 실행됨
        self.write(f'({return_address})')

    def writeReturn(self):
        # @LCL, D=M, @R14, M=D: R14(frame) = LCL
        self.write('@LCL')
        self.write('D=M')
        self.write('@R14')  # frame을 저장하는 임시 주소로 R14를 사용, R13~15는 VM 명세에서 사용되지 않는 값이라, VM 변환기가 마음대로 사용 가능
        self.write('M=D')

        # R15(ret_addr) = *(frame-5)
        self.write('@R14')
        self.write('D=M')
        self.write('@5')
        self.write('D=D-A')
        self.write('A=D')
        self.write('D=M')
        self.write('@R15')
        self.write('M=D')

        # *arg = pop() - 첫번째 arg에 결과를 저장
        # @SP, M=M-1: sp -= 1
        self.write('@SP')
        self.write('M=M-1')
        # A=M, D=M: D = *sp
        self.write('A=M')
        self.write('D=M')
        # @ARG, A=M, M=D: *arg = D
        self.write('@ARG')
        self.write('A=M')
        self.write('M=D')

        # @ARG, D=M, @SP, M=D+1: sp = D+1(arg+1) - 첫번째 arg의 다음으로 스택의 위치를 재설정.
        self.write('@ARG')
        self.write('D=M')
        self.write('@SP')
        self.write('M=D+1')

        for idx, segment in enumerate(['THAT', 'THIS', 'ARG', 'LCL']):
            # {segment} = *(frame-idx+1)
            self.write('@R14')
            self.write('D=M')
            self.write(f'@{idx + 1}')
            self.write('D=D-A')
            self.write('A=D')
            self.write('D=M')
            self.write(f'@{segment}')
            self.write('M=D')

        # goto R15(ret_addr)
        self.write('@R15')
        self.write('A=M')
        self.write('0;JMP')


    def setFileName(self, filename):
        self.curr_file = filename

    def close(self) -> None:
        self.file.close()

    # 여기까지가 API

    def write_address(self, segment, index) -> None:
        address = self.__address_dict[segment]
        if segment == 'constant':
            self.write('@' + str(index))
        elif segment == 'static':
            self.write('@' + self.curr_file + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self.write('@R' + str(address + int(index)))
        elif segment in ['local', 'argument', 'this', 'that']:
            # D에 base addr 저장
            self.write('@' + address)
            self.write('D=M')
            # A = base addr + @index
            self.write('@' + str(index))
            self.write('A=D+A')

    def write(self, string) -> None:
        return self.file.write(f"{string}\n")

    __address_dict = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
        'pointer': 3,  # R3~R4. THIS == R3
        'temp': 5,  # R5~R12
        'constant': None,  # 주소 안씀
        'static': None  # 주소 대신 별개의 값
    }


class VMTranslator:
    def __init__(self, args: list) -> None:
        if len(args) != 2:
            raise Exception('파일 경로를 포함하는 하나의 인자가 필요합니다.')

        self.path = args[1]
        self.is_dir = os.path.isdir(self.path)

        # asm_file_name == .vm 제외한 파일 이름 or 디렉토리 이름
        if self.is_dir:
            # 가장 깊은 디렉토리 이름
            file_name = os.path.basename(os.path.normpath(self.path))
        else:
            # 파일 경로의 OO.vm에서 확장자를 제거한 OO
            file_name = self.get_filename(self.path)
        file_location = os.path.split(self.path)[0]
        self.codeWriter = CodeWriter(os.path.join(file_location, file_name + ".asm"))
        self.parser = None

        if self.is_dir:
            self.codeWriter.init_sys()

    def run(self) -> None:
        if self.is_dir:
            self.translate_directory()
        else:
            self.translate_file(self.path, self.get_filename(self.path))

        self.codeWriter.close()

    def process_translate(self) -> None:
        while self.parser.hasMoreLines():
            self.parser.advance()
            cmd_type = self.parser.commandType()
            if cmd_type == 'C_ARITHMETIC':
                self.codeWriter.writeArithmetic(self.parser.arg1())
            elif cmd_type in ['C_POP', 'C_PUSH']:
                self.codeWriter.writePushPop(cmd_type, self.parser.arg1(), self.parser.arg2())
            elif cmd_type == 'C_LABEL':
                self.codeWriter.writeLabel(self.parser.arg1())
            elif cmd_type == 'C_GOTO':
                self.codeWriter.writeGoto(self.parser.arg1())
            elif cmd_type == 'C_IF':
                self.codeWriter.writeIf(self.parser.arg1())
            elif cmd_type == 'C_FUNCTION':
                self.codeWriter.writeFunction(self.parser.arg1(), int(self.parser.arg2()))
            elif cmd_type == 'C_CALL':
                self.codeWriter.writeCall(self.parser.arg1(), int(self.parser.arg2()))
            elif cmd_type == 'C_RETURN':
                self.codeWriter.writeReturn()
            else:
                raise Exception(f'처리하지 않는 CommandType: {cmd_type}')

    def translate_directory(self) -> None:
        vm_files = glob.glob(os.path.join(self.path, '*.vm'))
        for vm_file in vm_files:
            self.translate_file(vm_file, self.get_filename(vm_file))

    def get_filename(self, vm_file):
        return os.path.basename(vm_file)[:-3]

    def translate_file(self, path, file_name) -> None:
        self.parser = Parser(path)
        self.codeWriter.setFileName(file_name)
        self.process_translate()
        self.parser.close()


# 절대경로만 가능
VMTranslator(sys.argv).run()

# arg 변수 위치는 스택 최신 스택 - nArgs(그 인수 개수)
# caller의 정보를 가지고 있는 frame을 저장함. 거기에는 메모리 segment(LCL, THAT 등), return시 사용할 주소 등이 포함된다.

from io import TextIOWrapper
import os
import sys
from enum import Enum

"""
이거 구현 다시 하기로 함

주의점: 책에서 추천하는 인터페이스에 맞춰서 개발하는 중이다. 
메서드가 여러가지 일을 하는거 같으면, 그건 책에서 그렇게 제시했기 때문이다.
아니면 내가 잘못 구현하고 있거나, 리팩토링 해도 괜찮기는 함

코드에 대한 문맥은 결국 책을 읽어야 이해하기 쉽다.
-> 책 읽기 전에 영상이 더 빠르고 쉽게 이해 가능 - 많이 기억하면 책이 더 빠르긴 한데
-> 시각적으로 단계 별 진행 상태 변화를 눈으로 보려면 툴을 써야 하고, 툴 사용법은 엉상에서 알려줌

가장 중요한 건 이건 스택 기반의 가상머신이고...

가상머신인 만큼 하드워어의 주소를 직접 다루지 않고, 
스택에서는 포인터로 값을 담은 메모리 주소를 표시한다는 점. 이 코드에서는 SP가 스택의 포인터임, 현재 가장 높은 스택 주소 + 1을 가지고 있음

메모리 영역도 push, pop으로 다루는데, static, local 같은 영역이 따로 있고,
그걸 index 값으로 접근한다는 느낌
push는 메모리 접근해서 값 stack에 올리기
pop은 스택 최상단 값 해당 메모리에 저장하기

- 'A=M'은 포인터같은 역할

참고 자료

파일 읽고 쓰기: https://wikidocs.net/26
예외 던지기: https://dojang.io/mod/page/view.php?id=2400
Enum: https://www.daleseo.com/python-enum/
안풀어져서 참고한 다른사람 구현: https://github.com/kronosapiens/nand2tetris/blob/master/projects/07/VMtranslator.py

---

처음에는 뭐 안보고 했는데, CodeWriter 대충 작성까지는 했는데, 결과가 이상하게 나오고, 전혀 모르겠어서 구현된 코드좀 참고함.

그래도 계속 안되서, 그냥 처음부터 다시 만들기로 함
"""


class CommandType(Enum):
    C_ARITHMETIC = "C_ARITHMETIC"  # 산술
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNTION = "C_FUNTION"
    C_RETRUN = "C_RETRUN"
    C_CALL = "C_CALL"


class Parser:
    command_table = {
        "push": CommandType.C_PUSH,
        "pop": CommandType.C_POP,
        "add": CommandType.C_ARITHMETIC,
        "sub": CommandType.C_ARITHMETIC,
        "neg": CommandType.C_ARITHMETIC,
        "eq": CommandType.C_ARITHMETIC,
        "gt": CommandType.C_ARITHMETIC,
        "lt": CommandType.C_ARITHMETIC,
        "and": CommandType.C_ARITHMETIC,
        "or": CommandType.C_ARITHMETIC,
        "not": CommandType.C_ARITHMETIC
    }

    def __init__(self, file: TextIOWrapper) -> None:
        self.file = file
        self.command_type = None
        self.argument1 = None
        self.argument2 = None

    def hasMoreLines(self) -> bool:
        """
        다음 명령어가 있는지 확인합니다. 
        """
        # readline() 은 파일 포인터가 이동되므로 롤백하기 위해 사용
        current_position = self.file.tell()
        # readline() 은 읽은 줄이 아무것도 없으면 '\n', 파일의 끝이면 '' 반환
        while True:  # 리팩토링 포인트? - 가독성이 별로
            next_line = self.file.readline()
            if next_line == '':  # 마지막인 경우
                return False
            if next_line.startswith('//') or next_line.startswith('\n'):  # 주석이나 공백인 경우
                continue
            break
        self.file.seek(current_position)
        return True

    def advance(self) -> None:
        """
        현재 명령을 다음 명령으로 파일 포인터를 이동합니다. 
        초기화 직후의 현재 명령은 빈 상태입니다.
        hasMoreLines() 가 True일때만 사용해야 합니다.
        """
        while True:  # 리팩토링 포인트? - 가독성이 별로
            # 명령어 아니면 넘기기, 사실 유효한지 확인도 해야하는데, 귀찮아서 생략
            line = self.file.readline()
            if not (line.startswith('//') or line.startswith('\n')):
                for cmd, cmd_type in self.command_table.items():
                    if line.startswith(cmd):
                        self.command_type = cmd_type
                        self.__set_args(line, cmd_type)
                        break
                break

    def commandType(self) -> CommandType:
        return self.command_type

    def arg1(self) -> str:
        """
        현재 명령어의 첫번째 인수 반환.
        CommandType에 첫번째 인수가 아닌 명령어가 반환될 수 있다.
        """
        return self.argument1

    def arg2(self) -> int:
        """
        현재 명령어의 두번째 인수 반환.
        CommandType에 따라서 실행되지 않아야 할 수도 있다.
        """
        return self.argument2

    # 책에는 없는데, 내가 필요해서 추가함
    def close(self) -> None:
        self.file.close()

    def __set_args(self, line, cmd_type) -> None:
        lin = line.split()
        if cmd_type == CommandType.C_ARITHMETIC:
            self.argument1 = lin[0]
        else:
            self.argument1 = lin[1]
            self.argument2 = lin[2]


class CodeWriter:

    def __init__(self, file: TextIOWrapper, file_name: str) -> None:
        self.file = file
        self.file_name = file_name
        # file_name이 나중에 필요해서져서 추가함
        # 그냥 그... path를 받고 클래스에서 file을 생성하는게 나을듯? 만약 리팩토링 한다면

        # 이것도 나중에 추가
        self.bool_count = 0

    def writeArithmetic(self, command) -> None:
        # writePushPop()을 보면 알겠지만, 나중에 pop된게 D에 저장된 상태임
        if not (command == 'neg' or command == 'not'):  # x, y를 사용하는 연산을 위해 D에 미리 x 넣어놓기
            # 포인터 -1 -> stack 가장 최신 데이터가 있는 곳으로 이동
            self.__decrease_pointer()
            self.__write_file('@SP')  # 스택 top 포인터
            self.__write_file('A=M')  # 포인터(참조하는) 값 A에 저장(접근)
            self.__write_file('D=M')  # A의 값을 D에 저장

        self.__decrease_pointer()
        self.__write_file('@SP')
        self.__write_file('A=M')

        if command == "add":
            self.__write_file('M=M+D')
        elif command == 'sub':
            self.__write_file('M=M-D')
        elif command == 'neg':
            self.__write_file('M=-M')
        elif command == 'and':
            self.__write_file('M=M&D')
        elif command == 'or':
            self.__write_file('M=M|D')
        elif command == 'not':
            self.__write_file('M=!M')
        # 연산 결과에 따라 stack에 들어가는 값이 달라짐. ture면 -1, false 면 0
        # 그래서 분기 처리를 해야함
        # 참고: @위치 -> 값;조건 에서 값이 조건을 만족하면 A(`(위치)`)로 점프
        elif command in ['eq', 'gt', 'lt']:
            self.__write_file('D=M-D')

            # 조건을 만족하면 (BOOL{num})으로 Jump해서 결과를 true(-1)로 설정
            # 아니면 Jump가 발생하지 않아 결과를 0으로 설정하고 (BOOLSKIP)으로 이동, true 설정 부분 스킵
            self.__write_file(f'@BOOL{self.bool_count}')
            if command == 'eq':
                self.__write_file('D;JEQ')  # if x == y, x - y == 0
            elif command == 'gt':
                self.__write_file('D;JGT')  # if x > y, x - y > 0
            elif command == 'lt':
                self.__write_file('D;JLT')  # if x < y, x - y < 0

            self.__write_file(f'@BOOLSKIP{self.bool_count}')
            self.__write_file('M=0')  # 결과가 true면 실행 안됬을거임
            self.__write_file('0;JMP')

            self.__write_file(f'(BOOL{self.bool_count})')
            self.__write_file('M=-1')

            self.__write_file(f'(BOOLSKIP{self.bool_count})')
            self.bool_count += 1
        else:
            raise Exception(f'처리하지 않는 Command: {command}')

        # 이전 boolean 구현, 이해를 잘 못했음. 다른사람 구현 찾아보고 해결함
        # elif command == "eq":  # x == y
        #     self.__write_file('D=M-D')  # D = x(먼저 pop) - y(나중 pop)
        #     self.__write_file('D;JEQ')  # D == 0, 점프 문은 값;조건 에서 값이 조건을 만족하면 A로 점프
        # elif command == "gt":  # x > y
        #     self.__write_file('D=M-D')  # D = x - y
        #     self.__write_file('D;JGT')  # D > 0
        # elif command == "lt":  # x < y
        #     self.__write_file('D=M-D')  # D = x - y
        #     self.__write_file('D;JLT')  # D < 0

        # 연산 결과를 현재 스택 포인터 저장해서 스택 포인터 + 1
        self.__increase_pointer()

    def __increase_pointer(self):
        self.__write_file('@SP')
        self.__write_file('M=M+1')

    def __decrease_pointer(self):
        self.__write_file('@SP')
        self.__write_file('M=M-1')

    def writePushPop(self, command_type, segment, index) -> None:
        """
        command_type은 반드시 CommandType.C_PUSH, CommandType.C_POP 이여야 한다.
        segment, index를 어떻게 처리하는지는 위의 segments 딕셔너리도 함께 참고하기
        여기도 유효성 검사 생략함. 귀찮으니까

        index 대신 offset이 더 직관적이지 않나?
        """
        self.__get_address(segment, index)  # 목표하는 메모리 주소값 A에 등록된 상태
        if command_type == CommandType.C_PUSH:
            if segment == 'constant':
                self.__write_file('D=A')
            else:
                self.__write_file('D=M')  # constant는 값 자체를 의미하므로
            # RAM[SP++] = D
            self.__write_file('@SP')  # 스택 포인터를 A 레지스터에 등록
            self.__write_file('A=M')  # 포인터의 값(주소)를 A 레지스터에 등록
            self.__write_file('M=D')  # 새로운 데이터를 스택 포인터가 가지는 주소에 추가
            self.__increase_pointer()
        elif command_type == CommandType.C_POP:
            # 기존에 참조하는 주소의 값을 임시 (R13~15는 내부적인 임시 값임) 값에 저장
            self.__write_file('D=A')
            self.__write_file('@R13')
            self.__write_file('M=D')

            # RAM[SP--] = D
            self.__decrease_pointer()
            self.__write_file('A=M')  # top의 주소를 A 레지스터에 등록
            self.__write_file('D=M')  # top의 값을 D 레지스터에 저장

            # 저장해둔 임시 값 가져오기
            self.__write_file('@R13')
            self.__write_file('A=M')
            self.__write_file('M=D')

    def __write_file(self, string):
        return self.file.write(f"{string}\n")

    def close(self) -> None:
        self.file.close()

    # 아니 근데 이거 필요없는거 같은데? 아마 8장에서 쓰이지 않을까?
    def __get_address(self, segment, index) -> str:
        """
        딱히 유효성 검사 안하니까. 알아서 잘 들어온다는 가정하에 구현함
        segment 때문에 한 명령어 처리에 한 번만 호출되는게 좋을듯?
        """
        # 누가 구현한거 참고함
        address = self.__address_dict(segment)
        if segment == 'constant':
            self.__write_file('@' + str(index))
        elif segment == 'static':
            self.__write_file('@' + self.curr_file + '.' + str(index))
        elif segment in ['pointer', 'temp']:
            self.__write_file('@R' + str(address + int(index)))
        elif segment in ['local', 'argument', 'this', 'that']:
            # D에 base addr 저장
            self.__write_file('@' + address)
            self.__write_file('D=M')
            # A = base addr + @index
            self.__write_file('@' + str(index))
            self.__write_file('A=D+A')

        # 아래는 이전에 구현했던거, segment, index에 대한 이해가 부족했음
        # cur_static = 15
        # if segment == "local":
        #     return "@LCL"
        # if segment == "argument":
        #     return "@ARG"
        # if segment == "this":
        #     return "@THIS"
        # if segment == "that":
        #     return "@THAT"
        # if segment == "pointer":
        #     point_base_addr = 3
        #     return f"@R{str(point_base_addr + int(index))}"
        # if segment == "temp":
        #     temp_base_addr = 5
        #     return f"@R{str(temp_base_addr + int(index))}"
        # if segment == "constant":
        #     return f"@{str(index)}"
        # if segment == "static":
        #     # 값이 가변임, 16부터 순차적으로 증가함. << 아님 위에 새로 작성한 코드 참고
        #     # 책 설명에 따르면 메모라 공간떄문에 255까지 지원하고,
        #     # 코드 자체에서야 넘어갈수는 있지만 정상적으로 동작 안할 듯
        #
        #     cur_static += 1
        #     return f"@{self.file_name}.{str(cur_static)}"

    def __address_dict(self, segment: str):
        return {
            'local': 'LCL',  # Base R1
            'argument': 'ARG',  # Base R2
            'this': 'THIS',  # Base R3
            'that': 'THAT',  # Base R4
            'pointer': 3,  # Edit R3, R4
            'temp': 5,  # Edit R5-12
            # R13-15 are free
            'static': 16,  # Edit R16-255
        }


class VMTranslator:
    def __init__(self, args: list) -> None:
        # 리팩토링 포인트? - 생성자가 너무 많은 역할을 하는거 같지 않음?
        if len(args) != 2:
            raise Exception('파일 경로를 포함하는 하나의 인자가 필요합니다.')

        # TODO 파일 관련 유효성 검사 필요한데, 귀찮으니까 생략
        file_location, vm_file_name = os.path.split(args[1])
        file_name, vm_extension = os.path.splitext(vm_file_name)
        file_path = file_location + "/" + file_name

        vm_file_path = file_path + vm_extension
        vm_file = open(vm_file_path, 'r')  # 리팩토링 포인트? - with을 사용하는거 같던데, 이게 뭐지?
        # > 위와 같이 with 문을 사용하면 with 블록(with 문에 속해 있는 문장)을 벗어나는 순간, 열린 파일 객체 f가 자동으로 닫힌다. 참고: https://wikidocs.net/26
        # 지금 상황에서는 유효하지 않음, file을 넘겨줘야 하니까
        self.parser = Parser(vm_file)

        asm_extension = ".asm"
        asm_file_path = file_path + asm_extension
        asm_file = open(asm_file_path, 'w')
        self.codeWriter = CodeWriter(asm_file, file_name)

    # 리팩토링 포인트? - 하는 일이 너무 많지 않음? -> 근데 뭐 메인 클래스 역할이니까 이정도는 괜찮지 않나...
    def excute(self) -> None:
        while self.parser.hasMoreLines():
            self.parser.advance()
            cmd_type = self.parser.commandType()
            if cmd_type == CommandType.C_ARITHMETIC:
                cmd = self.parser.arg1()
                self.codeWriter.writeArithmetic(cmd)
            elif cmd_type == CommandType.C_POP or cmd_type == CommandType.C_PUSH:
                segment = self.parser.arg1()
                index = self.parser.arg2()
                self.codeWriter.writePushPop(cmd_type, segment, index)
            elif cmd_type == CommandType.C_ARITHMETIC:
                command = self.parser.arg1()
                self.codeWriter.writeArithmetic(command)
            else:
                raise Exception(f'처리하지 않는 CommandType: {cmd_type}')
        self.__close()

    def __close(self) -> None:
        self.parser.close()
        self.codeWriter.close()


# vm 파일 위치는 상대경로 대신 절대경로로 해야 함. 수정할 수 있으면 하고 싶은데, 지금도 잘 되니까 뭐... 굳이?
VMTranslator(sys.argv).excute()

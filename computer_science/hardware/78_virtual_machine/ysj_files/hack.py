from io import TextIOWrapper
import sys
import os

"""
이전 코드가 잘 안되서, 다시 구현하는 중
이번에는 유효성 검사, Enum같이 불필요한거 제외하고, 딱 필요한거만 작성할 예정

"""


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
            if not (line.startswith('//') or line.startswith('\n')):
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
        if not self.command_type == "C_ARITHMETIC":  # C_ARITHMETIC 은 인자가 없음
            self.argument1 = cmd_split[1]
            self.argument2 = cmd_split[2]

    def commandType(self) -> str:
        return self.command_type

    def arg1(self) -> str:
        if self.command_type == "C_ARITHMETIC":
            return self.argument0
        return self.argument1

    # 인자 2개인 경우만 호출
    def arg2(self) -> int:
        return self.argument2

    # 여기까지가 책 API

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
        'not': 'C_ARITHMETIC'
    }


class CodeWriter:

    def __init__(self, path) -> None:
        self.file = open(path, 'w')

    def writeArithmetic(self) -> None:
        pass

    def writePushPop(self) -> None:
        pass

    def close(self) -> None:
        self.file.close()


class VMTranslator:
    def __init__(self, args: list) -> None:
        if len(args) != 2:
            raise Exception('파일 경로를 포함하는 하나의 인자가 필요합니다.')

        # ex: 절대경로/OOO.asm
        file_path = os.path.split(args[1])

        self.parser = Parser(file_path[:-4] + ".vm")
        self.codeWriter = CodeWriter(file_path)

    def run(self) -> None:
        while self.parser.hasMoreLines():
            self.parser.advance()
            cmd_type = self.parser.commandType()
            if cmd_type == 'C_ARITHMETIC':
                self.codeWriter.writeArithmetic(self.parser.arg1())
            elif cmd_type in ['C_POP', 'C_PUSH']:
                self.codeWriter.writePushPop(cmd_type, self.parser.arg1(), self.parser.arg2())
            else:
                raise Exception(f'처리하지 않는 CommandType: {cmd_type}')

        # 파일 close
        self.parser.close()
        self.codeWriter.close()


# 절대경로만 가능
VMTranslator(sys.argv).excute()

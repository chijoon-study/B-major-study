# HackAssembler 만들기
# GPT를 많이 사용함
# .asm 파일의 명세는 모두 유효하다고 가정함 - 모든 예외처리 필요 없음, 구현만 하면 됨 - 예외처리까지 해야 했으면 많이 힘들었을 듯
# API 대로 딱 맞게 구현한건 아닌데, 걍 귀찮아서... 그냥 함


import sys
import os

from enum import Enum


class InstructionType(Enum):
    A_INSTRUCTION = "A_INSTRUCTION"
    C_INSTRUCTION = "C_INSTRUCTION"
    L_INSTRUCTION = "L_INSTRUCTION"


# 사실 이러면 2번 돌아야 하기 때문에 효율이 별로임, 나는 귀찮아서 이렇게 했는데
# 실제로 할꺼면 Parser에서 다음 idx로 갈때 주석이랑 공백 란은 스킵하는게 좋음
class Trimmer:
    def __init__(self, file):
        self.file = file

    def trim(self):
        trimmed_lines = [line.lstrip().rstrip() for line in self.file if
                         line.strip() and not line.strip().startswith('//')]
        return trimmed_lines


class Parser:
    def __init__(self, content_list):
        self.content_list = content_list
        self.cur_idx = 0

    def hasMoreLines(self) -> bool:
        return len(self.content_list) > self.cur_idx

    def advance(self) -> None:
        if self.hasMoreLines():
            self.cur_idx += 1

    def instructionType(self) -> InstructionType:
        line = self.content_list[self.cur_idx]
        if line.startswith('@'):
            return InstructionType.A_INSTRUCTION
        elif '=' in line or ';' in line:
            return InstructionType.C_INSTRUCTION
        elif line[0] == "(" and line[-1] == ")":
            return InstructionType.L_INSTRUCTION

    def symbol(self) -> str:
        t = self.instructionType()
        line = self.content_list[self.cur_idx]
        if t == InstructionType.A_INSTRUCTION:
            return line[1:]
        elif t == InstructionType.L_INSTRUCTION:
            return line[1:].split(')')[0]

    def dest(self) -> str:
        return self.__detachCInstruction()[0]

    def comp(self) -> str:
        return self.__detachCInstruction()[1]

    def jump(self) -> str:
        return self.__detachCInstruction()[2]

    def __detachCInstruction(self) -> tuple:
        line = self.content_list[self.cur_idx]
        parts = line.split('=')
        dest = parts[0] if len(parts) > 1 else None
        comp_jump = parts[-1].split(';')
        comp = comp_jump[0]
        jump = comp_jump[1] if len(comp_jump) > 1 else None
        return dest, comp, jump


class Code:
    dest_table = {
        None: "000",
        "M": "001",
        "D": "010",
        "DM": "011",
        "MD": "011", # 명세에는 없는데, Pong.asm에 MD=M+1 때문에 추가함,
        "A": "100",
        "AM": "101",
        "AD": "110",
        "ADM": "111"
    }

    comp_table = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101",
    }

    jump_table = {
        None: "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    def __init__(self):
        pass

    def dest(self, dec_dest) -> str:
        return self.dest_table.get(dec_dest)

    def comp(self, dec_comp) -> str:
        return self.comp_table.get(dec_comp)

    def jump(self, dec_jump) -> str:
        return self.jump_table.get(dec_jump)


class SymbolTable:
    def __init__(self):
        self.__symbol_table = {
            "R0": "0",
            "R1": "1",
            "R2": "2",
            "R3": "3",
            "R4": "4",
            "R5": "5",
            "R6": "6",
            "R7": "7",
            "R8": "8",
            "R9": "9",
            "R10": "10",
            "R11": "11",
            "R12": "12",
            "R13": "13",
            "R14": "14",
            "R15": "15",
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
            "SCREEN": "16384",
            "KBD": "24576"
        }

    def addEntry(self, symbol, address):
        self.__symbol_table[symbol] = address

    def contains(self, symbol) -> bool:
        return symbol in self.__symbol_table

    def getAddress(self, symbol) -> int:
        return self.__symbol_table[symbol]

# Label 주소 심볼 테이블에 저장, 별로 좋은 코드는 아닌데
# 다른거 다 구현한 상태에서 이 로직 빼먹어서 걍 대충 만든거
def addLabel(content, symbol_table):
    i=0
    for c in content:
        if c[0] == "(" and c[-1] == ")":
            symbol_table.addEntry(c[1:-1], i)
        else:
            i += 1


def main():
    #n = 0
    # 파일 경로를 입력 받습니다.
    # 스크립트가 실행될 때 전달된 모든 인자들을 확인합니다.
    args = sys.argv

    # 첫 번째 인자는 스크립트의 이름입니다.
    # 두 번째 인자는 변환할 어셈블리 코드 파일의 경로입니다.
    file_path = args[1]

    try:
        # 파일을 열어서 Trimer 클래스에 전달합니다.
        with open(file_path, 'r') as file:
            trimmer = Trimmer(file)
            trimmed_content = trimmer.trim()

            # 새 파일 이름을 생성합니다.
            output_file_path = os.path.splitext(file_path)[0] + '.hack'

            # 새 파일을 열어 기계어를 씁니다.
            with open(output_file_path, 'w') as output_file:
                parser = Parser(trimmed_content)
                code = Code()
                symbol_table = SymbolTable()
                next_symbol_addr = 16

                addLabel(trimmed_content, symbol_table)

                while parser.hasMoreLines():  # 다음 코드가 있을 때까지 반복
                    instruction_type = parser.instructionType()
                    if instruction_type == InstructionType.A_INSTRUCTION:
                        # A 명령어 처리
                        symbol = parser.symbol()
                        if symbol.isdecimal():  # 만약 변수가 아니라면
                            # A 명령어 기계어 생성
                            machine_code = '0' + format(int(symbol), '015b') + '\n'
                        else:  # 변수인 경우
                            if symbol_table.contains(symbol):  # 심볼 테이블에 있는가?
                                machine_code = '0' + format(int(symbol_table.getAddress(symbol)), '015b') + '\n'
                            else:
                                symbol_table.addEntry(symbol, next_symbol_addr)
                                machine_code = '0' + format(int(next_symbol_addr), '015b') + '\n'
                                next_symbol_addr += 1

                    elif instruction_type == InstructionType.C_INSTRUCTION:
                        # C 명령어 처리
                        dest = parser.dest()
                        comp = parser.comp()
                        jump = parser.jump()
                        # C 명령어 기계어 생성
                        machine_code = '111' + code.comp(comp) + code.dest(dest) + code.jump(jump) + '\n'
                    elif instruction_type == InstructionType.L_INSTRUCTION:
                        # 미리 위에서 label symbol은 다 등록해놓음
                        # 그리고 딱히 뭐 안함 애는 - (xxx)는 무슨 코드를 하는게 아님
                        machine_code = ""
                    # 기계어를 파일에 씁니다.
                    output_file.write(machine_code)
                    # 다음 줄로 넘기기
                    parser.advance()

                    # print(n)
                    # n += 1

            print("변환 완료: {}".format(output_file_path))

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")


main()

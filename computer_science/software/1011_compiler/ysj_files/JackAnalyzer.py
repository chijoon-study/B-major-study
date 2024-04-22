import glob
import os
import re
import heapq
import sys
from collections import deque


COMMENT = "(//.*)|(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)"
EMPTY_TEXT_PATTERN = re.compile("\s*")
KEY_WORD_PATTERN = re.compile("^\s*("
                              "class|constructor|function|method|static|field"
                              "|var|int|char|boolean|void|true|false|null|this|"
                              "let|do|if|else|while|return)\s*")
SYMBOL_PATTERN = re.compile("^\s*([{}()\[\].,;+\-*/&|<>=~])\s*")
DIGIT_PATTERN = re.compile("^\s*(\d+)\s*")
STRING_PATTERN = re.compile("^\s*\"(.*)\"\s*")
IDENTIFIER_PATTERN = re.compile("^\s*([a-zA-Z_][a-zA-Z1-9_]*)\s*")


DEBUGGING = False

class JackTokenizer:
    """
    JackTokenizer module as described in NAND2Tetris chapter 10
    """

    keyword = ["CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
                "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET",
                "DO", "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE",
                "NULL", "THIS"]

    KEYWORD = 0
    SYMBOL = 1
    INT_CONST = 2
    STRING_CONST = 3
    IDENTIFIER = 4

    def __init__(self, path):
        with open(path, "r") as file:
            self.text = file.read()
        self._clear_all_comments()
        self._tokenType = None
        self._currentToken = None

    def _clear_all_comments(self):
        self.text = re.sub(COMMENT, "", self.text)

    def hasMoreTokens(self):
        if re.fullmatch(EMPTY_TEXT_PATTERN, self.text):
            return False
        else:
            return True

    def advance(self):
        if self.hasMoreTokens():
            current_match = re.match(KEY_WORD_PATTERN, self.text)
            if current_match is not None:
                self.text = re.sub(KEY_WORD_PATTERN, "", self.text)
                self._tokenType = JackTokenizer.KEYWORD
                self._currentToken = current_match.group(1)
            else:
                current_match = re.match(SYMBOL_PATTERN, self.text)
                if current_match is not None:
                    self.text = re.sub(SYMBOL_PATTERN, "", self.text)
                    self._tokenType = JackTokenizer.SYMBOL
                    self._currentToken = current_match.group(1)
                else:
                    current_match = re.match(DIGIT_PATTERN, self.text)
                    if current_match is not None:
                        self.text = re.sub(DIGIT_PATTERN, "", self.text)
                        self._tokenType = JackTokenizer.INT_CONST
                        self._currentToken = current_match.group(1)
                    else:
                        current_match = re.match(STRING_PATTERN, self.text)
                        if current_match is not None:
                            self.text = re.sub(STRING_PATTERN, "", self.text)
                            self._tokenType = JackTokenizer.STRING_CONST
                            self._currentToken = current_match.group(1)
                        else:
                            current_match = re.match(IDENTIFIER_PATTERN, self.text)
                            if current_match is not None:
                                self.text = re.sub(IDENTIFIER_PATTERN, "", self.text)
                                self._tokenType = JackTokenizer.IDENTIFIER
                                self._currentToken = current_match.group(1)

    def tokenType(self):
        return self._tokenType

    def keyWord(self):
        return self._currentToken

    def symbol(self):
        return self._currentToken

    def identifier(self):
        return self._currentToken

    def intVal(self):
        return int(self._currentToken)

    def stringVal(self):
        return self._currentToken


#
# class JackTokenizer:
#     def __init__(self, path):
#         self.file = open(path, 'r')
#         self.currentLineTokens = []  # 현재 로드된 토큰, 가장 앞의 존재하는 토큰부터 가져온다.
#         self.cur_type = None
#         self.cur_val = None
#         pass
#
#     def has_more_tokens(self) -> bool:
#         """file에 더 많은 토큰이 있는가?"""
#         '''
#         다음 명령어가 있는지 확인하면서 다음 결과 바로 앞까지 이동.
#         변경/조회 기능이 합쳐져있기는 한데, 멱등성이 보장되니까 괜찮을듯?
#         '''
#         if len(self.currentLineTokens) >= 2:  # currentLineTokens이 남았으면 아직 토큰 있는거임
#             return True
#         else:
#             while True:
#                 current_position = self.file.tell()
#                 line = self.file.readline()
#                 if line == '':  # 마지막 줄인가?
#                     return False
#                 line = line.strip()
#                 if line.startswith('//'):  # 한줄 주석인가?
#                     continue
#                 elif line == '':  # 줄바꿈인가?
#                     continue
#                 elif line.startswith('/*') or line.startswith('/**') or line.startswith('*'):  # 여러줄 주석인가?
#                     continue
#                 else:
#                     self.file.seek(current_position)
#                     return True
#
#     def advance(self) -> None:
#         """다음 토큰을 현재 토큰으로. has_more_tokens가 true일 때만 사용해야 함"""
#         if len(self.currentLineTokens) < 2:  # self.currentLineTokens가 비면 새로운 값 가져오기
#             line = self.file.readline().strip()
#             self.currentLineTokens.extend(self.get_tokens(line))
#         else:  # 남아있으면 기존 self.currentLineTokens에서 기존 값 빼고 다음 값 사용하기
#             heapq.heappop(self.currentLineTokens)
#         cur_token = self.currentLineTokens[0][1]
#         self.cur_type = cur_token[0]
#         self.cur_val = self.get_val(cur_token[0], cur_token[1])
#
#     def token_type(self) -> str:
#         """현재 토큰의 타입 반환"""
#         return self.cur_type
#
#     def keyword(self) -> str:
#         """token_type이 KEYWORD일때만 호출해야 함. 현재 토큰의 키워드 반환"""
#         return self.cur_val
#
#     def symbol(self) -> str:
#         """token_type이 SYMBOL일때만 호출해야 함. 현재 토큰의 문자 반환."""
#         return self.cur_val
#
#     def identifier(self) -> str:
#         """token_type이 IDENTIFIER일때만 호출해야 함. 현재 토큰의 문자열 반환."""
#         return self.cur_val
#
#     def intVal(self) -> int:
#         """token_type이 INT_CONST일때만 호출해야 함. 현재 토큰의 정수값 반환."""
#         return self.cur_val
#
#     def stringVal(self) -> str:
#         """token_type이 STRING_CONST일때만 호출해야 함. 현재 토큰의 문자열에서 따옴표를 제거하고 반환."""
#         return self.cur_val
#
#     # 여기까지 API
#
#     def has_term_child(self) -> bool:
#         """해당 term(토큰)이 햐위 term을 가지는지 확인함. 예를 들어. arr[i]는 arr는 하위 i를 가짐"""
#         # term의 하위 term을 적을 때, 줄바꿈이 발생하지 않으므로 self.currentLineTokens을 확인해서 값을 구할 수 있음.
#         # 예를 들어, arr[i]를 표현할 때, 다음처럼 표현하지는 않는다.
#         # arr
#         # [i];
#         if len(self.currentLineTokens) < 2:
#             return False
#         next_token = heapq.nsmallest(2, self.currentLineTokens)[1][1]  # 값 작은 순으로 2개 뽑아서 2번째 가지기 (= 현재 다음 토큰 가져요기)
#         if next_token[1] in "[(.":  # [ ( . 중 하나면 하위 term이 있다는 소리
#             return True
#         else:
#             return False
#
#     def close(self, path):
#         """self.file을 포함한 자원 해제"""
#         pass
#
#     def get_tokens(self, text) -> list:
#         """입력받은 텍스트의 token 목록을 반환함"""
#         matches = []
#         for name in ['KEYWORD', 'SYMBOL', 'INT_CONST', 'STRING_CONST', 'IDENTIFIER']:
#             pattern = self.patterns[name]
#             for match in re.finditer(pattern, text):
#                 matches.append((match.start(), (name, match.group())))
#         heapq.heapify(matches)
#         return matches
#
#     def get_val(self, token_type: str, value: str):
#         """type에 맞는 값 설정"""
#         if token_type == 'KEYWORD':
#             return value
#         if token_type == 'SYMBOL':
#             return value
#         if token_type == 'IDENTIFIER':
#             return value
#         if token_type == 'INT_CONST':
#             return int(value)
#         if token_type == 'STRING_CONST':
#             return value[1:-1]  # 앞 뒤 따옴표 제거
#         raise Exception

class CompilationEngine:
    def __init__(self, path, jack_tokenizer: JackTokenizer):
        self.file = open(path, 'w')
        self.tokenizer = jack_tokenizer

    def compile_class(self):
        pass

    def compile_class_var_dec(self):
        pass

    def compile_subroutine(self):
        pass

    def compile_parameter_list(self):
        pass

    def compile_var_dec(self):
        pass

    def compile_statements(self):
        pass

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        self.tokenizer.advance()
        token_type = self.tokenizer.tokenType()
        if token_type == JackTokenizer.IDENTIFIER:
            token_value = self.tokenizer.identifier()
            self.write(f'<identifier> {token_value} </identifier>\n')
            if self.tokenizer.hasMoreTokens():  # 만약 하위 term이 있다면 재귀적으로 호출
                self.compile_term()
        elif token_type == JackTokenizer.STRING_CONST:
            token_value = self.tokenizer.stringVal()
            self.write(f'<stringConstant> {token_value} </stringConstant>\n')
        elif token_type == JackTokenizer.INT_CONST:
            token_value = self.tokenizer.intVal()
            self.write(f'<integerConstant> {token_value} </integerConstant>\n')
        elif token_type == JackTokenizer.KEYWORD:
            token_value = self.tokenizer.keyWord()
            self.write(f'<keyword> {token_value} </keyword>\n')
        elif token_type == JackTokenizer.SYMBOL:
            token_value = self.tokenizer.symbol()
            self.write(f'<symbol> {token_value} </symbol>\n')

    # 10장에서는 사용 안함
    def compile_expression_list(self):
        pass

    def write(self, text):
        self.file.write(text)


class JackAnalyzer:
    def __init__(self, args):
        self.path = args[1]
        self.jt = None
        self.ce = None

    def run(self):
        if os.path.isdir(self.path):
            #            dir_path = os.path.basename(os.path.normpath(self.path))
            self.analyze_dir()
        else:
            file_path = self.path[:-5]
            self.analyze_file(file_path)

    def analyze_dir(self):
        jack_files = glob.glob(os.path.join(self.path, '*.jack'))
        for jack_file in jack_files:
            file_path = jack_file[:-5]
            self.analyze_file(file_path)

    def analyze_file(self, file_path):
        self.jt = JackTokenizer(file_path + '.jack')
        self.ce = CompilationEngine(file_path + "Test" + '.xml', self.jt)
        self.ce.file.write('<tokens>\n')
        while self.jt.hasMoreTokens():
            self.ce.compile_term()
        self.ce.file.write('</tokens>\n')


JackAnalyzer(sys.argv).run()

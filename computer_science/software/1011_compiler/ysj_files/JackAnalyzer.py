import glob
import os
import re
import sys

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

FIELD = 'field'
STATIC = 'static'
LOCAL = 'local'
ARGUMENTS = 'argument'


class SymbolTable:

    def __init__(self):
        self.class_table = {}
        self.kind_idx = {'field': 0, 'static': 0, 'local': 0, 'argument': 0}
        self.sub_routine_table = {}

    def start_subroutine(self):
        self.sub_routine_table = {}
        self.kind_idx['local'] = 0
        self.kind_idx['argument'] = 0

    def define(self, name, var_type, kind):
        if kind in [FIELD, STATIC]:
            self.class_table[name] = [var_type, kind, self.kind_idx[kind]]
        elif kind in [LOCAL, ARGUMENTS]:
            self.class_table[name] = [var_type, kind, self.kind_idx[kind]]
        self.kind_idx[kind] += 1

    def var_count(self, kind):
        return self.kind_idx[kind]

    def kind_of(self, name):
        return self.get_row(name)[1]

    def type_of(self, name):
        return self.get_row(name)[0]

    def index_of(self, name):
        return self.get_row(name)[2]

    # 여기까지 API

    def get_row(self, name):
        if name in self.sub_routine_table:
            return self.sub_routine_table[name]
        if name in self.class_table:
            return self.class_table[name]
        raise Exception


class VMWriter:
    sign_to_op = {'+': 'add',
                  '-': 'sub',
                  '*': 'call Math.multiply 2',
                  '/': 'call Math.divide 2',
                  '&': 'and',
                  '|': 'or',
                  '<': 'lt',
                  '>': 'gt',
                  '=': 'eq'}

    kind_to_segment = {'static': 'static',
                       'field': 'this',
                       'arg': 'argument',
                       'var': 'local'}

    def __init__(self, path):
        self.file = open(path, 'w')

    def write_push(self, segment, index):
        self.file.write(f'push {segment} {str(index)}\n')

    def write_pop(self, segment, index):
        self.file.write(f'pop {segment} {str(index)}\n')

    def write_arithmetic(self, command):
        self.file.write(f'{command}\n')

    def write_label(self, label):
        self.file.write(f'label {label}\n')

    def write_goto(self, label):
        self.file.write(f'goto {label}\n')

    def write_if(self, label):
        self.file.write(f'if-goto {label}\n')

    def write_call(self, name, nArgs):
        self.file.write(f'call {name} {str(nArgs)}\n')

    def write_function(self, name, nLocals):
        self.file.write(f'function {name} {str(nLocals)}\n')

    def write_return(self):
        self.file.write('return\n')


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


class CompilationEngine:
    def __init__(self, path, jacktokenizer: JackTokenizer, vm_path):
        self.file = open(path, 'w')
        self.tokenizer = jacktokenizer
        self.indent_level = 0
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(vm_path)
        self.class_name = None
        self.expression_op_stack = []

    def compile_class(self):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()  # class

            self.tokenizer.advance()  # identifier - class name
            self.class_name = self.tokenizer.identifier()

            self.tokenizer.advance()  # {

            self.tokenizer.advance()
            while self.tokenizer.keyWord() == "static" or \
                    self.tokenizer.keyWord() == "field":
                self.compile_class_var_dec()
            while self.tokenizer.keyWord() == "constructor" or \
                    self.tokenizer.keyWord() == "function" \
                    or self.tokenizer.keyWord() == "method":
                self.compile_subroutine()

            # cur token is '}' because called by compile_class_var_dec() or compile_subroutine()

    def compile_class_var_dec(self):
        # self.write(f'<classVarDec>\n')
        # self.indent_level += 1
        # self.write_keyword()  # static, field

        kind = self.tokenizer.keyWord()

        self.tokenizer.advance()
        self.compile_type_and_varName(True, kind)

        # self.indent_level -= 1
        # self.write(f'</classVarDec>\n')

    def compile_subroutine(self):
        # self.write(f'<subroutineDec>\n')
        # self.indent_level += 1
        # self.write_keyword()  # constructor, method, function

        self.symbol_table.start_subroutine()  # 서브루틴 시작

        self.tokenizer.advance()  # return type - void or identifier(class)
        # if self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
        # self.write_keyword()  # void
        # elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
        # self.write_identifier()  # identifier - return type

        self.tokenizer.advance()  # identifier - name
        # self.write_identifier()
        name = self.tokenizer.identifier()

        self.tokenizer.advance()  # (
        # self.write_symbol()  # (

        self.tokenizer.advance()  # parameter_list
        n_args = self.compile_parameter_list()  # 파라미터

        self.vm_writer.write_function(f'{self.class_name}.{name}', n_args)

        # self.write_symbol()  # )

        self.tokenizer.advance()  # {
        # self.write(f'<subroutineBody>\n')
        # self.indent_level += 1
        # self.write_symbol()  # {

        self.tokenizer.advance()  # var or something
        while self.tokenizer.keyWord() == "var":
            self.compile_var_dec()  # var 처리

        self.compile_statements()  # statements

        # self.write_symbol()  # }

        # self.indent_level -= 1
        # self.write(f'</subroutineBody>\n')
        # self.indent_level -= 1
        # self.write(f'</subroutineDec>\n')
        self.tokenizer.advance()

    def compile_parameter_list(self) -> int:
        """원래 반환안하는데, 내가 구현하기 편하게 하려고 반환하게 함"""

        cnt = 0

        while self.tokenizer.tokenType() != self.tokenizer.SYMBOL:  # 현재 토큰이 SYMBOL 라는건 토큰이 ) 되었다는 의미
            cnt += 1
            if self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
                type = self.tokenizer.keyWord()  # type - int, char ...
            elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
                type = self.tokenizer.identifier()  # identifier - class

            self.tokenizer.advance()
            name = self.tokenizer.identifier()  # identifier - param name

            self.symbol_table.define(name, type, ARGUMENTS)

            self.tokenizer.advance()  # , or something
            if self.tokenizer.symbol() == ",":
                self.tokenizer.advance()
        return cnt

    def compile_var_dec(self):
        # self.write(f'<varDec>\n')
        # self.indent_level += 1

        # self.write_keyword()  # var
        self.tokenizer.advance()
        self.compile_type_and_varName(False, None)  # type varName

        # self.indent_level -= 1
        # self.write(f'</varDec>\n')

    def compile_statements(self):
        # self.write(f'<statements>\n')
        # self.indent_level += 1

        while self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
            if self.tokenizer.keyWord() == "let":
                self.compile_let()
            elif self.tokenizer.keyWord() == "if":
                self.compile_if()
            elif self.tokenizer.keyWord() == "while":
                self.compile_while()
            elif self.tokenizer.keyWord() == "do":
                self.compile_do()
            elif self.tokenizer.keyWord() == "return":
                self.compile_return()

        # self.indent_level -= 1
        # self.write(f'</statements>\n')

    def compile_do(self):
        self.tokenizer.advance()
        outer_identifier = self.tokenizer.identifier()  # identifier - method(this 생략 시) or class/instance name(클래스/인스턴스 호출 시)

        is_this_call = True

        self.tokenizer.advance()  # . or (
        if self.tokenizer.symbol() == ".":  # 클래스/인스턴스 호출 시
            self.tokenizer.advance()  # (
            identifier = self.tokenizer.identifier()  # identifier - function or method name
            is_this_call = False
            # self.tokenizer.advance()  # ( - 이거 10장에선 있어도 문제 없었는데, 왜 문제가 생긴거지... 다른 부분 수정하면서 꼬인건가?
            # TODO 문제 생기면 이쪽 관련된 부분일 수도 있음

        self.tokenizer.advance()  # expression_list
        n_arg = self.compile_expression_list()

        # skip ) by compile_expression_list()

        if is_this_call:
            self.vm_writer.write_call(f'this.{outer_identifier}', n_arg)
        else:
            self.vm_writer.write_call(f'{outer_identifier}.{identifier}', n_arg)
        self.vm_writer.write_pop('temp', 0)  # 결과 버리기

        self.tokenizer.advance()  # ;

        self.tokenizer.advance()

    def compile_let(self):
        self.write(f'<letStatement>\n')
        self.indent_level += 1
        self.write_keyword()  # let

        self.tokenizer.advance()
        self.write_identifier()  # identifier

        self.tokenizer.advance()
        if self.tokenizer.symbol() == "[":
            self.write_symbol()  # [
            self.tokenizer.advance()
            self.compile_expression()  # expression
            self.write_symbol()  # ]
            self.tokenizer.advance()

        self.write_symbol()  # =

        self.tokenizer.advance()
        self.compile_expression()  # expression

        self.write_symbol()  # ;

        self.indent_level -= 1
        self.write(f'</letStatement>\n')
        self.tokenizer.advance()

    def compile_while(self):
        self.write(f'<whileStatement>\n')
        self.indent_level += 1
        self.write_keyword()  # while

        self.tokenizer.advance()
        self.write_symbol()  # (

        self.tokenizer.advance()
        self.compile_expression()  # expression

        self.write_symbol()  # )

        self.tokenizer.advance()
        self.write_symbol()  # {

        self.tokenizer.advance()
        self.compile_statements()  # statements

        self.write_symbol()  # }

        self.indent_level -= 1
        self.write(f'</whileStatement>\n')
        self.tokenizer.advance()

    def compile_return(self):
        # cur token is return, advance by outer

        self.tokenizer.advance()
        if self.tokenizer.tokenType() != self.tokenizer.SYMBOL and \
                self.tokenizer.symbol() != ";":  # if not return void
            self.compile_expression()  # expression
        else:
            self.vm_writer.write_push('constant', 0)

        self.vm_writer.write_arithmetic('return')

        self.tokenizer.advance()

    def compile_if(self):
        self.write(f'<ifStatement>\n')
        self.indent_level += 1
        self.write_keyword()  # if

        self.tokenizer.advance()
        self.write_symbol()  # (

        self.tokenizer.advance()
        self.compile_expression()  # expression

        self.write_symbol()  # )

        self.tokenizer.advance()
        self.write_symbol()  # {

        self.tokenizer.advance()
        self.compile_statements()  # statements

        self.write_symbol()  # }

        self.tokenizer.advance()
        if self.tokenizer.tokenType() == self.tokenizer.KEYWORD and \
                self.tokenizer.keyWord() == "else":
            self.write_keyword()  # else

            self.tokenizer.advance()
            self.write_symbol()  # (

            self.tokenizer.advance()
            self.compile_statements()  # {

            self.write_symbol()
            self.tokenizer.advance()  # }

        self.indent_level -= 1
        self.write(f'</ifStatement>\n')

    def compile_expression(self):
        self.compile_term()
        # op라면 연산이 이어지는 경우이므로 (op term) 반복, 이 과정에서 다음 값까지 미리 읽은 상태가 됨
        while self.tokenizer.tokenType() == self.tokenizer.SYMBOL and \
                self.tokenizer.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op = self.tokenizer.symbol()
            self.expression_op_stack.append(op)
            self.tokenizer.advance()
            self.compile_term()

        while self.expression_op_stack:  # (op term)의 경우 후위연산자처럼 동작해야 하므로 stack에 op를 저장해서 나중에 사용
            op = self.expression_op_stack.pop()
            self.vm_writer.write_arithmetic(self.vm_writer.sign_to_op[op])

    def compile_term(self):
        sanity_check = True
        # test = self.tokenizer.tokenType() - 디버깅 용으로 추가한거

        if self.tokenizer.tokenType() == self.tokenizer.INT_CONST:
            val = self.tokenizer.intVal()
            self.vm_writer.write_push('constant', val)
        elif self.tokenizer.tokenType() == self.tokenizer.STRING_CONST:
            s = self.tokenizer.stringVal()[1:-1]  # 큰따옴표 제거
            self.vm_writer.write_push('constant', len(s))
            self.vm_writer.write_call(f'String.new', 1)  # maxLength 설정한 String 생성
            for c in s:
                self.vm_writer.write_push('constant', ord(c))  # unicode 상수
                self.vm_writer.write_call(f'String.appendChar', 1)  # 이거 2개인가?
        elif self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
            if self.tokenizer.keyWord() == 'this':
                self.vm_writer.write_push('pointer', 0)
            elif self.tokenizer.keyWord() == 'that':
                self.vm_writer.write_push('pointer', 1)
                pass
            elif self.tokenizer.keyWord() == 'true':
                self.vm_writer.write_push('constant', 0)  # 0은 false, 변환해서 true로 변경. 아마 바로 -1해도 될거 같긴 함.
                self.vm_writer.write_arithmetic('not')
                pass
            elif self.tokenizer.keyWord() == 'false' or self.tokenizer.keyWord() == 'null':
                self.vm_writer.write_push('constant', 0)
            else:
                self.vm_writer.write_push('constant', 0)

        elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
            outer_identifier = self.tokenizer.identifier()  # 경우에 따라 배열, 서브루틴의 이름

            self.tokenizer.advance()
            sanity_check = False
            if self.tokenizer.symbol() == "[":
                sanity_check = True
                self.tokenizer.advance()  # expression
                self.compile_expression()

                kind = self.symbol_table.kind_of(outer_identifier)
                index = self.symbol_table.index_of(outer_identifier)
                segment = self.kind_to_segment[kind]
                self.vm_writer.write_push(segment, index)  # TODO 이 부분 이해가 잘 안감

                self.vm_writer.write('add')

                self.vm_writer.write_pop('pointer', 1)
                self.vm_writer.write_push('that', 0)

            elif self.tokenizer.symbol() == ".":
                sanity_check = True
                self.tokenizer.advance()  # identifier - function or method name
                subroutine = self.tokenizer.identifier()
                self.tokenizer.advance()  # (
                self.tokenizer.advance()  # expression_list
                n_arg = self.compile_expression_list()

                self.vm_writer.write_call(f'{outer_identifier}.{subroutine}', n_arg)
            elif self.tokenizer.symbol() == "(":
                sanity_check = True
                self.tokenizer.advance()  # expression_list
                identifier = 'this'
                subroutine = outer_identifier
                n_arg = self.compile_expression_list()
                self.vm_writer.write_call(f'{identifier}.{subroutine}', n_arg)  # this.m(x,y)

        elif self.tokenizer.symbol() == "(":
            self.tokenizer.advance()  # expression
            self.compile_expression()
        elif self.tokenizer.symbol() == "~" or self.tokenizer.symbol() == "-":
            if self.tokenizer.symbol() == "~":
                self.vm_writer.write_arithmetic('not')
            elif self.tokenizer.symbol() == "-":
                self.vm_writer.write_arithmetic('neg')
            self.tokenizer.advance()
            self.compile_term()
            sanity_check = False
        else:  # 나머지 symbol은 compile_expression에서 op로 처리되기 때문에 생략
            sanity_check = False
            symbol = self.tokenizer.symbol()

        if sanity_check:
            self.tokenizer.advance()

    def compile_expression_list(self) -> int:
        """표현식 내의 int 수를 반환한다."""
        cnt = 0
        is_empty_list = self.tokenizer.tokenType() == self.tokenizer.SYMBOL and \
                        self.tokenizer.symbol() == ")"

        if not is_empty_list:
            cnt += 1
            self.tokenizer.advance()
            self.compile_expression()
            while self.tokenizer.tokenType() == self.tokenizer.SYMBOL and self.tokenizer.symbol() == ",":
                cnt += 1
                self.write_symbol()  # ,
                self.tokenizer.advance()
                self.compile_expression()  # expression

        return cnt


# API 끝

def write(self, text):
    self.file.write(f'{("  " * self.indent_level)}{text}')


def write_keyword(self):
    self.write(f'<keyword> {self.tokenizer.keyWord()} </keyword>\n')


def write_symbol(self):
    symbol = self.tokenizer.symbol()
    if symbol == "<":
        symbol = "&lt;"
    elif symbol == ">":
        symbol = "&gt;"
    elif symbol == "&":
        symbol = "&amp;"
    self.write(f'<symbol> {symbol} </symbol>\n')


def write_int_const(self):
    self.write(f'<integerConstant> {self.tokenizer.intVal()} </integerConstant>\n')


def write_str_const(self):
    self.write(f'<stringConstant> {self.tokenizer.stringVal()} </stringConstant>\n')


def write_identifier(self):
    self.write(f'<identifier> {self.tokenizer.identifier()} </identifier>\n')


def compile_type_and_varName(self, is_class, p_kind):
    """클래스인 경우 외부에서 kind를 주입받음. 서브루틴의 경우 kind는 local로 고정"""
    if is_class:
        kind = p_kind
    else:
        kind = LOCAL
    if self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
        # self.write_keyword()
        type = self.tokenizer.keyWord()  # void
    elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
        # self.write_identifier()  # identifier - class type
        type = self.tokenizer.tokenType()  # identifier - class type
    self.tokenizer.advance()
    # self.write_identifier()  # varName
    var_name = self.tokenizer.identifier()

    self.symbol_table.define(var_name, type, kind)

    self.tokenizer.advance()
    while self.tokenizer.symbol() == ",":
        # self.write_symbol()  # ,
        self.tokenizer.advance()
        # self.write_identifier()  # another varName
        another_var_name = self.tokenizer.identifier()
        self.symbol_table.define(another_var_name, type, kind)
        self.tokenizer.advance()
    # self.write_symbol()  # ;
    self.tokenizer.advance()


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
        self.ce = CompilationEngine(file_path + '.xml', self.jt, file_path + '.vm')
        self.ce.compile_class()
        self.ce.file.close()
        self.ce.vm_writer.file.close()


JackAnalyzer(sys.argv).run()

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
    arithmetic = {'ADD': 'add', 'SUB': 'sub', 'NEG': 'neg', 'EQ': 'eq', 'GT': 'gt', 'LT': 'lt', 'AND': 'and',
                  'OR': 'or', 'NOT': 'not'}

    def __init__(self, path):
        self.file = open(path, 'w')

    def write_push(self, segment, index):
        self.file.write(f'push {segment} {str(index)}\n')

    def write_pop(self, segment, index):
        self.file.write(f'call {segment} {str(index)}\n')

    def write_arithmetic(self, command):
        self.file.write(f'{self.arithmetic[command]}\n')

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

    def compile_class(self):
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.write("<class>\n")
            self.indent_level += 1

            self.write_keyword()  # class

            self.tokenizer.advance()
            self.write_identifier()  # identifier - class name

            self.tokenizer.advance()
            self.write_symbol()  # {

            self.tokenizer.advance()
            while self.tokenizer.keyWord() == "static" or \
                    self.tokenizer.keyWord() == "field":
                self.compile_class_var_dec()
            while self.tokenizer.keyWord() == "constructor" or \
                    self.tokenizer.keyWord() == "function" \
                    or self.tokenizer.keyWord() == "method":
                self.compile_subroutine()

            self.write_symbol()  # }

            self.indent_level -= 1
            self.write("</class>\n")

    def compile_class_var_dec(self):
        self.write(f'<classVarDec>\n')
        self.indent_level += 1
        self.write_keyword()  # static, field

        self.tokenizer.advance()
        self.compile_type_and_varName()

        self.indent_level -= 1
        self.write(f'</classVarDec>\n')

    def compile_subroutine(self):
        self.write(f'<subroutineDec>\n')
        self.indent_level += 1
        self.write_keyword()  # constructor, method, function

        self.tokenizer.advance()
        if self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
            self.write_keyword()  # void
        elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
            self.write_identifier()  # identifier - return type

        self.tokenizer.advance()
        self.write_identifier()  # identifier - name

        self.tokenizer.advance()
        self.write_symbol()  # (

        self.tokenizer.advance()
        self.compile_parameter_list()  # 파라미터

        self.write_symbol()  # )

        self.tokenizer.advance()
        self.write(f'<subroutineBody>\n')
        self.indent_level += 1
        self.write_symbol()  # {

        self.tokenizer.advance()
        while self.tokenizer.keyWord() == "var":
            self.compile_var_dec()  # var 처리

        self.compile_statements()  # statements

        self.write_symbol()  # }
        self.indent_level -= 1
        self.write(f'</subroutineBody>\n')
        self.indent_level -= 1
        self.write(f'</subroutineDec>\n')
        self.tokenizer.advance()

    def compile_parameter_list(self):
        self.write(f'<parameterList>\n')
        self.indent_level += 1

        while self.tokenizer.tokenType() != self.tokenizer.SYMBOL:  # 현재 토큰이 SYMBOL 라는건 토큰이 ) 되었다는 의미
            if self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
                self.write_keyword()  # type
            elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
                self.write_identifier()  # identifier

            self.tokenizer.advance()
            self.write_identifier()  # identifier
            self.tokenizer.advance()

            if self.tokenizer.symbol() == ",":
                self.write_symbol()  # ,
                self.tokenizer.advance()

        self.indent_level -= 1
        self.write(f'</parameterList>\n')

    def compile_var_dec(self):
        self.write(f'<varDec>\n')
        self.indent_level += 1

        self.write_keyword()  # var
        self.tokenizer.advance()
        self.compile_type_and_varName()  # type varName

        self.indent_level -= 1
        self.write(f'</varDec>\n')

    def compile_statements(self):
        self.write(f'<statements>\n')
        self.indent_level += 1

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

        self.indent_level -= 1
        self.write(f'</statements>\n')

    def compile_do(self):
        self.write(f'<doStatement>\n')
        self.indent_level += 1
        self.write_keyword()  # do

        self.tokenizer.advance()
        self.write_identifier()  # identifier - method(this 생략 시) or class/instance name(클래스/인스턴스 호출 시)

        self.tokenizer.advance()
        if self.tokenizer.symbol() == ".":  # 클래스/인스턴스 호출 시
            self.write_symbol()  # .
            self.tokenizer.advance()
            self.write_identifier()  # identifier - function or method name
            self.tokenizer.advance()

        self.write_symbol()  # (

        self.tokenizer.advance()
        self.compile_expression_list()

        self.write_symbol()  # )

        self.tokenizer.advance()
        self.write_symbol()  # ;

        self.indent_level -= 1
        self.write(f'</doStatement>\n')
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
        self.write(f'<returnStatement>\n')
        self.indent_level += 1
        self.write_keyword()  # return

        self.tokenizer.advance()
        if self.tokenizer.tokenType() != self.tokenizer.SYMBOL and \
                self.tokenizer.symbol() != ";":  # if not return void
            self.compile_expression()  # expression

        self.write_symbol()  # ;

        self.indent_level -= 1
        self.write(f'</returnStatement>\n')
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
        # term (op term)*

        self.write(f'<expression>\n')
        self.indent_level += 1

        self.compile_term()
        # op라면 연산이 이어지는 경우이므로 (op term) 반복, 이 과정에서 다음 값까지 미리 읽은 상태가 됨
        while self.tokenizer.tokenType() == self.tokenizer.SYMBOL and \
                self.tokenizer.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.write_symbol()
            self.tokenizer.advance()
            self.compile_term()

        self.indent_level -= 1
        self.write(f'</expression>\n')

    def compile_term(self):
        sanity_check = True
        self.write(f'<term>\n')
        self.indent_level += 1
        if self.tokenizer.tokenType() == self.tokenizer.INT_CONST:
            self.write_int_const()
        elif self.tokenizer.tokenType() == self.tokenizer.STRING_CONST:
            self.write_str_const()
        elif self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
            self.write_keyword()
        elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
            self.write_identifier()

            self.tokenizer.advance()
            sanity_check = False
            if self.tokenizer.symbol() == "[":
                sanity_check = True
                self.write_symbol()
                self.tokenizer.advance()
                self.compile_expression()
                self.write_symbol()
            elif self.tokenizer.symbol() == ".":
                sanity_check = True
                self.write_symbol()
                self.tokenizer.advance()
                self.write_identifier()
                self.tokenizer.advance()
                self.write_symbol()
                self.tokenizer.advance()
                self.compile_expression_list()
                self.write_symbol()
            elif self.tokenizer.symbol() == "(":
                sanity_check = True
                self.write_symbol()
                self.tokenizer.advance()
                self.compile_expression_list()
                self.write_symbol()

        elif self.tokenizer.symbol() == "(":
            self.write_symbol()
            self.tokenizer.advance()
            self.compile_expression()
            self.write_symbol()
        elif self.tokenizer.symbol() == "~" or self.tokenizer.symbol() == "-":
            self.write_symbol()
            self.tokenizer.advance()
            self.compile_term()
            sanity_check = False

        if sanity_check:
            self.tokenizer.advance()

        self.indent_level -= 1
        self.write(f'</term>\n')

    def compile_expression_list(self):
        self.write(f'<expressionList>\n')
        self.indent_level += 1

        is_empty_list = self.tokenizer.tokenType() == self.tokenizer.SYMBOL and \
                        self.tokenizer.symbol() == ")"

        if not is_empty_list:
            self.compile_expression()
            self.compile_remaining_expressions()

        self.indent_level -= 1
        self.write(f'</expressionList>\n')

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

    def compile_type_and_varName(self):
        if self.tokenizer.tokenType() == self.tokenizer.KEYWORD:
            self.write_keyword()  # type
        elif self.tokenizer.tokenType() == self.tokenizer.IDENTIFIER:
            self.write_identifier()  # identifier - class type
        self.tokenizer.advance()
        self.write_identifier()  # varName
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self.write_symbol()  # ,
            self.tokenizer.advance()
            self.write_identifier()  # another varName
            self.tokenizer.advance()
        self.write_symbol()  # ;
        self.tokenizer.advance()

    def compile_remaining_expressions(self):
        while self.tokenizer.tokenType() == self.tokenizer.SYMBOL and self.tokenizer.symbol() == ",":
            self.write_symbol()  # ,
            self.tokenizer.advance()
            self.compile_expression()  # expression


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


JackAnalyzer(sys.argv).run()

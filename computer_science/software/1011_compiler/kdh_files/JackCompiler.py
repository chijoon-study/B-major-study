import glob
import os
import re
import sys

sys.setrecursionlimit(100)

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


class SymbolTable:
    def __init__(self):
        self.class_table = {}
        self.sub_routine_table = {}
        self.kind_idx = {'field': 0, 'static': 0, 'local': 0, 'argument': 0}

    def start_subroutine(self):
        self.sub_routine_table = {}
        self.kind_idx['local'] = 0
        self.kind_idx['argument'] = 0

    def define(self, name, type_, kind):
        if kind in ['field', 'static']:
            if kind == 'field':
                kind = 'this'
            self.class_table[name] = [type_, kind, self.kind_idx[kind]]
        elif kind in ['local', 'argument']:
            self.sub_routine_table[name] = [type_, kind, self.kind_idx[kind]]
        self.kind_idx[kind] += 1

    def var_count(self, kind):
        return self.kind_idx[kind]

    def kind_of(self, name):
        return self.get_row(name)[1]

    def type_of(self, name):
        return self.get_row(name)[0]

    def index_of(self, name):
        return self.get_row(name)[2]

    def get_row(self, name):
        if name in self.sub_routine_table:
            return self.sub_routine_table[name]
        if name in self.class_table:
            return self.class_table[name]
        return None


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

    def __init__(self, vm_path):
        self.file = open(vm_path, 'w')

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

    def write_call(self, name, n_args):
        self.file.write(f'call {name} {str(n_args)}\n')

    def write_function(self, name, n_vars):
        self.file.write(f'function {name} {str(n_vars)}\n')

    def write_return(self):
        self.file.write('return\n')


class JackTokenizer:
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

    def has_more_tokens(self):
        if re.fullmatch(EMPTY_TEXT_PATTERN, self.text):
            return False
        else:
            return True

    def advance(self):
        if self.has_more_tokens():
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
        else:
            print("No more tokens")

        print(self._currentToken)

    def token_type(self):
        return self._tokenType

    def key_word(self):
        if self._tokenType == self.KEYWORD:
            return self._currentToken
        else:
            raise Exception(f"current token's type is {self._tokenType}, not 0(keyword)")

    def symbol(self):
        if self._tokenType == self.SYMBOL:
            return self._currentToken
        else:
            raise Exception(f"current token's type is {self._tokenType}, not 1(symbol)")

    def identifier(self):
        if self._tokenType == self.IDENTIFIER:
            return self._currentToken
        else:
            raise Exception(f"current token's type is {self._tokenType}, not 2(identifier)")

    def int_val(self):
        if self._tokenType == self.INT_CONST:
            return int(self._currentToken)
        else:
            raise Exception(f"current token's type is {self._tokenType}, not 3(int value)")

    def string_val(self):
        if self._tokenType == self.STRING_CONST:
            return self._currentToken
        else:
            raise Exception(f"current token's type is {self._tokenType}, not 4(string value)")


class CompilationEngine:
    def __init__(self, path, jack_tokenizer: JackTokenizer):
        self.class_name = ''
        self.if_counter = 0
        self.while_counter = 0
        self.expression_op_stack = []

        self.tokenizer = jack_tokenizer
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(path)

    def compile_class(self):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()  # class
            self.tokenizer.advance()  # class name
            self.class_name = self.tokenizer.identifier()
            self.tokenizer.advance()  # {

            self.tokenizer.advance()  # static | field | constructor | function | method
            while self.tokenizer.key_word() in ['static', 'field']:
                self.compile_class_var_dec()
            while self.tokenizer.token_type() == self.tokenizer.KEYWORD and \
                    self.tokenizer.key_word() in ['constructor', 'function', 'method']:
                self.compile_subroutine()

            self.tokenizer.advance()  # }

    def compile_class_var_dec(self):
        self.compile_type_and_varName(self.tokenizer.key_word())

    def compile_subroutine(self):
        self.symbol_table.start_subroutine()
        func_type = self.tokenizer.key_word()


        self.tokenizer.advance()  # return type
        self.tokenizer.advance()  # function name
        name = self.tokenizer.identifier()
        self.tokenizer.advance()  # (

        self.compile_parameter_list(func_type)

        self.compile_subroutine_body(name, func_type)

        self.tokenizer.advance()

    def compile_parameter_list(self, func_type):
        self.tokenizer.advance()  # parameter type | )

        if func_type == 'method':
            self.symbol_table.define('this', self.class_name, 'argument')

        if self.tokenizer.token_type() != self.tokenizer.SYMBOL:
            self.compile_type_and_varName('argument')  # {
            return

        self.tokenizer.advance()  # {

    def compile_subroutine_body(self, func_name, func_type):
        n_args = 0
        self.tokenizer.advance()  # var or statement
        if self.tokenizer.key_word() == 'var':
            n_args = self.compile_var_dec()  # statement
        self.vm_writer.write_function(f'{self.class_name}.{func_name}', n_args)

        if func_type == 'method':
            self.vm_writer.write_push('argument', 0)
            self.vm_writer.write_pop('pointer', 0)
        elif func_type == 'constructor':
            self.vm_writer.write_push('constant', self.symbol_table.var_count('field'))
            self.vm_writer.write_call('Memory.alloc', '1')
            self.vm_writer.write_pop('pointer', 0)

        self.compile_statements()

    def compile_var_dec(self):
        cnt = 0
        while self.tokenizer.key_word() == 'var':
            cnt += self.compile_type_and_varName('local')

        return cnt

    def compile_statements(self):
        while self.tokenizer.token_type() == self.tokenizer.KEYWORD:
            if self.tokenizer.key_word() == "let":
                self.compile_let()
            elif self.tokenizer.key_word() == "if":
                self.compile_if()
            elif self.tokenizer.key_word() == "while":
                self.compile_while()
            elif self.tokenizer.key_word() == "do":
                self.compile_do()
            elif self.tokenizer.key_word() == "return":
                self.compile_return()

    def compile_let(self):
        self.tokenizer.advance()  # target var name
        name = self.tokenizer.identifier()
        is_array = False

        self.tokenizer.advance()  # [ | =
        if self.tokenizer.symbol() == "[":
            is_array = True
            self.compile_array_index(name)  # ]
            self.tokenizer.advance()  # =

        self.tokenizer.advance()
        self.compile_expression()  # ;
        if is_array:
            self.vm_writer.write_pop("temp", 0)
            self.vm_writer.write_pop("pointer", 1)
            self.vm_writer.write_push("temp", 0)
            self.vm_writer.write_pop("that", 0)
        else:
            self.vm_writer.write_pop(self.symbol_table.kind_of(name), self.symbol_table.index_of(name))

        self.tokenizer.advance()  # next statement keyword

    def compile_array_index(self, name):
        # current token '['
        # name = 'arr'[i]
        self.vm_writer.write_push(self.symbol_table.kind_of(name), self.symbol_table.index_of(name))
        self.write_array_index()
        self.vm_writer.write_arithmetic('add')

    def write_array_index(self):
        self.compile_expression()
        self.tokenizer.advance()  # get ']' symbol

    def compile_if(self):
        self.tokenizer.advance()  # (
        self.compile_expression()
        self.tokenizer.advance()  # )
        self.if_counter += 1

        self.vm_writer.write_if('IF_TRUE' + str(self.if_counter))
        self.vm_writer.write_goto('IF_FALSE' + str(self.if_counter))
        self.vm_writer.write_label('IF_TRUE' + str(self.if_counter))

        self.tokenizer.advance()  # {
        self.compile_statements()  # }

        self.tokenizer.advance()  # else or next statement keyword
        if self.tokenizer.token_type() == self.tokenizer.KEYWORD and \
                self.tokenizer.key_word() == "else":
            self.vm_writer.write_goto('IF_END' + str(self.if_counter))
            self.vm_writer.write_label('IF_FALSE' + str(self.if_counter))
            self.tokenizer.advance()  # get '{' symbol
            self.compile_statements()  # }
            self.vm_writer.write_label('IF_END' + str(self.if_counter))
        else:
            self.vm_writer.write_label('IF_FALSE' + str(self.if_counter))

    def compile_while(self):
        self.write("<whileStatement>")
        self.indent_level += 1
        self.write_keyword()

        self.tokenizer.advance()
        self.write_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        self.write_symbol()

        self.tokenizer.advance()
        self.write_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        self.write_symbol()

        self.indent_level -= 1
        self.write("</whileStatement>")
        self.tokenizer.advance()

    def compile_do(self):
        self.tokenizer.advance()  # var name or method name
        self.compile_subroutine_call(is_do=True)  # ;
        self.vm_writer.write_pop('temp', '0')  # do는 반환값안 받으니까 반환값 버림
        self.tokenizer.advance()  # next statement keyword

    def compile_subroutine_call(self, name='', is_do=False):
        if name:
            first_name = name
        else:
            first_name = self.tokenizer.identifier()
            self.tokenizer.advance()  # . or (

        if self.tokenizer.symbol() == '(':  # method()
            self.vm_writer.write_push('pointer', 0)  # this
            full_name = self.class_name + '.' + first_name
        elif self.tokenizer.symbol() == '.':  # varname.subroutine(exp)
            if self.symbol_table.get_row(first_name) is not None:  # method, not function
                self.vm_writer.write_push(self.symbol_table.kind_of(first_name), self.symbol_table.index_of(first_name))  # this
                first_name = self.symbol_table.type_of(first_name)
            self.tokenizer.advance()
            last_name = self.tokenizer.identifier()
            full_name = first_name + '.' + last_name
        else:
            raise Exception("neither '(' nor '.' symbol")

        self.tokenizer.advance()  # (
        n_args = self.compile_expression_list()  # )
        self.vm_writer.write_call(full_name, n_args)

        if is_do:
            self.tokenizer.advance()  # ;

    def compile_return(self):
        self.tokenizer.advance()  # ; or return value
        is_void = (self.tokenizer.token_type() == self.tokenizer.SYMBOL and
                   self.tokenizer.symbol() == ';')
        if not is_void:
            self.compile_expression()  # expression
        else:
            self.vm_writer.write_push('constant', 0)

        self.vm_writer.write_arithmetic('return')

        self.tokenizer.advance()

    def compile_expression(self):
        self.compile_term()
        while self.tokenizer.token_type() == self.tokenizer.SYMBOL and \
                self.tokenizer.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            op = self.tokenizer.symbol()
            self.expression_op_stack.append(op)
            self.tokenizer.advance()
            self.compile_term()

        while self.expression_op_stack:
            op = self.expression_op_stack.pop()
            self.vm_writer.write_arithmetic(self.vm_writer.sign_to_op[op])

    def compile_term(self):
        print(self.tokenizer._currentToken, 'term')
        sanity_check = True

        if self.tokenizer.token_type() == self.tokenizer.INT_CONST:
            val = self.tokenizer.int_val()
            self.vm_writer.write_push('constant', val)
        elif self.tokenizer.token_type() == self.tokenizer.STRING_CONST:
            string = self.tokenizer.string_val()[1:-1]  # 큰따옴표 제거
            self.vm_writer.write_push('constant', len(string))
            self.vm_writer.write_call(f'String.new', 1)
            for char in string:
                self.vm_writer.write_push('constant', ord(char))  # unicode 상수
                self.vm_writer.write_call(f'String.appendChar', 1)
        elif self.tokenizer.token_type() == self.tokenizer.KEYWORD:
            if self.tokenizer.key_word() == "this":
                self.vm_writer.write_push('pointer', 0)
            else:
                self.vm_writer.write_push('constant', 0)
                if self.tokenizer.key_word() == "true":
                    self.vm_writer.write_arithmetic('not')
        elif self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            name = self.tokenizer.identifier()
            self.tokenizer.advance()  # [ or . or (
            sanity_check = False
            if self.tokenizer.symbol() == "[":  # e.g) identifier[expression]
                sanity_check = True
                self.compile_array_index(name)  # ]
            elif self.tokenizer.symbol() == ".":  # e.g) identifier.function(exp_list)
                sanity_check = True
                self.compile_subroutine_call(name)  # )
            elif self.tokenizer.symbol() == "(":  # e.g) identifier(exp_list)
                sanity_check = True
                self.compile_subroutine_call(name)  # )
            else:
                self.vm_writer.write_push(self.symbol_table.kind_of(name), self.symbol_table.index_of(name))

        elif self.tokenizer.symbol() == "(":
            self.tokenizer.advance()
            self.compile_expression()  # )
        elif self.tokenizer.symbol() == "~" or self.tokenizer.symbol() == "-":  # unary op
            op = self.tokenizer.symbol()
            self.tokenizer.advance()
            self.compile_term()
            if op == '-':
                self.vm_writer.write_arithmetic('neg')
            elif op == '~':
                self.vm_writer.write_arithmetic('not')
            sanity_check = False

        if sanity_check:
            self.tokenizer.advance()

    def compile_expression_list(self):
        cnt = 0
        self.tokenizer.advance()  # ) or exp
        is_no_expression = self.tokenizer.token_type() == self.tokenizer.SYMBOL and \
                           self.tokenizer.symbol() == ")"

        if not is_no_expression:
            cnt += 1
            self.compile_expression()  # , or )
            while self.tokenizer.token_type() == self.tokenizer.SYMBOL and \
                    self.tokenizer.symbol() == ",":
                cnt += 1
                self.tokenizer.advance()
                self.compile_expression()

        return cnt

    def compile_type_and_varName(self, kind_):
        cnt = 1
        self.tokenizer.advance()
        type = self._type()
        self.tokenizer.advance()
        name = self.tokenizer.identifier()
        self.tokenizer.advance()  # ; or , or )
        self.symbol_table.define(name, type, kind_)

        while self.tokenizer.symbol() == ",":
            self.tokenizer.advance()
            name = self.tokenizer.identifier()
            self.symbol_table.define(name, type, kind_)
            self.tokenizer.advance()  # ; or , or )
            cnt += 1

        self.tokenizer.advance()

        return cnt

    def _symbol(self):
        symbol = self.tokenizer.symbol()
        if self.tokenizer.symbol() == "<":
            symbol = "&lt;"
        elif self.tokenizer.symbol() == ">":
            symbol = "&gt;"
        elif self.tokenizer.symbol() == "&":
            symbol = "&amp;"

        return symbol

    def _type(self):
        if self.tokenizer.token_type() == self.tokenizer.KEYWORD:
            return self.tokenizer.key_word()
        elif self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            return self.tokenizer.identifier()


class JackCompiler:
    def __init__(self, args):
        self.path = args[1]
        self.jt = None
        self.ce = None

    def run(self):
        if os.path.isdir(self.path):
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
        self.ce = CompilationEngine(file_path + '.vm', self.jt)
        self.ce.compile_class()
        self.ce.vm_writer.file.close()


JackCompiler(['','/Users/humanlearning/chijoon-study/computer_science/software/1011_compiler/kdh_files/Seven']).run()

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
        self.file = open(path, "w")
        self.tokenizer = jack_tokenizer
        self.indent_level = 0

    def compile_class(self):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()  # class
            self.write("<class>")
            self.indent_level += 1
            self.write_keyword()
            self.tokenizer.advance()  # class name
            self.write_identifier()
            self.tokenizer.advance()  # {
            self.write_symbol()

            self.tokenizer.advance()  # static | field | constructor | function | method
            while self.tokenizer.key_word() in ['static', 'field']:
                self.compile_class_var_dec()
            while self.tokenizer.token_type() == self.tokenizer.KEYWORD and \
                    self.tokenizer.key_word() in ['constructor', 'function', 'method']:
                self.compile_subroutine()

            self.tokenizer.advance()  # }
            self.write_symbol()
            self.indent_level -= 1
            self.write("</class>")

    def compile_class_var_dec(self):
        self.write("<classVarDec>")
        self.indent_level += 1

        self.write_keyword()
        self.tokenizer.advance()  # int | char | boolean | class name
        self.compile_type_and_varName()

        self.indent_level -= 1
        self.write("</classVarDec>")

    def compile_subroutine(self):
        self.write("<subroutineDec>")
        self.indent_level += 1
        self.write_keyword()
        self.tokenizer.advance()  # return type
        self.write_type()
        self.tokenizer.advance()  # function name
        self.write_identifier()
        self.tokenizer.advance()  # (
        self.write_symbol()

        self.compile_parameter_list()

        self.write_symbol()

        self.compile_subroutine_body()

        self.indent_level -= 1
        self.write("</subroutineDec>")
        self.tokenizer.advance()

    def compile_parameter_list(self):
        self.write("<parameterList>")
        self.indent_level += 1
        self.tokenizer.advance()  # parameter type | )
        while self.tokenizer.token_type() != self.tokenizer.SYMBOL:
            self.write_type()
            self.tokenizer.advance()  # parameter name
            self.write_identifier()
            self.tokenizer.advance()  # , | )
            if self.tokenizer.symbol() == ',':
                self.write_symbol()
                self.tokenizer.advance()

        self.indent_level -= 1
        self.write("</parameterList>")

    def compile_subroutine_body(self):
        self.write("<subroutineBody>")
        self.indent_level += 1
        self.tokenizer.advance()  # {
        self.write_symbol()

        self.tokenizer.advance()  # var | let | if | while | do | return
        while self.tokenizer.key_word() == 'var':
            self.compile_var_dec()

        self.compile_statements()

        self.write_symbol()

        self.indent_level -= 1
        self.write("</subroutineBody>")

    def compile_var_dec(self):
        self.write("<varDec>")
        self.indent_level += 1

        self.write_keyword()
        self.tokenizer.advance()  # var type
        self.compile_type_and_varName()

        self.indent_level -= 1
        self.write("</varDec>")

    def compile_statements(self):
        self.write("<statements>")
        self.indent_level += 1

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

        self.indent_level -= 1
        self.write("</statements>")

    def compile_let(self):
        self.write("<letStatement>")
        self.indent_level += 1
        self.write_keyword()

        self.tokenizer.advance()  # var name
        self.write_identifier()

        self.tokenizer.advance()  # [ | =
        if self.tokenizer.symbol() == "[":
            self.write_symbol()

            self.compile_expression()

            self.tokenizer.advance()  # ]
            self.write_symbol()

            self.tokenizer.advance()  # =

        self.write_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        self.write_symbol()  # ;

        self.indent_level -= 1
        self.write("</letStatement>")
        self.tokenizer.advance()

    def compile_if(self):
        self.write("<ifStatement>")
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

        self.tokenizer.advance()
        if self.tokenizer.token_type() == self.tokenizer.KEYWORD and \
                self.tokenizer.key_word() == "else":
            self.write_keyword()

            self.tokenizer.advance()
            self.write_symbol()

            self.tokenizer.advance()
            self.compile_statements()

            self.write_symbol()
            self.tokenizer.advance()

        self.indent_level -= 1
        self.write("</ifStatement>")

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
        self.write("<doStatement>")
        self.indent_level += 1
        self.write_keyword()

        self.tokenizer.advance()  # function

        self.write_identifier()
        self.tokenizer.advance()
        if self.tokenizer.symbol() == ".":
            self.write_symbol()
            self.tokenizer.advance()
            self.write_identifier()
            self.tokenizer.advance()

        self.write_symbol()

        self.tokenizer.advance()
        self.compile_expression_list()

        self.write_symbol()

        self.tokenizer.advance()
        self.write_symbol()

        self.indent_level -= 1
        self.write("</doStatement>")
        self.tokenizer.advance()

    def compile_return(self):
        self.write("<returnStatement>")
        self.indent_level += 1
        self.write_keyword()

        self.tokenizer.advance()

        is_no_return = self.tokenizer.token_type() == self.tokenizer.SYMBOL and \
                self.tokenizer.symbol() == ";"
        if not is_no_return:
            self.compile_expression()

        self.write_symbol()

        self.indent_level -= 1
        self.write("</returnStatement>")
        self.tokenizer.advance()

    def compile_expression(self):
        self.write("<expression>")
        self.indent_level += 1

        self.compile_term()
        while self.tokenizer.token_type() == self.tokenizer.SYMBOL and \
                self.tokenizer.symbol() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']:
            self.write_symbol()
            self.tokenizer.advance()
            self.compile_term()

        self.indent_level -= 1
        self.write("</expression>")

    def compile_term(self):
        sanity_check = True
        self.write("<term>")
        self.indent_level += 1

        if self.tokenizer.token_type() == self.tokenizer.INT_CONST:
            self._write_int_const()
        elif self.tokenizer.token_type() == self.tokenizer.STRING_CONST:
            self._write_str_const()
        elif self.tokenizer.token_type() == self.tokenizer.KEYWORD:
            self.write_keyword()
        elif self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            self.write_identifier()

            self.tokenizer.advance()  # [ or . or (
            sanity_check = False
            if self.tokenizer.symbol() == "[":  # e.g) identifier[expression]
                sanity_check = True
                self.write_symbol()
                self.tokenizer.advance()
                self.compile_expression()
                self.write_symbol()
            elif self.tokenizer.symbol() == ".":  # e.g) identifier.function();
                sanity_check = True
                self.write_symbol()
                self.tokenizer.advance()  # function name
                self.write_identifier()
                self.tokenizer.advance()  # (
                self.write_symbol()
                self.tokenizer.advance()
                self.compile_expression_list()
                self.write_symbol()
            elif self.tokenizer.symbol() == "(":  # e.g) identifier();
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
        elif self.tokenizer.symbol() == "~" or self.tokenizer.symbol() == "-":  # unary op
            self.write_symbol()
            self.tokenizer.advance()
            self.compile_term()
            sanity_check = False

        if sanity_check:
            self.tokenizer.advance()

        self.indent_level -= 1
        self.write("</term>")

    def compile_expression_list(self):
        self.write("<expressionList>")
        self.indent_level += 1

        is_no_expression = self.tokenizer.token_type() == self.tokenizer.SYMBOL and \
                        self.tokenizer.symbol() == ")"

        if not is_no_expression:
            self.compile_expression()
            while self.tokenizer.token_type() == self.tokenizer.SYMBOL and \
                    self.tokenizer.symbol() == ",":
                self.write_symbol()
                self.tokenizer.advance()
                self.compile_expression()

        self.indent_level -= 1
        self.write("</expressionList>")

    def compile_type_and_varName(self):
        self.write_type()
        self.tokenizer.advance()
        self.write_identifier()
        self.tokenizer.advance()
        while self.tokenizer.symbol() == ",":
            self.write_symbol()
            self.tokenizer.advance()
            self.write_identifier()
            self.tokenizer.advance()
        self.write_symbol()
        self.tokenizer.advance()

    def write(self, text, newline=True):
        if newline:
            self.file.write(f'{("  " * self.indent_level)}{text}\n')
        else:
            self.file.write(f'{("  " * self.indent_level)}{text}')

    def write_keyword(self):
        self.write(f"<keyword> {self.tokenizer.key_word()} </keyword>")

    def write_symbol(self):
        symbol = self.tokenizer.symbol()
        if self.tokenizer.symbol() == "<":
            symbol = "&lt;"
        elif self.tokenizer.symbol() == ">":
            symbol = "&gt;"
        elif self.tokenizer.symbol() == "&":
            symbol = "&amp;"

        self.write(f"<symbol> {symbol} </symbol>")

    def write_identifier(self):
        self.write(f"<identifier> {self.tokenizer.identifier()} </identifier>")

    def _write_int_const(self):
        self.write(f"<integerConstant> {self.tokenizer.int_val()} </integerConstant>")

    def _write_str_const(self):
        self.write(f"<stringConstant> {self.tokenizer.string_val()} </stringConstant>")

    def write_type(self):
        if self.tokenizer.token_type() == self.tokenizer.KEYWORD:
            self.write_keyword()
        elif self.tokenizer.token_type() == self.tokenizer.IDENTIFIER:
            self.write_identifier()


class JackAnalyzer:
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
        self.ce = CompilationEngine(file_path + '.xml', self.jt)
        self.ce.compile_class()
        self.ce.file.close()

JackAnalyzer(sys.argv).run()


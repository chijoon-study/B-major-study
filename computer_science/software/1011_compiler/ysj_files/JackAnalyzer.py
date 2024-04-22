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
        self.ce.compile_class()


JackAnalyzer(sys.argv).run()

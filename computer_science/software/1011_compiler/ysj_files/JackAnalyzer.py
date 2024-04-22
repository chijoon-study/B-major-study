import glob
import os
import re
import heapq
import sys


class JackTokenizer:
    def __init__(self, path):
        self.file = open(path, 'r')
        self.currentLineTokens = []  # 현재 로드된 토큰, 가장 앞의 존재하는 토큰부터 가져온다.
        self.cur_type = None
        self.cur_val = None
        pass

    def has_more_tokens(self) -> bool:
        """file에 더 많은 토큰이 있는가?"""
        '''
        다음 명령어가 있는지 확인하면서 다음 결과 바로 앞까지 이동.
        변경/조회 기능이 합쳐져있기는 한데, 멱등성이 보장되니까 괜찮을듯?
        '''
        if len(self.currentLineTokens) >= 2:  # currentLineTokens이 남았으면 아직 토큰 있는거임
            return True
        else:
            while True:
                current_position = self.file.tell()
                line = self.file.readline()
                if line == '':  # 마지막 줄인가?
                    return False
                line = line.strip()
                if line.startswith('//'):  # 한줄 주석인가?
                    continue
                elif line == '':  # 줄바꿈인가?
                    continue
                elif line.startswith('/*') or line.startswith('/**') or line.startswith('*'):  # 여러줄 주석인가?
                    continue
                else:
                    self.file.seek(current_position)
                    return True

    def advance(self) -> None:
        """다음 토큰을 현재 토큰으로. has_more_tokens가 true일 때만 사용해야 함"""
        if len(self.currentLineTokens) < 2:  # self.currentLineTokens가 비면 새로운 값 가져오기
            line = self.file.readline().strip()
            self.currentLineTokens.extend(self.get_tokens(line))
        else:  # 남아있으면 기존 self.currentLineTokens에서 기존 값 빼고 다음 값 사용하기
            heapq.heappop(self.currentLineTokens)
        cur_token = self.currentLineTokens[0][1]
        self.cur_type = cur_token[0]
        self.cur_val = self.get_val(cur_token[0], cur_token[1])

    def token_type(self) -> str:
        """현재 토큰의 타입 반환"""
        return self.cur_type

    def keyword(self) -> str:
        """token_type이 KEYWORD일때만 호출해야 함. 현재 토큰의 키워드 반환"""
        return self.cur_val

    def symbol(self) -> str:
        """token_type이 SYMBOL일때만 호출해야 함. 현재 토큰의 문자 반환."""
        return self.cur_val

    def identifier(self) -> str:
        """token_type이 IDENTIFIER일때만 호출해야 함. 현재 토큰의 문자열 반환."""
        return self.cur_val

    def intVal(self) -> int:
        """token_type이 INT_CONST일때만 호출해야 함. 현재 토큰의 정수값 반환."""
        return self.cur_val

    def stringVal(self) -> str:
        """token_type이 STRING_CONST일때만 호출해야 함. 현재 토큰의 문자열에서 따옴표를 제거하고 반환."""
        return self.cur_val

    # 여기까지 API

    def has_term_child(self) -> bool:
        """해당 term(토큰)이 햐위 term을 가지는지 확인함. 예를 들어. arr[i]는 arr는 하위 i를 가짐"""
        # term의 하위 term을 적을 때, 줄바꿈이 발생하지 않으므로 self.currentLineTokens을 확인해서 값을 구할 수 있음.
        # 예를 들어, arr[i]를 표현할 때, 다음처럼 표현하지는 않는다.
        # arr
        # [i];
        if len(self.currentLineTokens) < 2:
            return False
        next_token = heapq.nsmallest(2, self.currentLineTokens)[1][1]  # 값 작은 순으로 2개 뽑아서 2번째 가지기 (= 현재 다음 토큰 가져요기)
        if next_token[1] in "[(.":  # [ ( . 중 하나면 하위 term이 있다는 소리
            return True
        else:
            return False

    def close(self, path):
        """self.file을 포함한 자원 해제"""
        pass

    def get_tokens(self, text) -> list:
        """입력받은 텍스트의 token 목록을 반환함"""
        matches = []
        for name in ['KEYWORD', 'SYMBOL', 'INT_CONST', 'STRING_CONST', 'IDENTIFIER']:
            pattern = self.patterns[name]
            for match in re.finditer(pattern, text):
                matches.append((match.start(), (name, match.group())))
        heapq.heapify(matches)
        return matches

    def get_val(self, token_type: str, value: str):
        """type에 맞는 값 설정"""
        if token_type == 'KEYWORD':
            return value
        if token_type == 'SYMBOL':
            return value
        if token_type == 'IDENTIFIER':
            return value
        if token_type == 'INT_CONST':
            return int(value)
        if token_type == 'STRING_CONST':
            return value[1:-1]  # 앞 뒤 따옴표 제거
        raise Exception

    '''
    AI 도움을 받아서 정규식을 구현함
    AI 피셜
    'KEYWORD': 프로그래밍 언어의 키워드를 매칭합니다. 예를 들어 class, function, if, return 등의 키워드를 식별합니다.
    'SYMBOL': 프로그래밍 언어에서 사용되는 기호를 매칭합니다. 예를 들어 {, }, (, ), [, ], ,, ;, +, -, *, /, &, |, <, >, =, ~ 등의 기호를 식별합니다.
    'INT_CONST': 정수 상수를 매칭합니다. 0부터 32767까지의 정수 상수를 인식할 수 있습니다.
    'STRING_CONST': 큰따옴표로 묶인 문자열을 매칭하며, 문자열 내부에 새줄 문자가 없어야 하고, (우측 내용은 책에서 포함된 건 아님, AI가 이렇게 구현했는데, 별로 중요한건 아니라 냅둔거) 큰따옴표나 백슬래시는 백슬래시로 이스케이프되어야 합니다.
    'IDENTIFIER': 식별자를 매칭합니다. 알파벳 또는 언더스코어로 시작하고, 알파벳, 숫자, 언더스코어로 이루어진 식별자를 인식합니다.
    '''
    patterns = {
        'KEYWORD': r'(?P<keyword>class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)',
        'SYMBOL': r'(?P<symbol>[{}()[\].,;+\-*/&|<>=~])',
        'INT_CONST': r'(?P<integerConstant>0|[1-9]\d{0,4}|[12]\d{4}|3[01]\d{3}|32[0-6][0-7][0-6]|327[0-5][0-7])',
        'STRING_CONST': r'(?P<stringConstant>(?:\"(?:[^"\\\n]|\\[\\"])*\"))',
        'IDENTIFIER': r'(?P<identifier>[A-Za-z_]\w*)'
    }

    __keyword = {
        'class': 'CLASS',
        'constructor': 'CONSTRUCTOR',
        'function': 'FUNCTION',
        'method': 'METHOD',
        'field': 'FIELD',
        'static': 'STATIC',
        'var': 'VAR',
        'int': 'INT',
        'char': 'CHAR',
        'boolean': 'BOOLEAN',
        'void': 'VOID',
        'true': 'TRUE',
        'false': 'FALSE',
        'null': 'NULL',
        'this': 'THIS',
        'let': 'LET',
        'do': 'DO',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'return': 'RETURN',
    }


class CompilationEngine:
    def __init__(self, path, jack_tokenizer: JackTokenizer):
        self.file = open(path, 'w')
        self.tokenizer = jack_tokenizer
        self.write('<tokens>')

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
        token_type = self.tokenizer.token_type()
        if token_type == 'IDENTIFIER':
            token_value = self.tokenizer.identifier()
            self.write(f'<identifier> {token_value} </identifier>\n')
            if self.tokenizer.has_term_child():  # 만약 하위 term이 있다면 재귀적으로 호출
                self.compile_term()
        elif token_type == 'STRING_CONST':
            token_value = self.tokenizer.stringVal()
            self.write(f'<stringConstant> {token_value} </stringConstant>\n')
        elif token_type == 'INT_CONST':
            token_value = self.tokenizer.intVal()
            self.write(f'<integerConstant> {token_value} </integerConstant>\n')
        elif token_type == 'KEYWORD':
            token_value = self.tokenizer.keyword()
            self.write(f'<keyword> {token_value} </keyword>\n')
        elif token_type == 'SYMBOL':
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
        while self.jt.has_more_tokens():
            self.ce.compile_term()


JackAnalyzer(sys.argv).run()

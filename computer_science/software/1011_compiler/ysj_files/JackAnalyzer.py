import glob
import os
import re
import heapq


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
        if not self.currentLineTokens:  # currentLineTokens이 남았으면 아직 토큰 있는거임
            return True
        while True:
            current_position = self.file.tell()
            line = self.file.readline()
            if line == '':  # 마지막 줄인가?
                return False
            if line.lstrip().startswith('//', '\n'):  # 한줄 주석 혹은 줄바꿈인가?
                continue
            if line.lstrip().startswith(('/*', '/**')):  # 여러줄 주석인가?
                while True:  # 주석 끝날때까지 반복
                    line = self.file.readline()  # 주석 다음줄로 넘기기
                    # 여기에 line.lstrip().startswith('*')로 주석 규칙 잘 지키나 확인해야 하는거 아닌가?, 문법 상 잘못쓰는건 고려 안하니까 일단 생략
                    if line.lstrip().startswith('*/'):  # 주석의 끝인가? 사실 이러면 무한루프 가능성 있는데, 마찬가지로 문법 잘 지키면 문제 없음
                        break

            # 주석도 아니고, 공백도 아니면 토큰이 있어야만 하므로 검사 없이 진행
            self.file.seek(current_position)
            return True

    def advance(self) -> None:
        """다음 토큰을 현재 토큰으로. has_more_tokens가 true일 때만 사용해야 함"""
        if not self.currentLineTokens:  # self.currentLineTokens가 비면 새로운 값 가져오기
            line = self.file.readline()
            self.currentLineTokens = self.get_tokens(line)
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

    def close(self, path):
        """self.file을 포함한 자원 해제"""
        pass

    def get_tokens(self, text) -> list:
        """입력받은 텍스트의 token 목록을 반환함"""
        matches = {}
        for name, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                matches[match.start()] = (name, match.group())
        heapq.heapify(matches)
        return matches

    def get_val(self, token_type: str, value: str):
        """type에 맞는 값 설정"""
        if token_type == 'KEYWORD':
            return self.keyword[value]
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

    keyword = {
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
        pass

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
            dir_path = os.path.basename(os.path.normpath(self.path))
            self.analyze_dir(dir_path)
        else:
            file_path = self.path[:-4]
            self.analyze_file(file_path)

    def analyze_dir(self, dir_path):
        jack_files = glob.glob(os.path.join(dir_path, '*.jack'))
        for jack_file in jack_files:
            file_path = jack_file[:-4]
            self.analyze_file(file_path)

    def analyze_file(self, file_path):
        self.jt = JackTokenizer(file_path + '.jack')
        self.ce = CompilationEngine(file_path + '.xml', self.jt)

# # 찾은 결과 출력
# for pos in sorted(matches.items()):
#     start = pos[0]
#     name, value = pos[1]
#     print(f"Found {name} At {start}: {value}")

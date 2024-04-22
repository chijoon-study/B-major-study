import re


class JackTokenizer:
    def __init__(self, path):
        self.file = open(path, 'r')
        self.currentLineTokens = []  # 현재 로드된 토큰, 가장 앞의 존재하는 토큰부터 가져온다.
        pass

    def has_more_tokens(self) -> bool:
        """file에 더 많은 토큰이 있는가?"""
        '''
        다음 명령어가 있는지 확인하면서 다음 결과 바로 앞까지 이동.
        변경/조회 기능이 합쳐져있기는 한데, 멱등성이 보장되니까 괜찮을듯?
        '''
        if not self.currentLineTokens:
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

            if self.file:
                self.file.seek(current_position)
                return True

    def advance(self) -> None:
        """다음 토큰을 현재 토큰으로. has_more_tokens가 true일 때만 사용해야 함"""
        pass

    def token_type(self) -> str:
        """현재 토큰의 타입 반환"""
        pass

    def keyword(self) -> str:
        """현재 토큰의 키워드 반환"""
        pass

    def symbol(self) -> str:
        """token_type이 SYMBOL일때만 호출해야 함. 현재 토큰의 문자 반환."""
        pass

    def identifier(self) -> str:
        """token_type이 IDENTIFIER일때만 호출해야 함. 현재 토큰의 문자열 반환."""
        pass

    def intVal(self) -> int:
        """token_type이 INT_CONST일때만 호출해야 함. 현재 토큰의 정수값 반환."""
        pass

    def stringVal(self) -> str:
        """token_type이 STRING_CONST일때만 호출해야 함. 현재 토큰의 문자열에서 따옴표를 제거하고 반환."""
        pass

    # 여기까지 API

    def set_file(self, path):
        """self.file 재설정. 여러 파일을 변환하는 경우가 있기 때문"""
        pass

    def close(self, path):
        """self.file을 포함한 자원 해제"""
        pass

    def get_tokens(self, path) -> list:
        """self.file을 포함한 자원 해제"""
        matches = {}
        for name, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                matches[match.start()] = (name, match.group())
        pass



'''
AI 도움을 받아서 정규식을 구현함
AI 피셜
'KEYWORD': 프로그래밍 언어의 키워드를 매칭합니다. 예를 들어 class, function, if, return 등의 키워드를 식별합니다.
'SYMBOL': 프로그래밍 언어에서 사용되는 기호를 매칭합니다. 예를 들어 {, }, (, ), [, ], ,, ;, +, -, *, /, &, |, <, >, =, ~ 등의 기호를 식별합니다.
'IDENTIFIER': 정수 상수를 매칭합니다. 0부터 32767까지의 정수 상수를 인식할 수 있습니다.
'INT_CONST': 문자열 상수를 매칭합니다. 세 개의 작은따옴표로 둘러싸인 문자열을 인식합니다. 작은따옴표 내부에 작은따옴표 또는 큰따옴표가 있어도 무시됩니다.
'STRING_CONST': 식별자를 매칭합니다. 알파벳 또는 언더스코어로 시작하고, 알파벳, 숫자, 언더스코어로 이루어진 식별자를 인식합니다.
'''
patterns = {
    'KEYWORD': r'(?P<keyword>class|constructor|function|method|field|static|var|int|char|boolean|void|true|false|null|this|let|do|if|else|while|return)',
    'SYMBOL': r'(?P<symbol>[{}()[\].,;+\-*/&|<>=~])',
    'INT_CONST': r'(?P<integerConstant>0|[1-9]\d{0,4}|[12]\d{4}|3[01]\d{3}|32[0-6][0-7][0-6]|327[0-5][0-7])',
    'STRING_CONST': r'(?P<stringConstant>\'\'\'(?:[^\'\"\n]|\'(?!\')|\"(?!\")|\'\"\')*\'\'\')',
    'IDENTIFIER': r'(?P<identifier>[A-Za-z_]\w*)'
}

text = """
class Main {
    static boolean test; // This is a test

    function void main() {
        var Array a;
        let b = null;

        let age = 32767;
        let name = 'This is a "very" long string constant!!!';
        let true_or_false = true;

        let c = a[0];
        do c = c * 2; while (c < age);

        if (c > b) {
            return c;
        } else {
            return age;
        }
    }

    /** This is a method
     *  @param x This is the first parameter
     *  @param y This is the second parameter
     *  @returnx + y
     */
    function int add(int x, int y) {
        let sum = x + y;
        return sum;
    }
}

// This is the end of the file.
"""

# 각 패턴에 대해 문자열에서 매칭된 위치 찾기
matches = {}
for name, pattern in patterns.items():
    for match in re.finditer(pattern, text):
        matches[match.start()] = (name, match.group())

print(matches)

# 찾은 결과 출력
for pos in sorted(matches.items()):
    start = pos[0]
    name, value = pos[1]
    print(f"Found {name} At {start}: {value}")

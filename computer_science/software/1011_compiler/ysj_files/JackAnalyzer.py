import heapq


class JackTokenizer:
    def __init__(self, path):
        self.file = open(path, 'r')
        self.currentLineTokens = []  # 현재 로드된 토큰, 가장 앞의 존재하는 토큰부터 가져온다.
        pass

    def has_more_tokens(self) -> bool:
        """file에 더 많은 토큰이 있는가?"""
        pass

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

    regex_token_type = {
        'class': ''
    }


import re

# 분석할 문자열
text = "Hello, my email is example@email.com and my phone number is 123-456-7890."

# 정규 표현식 패턴과 이름
patterns = {
    'email': r'\b(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b',
    'phone': r'\b(?P<phone>(?:\d{3}[-.]?){2}\d{4})\b'
}

# 각 패턴에 대해 문자열에서 매칭된 위치 찾기
matches = {}
for name, pattern in patterns.items():
    for match in re.finditer(pattern, text):
        matches[match.start()] = (name, match.group())

print(matches)

# 찾은 결과 출력
for pos in sorted(matches.keys()):
    name, value = matches[pos]
    print(f"Found {name}: {value}")
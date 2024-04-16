from io import TextIOWrapper
import sys
import os
from enum import Enum

"""
참고 자료

파일 읽고 쓰기: https://wikidocs.net/26


"""

class CommandType(Enum):
    C_ARITHMETIC = "C_ARITHMETIC" # 산술
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNTION = "C_FUNTION"
    C_RETRUN = "C_RETRUN"
    C_CALL = "C_CALL"

class Parser:
    def __init__(self, file: TextIOWrapper) -> None:
        pass

    def hasMoreLines(self) -> bool:
        pass
    
    def advance(self) -> None:
        pass

    def commandType(self) -> CommandType:
        pass
    
    def arg1(self) -> str:
        pass
    
    def arg2(self) -> int:
        pass

class CodeWriter:

    def __init__(self, file: TextIOWrapper) -> None:
        pass
    
    def writeArithmetic(self) -> None:
        pass
    
    def writePushPop(self) -> None:
        pass

    def close(self) -> None:
        pass

class VMTranslator:
    def __init__(self, args: list) -> None:
        pass
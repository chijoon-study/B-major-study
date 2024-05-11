## compile
컴파일은 어떤 언어로 쓰여진 파일을 다른 언어로 번역하는 과정이다.(보통 더 낮은 수준의 언어겠지)  
그리고 그런 작업을 수행하는 프로그램이 컴파일러라고 불린다.  

컴파일은 두가지 단계로 분리되어 수행된다.  
- 구문 분석(syntax analysis)
- 코드 생성(code generation)


## syntax analysis
구문 분석 단계에서는 코드 생성 단계에서 파일의 의도를 이해할 수 있게끔 파일을 미리 처리해둔다.  
주석, 공백 등을 미리 제거하고, 문법에 맞게 각 키워드별로 나눠준다.
![](./kdh_files/tokenizer_example.png)

Jack 언어에는 그런 키워드에 5가지 종류가 있다. 
- keywords 
- symbols   
- integer constants (17, 314)
- string constants ("FAQ", "Frequently Asked Question", 실제로 파일에 구문결과를 저장할땐 쌍따옴표를 제거한다)
- identifiers (변수, 클래스, 함수 이름)

위 단계를 토크나이징이라 하고 파싱 단계가 또 존재한다.  
파싱에서는 저렇게 분리된 토큰들을 다시 각 구문에 맞게 그룹화해준다.(사실 이렇게 그룹화 하는걸 파싱이라고 하는게 맞는건지는 모르겠다)  

예를 들어 while문이 있으면 while 다음에 (, expression, ), { ,statements, } 가 나온다.  
그러면 이것들을 하나의 whileStatement로 묶어주는 것이다.  
![](./kdh_files/grammar_sample.png)  

그리고 그 과정에서 예상치 못한 토큰이 다음 단계에 나온다면 이는 문법오류라고 볼 수 있다.  

그리고 그 다음토큰을 몇개 봐야하는 지에 따라 LL(k) 파서로 불리는데  
Jack에서는 하나의 예외를 제외하고 바로 다음에 나오는 토큰만 보면되서 LL1 파서이다.  
저 k값이 높아질수록 파서는 복잡하고 정교해져아한다.  

전체 문법은 다음과 같다.  
![](./kdh_files/grammar.png)




## note
과제가 점점 어려워진다..
그나마 10장은 문법보고 parsing만하면 되서 그나마 간단하긴했다.  
term부분이 재귀적인거 고려하느라 좀 어려웠음



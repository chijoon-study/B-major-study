## Unix philosophy
빅데이터 처리 기술은 최근들어 더 각광받고 개발되고 있지만, 그 철학은 사실 예전부터 존재했을지 모른다.  
Unix 시스템에서 대부분 잘알 pipes 연산자("|")를 개발한 Doug McIlroy가 처음 pipes를 설명할때 다음과 같이 설명했다. 
> “We should have some ways of connecting programs like garden hose—screw in another segment when it becomes necessary to massage data in another way. This is the way of I/O also”

그리고 이는 Unix철학의 일부가 되었다.

1. Make each program do one thing well. To do a new job, build afresh rather than complicate old
programs by adding new “features”.

2. Expect the output of every program to become the input to another, as yet unknown, program. Don’t
clutter output with extraneous information. Avoid stringently columnar or binary input formats.
Don’t insist on interactive input.

3. Design and build software, even operating systems, to be tried early, ideally within weeks. Don’t
hesitate to throw away the clumsy parts and rebuild them.

4. Use tools in preference to unskilled help to lighten a programming task, even if you have to
detour to build the tools and expect to throw some of them out after you’ve finished using them.

이런 Unix의 철학은 후에 애자일 방법론과 데브옵스 문화로까지 이어졌다.  
그리고 이 철학은 40년간 거의 변하지 않았다.


이런 Unix의 철학은 uniform interface와 stdin stdout을 통해 잘지켜지고 있다.  

uniform interface은 Unix의 철학중 한 프로그램의 output은 다른 프로그램(어쩌면 아직 개발되지도 않았을)의 input으로 들어갈 수 있어야한다. 를 지키기 위해  
모든 프로그램이 input format을 하나로 맞추는 것이다.  
그리고 이는 Unix에서 file단위로 이루어졌다.  
file은 단순히 bytes의 연속일 뿐이기에 표준으로 맞추기 좋았나보다.

stdin과 stdout은 프로그램에서 아무것도 건들지 않았다면 보통 keyboard의 입력이 stdin으로 들어오고 stdout으로 screen에 보여지지만, 다른 파일로부터 input을 받을 수도있고 다른 파일로 output을 보낼수도있다.  
pipes연산은 stdin과 stdout을 다른프로그램과 연결할 수 있게 해주는 역할을 한다.  

이러한 Unix에도 치명적인 한계가 있는데 바로 single machine에서만 동작한다는 것이다.  
때문에 Hadoop이 개발되었다.  



### 3부 파생 데이터

- 3부(10~12장)에서는 여러 데이터 시스템을 통합하는 법을 알아본다.
  - 시스템 아키텍처가 명료(뚜렷하고 분명한)성을 갖추기 위해서는 데이터가 어디로부터 파생되는지를 명확히 해야 한다.

- 레코드 시스템과 파생 시스템
  - 레코드 시스템
  - 파생 시스템
  - 시스템은 사용자가 결정한다.

### 10장 일괄 처리

- 유닉스 도구 유용하다는 내용이 있는데, 관련해서 생각난 자료
  - [Command-line Tools can be 235x Faster than your Hadoop Cluster](https://adamdrake.com/command-line-tools-can-be-235x-faster-than-your-hadoop-cluster.html)
  - [Using Unix Commands for Data Science](https://matheusrabetti.github.io/data%20analysis/command-line-datascience/)

- 유닉스 철학
  - 참고할만한 것들
    - [GPT 설명](https://chatgpt.com/share/3d41d149-3e93-46b5-8d7f-ce47c3a8c400)
    - [Unix philosophy - 기계인간 John Grib](https://johngrib.github.io/wiki/Unix-philosophy/)
    - [유닉스 철학 - 위키피디아](https://ko.wikipedia.org/wiki/%EC%9C%A0%EB%8B%89%EC%8A%A4_%EC%B2%A0%ED%95%99)
  - 설명
    1. 각 프로그램이 하나의 일을 잘 할 수 있게 만들 것. 새로운 일을 하려면, 새로운 기능들을 추가하기 위해 오래된 프로그램을 복잡하게 만들지 말고 새로 만들 것.
    2. 모든 프로그램 출력이 아직 잘 알려지지 않은 프로그램이라고 할지라도 다른 프로그램에 대한 입력이 될 수 있게 할 것. 무관한 정보로 출력을 채우지 말 것. 까다롭게 세로로 구분되거나 바이너리로 된 입력 형식은 피할 것. 대화식 입력을 고집하지 말 것.
    3. 소프트웨어를 설계하고 구축할 때 빠르게 써볼 수 있게 할 것. 심지어 운영체제라도 이상적으로는 수 주 내로. 어설픈 부분을 버리고 다시 만드는 것을 주저하지 말 것.
    4. 프로그래밍 작업을 가볍게 하기 위해, 심지어 우회하는 방법으로 도구를 만들고 바로 버릴지라도 어설픈 도움 보다는 도구 사용을 선호할 것.

- 맵리듀스 과정
  - 책에서 나온 내용 정리 + 이해 안가는 부분 보충 설명
  - 하둡과 같은 분산 환경(병렬 처리)에서 대규모 데이터셋을 다룰때 사용하는 기법(프레임워크).
    - 한 노드 성능으로 불가능하거나 가성비가 떨어지는 대규모 데이터 셋 처리 목적으로 탄생.
    - 구글에서 2014년에 논문으로 발표.
  - Map-Reduce: 
    - 4단계로 구성. 유닉스 파이프라인처럼 output이 다른 프로세스? 다음 절차? 의 input이 된다.
    - Map 함수와 Reduce 함수에 의해 원하는 결과를 출력한다.
    - 단계
      - Map: 분산 저장된 데이터를 서버에서 처리
        - 분할
          - 들어온 데이터를 여러 조각의 데이터로 분할
        - 매핑
          - (k : v) 형태로 매핑
          - 매핑 기준은 Map 함수에서 정의한다.
            - 아래 이미지에서의 Map 함수는 이미지를 공백 단위로 분리하는 로직임.
      - R1educe: 선정된 데이터 분석 및 통합
        - 셔플링  
          - (k : [v1, v2, v3]) 형태로 통합. (이름과 달리 뭔가 랜덤하게 섞는건 없다. Grouping이 더 적절하지 않을까?)
        - 리듀싱
          - Reduce 함수에 의해서 원하는 결과를 냄.
            - 아래 이미지에서의 Reduce 함수는 (k : sum(values))를 반환하는 로직.
      - ![example](example.png)

  - 추가 참고
    - https://youtu.be/2RPVFhxps_s?si=m-kxh5_YJzFZLa4c
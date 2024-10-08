## 12 데이터 시스템의 미래

### 정리

#### 데이터 통합

- 파생 데이터에 특화된 도구의 결합
  - 데이터 플로를 추론하기 위해서는 데이터 시스템의 입력과 출력을 명확하게 해야 한다.
    - 입력을 처리하는 시스템이 하나(최소)인게 제일 좋다. 여러 개인 경우 관리가 까다롭다.
  - 파생 데이터를 처리하는게 분산 트랜잭션보다 장래성 있다. (저자 피셜)
    - 분산 트랜잭션 시스템은 결함 대응에 취약하고 성능이 나쁘다.
    - 파생 데이터는 비동기라는 특징을 제외하면 결함 대응성이나 성능 면에서 더 좋다.
  - 선형성은 제약이 크다.
    - 단일 리더 시스템 외에는 불가능
    - 지역 분산도 불가능
    - 오프라인 작업도 불가능
  - (글 작성 시점에서) 선형성 없이는 인과성 의존성을 처리하기에는 한계가 있다.
    - (저자 생각) 지금은 없지만, 시간이 지나면 전체 순서 브로드캐스트 없이도 인과적 의존성을 잘 처리하는 개발 패턴이 등장할 것.
- 일괄 처리와 스트림 처리
  - 일괄 처리와 스트림의 차이는 줄어들고 있다.
    - 두 가지를 혼합하는 람다 아키텍처이나, 한 시스템에서 두 기능을 모두 제공하는 시스템이 생기고 있다.
  - 비동기 방식은 결합을 국소적으로 처리 가능하나, 동기 방식은 실패가 증폭된다.
  - 기존 데이터를 재처리(이벤트 - 일괄, 스트림)하면 점진적 발전이 가능하다.

#### 데이터베이스 언번들링

- 데이터 저장소 기술 구성하기
  - 색인, 구체화 뷰, 복제 로그, 전문 검색 색인 등의 기능이 있다.
    - 데이터 베이스의 내장 기능과 일괄/스트림 처리는 비슷하다.
      - DBMS 데이터 변경 시 내부적으로 색인을 수정한다. 스트림은 데이터 변경 발생 시 다른 데이터 시스템의 상태를 수정한다.
      - 크게 보면 내부에서 제공하느냐 외부에서 제공하느냐의 차이
  - 이러한 기능은 한 어플리케이션에서 모두 제공하는 것은 어려우므르, 앞으로는 여러 도구를 사용해서 동작할 것.
    - 그러나 하나의 데이터시스템으로 사용할 수 있으면 그렇게 쓰자. 성급한 최적화는 지양하는게 좋다.
    - 연합 데이터베이스: 읽기를 통합 - 여러 곳에서 쓰고, 한 곳에서 읽는다.
    - 언번들링 데이터베이스: 쓰기를 통함. - 한 곳에서 쓰고, 여러 곳에서 읽는다. 
    - 저자는 여러 이유로 언번들링 데이터베이스가 더 강력하고 현실적이라 생각함. (읽기가 쓰기보다 관리가 쉬움. 결합도 낮음 등)
  - (저자 피셜) 언번들링이 쉽도록 유닉스 파이프라인과 같이 동작할 수 있는 통합을 지원하는 방법이 생겨야 한다.
- 데이터 플로 주변 애플리케이션 설계 (하는 방법)
  - 파생 함수로서 애플리케이션 코드 작성하기
    - 보조 색인, 검색 엔진, 캐시, 머신러닝 등은 Source(원천) 데이터에 함수(색인 관리, 리버스 인덱스, 자주 요청하는 데이터 형식 변환, 특징 추출 및 학습)를 붙인 것으로 볼 수 있다.
    - 보조 색인과 같은 공통적인 기능 외에는 사용자가 어플리케이션 코드로 함수를 개발해야 한다.
  - 애플리케이션 코드와 상태의 분리
    - (저자 생각) 데이터 저장과 코드 실행을 전문으로 하는 2개의 서비스로 분리되어야 한다.
      - 하나만 잘 하고 통합을 하는게 좋다.
    - 최근에는 애플리케이션(아마 주로 서버)에서 상태를 저장하지 않는다.
      - 그러나 상태의 변경을 구독하는 기능이 부족하다. 데이터베이스의 변경을 확인하려면 폴링을 사용해야 한다. *(이게 왜 나오는거지? 좀 뜬금없는거 같은데)*
    - 데이터플로: 애플리케이션 코드와 상태 관리 간의 관계를 재조정하는 것 - *여기 절 이해 잘 안감. 의도적으로 DB를 이벤트 스트림같이 쓰자는건가?*
      - 데이터베이스가 수동적이지 않고, 애플리케이션 코드는 상태 변화를 트리거해 응답한다.
      - 안정적인 메시지 순서화와 내결함성이 있는 메시지 처리를 제공하는 스트림 처리자를 사용하여 가능함.
    - 스트림 처리자로 서비스 만들기
      - 최근에 MSA가 자주 쓰인다. (저자 피셜) 스트림 처리자로 서비스를 만드는게 것도 (아직 문제가 많지만) 유망한 아이디어이다.
      - 원천 데이터의 변경 발생 시 서비스의 로컬에 동일한 데이터 변경 저장 등의 방법이 있음.
        - MSA와 달리 네트워크 결함에도 안전함.
        - > 가장 빠르고 가장 신뢰성 있는 네트워크 요청은 네트워크 요청을 전혀 하지 않는 것이다.
- 파생 상태 관찰하기
  - 쓰기 경로와 읽기 경로
    - 데이터 플로 시스템에서 사용
    - 쓰기 경로: 사용자가 데이터를 쓰는 부분 - (파생 시스템의 쓰기는 포함 안됨. 여기의 쓰기는 원천 데이터를 의미함)
    - 읽기 경로: 사용자가 데이터를 읽는 부분 - (캐시를 사용하는 경우 캐시, 그냥 서버 요청의 경우 서버)
  - 쓰기 경로와 읽기 경로는 변할 수 있다.
    - 구체화된 뷰(캐시, 검색 엔진)
    - 사용자 로컬(오프라인 대응) - 이 경우 읽기(캐시)가 서버가 아니라 사용자 로컬이 된다. (쓰기도 로컬 아닌가 싶었는데 서버에서 동기화하니까 뭐... 아닌듯?)
    - 이러한 특징으로 인해서 요즘 최신 프로토콜은 요청/응답 패턴을 벗어나고 있다. EventSource API, WebSocket 등...
  - 종단 간 이벤트 스트림
    - 사용자의 이벤트가 서버를 거쳐 다른 사용자로 전달되는 구조. 
      - 게임이나 메시징 서비스(슬랙, 디코) 등
    - 기존의 요청/응답 아키텍처에 너무 의존하고 있어서 바뀌기는 쉽지 않다.
    - (저자 생각) 그러나 더 반응성 있는 사용자 서비스를 위해서 필요하고, 이를 위해서는 DBMS에서 요청/응답 외에도 변경을 구독하는 기능이 필요하다.
  - 읽기 또한 이벤트다.
    - 인과적 의존성을 추적하기 쉽다.
      - 상품 재고/평점을 보고 구매를 결정하거나 등...
    - 시스템 오버해드가 있으나, 이미 서비스 관리 등의 이유로 로깅하고 있는 상태라면 변경하는게 어렵지 않다.

#### 정확성을 목표로

- 데이터베이스에 관한 종단 간 논증
  - 데이터 유실/손상은 언제나 일어날 수 있다. 이를 문제 기능이라 함.
  - 종단 간 논증(end-to-end argument): 문제 기능(데이터 손상을 발생시키는)은 통신 시스템 자체로 해결 분가능하다.
  - 이를 방지하기 위해서 결과적으로 한 번만 실행되는 것을 보장해야 한다.
    - 연산에 멱등성을 보장함으로써 해결 가능 (요청에 고유 ID를 부여)
    - 하위(TCP, 디스크, 이더넷 등)에서 어느정도 보장해주나 완벽하지 않다. 
  - 종단 간 확인이 제일 안전하다. (암호화도 마찬가지)
  - 따라서 여러운 일이지만, 어플리케이션이 종단 간 대책을 갖춰야 한다. 
    - 왜냐면 단일 환경인 예전과 달리 분산 환경에서 트랜잭션을 사용하는 것은 좋지 않기 때문이다.
- 제약 조건 강제하기  
  - 유일성 제약 조건은 합의가 필요하다.
    - 단일 노드를 사용하거나, 유일성 제약 조건의 값을 기준으로 파티셔닝하면 가능. (사용자 명이 유일해야 하면 사용자 명을 해싱해서 파티셔닝)
  - 로그 기반 메시징을 사용해서 여러 제약 조건을 보장할 수 있다.
    - 제약 조건에 필요한 값을 기준으로 로그를 파티셔닝 하면 됨.
  - 이처럼 필요한 값을 기준으로 파티셔닝하더라도, 멱등성을 보장한다면 원자적 커밋과 동등한 정확성을 가질 수 있다.
    - (송금 요청 이벤트 발행 -> 요청 이벤트를 읽고 각 사용자의 출금/입급 이벤트 발생 -> 각 서비스에서 계좌 잔고에 반영) - 요청이 누락 된 경우 확인하고 재요청, 중복 된 요청이 오는 경우 멱등성으로 막힘
    - **로그 기반 메시징에서 분산 처리가 가능하면서 원자적 커밋과 동등한 기능을 제공할 수 있다.** - 이거 F-Lab에서 송금 어쩌구에서 본거 같기도?
- 적시성과 무결성
  - 일관성은 2가지 요구사항을 가진다.
    - 적시성: 변경 후 항상 최신 상태.
    - 무결성: 데이터가 손상되지 않음.
  - 트랜잭션은 둘 다 보장해서 구분이 필요 없었으나, 분산 시스템은 아니므로 구분이 필요함.
  - 적시성보다 무결성이 훨씬 중요하다.
  - 비즈니스에 따라서 유일성 제약 조건을 완화할 수 있다. - (적시성이 필수가 아님. 예전 데이터를 보고 중복예약하는 등의 문제가 일어나도 ㄱㅊ하다는 뜻)
    - 보상 트랜잭션: 일단 여러 예약을 받고, 이후에 한 사용자가 바꾸도록 함. 
    - 항공권 예약의 초과 예약, 쇼핑몰, 은행 등에서 비즈니스 상으로 이런 문제를 수용할 수 있다.
      - 그러나 무결성은 반드시 필수다.
    - 코디네이션(여러 서비스의 협력) 회피: 동기식 코디네이션보다 내결함성이 좋고 성능이 좋다. 
    - 비즈니스 적 보상(재고,항공권 부족 사과)과 서비스의 성능 면에서 적절하게 트레이드 오프 할 것.
- 믿어라. 하지만 확인하라
  - 이처럼 무결성은 중요하다.
  - 여러 데이터 시스템이 보장한다고 해서 그걸 꼭 보장하지 않을 수 있다. (버그 등의 문제)
    - 또한 최근에 나온 분산 시스템은 오래된 DBMS와 달리 버그가 많을 수 있다.
  - 따라서 감사 시스템을 도입하고 주기적으로 확인해야 안전하다.
    - 종단 간 무결성이 최선이다.
    - 최소한 데이터의 무결성이라도 확인해야 한다.
    - 문제가 생겨서 무결성이 위배된 것을 파악한 경우, 이미 너무 많은 문제가 일어났을 확률이 크다.

#### 옮은 일 하기

- 예측 분석
  - 알고리즘은 편견과 차별을 가질 수 있다. ([X가 트위터인 시절에 크롭 알고리즘의 인종편향 문제](https://edition.cnn.com/2021/05/19/tech/twitter-image-cropping-algorithm-bias/index.html), [제미나이 정치적 올바름 문제](https://www.bbc.com/korean/articles/cg3kmy2rr97o))
  - 책임이 모호하다. 
    - 이유 또한 명확하게 알기 어렵다.
  - 데이터는 과거만을 알 수 있다. 이는 편향적인 시선을 키운다. 부정적인 피드백 루프가 발생한다.
  - 따라서 인간적인 시선과 시스템 사고가 필요하다.
- 사생활과 추적
  - 데이터의 수집 자체가 윤리적인 문제.
    - 개인의 사생활이 없고, 기업으로 소유권이 넘어가고 있음. 본인이 본인의 정보를 제공할 자유를 가지지 못함.
    - 서비스를 사용하려면 무조건 정보 제공에 동의해야 함. (사회 네트워크 등의 문제로) 기업이 이를 강제함. (SNS부터 업무용 도구 등)
  - 데이터가 자산과 권력을 가진다.
    - 데이터는 가치 있다.
    - 기업이 그렇게 사용할 의도가 없어도, 그 자체로 권력이 된다. (핵 같네)
    - 나쁜 정부가 데이터를 가져갈 수도 기업의 데이터를 있고, 탈취당할 수도 있음.
    - 이를 막기 위해서 법률과 발전을 차단하지 않을 정도의 적절한 규제가 필요함. - (현실적으로 가능할까? 구글이나 메타만 해도 이런거 이슈는 많이 있는걸로 아는데)
      - (저자 의견) 산업혁명 시대의 어린이 노동, 근무 환경, 인권 보장 등의 문제처럼 봐야 한다.
      - 불변 데이터의 경우 암호화 프로토콜을 통해서 접근 제어(삭제와 동일한)가 가능하다.

### 느낀점

장 내용

- 드디어 마지막 장. 전체 내용을 가볍게 요약하면서, 이론적인 부분보다는 저자의 생각이 담긴 부분이 많아서 재미있게 보았다.
  - 여러 생각해보지도 못한 관점이 많았고, 신선해서 재미있었음.
    - 색인 <-> 검색 엔진,캐시 는 둘 다 파생 데이터로 볼 수 있다.
    - 쓰기/읽기 경로를 기반으로 하는 데이터 아키텍처? 설명이나
- 앞에서 다루었던 내용을 통해서 "어떻게 시스템을 구성할 수 있는가?"를 다루는데, 이 부분이 사실 상 책의 제목(데이터 중심 어플리케이션 설계)에 알맞은 내용이 아닐까...
- 불변 데이터의 삭제를 처리하는데 암호화 프로토콜을 사용한다는 부분이 인상깊었음.
  - 랜덤 데이터(UUID나 라바 램프 등)를 사용한 단방향 암호화를 사용하면, 복구가 불가능해보임.
  - 뭔가 구현하면 재밌을거 같긴 함. 토이 프로젝트에서 데이터 제거를 다룰 때 이런거 하면 좋을듯?
    - 근데 이러면 불변성을 보장하지 못하는게 아닌가 싶지만, 삭제라는 의미 상 그게 맞는거 같기도 함.

책 전체 후기

나중에 따로 쓸 수도 있어서 간단하게만,

이번에는 막연한 분산 시스템의 두려움을 지우고 Context나 배경지식을 채우기 위해 가볍게 봄.      
그래도 분량이 무시 못할 정도...

그래도 목적은 충분히 달성한 것 같다.

컨퍼런스 영상을 볼 때, 분산 시스템 관련 내용이 나올 때 더 잘 이해할 수 있게 되었음.         
막연한 두려움도 줄어들었고, 나중에 언젠가 토이 프로젝트를 한다면 이 책에서 다루는 기술을 좀 써보고 싶다는 생각도 들었다.    

앞으로 다시 필요해져서 공부할 때도 더 빠르게 알 수 있지 않을까?

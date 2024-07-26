### 7장 트랜잭션

### 정리
#### 트랜잭션 간단 설명

목표: 데이터 시스템의 문제(네트워크, 중단, 경쟁 조건, 덮어쓰기, 작성 중인 데이터 읽기)를 단순화한다.

어떻게: 몇개의 읽기와 쓰기를 하나의 논리적 단위로 읽는다.

성과: 안전성, 프로그래밍 모델 단순화(트랜잭선 없이 중간 상태를 포함하는 결제 프로세스를 개발한다고 생각해보자…) 

최근 개념: 분산 서비스가 나오면서 고전의 강력한 트랜잭션 대신, 약한 보장을 의미하게 재정의되기도 한다. 확장성과 트랜잭션은 어느정도 반비례할 수 있으나. 둘 중 하나만 선택해야 하는건 아니다.

(어느정도 트레이드 오프 관계가 있다. 분산 시스템에서 트랜잭션을 처리할려면 별도의 어플리케이션 단 구현(e.g. saga 패턴) + 실패 복구 기능이 필요하다. [토스 MSA 전환기 영상](https://youtu.be/amTJyIE1wO0?si=iC97CgfeXcYuOFtb&t=660)을 보면 MSA 간 긴 트랜잭션을 포기하고 비동기 + 실패 복구 로직을 구현해서 해결한다. )

#### ACID

p. 223 - ACID는 유감스럽게도 거의 마케팅 용어가 되어버렸다.

ACID 하다는게 진짜 어떤 의미인지 사람들이 잘 모르기 때문. 또한 벤더마다 ACID 구현이 제각각이다.

- A: 원자성, 커밋 or 롤백(abort) - 저자는 abortability (어보트 능력)이라는 말을 더 좋아함.
- C: 일관성, (저자 피셜) 어플리케이션 단에서 신경쓰기 + 구현해야 하므로 ACID에 속하지 않는다.
    - 막 default나 non null 같은 설정을 아무리 해봐야 “결제 프로세스 일관성” 같은걸 DBMS가 해줄 수 없다. 서비스마다 일관성 목표가 다르고, 구현 방법이 다르므로.
- I: 격리성, 이전에는 직렬성이라고 부름. 하나의 실행 단위에서 순차적으로 실행되는 것과 동일한 결과 (외부의 영향을 받지 않는 결과) 가 나와야 한다.
- D: 지속성, WAL(Write-Ahead Log) 등으로 해결하나, 결국 완벽한 지속성은 존재하지 않는다. 트랜잭션 결과는 언젠가는 유실될 수 있다.
    - 따라서 지속성 보장을 위한 여러 기법을 병행해서 사용하는 것이 좋다.

#### 직렬성

ACID중 I

한개의 스트림? 에서 실행되는 것처럼 실행되는 거.

이상현상 없이 실행되고, 롤백(어보트)도 문제없이 수행할 수 있는 상태.

성능 때문에 어느정도 포기하는 옵션을 제공한다.

> [[쉬운코드 블로그 중](https://easy-code-yo.tistory.com/38)]

하지만 이 isolation 속성은 트랜잭션의 ACID 속성들 중에 가장 많이 타협되는 속성이기도 하다
> 
> 
> DBMS의 성능과 연관이 있기 때문이다
> 
> isolation의 엄격함과 DBMS의 트랜잭션 처리량과 사이에서 개발자가 트레이드할 수 있도록
> 
> isolation level을 제공하는 이유도 이것 때문이다.
> 

##### 직렬성 관련해서 쉬운코드 설명

https://easy-code-yo.tistory.com/25#conflict%--serializable

**트랜잭션들이 동시에 실행될 때 isolation을 보장하는 기초 이론**

**scheudle**   ->   **conflict operations**  ->   **conflict equivalent**  ->   **conflict serializable**

- **schedule:** 각 transaction의 operation이 실행되는 순서
    - 아래는 동일한 연산의 다양한 schedule - tx1과 tx2 둘 다 x를 read → write 한다.
        
        (1)   r1(x) w1(x) r2(x) w2(x)
        
        (2)   r1(x) r2(x) w1(x) w2(x)
        
        (3)   r1(x) r2(x) w2(x) w1(x)
        
        (4)   r2(x) w2(x) r1(x) w1(x)
        
- **serial schedule:**  transaction이 하나 끝나면 다른 하나가 시작되는 형태의 schedule (위의 4번쨰 schedule)
- **conflict operations:** schedule에 존재하는 두 operations의 특정 조건을 만족하는 상태.
    - 두 operation이 서로 다른 transaction에 속해 있다
    - 두 operation이 같은 데이터에 접근한다
    - 두 operation 중에 적어도 하나는 데이터를 쓴다(write)
    - (이름 생각하면 됨. 충돌.)
- **conflict equivalent:** 두 개의 schedule이 특정 조건을 만족하는 상태
    - 두 schedule은 같은 transaction들을 가진다
    - 어떤(any) conflict operations의 순서도 양쪽 schedule이 모두 동일하다
- **conflict serializable:**
    - 어느 한 schedule이 serial schedule과 conflict equivalent하다면, '이 schedule은 conflict serializable하다
    - 두 개의 schedule이 conflict equivalent 할 때, 한 schedule이 serial schedule이라면, '다른 한 schedule은 conflict serializable하다

- **serial schedule의 문제점과 아이디어**
    - 한번에 하나의 트랜잭션만 실행되기 때문에 높은 성능을 낼 수 없다.
    - non-serial 는 여러 트랜잭션이 동시에 수행되므로 더 빠르나, 이상현상이 발생할 수 있다.
    - 즉, non-serial이면서 serial과 동일하게 수행되는 schedule을 사용하면 된다.
        - conflict serializable한 schedule이 serial과 동일하게 수행된다.
    - 그 전에 serial 하다는 것의 정의를 구해야 한다. (쉬운코드 영상에서 나오는데 생략)

- **실제 구현은?**
    - 현실적으로 동시에 실행된느 트랜잭션마다 conflict serializable하게 동작하게 하는건 너무나 어렵다.
        - (내 생각: DBMS가 가능한지 확인하고, 실패하게 하면 어플리케이션 단에서 너무나 많이 고려해야 함.)
    - conflict serializable하게 동작하도록 보장하는 프로토콜을 사용.

아래는 recoverability 설명

- unrecoverable schedule
    - 복구 불가능한 스케줄. tx1에서 수정한 작업을 tx2가 읽고 커밋한 경우,  tx1을 롤백하면 해당 작업이 tx2또한 롤백해야 하므로 D를 지키지 못한다.
    - 일어나면 안되는 현상
- recoverable schedule
    - 복구 가능한 스케줄.
    - 자신(tx)이 read한 데이터를 write한 다른 tx가 커밋 or 롤백 하기 전까지 commit하지 않는 것
    - 트랜잭션을 커밋하려면 다른 트랜잭션이 커밋or롤백되기를 기다려야 함.
- cascading rollback
    - 롤백하면 다른 트랜잭션도 연쇄적으로 롤백해야 하는 경우
- cascadeless schedule
    - 데이터를 write한 tx가 커밋or롤백 한 이후 데이터를 읽는 schedule만 허용하기
    - avoid cascading rollback이라고도 부름
- strict schedule
    - schedule내에서 어떤 tx도 커밋되지 않는 tx들이 write한 데이터는 쓰지도 읽지도 않는 경우

**결국 그래서 isolation이란?**

**concurrency control provides serializability & recoverability**

serializability & recoverability를 제공하는 일관성 제어

근데 전에 말했다시피 현실적으로 tx가 실행될 때마다 특정 조건을 만족하는 schedule 만 실행하는건 불가능함.

따라서 어느정도 제공하는 격리성을 낮추고, 그 격리성 레벨을 보장하는 프로토콜을 사용함으로써 해결함.

#### 단일 객체 연산과 다중 객체 연산

객체: 로우(RDB), 문서(DocumentDB), 레코드(?)

- 단일 객체 연산
    - 일반적으로 많이 제공, 구현이 쉬운 편
    - 원자적 연산(read-modify-write말고 compare-and-set)을 제공하기도 한다.
- 다중 객체 연산
    - 구현 어려움, 여러 분산 DB는 제공 안하는 곳도 있음.
    - 대다수 다중 객체 연산이 필요하다. (e.g. BEGIN TRANSACTION, COMMIT/ROLLBACK)

#### isolation level - 완화된 격리 수준

https://www.atobaum.dev/archives/2020/9/DDIA-ch07  << 이거 괜찮음. 물론 나중에 지워야하는데, 그냥 전반적인 책 구조 참고용으로 ㄱㅊ

isolation level의 필요성: 모든 이상현상이 발생하지 않게 (완전한 isolation) 할 수 있으나, 성능이 너무 낮다.

> [[쉬운코드 블로그 중](https://easy-code-yo.tistory.com/38)]

하지만 이 isolation 속성은 트랜잭션의 ACID 속성들 중에 가장 많이 타협되는 속성이기도 하다
> 
> 
> DBMS의 성능과 연관이 있기 때문이다
> 
> isolation의 엄격함과 DBMS의 트랜잭션 처리량과 사이에서 개발자가 트레이드할 수 있도록
> 
> isolation level을 제공하는 이유도 이것 때문이다.
> 

동시성 문제와 어떤 isolation level이 이걸 해결할 수 있는지를 낮은 레벨부터 높은 레벨까지 봄.

![isolation level table](https://media.licdn.com/dms/image/D4D12AQHpQ9yVwj_wgw/article-cover_image-shrink_600_2000/0/1656329886789?e=2147483647&v=beta&t=U2UKYYVR9skiFO56MaLvaDvR92vD5QQ88IH1obWmsuQ)

- isolation level 순서
    - Read uncommited
    - Read commited
    - Repeatable read
    - Serializable: SQL 92 표준에서 다루지 않는 이상현상을 포함한 모든 이상현상이 발생하지 않음.
  
- SQL 92에서 정의한 isolation level의 비판하는 논문 설명 - [쉬운코드 영상 피셜](https://youtu.be/bLLarZTrebU?si=-O0825IDfO1S3Acs) 
  - 이상현상은 3가지 외에 더 있다.
  - 세 가지 이상 현상의 정의가 모호하다.
  - 상업적인 DBMS에서 사용하는 방법을 반영해서 isolation level을 구분하지 않았다.
  - 그래서 추가적으로 이상현상을 정의하고, 실제 DBMS에서 사용하는 Snapshot isolation을 설명한다. (이는 MVCC의 일종이다.)

- 실제 DBMS 사용 시 주의점 - 쉬운코드 영상 피셜
  - 실제 DBMS는 주로 SQL 표준에 기반해서 isolation level을 정의한다.
  - 각 DBMS마다 지원하는 isolation level이 다르다. 
  - 같은 isolation level이더라도 구현 방법이 다를 수 있다.


##### 발생 가능한 이상현상 - 이상현상: 직렬성이 위배되는 현상
- 더티 읽기(dirty read)
    - commit 되지 않은 변화 (유효하지 않을 수 있음)를 읽는 경우 발생 가능
    - 꼭 다른 트랜잭션이 abort하지 않아도, 발생할 수 있음. (다중 객체 수정 작업 중 읽는다거나)
    - e.g. t1에서 수정한 커밋되지 않는 값을 t2에서 읽고 + 1해서 쓰고, t1이 롤백하는 경우
- 더티 쓰기(dirty write)
    - 나중에 수행된 트랜잭션이 먼저 다른 트랜잭션에서 commit 되지 않은 변화 (유효하지 않을 수 있음)를 덮어 쓰는 경우 발생 가능
      - 정상적인 recovery가 불가능하므로 허용되면 안됨.
- 읽기 스큐(비반복 읽기)
    - 한 트랜잭션에서 (변경하지 않은) 같은 데이터를 여러번 읽었을 때, 값이 바뀌는 현상
- 갱신손실(lost update)
  - 한 tx의 갱신을 다른 tx가 덮어씌우는 것. (없던 일처럼 되어버림)
- 읽기 스큐(read skew)
  - inconsistent(비일관적인) 데이터 읽기
  - 각 트랜잭션은 독립적인 경우 문제가 없지만, 동시에 실행되는 경우 일관성 문제가 발생한다.
- 쓰기 스큐(write skew)
  - inconsistent(비일관적인) 데이터 쓰기
  - 각 트랜잭션은 독립적인 경우 문제가 없지만, 동시에 실행되는 경우 일관성 문제가 발생한다.
- 팬텀 읽기(phantom read)
    - 없던 데이터가 생기는 것

##### isolation level 구현 방법
- Read uncommited
  - 아무것도 예방하지 않는 날것
- Read commited: 더티 읽기/쓰기 예방
  - 로우 수준 잠금
    - 성능때문에 잘 사용하지 않는다.
    - 쓰기가 발생하는 로우를 읽으려면 대기해야하기 때문이다.
  - DBMS가 해당 값의 과거를 기억하고 있다가, 커밋되면 보여주는 식으로 구현한다.
- Repeatable read: 읽기/쓰기 스큐 예방 - 일관성 있는 읽기가 필요한 백업(사본 만들기), 무결성 확인 등의 작업에서 필요하다.
  - 스냅숏 격리(Snapshot isolation)를 사용하여 구현한다.
- Serializable
  - 정말로 순차적으로 실행하기
  - 2단계 잠금 (2PL)
  - 직렬성 스냅숏 격리 (SSI)


##### TODO 스냅숏 격리, MVCC 설명하기

스냅숏 격리는 보통 MVCC를 써서 구현한다.


##### TODO 직렬화 설명하기


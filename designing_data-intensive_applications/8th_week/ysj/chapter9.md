## 9장 일관성과 합의

### 정리

#### 기타

- 용어 정리
  - 레지스터: 분산 시스템에서 x로 표현, 데이터베이스의 개별 객체를 의미한다. 키, 로우, document 등.
  - 코디네이션(합의) 서비스: 주키퍼나 etcd 등이 해당되며, 전체 순서 브로드캐스트를 제공한다. 이를 통해서 선형성 저장소를 구현할 수 있다.
    - 그 외에 여러 유용한 기능을 제공한다. (CAS 연산, 리더 선출, 연산의 전체 순서화(아마 전체 순서 브로드캐스트?), 장애 감지, 변경 알림.)
      - 이 기능을 조합해서 작업을 노드에 할당하거나 서비스 찾기 등의 기능을 구현할 수 있다.

- 내결함성을 구축하는 가장 좋은 방법은 유용한 보장을 해주는 **범용 추상화**에 의존하는 것임.
  - e.g. 트랜잭션
  - 분산 환경에서 발생하는 여러 문제의 내결함성을 가지는 추상화가 선형성, 최종적 일관성, 인과성 등임.

- 최종적 일관성(저자는 수렴이라는 용어가 더 좋다고 생각)
  - 너무 약한 보장. 이로 인해 그 제한을 인식하고 개발해야 함.

#### 선형성

- 선형성(최신성 보장)
  - 가장 강한 일관성 모델 중 하나.
  - 데이터베이스의 복제본이 하나만 있는 것과 동일하게 동작함.
  - > 복제된 데이터가 오직 하나의 복사본만 있는 것처럼 보이게 하고 데이터에 대한 모든 연산을 원자적으로 만드는 것. ...(생략)... (데이터페이스가 단일 스레드 프로그램의 변수처럼 동작하게 만들어준다.)
  - 개별 객체(레지스터)에 실행되는 읽기와 쓰기 순서 보장. 
    - 한 노드에서 쓴 값을 다른 노드에서 읽는다면 또 다른 노드에서는 그 이전 시점의 데이터를 읽지 말아야 한다. (+ 아마? CAS 연산을 제공해야 한다.)
    - 직렬성과 다르다! - 선형성은 트랜잭션(격리)과 별개의 개념으로, 이상현상을 보장해주지 못한다. (+ 여러 요청이 "동시적"일 수 있다. 네트워크 지연에 의한 순서 보장 X)

- 선형성이 유용한 경우
  - 잠금과 리더 선출
    - 이를 위해 코디네이션 서비스인 주키퍼나 etcd가 사용된다.
  - 제약 조건과 유일성 보장
    - 분산 환경에서 예약, 잔고, 재고 등의 제약조건을 지키기 위해 필요하다.
    - 단, 외래 키(유일성 보장, unique 조건 제외)나 속성 제약 조건(Enum, Range 제약)은 제외.
  - 채널 간 타이밍 의존성
    - 여러 서비스가 의존하는 분산 서비스에서 경쟁 조건이 발생할 수 있다. (공유 데이터에 대한 동시 접근 문제이므로, 아직 없는 데이터에 접근하는 것도 경쟁 조건이다.)
    - 다른 방법으로도 해결할 수 있으나, 선형성이 가장 직관적이다.

- 선형성 구현하기
  - 구현 가능성
    - 단일 리더 복제: 선형적일 수도 있음. (리더와 동기식 복제 노드에서만 읽는 경우)
    - 합의 알고리즘: 선형적임.
    - 다중 리더 복제: 비선형적.
    - 리더 없는 복제: 아마도 비선형적. (정의에 따라 된다고 볼 수 있으나, 없다고 보는게 안전하다.)

- 선형성의 비용
  - CAP는 도움이 안된다.
    - CAP: "선형성이 없는 애플리케이션은 네트워크 문제에 더 강인하다."는 정리.
    - 단, 하나의 일관성 모델(선형성)과 네트워크 분단만을 고려한다.
    - 실제로는 더 많은 모델과 분산 환경의 문제(노드 죽음, 네트워크 지연 등)가 있으므로, 현대에는 도움이 되지 않는다.
  - 선형성은 느리다.
    - 컴퓨터 밑바닥의 다중코어 CPU나 RAM 조차 선형성을 보장하지 않고, 캐시를 사용해 비동기적으로 동작한다.
    - 이는 성능을 위한 것으로 선형성을 보장하는 알고리즘은 항상 느리기 때문에, 성능을 위해서 선형성을 포기하기도 한다.

#### 순서화

- 순서화 보장(+ 인과성)
  - 순서화는 인과성을 보장해준다.
  - 인과성은 선형성보다 조금 더 느슨한 일관성 모델이다.
  - 인과성은 "happens-before" 관계를 보장한다. 즉, 한 이벤트가 다른 이벤트의 원인이 될 수 있는 경우(인과 관계가 있는 연산), 그 순서가 보장된다. 그 외의 경우 보장하지 못한다.
  - 구현 방법
    - 일련번호나 타임스템프
    - 단, 단일 리더가 아닌 경우 인과성에 일관적이지 않다.
    - 이 문제를 해결하기 위해 램포트 타임스탬프를 사용할 수 있다.
    - 버전 백터는 전체 순서화를 제공하지 않지만, 램포트 타임스탬프는 보장한다.
    - 그러나 한계가 있는데, 당장 성공 여부를 확인할 수 없다. (이를 위해선 다른 노드를 전부 확인해야 하는데, 이러면 내결함성이 낮아진다.)
      - 쓰는 시점에는 순서를 알 수 없고, 나중에 전체적인 결과를 기반으로 순서를 파악할 수 있다.
    - 이러한 문제점으로 인해서 "합의"가 필요하다.

- 전체 순서 브로드캐스트
  - 램포트 타임스탬프보다 강력하다. 메시지 전달 시점에 순서가 확정된다.
  - 노드 사이에 메시지를 교환하는 프로토콜로 기술된다.
  - 비공식적으로 두 가지 안전성 속성을 항상 만족한다. (비동기적으로)
    - 1. 신뢰성 있는 전달(전송된 메시지는 모든 곳에 전달된다.)
    - 2. 전체 순서가 정해진 전달(메시지는 모두 같은 순서로 전달된다.)
  - 전체 순서 브로드캐스트를 사용해서 선형성 저장소를 만들 수 있다. (어떻게 되는지는 생략, 추가로 반대로 구현하는 것도 가능)

#### 분산 트랜잭션과 합의

- 분산 트랜잭션과 합의 (요 장은 이해 안가는게 많음)
  - 합의: 모든 노드가 특정 결정을 인식하고 결정을 되돌릴 수 없는 방법으로 동의하는 것.
  - 원자적 커밋: 모든 노드가 트랜잭션에 결과에 동의하는 것.
  - 2PC(2 phase commit)
    - 원자적 커밋을 보장하는 방법 중 하나.
    - 코디네이터라는 서비스(각 노드의 어플리케이션에 라이브러리 형태로 존재하거나 별도 서비스(노드)로 존재함)가 있다.
    - 순서: 1. 코디네이터(모든 노드에 준비 요청) -> 2. 모든 노드(준비 완료 ok 응답) -> 3. 코디네이터(커밋 및 커밋 요청) -> 4. 모든 노드(확인 ok 응답 시 커밋, 하나라도 거부시 롤백)
      - 만약 3에서 모든 노드에 요청이 가지 않는다면 될때까지 대기해야만 한다. 이미 커밋되었으므로
      - 단, 코디네이터가 죽는 경우 모든 노드는 대기해야 한다.
    - 이론상으로 3PC라는 더 좋은 프로토콜이 있으나, 신뢰성 있는 네트워크 환경에서만 유효하므로 거의 쓰이지 않는다.
      - 2PC는 블로킹이나 3PC는 논블로킹임.

- 현실의 분산 트랜잭션
  - 성능이 낮아지고 운영상의 문제를 일으키므로 특정 서비스는 분산 트랜잭션을 구현하지 않기도 한다.
  - 종류
    - 데이터베이스 내부 트랜잭션: 데이터베이스 내부에서만 호환되면 되므로 사용하므로 특화된 기법 가능.
    - 이종 분산 트랜잭션: 여러 다른 서비스에서 호환되어야 하므로 더 어렵다.
      - 모든 시스템이 동일한 원자적 커밋 프로토콜을 사용할 수 있어야만 구현 가능하다.
  - XA 트랜잭션
    - 이종 기술에서 2PC를 구현하는 표준. 여러 서비스에서 지원한다. (현실에서는 프로세스에 로딩되는 단순 라이브러리다.)
    - 장애 대처가 중요한 이유
      - 트랜잭션은 잠금을 수반하며, 중간에 장애가 발생하면 스스로 복구하거나 인위적인 개입이 발생하기 전까지 잠금이 절대 풀리지 않는다. 
      - 현실적으론 복구가 불가능한 경우도 있다. 이 경우 원자성을 깨는 선택을 해야만 할 수도 있다.
    - (이 사이에 소주제 2~3개 더 있는데, 이해 잘 안가서 생략함.)

- 합의 (소제목 *정리* 파트 참고)
  - 분산 환경에서 발생하는 여러 문제는 "합의"를 구현하므로 해결할 수 있고, 한 문제만 해결된다면 다른 문제도 쉽게 해결할 수 있다. (선형성 구현 가능)
    - 선형셩 CAS 레지스터(분산 환경에서 key를 말한다.)
    - 원자적 트랜잭션
    - 전체 순서 브로드캐스트
    - 잠금과 임차권(리더 권한)
    - 멤버십/코디네이션 서비스
    - 유일성 제약 조건
  - 이는 단일 리더 노드로 구현할 수 있다.
  - 단일 리더 노드가 문제가 발생했을 때, 해결 방법
    - 차단 및 복구 대기 
    - 인위적인(사람의 개입으로) 새 노드 사용
    - 자동으로 새 리더 노드 선출 - 알고리즘
  - 다중 리더 or 리더 없는 분산 시스템은 전체 합의를 제공할 수 없다.
    - 즉, 어플리케이션 개발자나 분산 시스템이 등이 선형성 없이 발생하는 여러 문제를 대응할 수 있어야 한다.

### 스터디 미팅 중 나온 내용

- 의문: 램포트 타임 스템프 방식은 데이터의 최신 여부를 파악하지 못하는건가?
  - (counter, node_identifier)로 구성된 버전 비교에서 발생할 수 있는 문제, 특히 데이터의 최신 여부를 어떻게 판단하는지
  - 동일한 counter 값을 가지는 타임스탬프 (2,1)과 (2,2)의 비교에서 어떤 연산이 최신인지 파악 못하는 문제
  - 결론: 
    - (GPT 피셜) - [링크](https://chatgpt.com/share/2b50370c-51c9-411c-848b-24fc80cb1685)
      - Lamport 타임스탬프는 이벤트의 순서를 추적할 수 있지만, 인과 관계를 완벽하게 보장하지는 못함. 그래서 실제로 어떤 이벤트가 "인과적으로" 더 늦게 발생했는지를 정확히 판단하기 어려울 수 있음.
      - 이 문제를 해결하기 위해 벡터 클럭을 사용할 수 있음. 
    - (책 내용) 
      - 버전 백터는 두 연산이 동시적인지 또는 어떤 연산이 다른 연산에 인과적으로 의존하는지 구분할 수 있음.
      - 램포트 타임스탬프는 확실한 전체 순서화를 강제하고, 크기가 작다는 장점이 있음.


### 장 요약

- **선형성(Linearizability)**:
  - 시스템이 하나의 동기식 복사본처럼 동작하는 것처럼 보이는 것을 의미한다.
  - 이를 구현하기 위해 합의 프로토콜을 사용하는 시스템으로는 Zookeeper와 etcd가 있다. Zookeeper와 etcd는 선형성 보장 외에도 다양한 기능을 제공한다.
  - 선형성은 일반적으로 처리 속도가 느리고 장애 상황에서 Blocking이 발생할 수 있다. 따라서 선형성은 일반적인 DBMS보다는 순서가 중요한 리더 선출, 제약 조건 관리, 분산 시스템의 순서 보장 등에 주로 사용된다.
  - 선형성은 트랜잭션의 직렬성과는 별개의 개념이다. 직렬성은 데이터베이스의 트랜잭션 간의 일관성을 보장하는 것이고, 선형성은 분산 시스템에서 연산의 일관성을 보장하는 것이다.

- **순서화(인과성) (Causal Consistency)**:
  - 인과 관계가 있는 작업 간의 순서를 보장한다.
  - 선형성보다 더 약한 일관성을 제공한다.
  - 쓰는 시점에서 본인의 순서를 정확히 알 수 없다는 단점이 있다.

- **전체 순서 브로드캐스트(Total Order Broadcast or Atomic broadcast)**:
  - 전체 순서 브로드캐스트는 모든 노드가 특정 순서에 동의하도록 하는 "합의"를 구현하는 메커니즘이다.
  - 이는 선형성을 구현하는 데 사용될 수 있다.
  - Zookeeper는 이를 사용한 Zookeeper Atomic Broadcast (ZAB) protocol을 지원한다. (Zookeeper의 구성요소 중 하나라 지원한다는 말이 맞는지는 잘 모르겠음.)

### 느낀점

너무 이론적인 부분에 치중되기도 했고, 분산 시스템을 사용해본 경험이 없다보니 관련 배경 지식도 없어서 지금까지 제일 어려운 장이였음.


주키퍼나 etcd가 분산 시스템에서 이렇게 중요한 역할을 수행하는 것을 처음 알았다. 예전에 공부할 때는 서비스 디스커버리 정도 역할만 수행하는 줄 알았는데... 왜 이런 중요한 내용을 잘 다루지 않을까?

<details>
<summary>perplexity 답변</summary>
<div markdown="1">

etcd는 실제로 전체 순서 브로드캐스트(total order broadcast)를 제공하는 코디네이션 서비스의 역할을 수행합니다. 이 기능은 etcd의 핵심적인 특성 중 하나이지만, 일반적인 사용 사례나 소개에서 자주 언급되지 않는 이유는 다음과 같습니다:

## 복잡성과 추상화

1. **기술적 복잡성**: 전체 순서 브로드캐스트는 분산 시스템의 복잡한 개념으로, 일반 사용자나 개발자가 이해하기 어려울 수 있습니다[1].

2. **추상화 레벨**: etcd는 이 기능을 내부적으로 구현하여 사용자에게 더 간단한 인터페이스를 제공합니다. 대부분의 사용자는 이 낮은 수준의 세부 사항을 알 필요가 없습니다[2].

## 실용적 접근

1. **실제 사용 사례 중심**: 서비스 디스커버리, 설정 관리 등은 etcd의 가장 일반적인 사용 사례이며, 이러한 기능들이 사용자들에게 더 직접적으로 관련이 있습니다[3].

2. **사용 편의성 강조**: 공식 문서와 소개 자료는 주로 etcd를 어떻게 사용하고 구성할 수 있는지에 초점을 맞추고 있습니다[4].

## 대상 독자 고려

1. **일반 개발자 대상**: 대부분의 문서는 일반 개발자나 시스템 관리자를 대상으로 작성되어 있어, 복잡한 분산 시스템 이론보다는 실제 적용 방법에 중점을 둡니다[5].

2. **특정 사용 맥락**: etcd는 주로 쿠버네티스와 같은 특정 플랫폼의 컨텍스트에서 소개되는 경우가 많아, 그 플랫폼에서의 역할에 초점이 맞춰집니다[2].

전체 순서 브로드캐스트와 같은 고급 기능은 etcd의 내부 동작과 설계 철학을 이해하는 데 중요하지만, 대부분의 사용자에게는 직접적으로 관련이 없을 수 있습니다. 그러나 분산 시스템 전문가나 etcd의 내부 동작에 관심 있는 개발자들에게는 이러한 정보가 매우 중요할 수 있습니다.

</div>
</details>

CAP 이론이 이제 중요하지 않다는게 좀 신기하긴 했음. 그런데 왜 여러 공신력있는 [사이트](https://www.ibm.com/kr-ko/topics/cap-theorem)에서 CAP를 설명하고 있을까? 
(사담이지만, 이런 단순 인터넷 검색으로 알기 어려운 정보를 알려주는 부분이 있어서 이 책이 좋다고 생각함.)

<details>
<summary>perplexity 답변</summary>
<div markdown="1">

CAP 이론이 분산 시스템 설계에서 중요하지 않다는 의견이 일부 개발자들 사이에서 나오고 있지만, 여전히 여러 공신력 있는 사이트에서 CAP 이론을 기준으로 설명하는 이유는 다음과 같습니다:

## CAP 이론의 지속적인 중요성

1. **기본적인 개념**: CAP 이론은 분산 시스템의 근본적인 제약 조건을 설명하는 중요한 이론입니다. 이는 분산 시스템이 직면하는 필수적인 트레이드오프를 이해하는 데 도움을 줍니다[1][3].

2. **교육적 가치**: CAP 이론은 분산 시스템 설계의 기초를 이해하는 데 유용하며, 시스템 설계와 아키텍처를 교육하는 데 여전히 많이 사용됩니다. 이는 개발자들이 시스템의 특성을 이해하고 적절한 설계 결정을 내리는 데 도움을 줍니다[4].

3. **실제 적용 사례**: CAP 이론은 다양한 데이터베이스와 분산 시스템의 설계에 직접적인 영향을 미칩니다. 예를 들어, NoSQL 데이터베이스는 CAP 이론에 따라 설계되어 특정 특성을 강조합니다. 이러한 실제 사례는 CAP 이론이 여전히 실무에서 중요하다는 것을 보여줍니다[1][3].

## 현대 시스템에서의 변화

1. **기술 발전**: 현대의 분산 시스템은 CAP 이론의 제약을 완화하는 새로운 기술과 모델을 사용하고 있습니다. 예를 들어, 부분적으로 동기화된 모델이나 약한 일관성 모델을 통해 CAP 이론의 제약을 극복하려는 시도가 있습니다[3].

2. **복잡한 트레이드오프**: CAP 이론은 여전히 유효하지만, 현대 시스템에서는 더 복잡한 트레이드오프와 요구사항이 존재합니다. 따라서 CAP 이론만으로는 모든 문제를 설명하기 어려울 수 있습니다[2][3].

결론적으로, CAP 이론은 여전히 분산 시스템 설계의 중요한 부분으로 남아 있으며, 많은 공신력 있는 사이트에서 이를 설명하는 것은 이론의 기본적인 중요성과 교육적 가치를 반영합니다. 그러나 현대의 시스템 설계에서는 CAP 이론 외에도 다양한 요소를 고려해야 합니다.

</div>
</details>
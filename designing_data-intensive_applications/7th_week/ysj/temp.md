### 8장 분산 시스템의 골칫거리

### 정리
이 장에서는 분산 환경에서 발생하는 여러 문제점을 다룬다.

[아무리 작은 확률이라도 잘못될 가능성이 있다면 잘못된다.](https://ko.wikipedia.org/wiki/%EB%AC%B4%ED%95%9C_%EC%9B%90%EC%88%AD%EC%9D%B4_%EC%A0%95%EB%A6%AC)

#### 결함과 부분 장애 - 분산/단일 시스템의 장애 차이

- 단일 시스템
  - 슈퍼 컴퓨터, 범용 컴퓨터 등
  - (좋은 소프트웨어가 설치된 기기는) 문제가 발생했을 떄, 결정적(이상화)이다.
    - 실패 or 성공
  - 따라서 동작을 예측할 수 있다.
- 분산 시스템
  - 클라우드 컴퓨팅 등
  - 비결정적이다.
    - 부분 장애(partial failure)가 생긴다.
  - 따라서 동작을 예측할 수 없다. 
    - 더 많은 부분이 연관되어 있을수록 실패 확률은 늘어난다.

#### 신뢰성 없는 네트워크

- 대부분의 인터넷은 주로 비동기 패킷 네트워크이다. 이는 신뢰성이 없다. 
  - 언제 받을지 알 수 없으며(누락, 딜레이), 전달 여부도 알 수 없다.
- 현실에는 많은 결함이 있다.
  - 인적오류, 라우터 병목, 클라우드 컴퓨팅의 물리 컴퓨터에 쏠리는 네트워크 부하(여러 가상 컴퓨터를 가진다. 네트워크 딜레이(큐), 컨텍스트 스위칭 등에 영향을 줄 수 있다.)
- 자동 결함 감지 기능이 필요하다.
  - 문제있는 노드로부터 연락을 받을수도 있으나 이것만으로는 신뢰할 수 없다. (전달을 못할수도 있음.)
  - 따라서, **주기적**으로 **여러 번** 요청하여 확실하게 결함이 발생하였음을 알 수 있어야 한다.
- 타임아웃
  - 비동기 네트워크는 기약 없는 지연(unbounded delay)를 가지므로 적절한 타임아웃 시간을 예측할 수 없다.
  - 따라서, 테스트를 통해서 적절한 타임아웃 시간을 정해야 한다.
- 네트워크 혼잡
  - 패킷 통신 기기는 출력/입력 큐가 있다. 
    - 각 디바이스(끝단) 뿐만 아니라 스위치나 라우터에도 병목이 생기거나 큐가 부족해서 패킷 손실이 발생할 수 있다.
  - 따라서, 이러한 혼잡 상황을 고려해서 장애 감지와 이른 타임아웃 위험성의 trade-off를 고려해서 적절한 시간을 선택해야 한다.
    - 네트워크 변동성(jitter)를 측정하고 자동으로 타임아웃 시간을 설정하는 도구를 사용하는 것도 좋다.
      - (TCP도 이런 식으로 동작한다는데, 나중에 공부할 때 찾아보면 좋을듯)
- (TIP) TCP와 UDP 중 선택 기준
  - 신뢰성과 헤더 크기의 차이 등 (차이 내용은 생략)
  - UDP: 지연된 데이터의 가치가 없는 상황
    - 실시간 스트리밍, 전화(VoIP)
- 동기 네트워크 vs 비동기 네트워크
  - 동기(회선 방식)
    - 고정된 양의 대역폭이 할당된다.
    - 지속적인 데이터 전송이 발생하지 않으면 낭비가 크다. - 주로 전화(ISDN)가 여기 해당됨.
    - 큐 대기가 없으므로 네트워크 종단 시간의 최대치가 고정되어 있다. 기약 있는 지연(bounded delay)
  - 비동기(패킷, 가상회선 방식)
    - 인터넷에서 일반적으로 쓰는 방식
    - 순간적으로 몰리는 트래픽에 최적화 되어있다.
    - 큐 대기로 인해서 기약 없는 지연(unbounded delay)을 가진다.

#### 신뢰성 없는 시계

- 단조 시계 vs 일 기준 시계
  - 일 기준 시계
    - NTP (Network Time Protocol)로 동기화되는 시간 정보.
    - 로컬 입장에서, NTP 서버에 요청하여 네트워크를 통해 동기화하므로 로컬의 시간이 변화(앞당겨지거나 느려지거나)할 수 있다.
      - NTP 서버와 로컬 사이의 네트워크 딜레이로 인해서 실제 시간과 약간의 오차가 있을 수 있다.
    - 주로 epoch를 기준으로 삼는다. (그 외 별개의 다른 기준 시점을 사용하기도 한다.)
    - ([나무위키](https://namu.wiki/w/NTP), [위키피디아](https://en.wikipedia.org/wiki/Network_Time_Protocol))
  - 단조 시계
    - 단조(단조로운 할때 그 단조) 시계는 로컬 시스템에서 가지고 있으며 시간이 변화하지 않고 항상 앞으로 일정하게 흐른다.
    - 따라서, 지속 시간(시간 구간)을 재는데 유용하다.
    - 주로 마이크로초나 그 이하 단위로 측정 가능하다.
    - 각 시스템에 각자 존재하므로, 다른 기기 or 하드웨어(CPU 등) 사이의 단조 시계 값은 비교하는게 의미 없다.
      - OS는 여러 CPU에 걸쳐 스케줄링 되더라도 단조적으로 보이게 보장하나, (정말 정확해야 하는 경우) 신뢰할 수는 없다.
  - [GPT 질문 결과 - 질문 내용은 나무위키 긁음](https://chatgpt.com/share/4c79980a-5af8-4d46-b46b-cf907b45873e)

- NTP를 통한 시계 동기화는 정확하지 않다.
  - NTP 서버와의 문제: 네트워크 지연, NTP 서버 이상, 방화벽 등
  - 로컬의 문제: 드리프트(로컬 수정 시계의 오차로 인한 gap), 동기화 시 조정으로 인한 시간 변화 등
  - 더 정확한 동기화를 위해선 GPT 수신기, PTP, 꾸준한 모니터링과 배포 등이 요구된다.

- 동기화된 시계에 의존하기
  - `동기화된 시계 == 일 기준 시계`
  - 그러나, 일 기준 시계의 경우 부정확하다. 따라서 타임스탬프 값 자체로는 어떤 작업이 먼저 수행되었는지 보장할 수 없다.
  - 해결법
    - 신뢰 구간 사용하기: 구글의 TrueTime API가 있는데 2가지 타임스탬프(earliest, lateset) 시간 범위를 가지는걸 보장한다.
      - 이 API를 사용해서 분산환경(구글의 Spanner DBMS)의 snapshot isolation의 Transtion ID를 사용하기 위해 사용하기도 한다. 단, overlap되지 않기 위해 타임스탬프의 lateset까지 기다린다. 이는 (9장에서 설명) 인과성을 보장한다. 
    - 논리적 시계 사용하기: 증가하는 카운트 값으로 정확한 순서를 알 수 있다. (일 기준, 단조 시계의 경우 물리적 시계라고 한다.)

- 프로세스 중단
  - 프로세스는 어느 시점에서 아주 오랬동안 멈출 수 있다.
    - GC의 stop-the-world, 가상 환경의 가상 장비의 suspend(가상 머신 일시중지), 컨텍스트 스위칭, I/O 등
  - 따라서, 분산 시스템의 노드는 어느 시점에 상당한 시간동안 멈출 수 있다고 가정해야 한다.
  - (TIP) 단일 기기의 경우 공유 메모리를 사용해서 mutex, semaphore, atomic counter 등을 사용해서 선점(preempt)하여 해결할 수 있다.
  - 응답 시간 보장 방법: 리얼 타임 OS(데드라인 보장, 대신 전체적인 속도 느릴 수 있음. 경제적이지 않음), 일반적인 서버용 컴퓨터는 보장할 수 있는 방법이 없다.
  - GC 영향 적게 받기: GC에 가까운 노드를 파악하고 요청을 다른 곳으로 분산하기, GC가 발생하기 전에 끄고 다시 키기
    - (책에는 없는데, GC 없는거 쓰는것도 해결 방법 중 하나가 아닐까? Discord가 Rust를 사용한 것처럼)

#### 지식, 진실 그리고 거짓말

- 진실은 다수결로 결정된다
  - 분산 환경은 한 노드에만 의존할 수 없으므로, 분산 알고리즘은 정족수 노드의 투표에 의존한다.
  - 리더와 잠금
    - 분산 환경에서 하나만 뭔가를 가져야 하는 경우가 있다.
    - 이 경우 펜싱(fencing) 토큰을 사용하여, 내가 '선택된 자'라고 착각하는 노드의 요청을 무시할 수 있어야 한다.
- 비잔틴 결함(Byzantine Fault)
  - 때로는 노드가 진실을 말하지 않을 수 있다.
    - (여기서 말하는 신뢰(응답을 받을 수 있는가?)와 진실(거짓말을 하는가?)은 다르다.)
  - 신뢰할 수 없는 환경에서 올바르게 동작하는 경우, [비잔티움 장애 허용, 비잔티움 내결함성](https://ko.wikipedia.org/wiki/%EB%B9%84%EC%9E%94%ED%8B%B0%EC%9B%80_%EC%9E%A5%EC%95%A0_%ED%97%88%EC%9A%A9)을 가진다고 한다.
  - 하지만, 일반적인 웹 서비스의 경우 불필요하다.
    - 비잔틴 내결함성을 가지도록 하는 프로토콜은 복잡하다. 
    - 웹 어플리케이션의 특징과 잘 맞지 않는다.
      - 요청을 하는 클라이언트가 악의적이라고 가정한다. 
      - 서버는 이를 받고 검증하여 요청의 허가 여부를 결정하는 모든 권한을 가진다.
      - 따라서 클라이언트의 요청과, '사소한 거짓말'(네트워크, 하드웨어 결함, 소프트웨어 버그)을 검증하고 보호하는 것이 적절하다.
    - 사용 예시: 항공우주 산업(방사능 오염), P2P(비트코인, 블록체인, 탈중앙화)
- 시스템 모델과 현실
  - 시스템 모델: 알고리즘이 가정하는 것을 기술한 추상화
  - 타이밍 가정
    - 동기식 모델: 확실한 제한이 있다. (회선 네트워크, 리얼타임 OS)
    - 부분 동기식 모델: 일반적이고 현실적인 모델. 대부분 동기식처럼 동작하지만, 때때로 한계치를 초과한다.
    - 비동기식 모델: 이 모델의 알고리즘은 아무 가정도 할 수 없다. 따라서 매우 제한적이다.
  - 노드 장애
    - 죽으면 중지하는(crash-stop) 결함: 노드가 결함으로 중지된다면 절대 복구할 수 없다.
    - 죽으면 복구하는(crash-recovery) 결함: 노드가 결함으로 중지된다면, 시간이 지나서 다시 응답한다.
    - 비잔틴(임의적인) 결함: 다른 노드를 속이는 등 무슨 일이든 일어날 수 있다.
  - 분산 시스템 알고리즘의 속성
    - 안전성과 활동성으로 나뉜다.
    - 안전성: 위반이 발생할 수 있지만 실패하고, 실패를 즉시 감지할 수 있다.
      - e.g. 유일성, 단조 일련번호
      - 안전성은 반드시 유지되어야 하는 특성으로, 시스템이 동작하는 동안 이 속성이 위반되면 시스템이 잘못된 상태에 있다는 의미이다.
    - 활동성: 정확한 시점을 알 수는 없지만, 언젠가 완료될 것이라는 걸 보장한다.
      - e.g. 가용성, 최종적 일관성
      - 시스템이 아직 완료되지 않았다는 경고나 신호를 보낼 수 있으며, 이는 활동성 속성의 일부로 허용된다.
  - 현실은?
    - 알고리즘을 이론적으로 설명할 때는 어떤 일이 일어나지 않을 것이라 '가정' 할 수 있다.
      - 하지만 현실은 어떤 일이든 일어날 수 있다.
    - 알고리즘이 올바르더라도 구현까지 올바른 것은 아니다.
    - 따라서, 현실에서는 알고리즘이 보장하는 내용에 대한 경우를 처리해야 할 수 있다.
    - 그럼에도 시스템 모델(알고리즘)의 증명은 드물게 발생하는 문제를 미리 예방할 수 있게 하므로 중요하다. 

### 후기 

클라우드 환경에서는 가상 컴퓨터를 사용하기 때문에,    
내가 점유하지 않은 다른 가상 컴퓨터가 물리적 컴퓨터의 네트워크 혼잡(큐 병목)을 유발할 수 있다.   
이로 인해 내가 사용하는 가상 컴퓨터에서도 병목 현상이 발생할 수 있다는 점은 미처 생각하지 못했던 중요한 포인트라고 생각함.

일 기준 시계나 단조 시계, 가상환경(AWS 인스턴스)의 중지 등. 사용은 하고 있었지만 어떻게 동작하는지는 궁금해하지도 않았는데, 꽤나 재미있게 읽었다.

대신 내 상황(일반적인 웹 서버 개발)에서 응용하거나 사용하기에 적절한 내용은 아니라 엄청 관심을 가지고 보지는 않았음.

정리하자면 분산 시스템은 부분 실패, 부정확한 시계, 비신뢰성 네트워크를 가지고 있고, 이게 많은 문제를 유발한다는 거.






## Section 05 정리

#### OSI Model - Layer 4 Transfer Layer

- Host 간의 데이터를 전송하는 역할
- 세션 다중화(Session Multiplexing) 지원
    - Host가 여러 Session을 지원하고, 단일 링크(두 호스트 간의 네트워크 연결)에서 개별 트래픽 흐름을 관리
    - Post를 사용해서 같은 Host더라도 여러 Session을 가지고, 어떤 어플리케이션에 사용되는 트래픽인지 식별할 수 있음.

- 트래픽을 주고받는 과정
    - Sender의 Port와 Host의 Port가 연결됨.
    - 각 Port로만 주고 받음.
    - Sender Port가 15000이고 Receiver Port가 80로 연결을 맺으면 해당 포트로만 통신.
        - 어디로부터 온 요청인 지 식별 가능.
            - Stateful 방화벽의 동작 원리.   

#### TCP, UDP

- TCP
    - 순서가 보장된 데이터 전송: 발신자는 순서 번호를 포함하여 데이터 전송, 수신자는 해당 번호를 확인하여 올바른 순서로 트래픽 조립.
    - 세그먼트 누락 여부: 누락된 세그먼트를 확인하여 발신자에게 알릴 수 있음. (응답을 받은경우 수취 알림을 보내고, 누락이 생기면 보내지 않는 방식)
    - 흐름 제어: 수신 Host가 데이터를 전부 처리할 수 있도록 발신자의 데이터 흐름 조정
    - 연결 기반: TCP 3-Way Handshake를 통한 연결과 4-Way Handshake를 통한 해제
    - 헤더를 보면 꽤 많은 내용이 있음. (20 Byte) 각 내용과 역할은 [링크](https://networklessons.com/cisco/ccie-routing-switching-written/tcp-header) 참고 
    - (혼잡 제어도 있는데, 여기선 설명 안함.)

- UDP
    - best effort 방식 사용
        - 발신자가 패킷을 구성해서 수신자에게 보내기만 하고, 따로 응답 확인을 하지 않음.
    - 발신/수신자 사이의 아무 연결이 없음.
    - 따라서 신뢰할 수 없음.
        - 흐름 제어, 세그먼트 누락, 순서 제어 지원하지 않음.
    - 신뢰성을 보장하려면 더 상위 계층에서 이루어져야 함.
    - 헤더를 보면 출발지, 목적지 포트, 체크섬, 데이터만 포함함. (8 Byte)
        - 따라서 간접 비용(오버헤드)가 적게 듬.
- 언제 사용하는가?
    - TCP: 신뢰성이 중요한 경우
    - UDP: 지연에 민감한 실시한 트래픽
    - 꼭 하나만 사용하지는 않고, 두 방식을 함꼐 사용하는 어플리케이션도 있다. (e.g. DNS)


## 후기

- [널널한 개발자 TV - TCP 연결이라는 착각에 대해](https://youtu.be/DC9FfKSgisg?si=fuJ0XrQ1-3vrt4sm)를 시간되면 보면 좋을듯.
    - 설명 잘해줌. 좀 어그로 같은 제목이긴 한데...
    - `연결 != 보안성`이라는 의미
    - 간단 정리
        - TCP 연결은 segment 단위의 3-way handshake로 이루어짐.
        - 서로의 정보을 주고 받는 것. (syn, MSS, 혼잡제어 정책 등...)
            - 신뢰성 있는 데이터 송수신을 가능하게 하는데 필요한 정보들
        - 연결 이후 각 커널에 상대방의 정보를 저장(TCB)하고, 사용함.
        - 위 과정에서 보안성을 지켜주는게 없음. TCP Session hijacking 같은 문제가 발생할 수 있다.
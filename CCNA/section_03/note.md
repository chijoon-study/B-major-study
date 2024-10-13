## Section 03 정리

#### OSI Model
> 네트워크 프로토콜의 상호 작용 방식을 이해하는데 도움을 주는 개념적 프레임워크 

(개념적 = 실제가 아님)   

[관련해서 정리했던 글](https://github.com/YangSiJun528/memory/blob/master/notes/Computer%20Science/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%20%EA%B8%B0%EC%B4%88%20%EA%B0%9C%EB%85%90.md)

#### 내트워크 개요

- Node(노트북, 프린터)
- 이더넷 케이블: 유선 통신
- 스위치: 많은 포트
- 무선 액세스 포인트 (= 공유기)
- 인터넷 (=외부 연결 시 사용)
- 라우터: 인터넷 간 통신, 여러 포트 타입 지원 = 여러 종류의 네트워크 접근 가능, 보안을 위한 방화벽
- Local Area Network: 라우터를 넘어가지 않는 범위?
- Wide Area Network: 특정 라우터 간의 전용 연결?

- 네트워크 핵심: 엔드 호스트 간의 연결

- 네트워크 핵심
    - 토폴로지: 장치가 어떤 식으로 연결되었는가?
    - 속도
    - 비용
    - 보안
    - 가용성(Availability): 항상 사용 가능한 상태
    - 확장성(Scalability)
    - 신뢰성(Relaibility): 계속 작동


#### OSI 모델 개요

- 7 layer로 네트워크 통신 분리
- ISO에 속한 표준
- 위,아래 계층끼리 상호작용
- 각 level에서 내려갈 때 Encapsulation(상위 정보 + 본인 level의 정보), 올라갈 때 Decapsulation
- (각 layer 별 설명 생략)
- ![](https://storage.googleapis.com/blogs-images-new/ciscoblogs/1/osi-768x593.gif)
    - [출처](https://blogs.cisco.com/cloud/an-osi-model-for-cloud), 강의에 포함된건 아닌데, layer 별 설명으론 충분해 보임
- OSI 모델은 여전히 네트워크 문제를 해결하는 데 유용하다. (의사소통, 관심사 분리, 네트워크 이해)

#### TCP/IP Suite
여기서 Suite는 Set 보다는 더 격식있는 표현 정도라고 함.

OSI와 같은 Model이 아니라 실제로 사용되는 프로토콜 스택, 집합 정도로 해석할 수 있음.

이전에는 TCP/IP 외에 다른 스택도 있었으나 사라짐.

OSI 계층을 사용하긴 하지만, 더 적게 4(어떤 곳에서는 5)개 정도만 가짐.

![](https://www.cisco.com/c/dam/en/us/support/docs/ip/routing-information-protocol-rip/13769-5-01.gif)
[출처](https://www.cisco.com/c/en/us/support/docs/ip/routing-information-protocol-rip/13769-5.html)

###### 주요 용어
- 계층 별 통신 시 사용하는 데이터의 이름
    - Data
    - Segemt
    - Packet
    - Frame
- PDU(Protocol Data Unit)
    - OSI의 1~7 계층까지의 전체 통신
    - 두 호스트 간의 통신 시 PDU 프로토콜 데이터 단위를 교환한다.
- 일상적으론 명확히 데이터의 이름을 구분하지는 않고, PDU를 포함해 Packet이라고 부르기도 함.


#### OSI 상위 계층

5~7 계층이 해당

(설명 생략 - 나중에 참고할때는 cisco 공식문서 설명 참고하기)

#### OSI 하위 계층

4~1 계층이 해당

(설명 생략 - 나중에 참고할때는 cisco 공식문서 설명 참고하기)

## 느낀점

책 읽는것보다는 정보가 적을듯. 

여기 섹션이 30분정도 쓰는데, 대본으로 하면 좀 큰 개발서적 기준으로 10페이지 안으로 끝날거 같은 분랑임.

"OSI는 개념적이고 TCP/IP는 실질적인 프로토콜 집합이다." 이 개념을 몰라서 계속 삽질하고 착각했었는데, 이 강의에서는 이름부터 확실하게 구분짓고 명확하게 설명하는게 좋았다.

위에 예전에 삽질하면서 정리했던 노트 링크가 있음. 강의 내용이랑 겹치는게 많은데, 한 번 보면 좋을듯.


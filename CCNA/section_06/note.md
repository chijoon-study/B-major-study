## Section 06 정리

#### OSI Model - Layer 3 Network Layer

패킷을 네트워크 상의 목적지로 라우팅하는 역할.

라우터가 네트워크 층에서 동작.

서비스 품질 담당 역할: 더 나은 수준의 서비스를 필요로하는 트래픽을 우선 처리

논리적 주소 지정 체계인 IP 주소를 사용함.

#### IP Protocol

3계층의 가장 유명한 프로토콜. (이외에는 ICMP, IPSec)

Connectionless Protocol이므로 응답을 받을 수 없음.

IPv4와 IPv6를 사용함.
- 둘은 다른 버전이고, 다른 헤더 형식을 가짐. (상호 호환성 X)
- [IPv4](https://www.geeksforgeeks.org/introduction-and-ipv4-datagram-header/), [IPv6](https://www.geeksforgeeks.org/internet-protocol-version-6-ipv6-header/)
- 다른 버전도 있었는데, 거의 사용 안함.
- 각 헤더의 역할은 위에 링크한거 참고.

#### Unicast, Broadcast, Multicast Traffic

IP 네트워크를 통해 전송되는 트래픽 유형.

유형 별로 스위치에서 어떻게 각 Host에 트래픽을 전달하는지가 다름.

- Unicast: 
    - 유효한 단일 Host로 전송
- Broadcast: 
    - 스위치에 연결된 모든 Host로 이동함.
    - Host의 요청 여부와 무관하게 모든 곳으로 전송.
- Multicast: 
    - 하나의 사본을 여러 목적지로 전송함.
    - Unicast 여러 번 보내는 것보다 효율적임. (1MB 데이터를 한 번만 받고, 사본을 여러 번 보내면 효율적. 대신 목표 Host(n명이라 가정) 만큼 여러번 보내면 nMB의 트래픽이 필요함.)
    - 수신자가 어떤 유형의 데이터가 필요한지 일종의 등록을 한다. (IPTV 채널 or 라디오 방송의 주파수 같은 느낌. 실제로 재네가 Multicast를 쓴다는건 아님.)

#### 2진수 계산법, IPv4 Format - 강의에 있는데 아니까 생략

#### Subnet Network

하나의 큰 네트워크를 여러 작은 서브넷 네트워크로 나눔.

이를 통해 관리적 용의, 트래픽의 범위 제한을 통한 성능 향상 등의 이점을 가짐.

#### Subnet Mask

Host는 목적지의 IP 주소를 자신의 IP 주소 + 서브넷 마스크를 비교함으로써, 목적지가 같은 서브넷 상에 있는지 알 수 있다.

이를 통해 로컬 라우터(기본 게이트웨이)를 통해서 전송할지, 아닌지가 결정됨.

Host의 IP 주소는 Network Portion(영역)과 Host Portion으로 구분되며, 그것을 결정짓는 것이 Subnet Mask이다.

255.255.255.0 와 같이 연속된 1이후 연속된 0이 나오는 형식을 띄는데, 2진수로 1의 경우 Network Portion, 0의 경우 Host Portion이라고 볼 수 있다.

이렇게 길게 작성하지 않고, Host의 IP 뒤에 1의 개수를 사용하는 슬래쉬 표기법을 사용해 `192.168.10.15/24` (`/24`가 subnet mask) 같이 작성하기도 한다.

Host의 IP로 할당할 수 없는 주소가 있는데, subnet의 최솟값과 최대값이다. 최소값은 네트워크 주소, 최대값은 브로드케스트 주소 역할을 한다.


## 후기

IPv4, IPv6가 그냥 형식 차이인줄 알았는데, 다른 버전의 프로토콜이였음. 


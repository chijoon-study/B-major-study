## Section 18 정리

#### 기본 연결성 문제 해결 - GPT

- Ping: ICMP 프로토콜을 사용해 목적지의 연결성을 확인합니다. ICMP 에코 요청을 보내고 회신을 받으면, 양방향 연결이 가능함을 의미합니다. Cisco 라우터에서 핑 성공 시 느낌표가, 실패 시 마침표나 "U"(도달 불가) 등이 표시됩니다. 확장된 핑 명령어로 특정 출발지 IP 주소에서 핑을 보낼 수 있어 문제 해결 시 유용합니다.

- Traceroute: 트래픽이 네트워크를 통과하는 경로를 확인하며, TTL 값을 1씩 증가시키며 목적지까지의 각 홉을 추적합니다. 이는 루프 방지에도 유용하며, 경로 상의 문제 지점을 빠르게 파악할 수 있습니다.

- 추가 문제 해결 툴 요약:
    - 1계층: show ip interface brief, show interface 명령어로 인터페이스 상태 점검.
    - 2계층: show arp, show mac address-table 명령어로 MAC 주소 테이블 및 ARP 정보 확인.
    - 4계층: 텔넷(telnet)으로 포트 응답 확인.
    - DNS: nslookup으로 DNS 서버의 이름 변환 기능 확인.

#### 추가 정리

- ping은 ICMP 프로토콜, traceroute은 구현에 따라 UDP나 ICMP가 쓰인다고 함.
- TTL이 있는 이유는 루프 방지를 위해서임.
- Traceroute는 일반 핑처럼 동작하지만 목적지에 닿을 때까지 TTL을 1부터 늘려가면서 각 패킷의 경로(홉)를 추적하는 식으로 동작함. TTL이 0이 되는 경우, 시간 만료 응답을 보내는데, 그 요청을 통해서 해당 hop을 파악하고, 이걸 반복해서 경로를 추적함.
- 시스코 링크: https://www.cisco.com/c/ko_kr/support/docs/ios-nx-os-software/ios-software-releases-121-mainline/12778-ping-traceroute.html


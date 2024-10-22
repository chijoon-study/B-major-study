14 Cisco 라우터 및 스위치 기본 사항 - 답변 키

이 실습에서는 스위치에 대한 기본 구성을 완료하고, Cisco Discovery Protocol CDP를 확인하며, 인터페이스 속도 및 이중 구성의 효과를 분석합니다.

Cisco 라우터 및 스위치 초기 구성
1) Router 1을 'R1'이라는 호스트 이름으로 구성

Router(config)#hostname R1
R1(config)#

2) Router 2를 'R2'라는 호스트 이름으로 구성

Router(config)#hostname R2
R2(config)#

3) Switch 1을 'SW1'이라는 호스트 이름으로 구성

Switch(config)#hostname SW1
SW1(config)#

4) 토폴로지 다이어그램에 따라 R1의 IP 주소 구성

R1(config)#interface FastEthernet0/0
R1(config-if)#ip address 10.10.10.1 255.255.255.0
R1(config-if)#no shutdown

5) 토폴로지 다이어그램에 따라 R2의 IP 주소 구성

R2(config)#interface FastEthernet0/0
R2(config-if)#ip address 10.10.10.2 255.255.255.0
R1(config-if)#no shutdown

6) SW1에 관리 IP 주소 10.10.10.10/24 부여

SW1(config)#interface vlan1
SW1(config-if)#ip address 10.10.10.10 255.255.255.0
SW1(config-if)#no shutdown

7) 스위치는 R2를 통해 다른 IP 서브넷에 연결성을 가져야 함

SW1(config)#ip default-gateway 10.10.10.2

8) 스위치가 기본 게이트웨이를 ping할 수 있는지 확인

SW1#ping 10.10.10.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.2, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = (1 / 2 / 8 ms)

9) 장치를 연결하는 인터페이스에 적절한 설명 입력

R1(config)#interface FastEthernet 0/0 R1(config-if)#description Link to SW1

R2(config-if)#interface FastEthernet 0/0
R2(config-if)#description Link to SW1

SW1(config)#interface FastEthernet 0/1
SW1(config-if)#description Link to R1
SW1(config-if)#interface FastEthernet 0/2
SW1(config-if)#description Link to R2

10) SW1에서 R1로의 링크에서 속도와 이중 모드가 100 Mbps 전이중으로 자동 협상되는지 확인

SW1#show interface f0/1
FastEthernet0/1 is up, line protocol is up (connected)
Hardware is Lance, address is 00e0.8fd6.8901 (bia
00e0.8fd6.8901)
Description: Link to R1
BW 100000 Kbit, DLY 1000 usec,
reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (10 sec)
Full-duplex, 100Mb/s

11) R2로의 링크에 전이중 및 FastEthernet 속도를 수동으로 구성

SW1(config)#interface FastEthernet 0/2
SW1(config-if)#speed 100
SW1(config-if)#duplex full

R2에서 일치하는 설정을 구성하는 것을 잊지 마세요!
R2(config)#interface FastEthernet 0/0
R2(config-if)#speed 100
R2(config-if)#duplex full

12) 스위치가 실행 중인 IOS 버전은 무엇입니까?

SW1#show version
Cisco IOS Software, C2960 Software (C2960-LANBASE-M), Version 12.2(25)FX, RELEASE SOFTWARE (fc1)

CDP 구성
13) Cisco Discovery Protocol을 사용하여 직접 연결된 Cisco 이웃 확인

SW1#show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone
Device ID Local Intrfce Holdtme Capability Platform Port ID
R1 Fas 0/1 (170   R   C 2800) Fas 0/0
R2 Fas 0/2 (134   R   C 2800) Fas 0/0

14) R1이 CDP를 통해 Switch 1에 대한 정보를 발견하지 못하도록 방지

SW1(config)#interface FastEthernet 0/1
SW1(config-if)#no cdp enable

15) 전역 구성 모드에서 'no cdp run' 명령을 입력한 다음 'cdp run' 명령을 입력하여 R1의 CDP 캐시를 플러시

R1(config)#no cdp run
R1(config)#cdp run

16) R1이 CDP를 통해 SW1을 볼 수 없는지 확인

R1#show cdp neighbors
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone, D - Remote, C - CVTA, M - Two-port Mac Relay

Device ID Local Intrfce Holdtme Capability Platform Port ID R1#

스위치 문제 해결
17) show ip interface brief 명령으로 R2에 연결된 스위치 포트의 상태를 확인합니다. 상태와 프로토콜이 up/up으로 표시되어야 합니다.

SW1#show ip interface brief Interface Protocol
Vlan1 10.10.10.10
FastEthernet0/1
FastEthernet0/2

IP-Address
unassigned
unassigned

OK? Method Status
YES manual up up
YES unset up up
YES unset up up

18) R2에 연결된 인터페이스를 종료하고 show ip interface brief 명령을 다시 실행합니다. 상태와 프로토콜이 administratively down/down으로 표시되어야 합니다.

SW1(config)#interface FastEthernet 0/2
SW1(config-if)#shutdown
*Mar 1 00:44:34.212: %LINK-5-CHANGED: Interface
FastEthernet0/2, changed state to administratively down
*Mar 1 00:44:35.219: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/2, changed state to down

SW1(config-if)#do show ip interface brief
Interface IP-Address OK? Method Status
Protocol
Vlan1 10.10.10.10 YES manual up up
FastEthernet0/1 unassigned YES unset up up
FastEthernet0/2 unassigned YES unset administratively down down

19) 인터페이스를 다시 활성화합니다. 속도와 이중 설정을 확인합니다.

SW1(config)#interface FastEthernet 0/2
SW1(config-if)#no shutdown
SW1(config-if)#
*Mar 1 00:45:52.637: %LINK-3-UPDOWN: Interface
FastEthernet0/2, changed state to up
*Mar 1 00:45:53.644: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/2, changed state to up

SW1#sh interface f0/2
FastEthernet0/2 is up, line protocol is up (connected)
Hardware is Lance, address is 00e0.8fd6.8902 (bia 00e0.8fd6.8902)
BW 100000 Kbit, DLY 1000 usec,
reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (10 sec)
Full-duplex, 100Mb/s

20) Switch 1에서 이중 모드를 반이중으로 설정합니다. R2의 설정은 그대로 둡니다.

SW1(config-if)#duplex half
SW1(config-if)#
%LINK-5-CHANGED: Interface FastEthernet0/2, changed state to down
%LINEPROTO-5-UPDOWN: Line protocol on Interface
FastEthernet0/2, changed state to down

21) 인터페이스의 상태를 확인합니다.

인터페이스는 down/down 상태입니다. 트래픽을 전달하지 않을 것입니다.
SW1#show ip interface brief
Interface IP-Address OK? Method Status Protocol
FastEthernet0/1 unassigned YES manual up up
FastEthernet0/2 unassigned YES manual down down

22) 이중 모드를 다시 전이중으로 설정합니다.

SW1(config)#int f0/2
SW1(config-if)#duplex full
SW1(config-if)#
%LINK-5-CHANGED: Interface FastEthernet0/2, changed state to up
%LINEPROTO-5-UPDOWN: Line protocol on Interface
FastEthernet0/2, changed state to up

23) 속도를 10 Mbps로 설정합니다.

SW1(config)#int f0/2
SW1(config-if)#speed 10
SW1(config-if)#
%LINK-5-CHANGED: Interface FastEthernet0/2, changed state to down
%LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/2, changed state to down

24) 인터페이스가 여전히 작동하는지 확인합니다.

SW1#show ip interface brief
Interface IP-Address OK? Method Status Protocol
Vlan1 10.10.10.10 YES manual up up
FastEthernet0/1 unassigned YES unset up up
FastEthernet0/2 unassigned YES unset down down

인터페이스 상태는 down/down입니다.

25) R2에서 인터페이스가 작동하는지 확인합니다. 인터페이스의 상태는 어떻습니까?

R2#show ip interface brief
Interface IP-Address
FastEthernet0/0 10.10.10.2

R2의 인터페이스 상태는 up/down입니다.


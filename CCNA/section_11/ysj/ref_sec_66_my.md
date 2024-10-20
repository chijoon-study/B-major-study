
# 11 Cisco 장치 기능 - 실습 연습

이 실습은 Cisco IOS 스위치의 MAC 주소 테이블과 Cisco IOS 라우터의 라우팅 테이블을 탐구합니다.

이 실습은 Cisco 장치 기능에 대한 안내된 연습입니다. 여기에 있는 모든 명령을 아직 이해하지 못하더라도 걱정하지 마세요 - 과정의 나머지 부분을 진행하면서 더 자세히 다룰 것입니다.

## 실습 토폴로지
[이미지]

## 시작 구성 로드하기

Packet Tracer에서 '11 Cisco Device Functions.pkt' 파일을 열어 실습을 로드하세요.
이는 각 라우터를 10.10.10.0/24 네트워크의 IP 주소로 미리 구성합니다.

## 스위치 MAC 주소 테이블 확인하기

1) R1에서 R4까지의 라우터에 로그인하고 10.10.10.0/24 네트워크에 구성된 인터페이스를 확인하세요.

```
R1#show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0 10.10.10.1 YES manual up up
GigabitEthernet0/1 unassigned YES unset administratively down down 
GigabitEthernet0/2 unassigned YES unset administratively down down 
Vlan1 unassigned YES unset administratively down down

R2#show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0 10.10.10.2 YES manual up up
GigabitEthernet0/1 unassigned YES unset administratively down down
GigabitEthernet0/2 unassigned YES unset administratively down down
Vlan1 unassigned YES unset administratively down down

R3#show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0 unassigned YES unset administratively down down
GigabitEthernet0/1 10.10.10.3 YES manual up up
GigabitEthernet0/2 unassigned YES unset administratively down down
Vlan1 unassigned YES unset administratively down down

R4#show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0 10.10.10.4 YES manual up up
GigabitEthernet0/1 unassigned YES unset administratively down down 
GigabitEthernet0/2 unassigned YES unset administratively down down 
Vlan1 unassigned YES unset administratively down down
```

R1, R2, R4는 GigabitEthernet0/0을 사용하고, R3는 GigabitEthernet0/1을 사용합니다.

2) 이 인터페이스들의 MAC 주소를 기록하세요.

```
R1#show interface gig0/0
GigabitEthernet0/0 is up, line protocol is up (connected) 
Hardware is CN Gigabit Ethernet, address is 0090.2b82.ab01 (bia 0090.2b82.ab01)

R2#show interface gig0/0
GigabitEthernet0/0 is up, line protocol is up (connected) 
Hardware is CN Gigabit Ethernet, address is 0060.2fb3.9152 (bia 0060.2fb3.9152)

R3#show interface gig0/1 
GigabitEthernet0/1 is up, line protocol is up (connected) 
Hardware is CN Gigabit Ethernet, address is 0001.9626.8970 (bia 0001.9626.8970)

R4#show interface gig0/0
GigabitEthernet0/0 is up, line protocol is up (connected) 
Hardware is CN Gigabit Ethernet, address is 00d0.9701.02a9 (bia 00d0.9701.02a9)
```

**참고: 실습에서의 MAC 주소는 다를 수 있습니다.**

3) R1에서 R2, R3, R4로 ping을 보내 라우터 간 연결을 확인하세요.

- (`enable` 키워드 사용해서 특권? 더 높은 권한 프롬프트로 이동)

```
R1#ping 10.10.10.2
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.2, timeout is 2 seconds:
.!!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 0/0/3 ms

R1#ping 10.10.10.3
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.3, timeout is 2 seconds:
.!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 0/0/1 ms

R1#ping 10.10.10.4
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.4, timeout is 2 seconds:
.!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 0/0/1 ms
```

4) R2에서 R3와 R4로 ping을 보내세요.

```
R2#ping 10.10.10.3
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.3, timeout is 2 seconds:
.!!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 0/0/1 ms

R2#ping 10.10.10.4
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.4, timeout is 2 seconds:
.!!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 0/0/1 ms
```

5) SW1에서 동적으로 학습된 MAC 주소를 보고 라우터의 MAC 주소가 예상된 포트를 통해 도달 가능한지 확인하세요. 테이블의 다른 MAC 주소는 무시하세요.

```
SW1#show mac address-table dynamic
Mac Address Table

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    0001.9626.8970    DYNAMIC     Fa0/24
   1    000c.cf84.8418    DYNAMIC     Fa0/24
   1    0060.2fb3.9152    DYNAMIC     Fa0/2
   1    0090.2b82.ab01    DYNAMIC     Fa0/1
   1    00d0.9701.02a9    DYNAMIC     Fa0/24
```

6) SW2에서 반복하세요.

```
SW2#show mac address-table dynamic 
Mac Address Table

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    0001.9626.8970    DYNAMIC     Fa0/3
   1    000b.be53.6418    DYNAMIC     Fa0/24
   1    0060.2fb3.9152    DYNAMIC     Fa0/24
   1    0090.2b82.ab01    DYNAMIC     Fa0/24
   1    00d0.9701.02a9    DYNAMIC     Fa0/4
```


7) SW1의 동적 MAC 주소 테이블을 지우세요.

```
SW1#clear mac address-table dynamic
```

8) SW1의 동적 MAC 주소 테이블을 보여주세요. MAC 주소가 보이나요? 왜 그런가요?

- (내가 하면 이거 지워진 버전으로 아무것도 없이 보임.)

```
SW1#show mac address-table dynamic 
Mac Address Table

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    0001.9626.8970    DYNAMIC     Fa0/24
   1    000c.cf84.8418    DYNAMIC     Fa0/24
   1    0060.2fb3.9152    DYNAMIC     Fa0/2
   1    0090.2b82.ab01    DYNAMIC     Fa0/1
   1    00d0.9701.02a9    DYNAMIC     Fa0/24
```

실제 네트워크의 장치들은 자주 트래픽을 보내는 경향이 있어 MAC 주소 테이블이 업데이트됩니다(Packet Tracer에서는 더 적은 항목을 볼 수 있습니다).

스위치는 주기적으로 오래된 항목을 삭제합니다.

## 라우팅 테이블 검사하기

1) R1의 라우팅 테이블을 보세요. 어떤 경로가 있고 왜 그런가요?

```
R1#show ip route

Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
C        10.10.10.0/24 is directly connected, GigabitEthernet0/0
L        10.10.10.1/32 is directly connected, GigabitEthernet0/0
```

라우터는 10.10.10.0/24 네트워크에 대한 연결된 경로와 10.10.10.1/32에 대한 로컬 경로를 가지고 있습니다. 이 경로들은 GigabitEthernet0/0 인터페이스에 IP 주소 10.10.10.1/24가 구성되었을 때 자동으로 생성되었습니다.

2) GigabitEthernet0/1 인터페이스에 IP 주소 10.10.20.1/24를 구성하세요.

- (`config` 프롬프트로 들어가기 위한 키워드)
      - (`enable` -> `config t`)

```
R1(config)#interface GigabitEthernet 0/1
R1(config-if)#ip address 10.10.20.1 255.255.255.0
R1(config-if)#no shutdown
```

- (ip address 10.10.20.1 255.255.255.0 해석?)
      - ip address 할당
      - 주소: 10.10.20.1 
      - 서브넷: 255.255.255.0

3) 지금 라우팅 테이블에는 어떤 경로가 있나요?

```
R1#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
C        10.10.10.0/24 is directly connected, GigabitEthernet0/0
L        10.10.10.1/32 is directly connected, GigabitEthernet0/0
C        10.10.20.0/24 is directly connected, GigabitEthernet0/1
L        10.10.20.1/32 is directly connected, GigabitEthernet0/1
```

- (ip 경로 추가된 모습 확인 가능)
      - 아마 보면 C가 직접 연결된 범위, L은 직접 연결된 Host

라우터는 두 인터페이스에 대한 경로를 가지고 있으며 10.10.10.0/24와 10.10.20.0/24 네트워크의 호스트 간 트래픽을 라우팅할 수 있습니다.

4) 10.10.30.0/24에 대한 정적 경로를 다음 홉 주소 10.10.10.2로 구성하세요.

```
R1(config)#ip route 10.10.30.0 255.255.255.0 10.10.10.2
```

- (위에 키워드 참고해서 똑같이)

5) 지금 라우팅 테이블에는 어떤 경로가 있나요?

```
R1(config)#do show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
C        10.10.10.0/24 is directly connected, GigabitEthernet0/0
L        10.10.10.1/32 is directly connected, GigabitEthernet0/0
C        10.10.20.0/24 is directly connected, GigabitEthernet0/1
L        10.10.20.1/32 is directly connected, GigabitEthernet0/1
S        10.10.30.0/24 [1/0] via 10.10.10.2
```
라우터에는 로컬로 연결된 네트워크에 대한 경로가 있으며 10.10.10.2를 통해 사용할 수 있는 10.10.30.0/24에 대한 경로도 있습니다.

- (S는 static이라는데, GPT 피셜로는 자동 라우팅 프로토콜 없이 수동으로 설정하면 저렇게 뜨는듯.)

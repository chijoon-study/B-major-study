### Say no when asked if you would like to enter the initial configuration dialog on each router.
![](src/assg_1.png)
답지보면 위처럼도 뜬다는데, 난 안떠서 뭐..

### Configure hostnames on the routers according to the Lab Topology diagram.
이건 뭐 모를수가
근데 활성화 프롬프트인지 전역 설정 프롬프트인지 까먹었었음 ㅋㅋ;

### Configure IP addresses on R1 according to the Lab Topology diagram
```
R1(config)#int f0/0
R1(config-if)#ip add 10.0.0.1 255.255.255.0
R1(config-if)#no sh
```
나머지 인터페이스도 해줬습니다.

### Verify routes have been automatically added for the connected and local networks (note that local routes only appear from IOS 15)
```
R1#sh ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
```

### Do you see routes for all networks that R1 is directly connected to? Why or why not?
라우터랑 이어진 인터페이스의 주소는 안보
이유는 답지를 보니 양쪽다 up 상태여야 라우팅 테이블에 추가된다네  
하긴 down된 곳으로 트래픽을 보내면 안될테니..

### Should you be able to ping from PC1 to PC2? Verify this.
yes
R1통해서 잘 연결돼있자네

### Verify the traffic path from PC1 to PC2. Use the "tracert command.
```
C:\>tracert 10.0.2.10

Tracing route to 10.0.2.10 over a maximum of 30 hops: 

  1   1 ms      0 ms      0 ms      10.0.1.1
  2   0 ms      0 ms      0 ms      10.0.2.10

Trace complete.
```

### Should you be able to ping from PC1 to PC3? Verify this.
안되겠져

### Configure IP addresses on R2, R3 and R4 according to the Lab Topology diagram. Do not configure the Internet FastEthernet 1/1 interface on R4, Do not configure R5
노가다

### Verify PC3 can ping its default gateway at 10.1.2.1
```
C:\>ping 10.1.2.1

Pinging 10.1.2.1 with 32 bytes of data:

Reply from 10.1.2.1: bytes=32 time=1ms TTL=255
Reply from 10.1.2.1: bytes=32 time<1ms TTL=255
Reply from 10.1.2.1: bytes=32 time<1ms TTL=255
Reply from 10.1.2.1: bytes=32 time<1ms TTL=255

Ping statistics for 10.1.2.1:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 1ms, Average = 0ms
```

### Configure static routes on R1, R2, R3 and R4 to allow connectivity between all their subnets. Use /24 prefixes for each network.
노가다

### Verify connectivity between PC1, PC2 and PC3.
```
C:\>ping 10.0.2.10

Pinging 10.0.2.10 with 32 bytes of data:

Reply from 10.0.2.10: bytes=32 time<1ms TTL=127
Reply from 10.0.2.10: bytes=32 time<1ms TTL=127
Reply from 10.0.2.10: bytes=32 time=1ms TTL=127
Reply from 10.0.2.10: bytes=32 time=1ms TTL=127

Ping statistics for 10.0.2.10:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 1ms, Average = 0ms

C:\>tracert 10.0.2.10

Tracing route to 10.0.2.10 over a maximum of 30 hops: 

  1   1 ms      0 ms      0 ms      10.0.1.1
  2   0 ms      0 ms      0 ms      10.0.2.10

Trace complete.
```

```
C:\>ping 10.1.2.10

Pinging 10.1.2.10 with 32 bytes of data:

Reply from 10.1.2.10: bytes=32 time<1ms TTL=124
Reply from 10.1.2.10: bytes=32 time=12ms TTL=124
Reply from 10.1.2.10: bytes=32 time<1ms TTL=124
Reply from 10.1.2.10: bytes=32 time<1ms TTL=124

Ping statistics for 10.1.2.10:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 12ms, Average = 3ms
```

### Verify the path traffic takes from PC1 to PC3.
```
C:\>tracert 10.1.2.10

Tracing route to 10.1.2.10 over a maximum of 30 hops: 

  1   0 ms      0 ms      0 ms      10.0.1.1
  2   0 ms      0 ms      0 ms      10.0.0.2
  3   0 ms      0 ms      0 ms      10.1.0.1
  4   0 ms      0 ms      0 ms      10.1.1.1
  5   0 ms      1 ms      0 ms      10.1.2.10

Trace complete.
```

### Remove all the static routes on R1
```
R1(config)#no ip route 10.1.0.0 255.255.255.0 10.0.0.2
R1(config)#no ip route 10.1.1.0 255.255.255.0 10.0.0.2
R1(config)#no ip route 10.1.2.0 255.255.255.0 10.0.0.2
R1(config)#no ip route 10.1.3.0 255.255.255.0 10.0.0.2
```

### Verify that PC1 loses connectivity to PC3
```
C:\>ping 10.1.2.10ㅔ

Pinging 10.1.2.10 with 32 bytes of data:

Reply from 10.0.1.1: Destination host unreachable.
Request timed out.
Reply from 10.0.1.1: Destination host unreachable.
Reply from 10.0.1.1: Destination host unreachable.

Ping statistics for 10.1.2.10:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
```

### Restore connectivity to all subnets with a single command on R1.
```R1(config)#ip route 10.1.0.0 255.255.0.0 10.0.0.2```

### Verify the routing table on R1 does not contain /24 routes to remote subnets.
```
R1#sh ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 7 subnets, 3 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
S       10.1.0.0/16 [1/0] via 10.0.0.2
```

### Ensure that connectivity is restored between PC1 and PC3.
```
C:\>ping 10.1.2.10

Pinging 10.1.2.10 with 32 bytes of data:

Reply from 10.1.2.10: bytes=32 time<1ms TTL=124
Reply from 10.1.2.10: bytes=32 time<1ms TTL=124
Reply from 10.1.2.10: bytes=32 time<1ms TTL=124
Reply from 10.1.2.10: bytes=32 time<1ms TTL=124

Ping statistics for 10.1.2.10:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms
```

### Configure IP addresses on R5 according to the Lab Topology diagram
노가다

### Do not add any additional routes. Does PC1 have reachability to the FastEthernet 0/0 interface on R5? If so, which path will the traffic take?
실패함
```
C:\>ping 10.1.3.2

Pinging 10.1.3.2 with 32 bytes of data:

Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 10.1.3.2:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
```
```
C:\>tracert 10.1.3.2

Tracing route to 10.1.3.2 over a maximum of 30 hops: 

  1   0 ms      0 ms      0 ms      10.0.1.1
  2   0 ms      0 ms      0 ms      10.0.0.2
  3   0 ms      0 ms      0 ms      10.1.0.1
  4   0 ms      0 ms      0 ms      10.1.1.1
  5   *         *         *         Request timed out.
```

### Ensure reachability over the shortest possible path from R5 to all directly connected networks on R1. Achieve this with a single command.
```
R5(config)#ip route 10.0.0.0 255.255.0.0 10.0.3.1
```

### Verify the path traffic takes from PC1 to the FastEthernet 0/0 interface on R5.
```
C:\>tracert 10.1.3.2

Tracing route to 10.1.3.2 over a maximum of 30 hops: 

  1   0 ms      0 ms      0 ms      10.0.1.1
  2   0 ms      0 ms      0 ms      10.0.0.2
  3   0 ms      0 ms      0 ms      10.1.0.1
  4   0 ms      0 ms      0 ms      10.1.1.1
  5   0 ms      0 ms      0 ms      10.1.3.2

Trace complete.
```

### Verify the path the return traffic takes from R5 to PC1.
```
R5#trace 10.0.1.10
Type escape sequence to abort.
Tracing the route to 10.0.1.10

  1   10.0.3.1        0 msec    0 msec    0 msec    
  2   10.0.1.10       0 msec    0 msec    0 msec    
```

### Ensure that traffic between PC1 and the FastEthernet 0/0 interface on R5 takes the most direct path in both directions.
```
R1(config)#ip route 10.1.3.0 255.255.255.0 10.0.3.2
```

### Verify that traffic between PC1 and the FastEthernet 0/0 interface on R5 takes the most direct path in both directions.
```
R5(config)#do trace 10.0.1.10
Type escape sequence to abort.
Tracing the route to 10.0.1.10

  1   10.0.3.1        0 msec    0 msec    0 msec    
  2   10.0.1.10       0 msec    0 msec    0 msec    
```

### Configure an IP address on the Internet FastEthernet 1/1 interface on R4 according to the lab topology diagram.
```
R4(config)#int f1/1
R4(config-if)#ip add 203.0.113.1 255.255.255.0
R4(config-if)#no sh
```

### Ensure that all PCs have a route out to the internet through the Internet Service Provider connection on R4. (Note that the lab does not actually have Internet connectivity.)
```
ip route 0.0.0.0 0.0.0.0 hop
```
### Traffic from PC1 and PC2 going to the internet should be load balanced over R2 and R5.
```
R1(config)#ip route 0.0.0.0 0.0.0.0 10.0.3.2
```
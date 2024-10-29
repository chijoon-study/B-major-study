### Enter the commands below on each router to provision a basic RIPv1 configuration and enable RIP on every interface.
```
router rip
network 10.0.0.0
no auto-summary
```
### Debug the routing protocol updates on R1 with the `debug ip rip` command. Observe the updates being sent and received. What kind of traffic is used (unicast, broadcast or multicast)?
```
R1#RIP: received v1 update from 10.0.3.2 on FastEthernet1/1
      10.1.1.0 in 2 hops
      10.1.2.0 in 2 hops
      10.1.3.0 in 1 hops

R1#RIP: received v1 update from 10.0.0.2 on FastEthernet0/0
      10.1.0.0 in 1 hops
      10.1.1.0 in 2 hops
      10.1.2.0 in 3 hops

R1#RIP: sending  v1 update to 255.255.255.255 via FastEthernet0/0 (10.0.0.1)
RIP: build update entries
      network 10.0.1.0 metric 1
      network 10.0.2.0 metric 1
      network 10.0.3.0 metric 1
      network 10.1.2.0 metric 3
      network 10.1.3.0 metric 2
RIP: sending  v1 update to 255.255.255.255 via FastEthernet0/1 (10.0.1.1)
RIP: build update entries
      network 10.0.0.0 metric 1
      network 10.0.2.0 metric 1
      network 10.0.3.0 metric 1
      network 10.1.0.0 metric 2
      network 10.1.1.0 metric 3
      network 10.1.2.0 metric 3
      network 10.1.3.0 metric 2
RIP: sending  v1 update to 255.255.255.255 via FastEthernet1/0 (10.0.2.1)
RIP: build update entries
      network 10.0.0.0 metric 1
      network 10.0.1.0 metric 1
      network 10.0.3.0 metric 1
      network 10.1.0.0 metric 2
      network 10.1.1.0 metric 3
      network 10.1.2.0 metric 3
      network 10.1.3.0 metric 2
RIP: sending  v1 update to 255.255.255.255 via FastEthernet1/1 (10.0.3.1)
RIP: build update entries
      network 10.0.0.0 metric 1
      network 10.0.1.0 metric 1
      network 10.0.2.0 metric 1
      network 10.1.0.0 metric 2
```
브로드캐스트
### Enter the commands below to enable RIPv2 on every router.
```
router rip
version 2
```
### What kind of traffic is used for the updates now?
```
R1#debug ip rip
RIP protocol debugging is on
R1#RIP: sending  v2 update to 224.0.0.9 via FastEthernet0/0 (10.0.0.1)
RIP: build update entries
      10.0.1.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.2.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.3.0/24 via 0.0.0.0, metric 1, tag 0
      10.1.2.0/24 via 0.0.0.0, metric 3, tag 0
      10.1.3.0/24 via 0.0.0.0, metric 2, tag 0
RIP: sending  v2 update to 224.0.0.9 via FastEthernet0/1 (10.0.1.1)
RIP: build update entries
      10.0.0.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.2.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.3.0/24 via 0.0.0.0, metric 1, tag 0
      10.1.0.0/24 via 0.0.0.0, metric 2, tag 0
      10.1.1.0/24 via 0.0.0.0, metric 3, tag 0
      10.1.2.0/24 via 0.0.0.0, metric 3, tag 0
      10.1.3.0/24 via 0.0.0.0, metric 2, tag 0
RIP: sending  v2 update to 224.0.0.9 via FastEthernet1/0 (10.0.2.1)
RIP: build update entries
      10.0.0.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.1.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.3.0/24 via 0.0.0.0, metric 1, tag 0
      10.1.0.0/24 via 0.0.0.0, metric 2, tag 0
      10.1.1.0/24 via 0.0.0.0, metric 3, tag 0
      10.1.2.0/24 via 0.0.0.0, metric 3, tag 0
      10.1.3.0/24 via 0.0.0.0, metric 2, tag 0
RIP: sending  v2 update to 224.0.0.9 via FastEthernet1/1 (10.0.3.1)
RIP: build update entries
      10.0.0.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.1.0/24 via 0.0.0.0, metric 1, tag 0
      10.0.2.0/24 via 0.0.0.0, metric 1, tag 0
      10.1.0.0/24 via 0.0.0.0, metric 2, tag 0

R1#RIP: received v2 update from 10.0.3.2 on FastEthernet1/1
      10.1.1.0/24 via 0.0.0.0 in 2 hops
      10.1.2.0/24 via 0.0.0.0 in 2 hops
      10.1.3.0/24 via 0.0.0.0 in 1 hops
```
멀티캐스트
### Turn off all debugging on R1.
```
undebug all
```
### Check that RIP routes have been added to R1 and it has a route to every subnet in the lab.
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

     10.0.0.0/8 is variably subnetted, 12 subnets, 2 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
R       10.1.0.0/24 [120/1] via 10.0.0.2, 00:00:26, FastEthernet0/0
R       10.1.1.0/24 [120/2] via 10.0.0.2, 00:00:26, FastEthernet0/0
                    [120/2] via 10.0.3.2, 00:00:10, FastEthernet1/1
R       10.1.2.0/24 [120/2] via 10.0.3.2, 00:00:10, FastEthernet1/1
R       10.1.3.0/24 [120/1] via 10.0.3.2, 00:00:10, FastEthernet1/1
```
### Why are there two routes to the 10.1.1.0/24 network in the routing table?
metric이 같아서
### View the RIP database on R1.
```
R1#sh ip rip data
10.0.0.0/24    auto-summary
10.0.0.0/24    directly connected, FastEthernet0/0
10.0.1.0/24    auto-summary
10.0.1.0/24    directly connected, FastEthernet0/1
10.0.2.0/24    auto-summary
10.0.2.0/24    directly connected, FastEthernet1/0
10.0.3.0/24    auto-summary
10.0.3.0/24    directly connected, FastEthernet1/1
10.1.0.0/24    auto-summary
10.1.0.0/24
    [1] via 10.0.0.2, 00:00:10, FastEthernet0/0
10.1.1.0/24    auto-summary
10.1.1.0/24
    [2] via 10.0.0.2, 00:00:10, FastEthernet0/0    [2] via 10.0.3.2, 00:00:22, FastEthernet1/1
10.1.2.0/24    auto-summary
10.1.2.0/24
    [2] via 10.0.3.2, 00:00:22, FastEthernet1/1
10.1.3.0/24    auto-summary
10.1.3.0/24
    [1] via 10.0.3.2, 00:00:22, FastEthernet1/1
```
### Enter the commands below on each router to provision a basic OSPF configuration and enable OSPF on every interface.
```
router ospf 1
network 10.0.0.0 0.255.255.255 area 0
```
network 명령어가 뭔지는 모르겠음..
### Give OSPF time to converge. Are RIP routes included in the routing table on R1 now? Why or why not?
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

     10.0.0.0/8 is variably subnetted, 12 subnets, 2 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
O       10.1.0.0/24 [110/2] via 10.0.0.2, 00:00:12, FastEthernet0/0
O       10.1.1.0/24 [110/3] via 10.0.0.2, 00:00:02, FastEthernet0/0
O       10.1.2.0/24 [110/4] via 10.0.0.2, 00:00:02, FastEthernet0/0
O       10.1.3.0/24 [110/13] via 10.0.0.2, 00:00:02, FastEthernet0/0
```
ospf의 AD가 더 작아서 대체됨
### Why is there now only one route to the 10.1.1.0/24 network?
```
R5#sh run | section interface
interface FastEthernet0/0
 bandwidth 10000
 ip address 10.1.3.2 255.255.255.0
 duplex auto
 speed auto
interface FastEthernet0/1
 bandwidth 10000
 ip address 10.0.3.2 255.255.255.0
 duplex auto
```
대역폭 때문에
### Disable interface FastEthernet 0/0 on R2. What do you expect to happen to R1's routing table?
```
R2(config-router)#exit
R2(config)#int fa0/0
R2(config-if)#sh

R2(config-if)#
%LINK-5-CHANGED: Interface FastEthernet0/0, changed state to administratively down

%LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/0, changed state to down

02:20:48: %OSPF-5-ADJCHG: Process 1, Nbr 10.0.3.1 on FastEthernet0/0 from FULL to DOWN, Neighbor Down: Interface down or det
```
대체 되겠지 R5통해서 가는거로
### Verify your expected changes to R1's routing table.
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

     10.0.0.0/8 is variably subnetted, 10 subnets, 2 masks
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
O       10.1.0.0/24 [110/22] via 10.0.3.2, 00:00:25, FastEthernet1/1
O       10.1.1.0/24 [110/21] via 10.0.3.2, 00:00:25, FastEthernet1/1
O       10.1.2.0/24 [110/21] via 10.0.3.2, 00:00:25, FastEthernet1/1
O       10.1.3.0/24 [110/20] via 10.0.3.2, 00:00:25, FastEthernet1/1
```
### Aside from the next hop address, what else has changed on the routing table?
metric이 커짐
### View the OSPF database on R1 with the `show ip ospf database` command. What is different between it and the RIP database? Why?
```
R1#sh ip ospf database
            OSPF Router with ID (10.0.3.1) (Process ID 1)

                Router Link States (Area 0)

Link ID         ADV Router      Age         Seq#       Checksum Link count
10.1.1.2        10.1.1.2        244         0x80000004 0x003cb6 2
10.1.3.2        10.1.3.2        244         0x80000004 0x00844e 2
203.0.113.1     203.0.113.1     244         0x80000005 0x00df85 3
10.0.3.1        10.0.3.1        140         0x80000007 0x00775c 3
10.1.0.2        10.1.0.2        140         0x80000005 0x00c15c 1

                Net Link States (Area 0)
Link ID         ADV Router      Age         Seq#       Checksum
10.1.0.1        10.1.1.2        256         0x80000001 0x002bfb
10.0.3.2        10.1.3.2        251         0x80000001 0x00150a
10.1.1.1        203.0.113.1     244         0x80000001 0x007e46
10.1.3.1        203.0.113.1     244         0x80000002 0x00704f
```
ospf는 링크상태 라우팅 프로토콜이라
속한 네트워크의 모든 링크의 정보를 가지고있음 

### Enter the command below to remove OSPF on every router
```
no router ospf 1
```
### Will R1 still have connectivity to R4?
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

     10.0.0.0/8 is variably subnetted, 10 subnets, 2 masks
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
R       10.1.0.0/24 [120/3] via 10.0.3.2, 00:00:14, FastEthernet1/1
R       10.1.1.0/24 [120/2] via 10.0.3.2, 00:00:14, FastEthernet1/1
R       10.1.2.0/24 [120/2] via 10.0.3.2, 00:00:14, FastEthernet1/1
R       10.1.3.0/24 [120/1] via 10.0.3.2, 00:00:14, FastEthernet1/1
```
rip로 대체됨

### What is the metric to the 10.1.1.0/24 network on R1?
hop count 2

### Why is there only one route on R1 to the 10.1.1.0/24 network now?
R2로 가는 인터페이스가 닫혀있어서

### Make the required change so that there are two routes to the 10.1.1.0/24 network in the routing table on R1.
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

     10.0.0.0/8 is variably subnetted, 12 subnets, 2 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
R       10.1.0.0/24 [120/1] via 10.0.0.2, 00:00:12, FastEthernet0/0
R       10.1.1.0/24 [120/2] via 10.0.3.2, 00:00:11, FastEthernet1/1
                    [120/2] via 10.0.0.2, 00:00:12, FastEthernet0/0
R       10.1.2.0/24 [120/2] via 10.0.3.2, 00:00:11, FastEthernet1/1
R       10.1.3.0/24 [120/1] via 10.0.3.2, 00:00:11, FastEthernet1/1
```
R2에서 `no sh`해줌

### Enter the commands below on each router to provision a basic EIFRP configuration and enable EIGRP on every interface
```
router eigrp 100
no auto-summary
network 10.0.0.0 0.255.255.255
```
### What changes do you expect to see in the routing tables? Why?
EIGRP로 대체 되겠지 AD가 더 낮으니까

### Verify the changes to the routing table on R1.
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

     10.0.0.0/8 is variably subnetted, 12 subnets, 2 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
D       10.1.0.0/24 [90/30720] via 10.0.0.2, 00:00:47, FastEthernet0/0
D       10.1.1.0/24 [90/33280] via 10.0.0.2, 00:00:40, FastEthernet0/0
D       10.1.2.0/24 [90/35840] via 10.0.0.2, 00:00:29, FastEthernet0/0
D       10.1.3.0/24 [90/261120] via 10.0.3.2, 00:00:35, FastEthernet1/1
```
### What is the metric to the 10.1.1.0/24 network on R1?
33280

### Why is there only one route to the 10.1.1.0/24 network on R1?
EIGRP도 대역폭 고려하니까 R5거쳐서 가는건 비효율적인걸 아는거지

### Disable RIP and EIGRP on R5 with the commands below.
```
R5(config)#no router rip
R5(config)#no router eigrp 100
```
### Configure the network so that there is still connectivity between all subnets if the link between R1 and R2 goes down. Accomplish this with six commands. Do not enable EIGRP on R5 but note that the routing protocol is expected to be enabled there in the future.
R5 거쳐서가는 정적라우팅 설정해줌

### What changes do you expect to see to the routing table on R1?
백업 라우팅 경로 추가돼있겠지
### Verify the changes to the routing table on R1.
```
R1#sh ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
D - EIGRP, EX - EIGRP external, 0 - OSPF, IA - OSPF inter area
N1 - OSPE NSSA external type 1, N2 - OSPE NSSA external type 2
El - OSPF external type 1, E2 - OSPF external type 2
1 - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, 12 - IS-IS level-2
ia - IS-IS inter area, * - candidate default, U - per-user static route
• - ODR, P - periodic downloaded static route, H - NHRP, 1 - LISP
+ - replicated route, % - next hop override

Gateway of last resort is not set

10.0.0.018 is variably subnetted, 13 subnets, 3 masks C 10.0.0.0/24 is directly connected, FastEthernet0/0
L 10.0.0.1/32 is directly connected, FastEtherneto/0
C 10.0.1.0/24 is directly connected, FastEthernet0/1
L 10.0.1.1/32 is directly connected, FastEthernet0/1 c 10.0.2.0/24 is directly connected, FastEthernet1/0
L 10.0.2.1/32 is directly connected, FastEthernet1/0
C 10.0.3.0/24 is directly connected, FastEthernet1/1
L 10.0.3.1/32 is directly connected, FastEthernet1/1
s 10.1.0.0/16 [95/0] via 10.0.3.2
D 10.1.0.0/24
[90/307201 via 10.0.0.2, 00:04:48, FastEtherneto/0
D 10.1.1.0/24 [90/332801 via 10.0.0.2, 00:04:45, FastEthernet0/0
D 10.1.2.0/24
[90/358401 via 10.0.0.2, 00:04:41, FastEthernet0/0
D 10.1.3.0/24
[90/2662401 via 10.0.0.2, 00:03:02, FastEthernet0/0
```
### Verify that traffic from PC1 to PC3 still goes via R2.
```
C:\>tracert 10.1.2.10
Tracing route to 10.1.2.10 over a maximum of 30 hops:
1 1 ms 0 ms 1 ms 10.0.1.1
2 0 ms 3 ms 0 ms 10.0.0.2
3 1 ms 0 ms 0 ms 10.1.0.1
4 0 ms 1 ms 0 ms 10.1.1.1
5 * 0 ms 0 ms 10.1.2.10

Trace complete.
```
### Shut down interface FastEthernet 0/0 on R2.
```
R2 (config)#interface f0/0
R2 (config-if) #shutdown
```
### What changes do you expect to see on R1's routing table?
EIGRP 라우팅 경로 사라지고 백업 라우팅 경로가 남아있겠지

### Verify the changes to the routing table on R1.
```
sh ip route
```
### Verify connectivity between PC1 and PC3.
```
ping 10.1.2.10
```
### Verify the traffic goes via R5.
```
tracert 10.1.2.10
```
### Bring interface FastEthernet 0/0 on R2 back up.
`no sh` 해줌 
### Enter the commands below on R5 to provision a basic EIGRP configuration and enable EIGRP on every interface.
```
R5(config)#router eigrp 100
R5(config-router)#no auto
R5(config-router)#net 10.0.0.0 0.255.255.255
```
### Configure loopback interface 0 on each router. Assign the IP address 192.168.0.x/32, where 'x' is the router number (for example 192.168.0.3/32 on R3.)
```
interface loopback0
ip add 192.168.0.{router number} 255.255.255.255
```
### Is there connectivity to the loopback interfaces from the PCs? Why or why not?
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

     10.0.0.0/8 is variably subnetted, 12 subnets, 2 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
D       10.1.0.0/24 [90/30720] via 10.0.0.2, 00:19:53, FastEthernet0/0
D       10.1.1.0/24 [90/33280] via 10.0.0.2, 00:19:46, FastEthernet0/0
D       10.1.2.0/24 [90/35840] via 10.0.0.2, 00:19:35, FastEthernet0/0
D       10.1.3.0/24 [90/261120] via 10.0.3.2, 00:10:37, FastEthernet1/1
     192.168.0.0/32 is subnetted, 5 subnets
C       192.168.0.1/32 is directly connected, Loopback0
```
loopback 인터페이스는 뭐 연결성은 없다고하지 않았나 

답지보니까 저거때문은 아니고 라우팅 테이블에 없어서라는데, 다음 질문 명령어 보면 network 명령어가 뭔가 있는데.. 잘 모르겠다

### Enter the commands below on each router to include the loopback interfaces in EIGRP.
```
router eigrp 100
network 192.168.0.0 0.0.0.255
```

### Verify the loopback interfaces are in the routing table on R1.
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

     10.0.0.0/8 is variably subnetted, 12 subnets, 2 masks
C       10.0.0.0/24 is directly connected, FastEthernet0/0
L       10.0.0.1/32 is directly connected, FastEthernet0/0
C       10.0.1.0/24 is directly connected, FastEthernet0/1
L       10.0.1.1/32 is directly connected, FastEthernet0/1
C       10.0.2.0/24 is directly connected, FastEthernet1/0
L       10.0.2.1/32 is directly connected, FastEthernet1/0
C       10.0.3.0/24 is directly connected, FastEthernet1/1
L       10.0.3.1/32 is directly connected, FastEthernet1/1
D       10.1.0.0/24 [90/30720] via 10.0.0.2, 00:19:53, FastEthernet0/0
D       10.1.1.0/24 [90/33280] via 10.0.0.2, 00:19:46, FastEthernet0/0
D       10.1.2.0/24 [90/35840] via 10.0.0.2, 00:19:35, FastEthernet0/0
D       10.1.3.0/24 [90/261120] via 10.0.3.2, 00:10:37, FastEthernet1/1
     192.168.0.0/32 is subnetted, 5 subnets
C       192.168.0.1/32 is directly connected, Loopback0
D       192.168.0.2/32 [90/156160] via 10.0.0.2, 00:00:40, FastEthernet0/0
D       192.168.0.3/32 [90/158720] via 10.0.0.2, 00:00:27, FastEthernet0/0
D       192.168.0.4/32 [90/161280] via 10.0.0.2, 00:00:18, FastEthernet0/0
D       192.168.0.5/32 [90/386560] via 10.0.3.2, 00:00:32, FastEthernet1/1
```
### Verify connectivity from PC1 to the loopback interface on R5.
```
ping 192.168.0.5
```
통신 됨

### Enter the command below to verify that R1 has established EIGRP adjacencies with R2 and R5.
```
R1#show ip eigrp neighbors
IP-EIGRP neighbors for process 100
H   Address         Interface      Hold Uptime    SRTT   RTO   Q   Seq
                                   (sec)          (ms)        Cnt  Num
0   10.0.0.2        Fa0/0          14   00:21:08  40     1000  0   24
1   10.0.3.2        Fa1/1          11   00:11:52  40     1000  0   29
```
### Verify that traffic from R5 to the directly connected interfaces on R1 goes via the FastEthernet 0/1 interface.
```
R5#sh ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 10 subnets, 2 masks
D       10.0.0.0/24 [90/261120] via 10.0.3.1, 00:12:22, FastEthernet0/1
D       10.0.1.0/24 [90/261120] via 10.0.3.1, 00:12:22, FastEthernet0/1
D       10.0.2.0/24 [90/261120] via 10.0.3.1, 00:12:22, FastEthernet0/1
```
### Enter the commands below to configure the loopback interface and the link to R5 as passive interfaces on R1.
```
R1(config)#router eigrp 100
R1(config-router)#passive-interface loopback0
R1(config-router)#passive fa1/1
```
### What changes do you expect to see in the routing table on R5 and why?
R1 통해서 가는 경로가 사라지겠지

### Verify the expected changes to the routing table on R5.
```
R5#sh ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/8 is variably subnetted, 10 subnets, 2 masks
D       10.0.0.0/24 [90/266240] via 10.1.3.1, 00:14:15, FastEthernet0/0
D       10.0.1.0/24 [90/268800] via 10.1.3.1, 00:14:15, FastEthernet0/0
D       10.0.2.0/24 [90/268800] via 10.1.3.1, 00:14:15, FastEthernet0/0
C       10.0.3.0/24 is directly connected, FastEthernet0/1
L       10.0.3.2/32 is directly connected, FastEthernet0/1
D       10.1.0.0/24 [90/263680] via 10.1.3.1, 00:14:15, FastEthernet0/0
D       10.1.1.0/24 [90/261120] via 10.1.3.1, 00:14:15, FastEthernet0/0
D       10.1.2.0/24 [90/261120] via 10.1.3.1, 00:14:15, FastEthernet0/0
C       10.1.3.0/24 is directly connected, FastEthernet0/0
L       10.1.3.2/32 is directly connected, FastEthernet0/0
     192.168.0.0/32 is subnetted, 5 subnets
D       192.168.0.1/32 [90/394240] via 10.1.3.1, 00:04:24, FastEthernet0/0
D       192.168.0.2/32 [90/391680] via 10.1.3.1, 00:04:18, FastEthernet0/0
D       192.168.0.3/32 [90/389120] via 10.1.3.1, 00:04:05, FastEthernet0/0
D       192.168.0.4/32 [90/386560] via 10.1.3.1, 00:03:56, FastEthernet0/0
C       192.168.0.5/32 is directly connected, Loopback0
```
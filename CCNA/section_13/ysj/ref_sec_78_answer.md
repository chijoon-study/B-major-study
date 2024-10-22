## 13 시스코 문제해결 방법론 - 답변 키

이 실습은 네트워크 문제해결 능력을 테스트합니다.

**DNS 서버 연결 문제 해결**

Packet Tracer에서는 라우터가 DNS 서버가 될 수 없으므로('ip dns server' 명령을 지원하지 않음) Packet Tracer 서버 장치를 DNS 서버로 사용하고 있습니다.

1) IP 주소가 10.10.10.10인 호스트가 DNS 서버로 구성되어 'R1', 'R2', 'R3'에 대한 요청을 해결할 수 있어야 합니다. 직원들이 DNS가 작동하지 않는다고 불평했습니다.

2) R3에서 Telnet을 사용하여 10.10.10.10의 DNS 서버에서 DNS 서비스가 작동하는지 확인하십시오.

R3#telnet 10.10.10.10
Trying 10.10.10.10 ...
% Connection timed out; remote host not responding

3) DNS가 작동하지 않는 것을 확인한 후 문제를 해결하고 수정하십시오. R3가 호스트 이름으로 R1을 ping할 수 있을 때 문제가 해결된 것입니다. 문제의 원인이 하나 이상일 수 있습니다.
(DNS 서버를 클릭한 다음 '서비스' 탭을 클릭하여 서버의 DNS 구성을 확인할 수 있습니다.)

[이미지]

문제를 해결하는 방법은 여러 가지가 있습니다. 제안된 워크플로우는 아래와 같습니다.

문제를 해결할 때 처음 두 가지 질문은 다음과 같습니다:
1. 이전에 작동했습니까? 그렇다면 문제를 일으킬 수 있는 변경 사항이 있었습니까? 이는 일반적으로 원인을 가리킵니다.

이 질문은 DNS 서버가 처음으로 온라인 상태가 되었기 때문에 우리의 예시에는 특별히 유용하지 않습니다.

2. 문제가 모든 사람에게 영향을 미치나요, 아니면 특정 사용자에게만 영향을 미치나요? 한 사용자에게만 영향을 미친다면 문제가 그 사용자 쪽에 있을 가능성이 높습니다.

이 경우 문제는 모든 사용자에게 영향을 미치므로 문제는 서버 쪽이나 네트워크에 있을 가능성이 높습니다.

Telnet을 시도했을 때 오류 메시지는 '원격 호스트가 응답하지 않음'이었으므로 연결 문제로 보입니다.

R3에서 DNS 서버로 ping을 보냅니다.

R3#ping 10.10.10.10
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.10, timeout is 2 seconds:
U.U.U

Success rate is 0 percent (0/5)

ping이 네트워크 계층에서 실패하므로 이 문제를 해결할 때까지 더 높은 계층에서 DNS 서비스를 확인할 필요가 없습니다.

hop by hop으로 연결을 확인하는 대신 traceroute를 사용하여 시간을 절약할 수 있습니다.

R3#traceroute 10.10.10.10
Type escape sequence to abort.
Tracing the route to 10.10.10.10
1 10.10.20.2 0 msec 0 msec 0 msec
2 10.10.20.2 !H * !H
3 * *

traceroute가 R2까지 도달했음을 알 수 있으며, 이는 R3가 DNS 서버에 도달하기 위한 올바른 경로를 가지고 있고 문제가 R2와 DNS 서버 사이에 있을 가능성이 높다는 것을 알려줍니다.

R2는 10.10.10.0/24 네트워크에 연결된 인터페이스를 가지고 있으므로 DNS 서버로의 경로가 있는지 확인할 필요가 없습니다. 하지만 인터페이스가 작동 중인지 확인해야 합니다.

R2#sh ip int brief
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            10.10.10.2      YES NVRAM  administratively down down
FastEthernet0/1            unassigned      YES NVRAM  administratively down down
FastEthernet1/0            10.10.20.2      YES NVRAM  up                    up
FastEthernet1/1            unassigned      YES NVRAM  administratively down down
Vlan1                      unassigned      YES NVRAM  administratively down down

문제가 여기 있습니다 - DNS 서버를 향하는 FastEthernet0/0이 관리적으로 종료되어 있습니다. 이를 수정합시다.

R2(config)#interface f0/0
R2(config-if)#no shutdown

다음으로 R3에서 DNS 서버로 다시 ping을 보내 연결이 수정되었는지 확인합니다.

R3#ping 10.10.10.10
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.10, timeout is 2 seconds:
. .!!!
Success rate is 60 percent (3/5), round-trip min/avg/max = 0/0/0 ms

더 나아 보입니다 - 처음 한두 개의 ping이 떨어져도 걱정하지 마세요. ARP 캐시가 업데이트되는 동안 지연이 있을 수 있습니다. 다음으로 DNS가 작동하는지 확인합니다.

R3#ping R1
Translating "R1"...domain server (10.10.10.1)
% Unrecognized host or address or protocol not running.

오류 메시지를 자세히 읽어보면 문제를 알 수 있습니다 - R3가 10.10.10.1을 DNS 서버로 사용하고 있지만 올바른 주소는 10.10.10.10입니다.

다음으로 이를 수정합니다. 잘못된 항목을 먼저 제거하는 것을 잊지 마세요.

R3(config)#no ip name-server 10.10.10.1
R3(config)#ip name-server 10.10.10.10

그런 다음 다시 테스트합니다.

R3#ping R1
Translating "R1"...domain server (10.10.1)
% Unrecognized host or address or protocol not running.

오류 메시지가 여전히 있습니다. 우리는 연결이 있고 R3에서 DNS 서버가 올바르게 구성되어 있다는 것을 알고 있으므로 문제는 DNS 서버에 있는 것 같습니다.

10.10.10.10 호스트에서 DNS 서비스가 실행 중인지, 그리고 'R1', 'R2', 'R3'에 대한 주소 레코드가 구성되어 있는지 확인합니다.

[이미지]

주소 레코드는 있지만 DNS 서비스가 꺼져 있습니다. 다시 켭니다.

[이미지]

R3에서 다시 테스트할 시간입니다.

R3#ping R1
Translating "R1"...domain server (10.10.10.10)
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.10.10.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 0/0/4 ms

문제가 해결되었습니다.

요약하자면 문제는 다음과 같았습니다: R2의 FastEthernet0/0 포트가 종료되어 있었고, R3가 DNS 서버에 대해 잘못된 IP 주소를 사용하고 있었으며, 서버에서 DNS 서비스가 실행되지 않고 있었습니다.

실제 세계에서의 문제는 보통 이 경우처럼 세 가지 오류가 아닌 하나의 오류로 인해 발생합니다. 그러나 특히 새로운 서비스가 배포될 때는 여전히 이런 일이 발생할 수 있습니다.

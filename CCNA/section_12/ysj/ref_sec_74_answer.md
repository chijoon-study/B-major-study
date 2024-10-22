이 실습은 Cisco 라우터의 DNS 클라이언트 구성과 ARP 캐시를 탐구합니다.

## 라우터를 DNS 클라이언트로 구성

**참고:** Packet Tracer에서 라우터는 DNS 서버가 될 수 없습니다('ip dns server' 명령을 지원하지 않음). 따라서 Packet Tracer 서버 장치를 DNS 서버로 사용합니다.

IP 주소가 10.10.10.10인 호스트가 DNS 서버로 구성되어 'R1', 'R2', 'R3'에 대한 DNS 요청을 해결할 수 있습니다. 도메인 이름은 사용되지 않습니다.

1) R1, R2, R3을 10.10.10.10을 DNS 서버로 사용하도록 구성하세요. 도메인 이름이나 도메인 목록을 구성할 필요는 없습니다.

```
R1(config)#ip domain-lookup
R1(config)#ip name-server 10.10.10.10
R2(config)#ip domain-lookup
R2(config)#ip name-server 10.10.10.10
R3(config)#ip domain-lookup
R3(config)#ip name-server 10.10.10.10
```

2) R1에서 호스트 이름 'R2'와 'R3'을 사용하여 R2와 R3에 ping을 보낼 수 있는지 확인하세요(DNS 서버가 DNS 요청을 해결하는 데 시간이 걸릴 수 있습니다).

```
R1#ping R2
```

3) R3에서 호스트 이름 'R1'과 'R2'를 사용하여 R1과 R2에 ping을 보낼 수 있는지 확인하세요.

```
R3#ping R1
R3#ping R2
```

## 라우터의 ARP 캐시 검사

4) R1의 ARP 캐시에 R3에 대한 항목이 있을 것으로 예상하나요? 그 이유는 무엇인가요?

ARP 요청은 브로드캐스트 트래픽을 사용하므로 라우터에 의해 전달되지 않습니다. R1은 직접 연결된 네트워크(10.10.10.0/24)에서 본 모든 호스트에 대한 항목을 ARP 캐시에 가지게 됩니다.

R1은 10.10.20.0/24 네트워크에 직접 연결되어 있지 않으므로 10.10.20.1의 R3에 대한 항목이 ARP 캐시에 없을 것입니다.

R1은 R2의 IP 주소 10.10.10.2를 통해 R3에 도달할 수 있습니다 - 이 IP 주소는 ARP 캐시에 포함됩니다.
10.10.10.10의 DNS 서버도 R1과 동일한 IP 서브넷에 있으므로 ARP 캐시에 나타날 것입니다.

5) R1, R2, R3의 ARP 캐시를 확인하세요.

```
R1#show arp
R2#show arp
R3#show arp
```

R2는 10.10.10.0/24와 10.10.20.0/24에 직접 연결되어 있으므로 두 네트워크 모두에 대한 항목이 ARP 캐시에 있습니다.

R3는 10.10.20.0/24 네트워크에 직접 연결되어 있으므로 해당 네트워크에 대한 항목만 ARP 캐시에 있습니다. 10.10.10.0/24 네트워크에 대한 항목은 없습니다.
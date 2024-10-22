# 12 패킷의 생명 - 실습 연습

이 실습은 Cisco 라우터의 DNS 구성과 ARP 캐시를 탐구합니다.

## 실습 토폴로지


Packet Tracer에서 '12 The Life of a Packet.pkt' 파일을 열어 실습을 로드하세요.
이는 위에 표시된 대로 실습 토폴로지를 구성하고 R1과 R3 사이에 정적 경로를 추가합니다.

## 라우터를 DNS 클라이언트로 구성

Packet Tracer에서는 라우터가 DNS 서버가 될 수 없음('ip dns server' 명령을 지원하지 않음)에 유의하세요. 따라서 우리는 Packet Tracer 서버 장치를 DNS 서버로 사용하고 있습니다.

IP 주소가 10.10.10.10인 호스트가 DNS 서버로 구성되어 있으며 'R1', 'R2', 'R3'에 대한 DNS 요청을 해결할 수 있습니다.
도메인 이름은 사용되지 않습니다.

1) R1, R2, R3가 10.10.10.10을 DNS 서버로 사용하도록 구성하세요. 도메인 이름이나 도메인 목록을 구성할 필요는 없습니다.
2) R1에서 호스트 이름 'R2'와 'R3'를 사용하여 R2와 R3에 ping을 보낼 수 있는지 확인하세요(DNS 서버가 DNS 요청을 해결하는 데 시간이 걸릴 수 있습니다).
3) R3에서 호스트 이름 'R1'과 'R2'를 사용하여 R1과 R2에 ping을 보낼 수 있는지 확인하세요.

## 라우터의 ARP 캐시 검사
4) R1의 ARP 캐시에 R3에 대한 항목이 있을 것으로 예상하나요? 그 이유는 무엇인가요?
5) R1, R2, R3의 ARP 캐시를 확인하세요. 무엇이 보이나요?
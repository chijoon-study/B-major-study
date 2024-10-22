14 Cisco 라우터 및 스위치 기본 사항 - 실습 연습

이 실습에서는 스위치에 대한 기본 구성을 완료하고, Cisco Discovery Protocol CDP를 확인하며, 인터페이스 속도 및 이중 구성의 효과를 분석합니다.

실습 토폴로지


시작 구성 로드

Packet Tracer에서 '14 Cisco Router and Switch Basics.pkt' 파일을 열어 실습을 로드합니다.

Cisco 라우터 및 스위치 초기 구성
1) Router 1을 'R1'이라는 호스트 이름으로 구성
2) Router 2를 'R2'라는 호스트 이름으로 구성
3) Switch 1을 'SW1'이라는 호스트 이름으로 구성
4) 토폴로지 다이어그램에 따라 R1의 IP 주소 구성
5) 토폴로지 다이어그램에 따라 R2의 IP 주소 구성
6) SW1에 관리 IP 주소 10.10.10.10/24 부여
7) 스위치는 R2를 통해 다른 IP 서브넷에 연결성을 가져야 함
8) 스위치가 기본 게이트웨이를 ping할 수 있는지 확인
9) 장치를 연결하는 인터페이스에 적절한 설명 입력
10) SW1에서 R1로의 링크에서 속도와 이중 모드가 100 Mbps 전이중으로 자동 협상되는지 확인
11) R2로의 링크에 전이중 및 FastEthernet 속도를 수동으로 구성
12) 스위치가 실행 중인 IOS 버전은 무엇입니까?

CDP 구성
13) Cisco Discovery Protocol을 사용하여 직접 연결된 Cisco 이웃 확인
14) R1이 CDP를 통해 Switch 1에 대한 정보를 발견하지 못하도록 방지
15) 전역 구성 모드에서 'no cdp run' 명령을 입력한 다음 'cdp run' 명령을 입력하여 R1의 CDP 캐시를 플러시
16) R1이 CDP를 통해 SW1을 볼 수 없는지 확인

스위치 문제 해결
17) show ip interface brief 명령으로 R2에 연결된 스위치 포트의 상태를 확인합니다. 상태와 프로토콜이 up/up으로 표시되어야 합니다.
18) R2에 연결된 인터페이스를 종료하고 show ip interface brief 명령을 다시 실행합니다. 상태와 프로토콜이 administratively down/down으로 표시되어야 합니다.
19) 인터페이스를 다시 활성화합니다. 속도와 이중 설정을 확인합니다.
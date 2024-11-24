## 1. WAN (Wide Area Network) 기본 개념

### 네트워크 유형 분류
1. LAN (Local Area Network)
- 단일 건물이나 캠퍼스와 같은 제한된 지리적 영역의 네트워크
- 일반적으로 단일 조직이 소유/관리
- 높은 대역폭, 낮은 지연시간 특성

2. WAN (Wide Area Network) 
- 지리적으로 분산된 LAN들을 상호 연결하는 네트워크
- 예: 뉴욕 본사와 보스턴 지사 간 네트워크 연결
- 서비스 제공자(Service Provider)의 인프라 활용이 일반적

3. MAN (Metropolitan Area Network)
- LAN보다 크고 WAN보다 작은 도시 규모의 네트워크
- 같은 도시 내 여러 지점을 연결
- WAN에 비해 상대적으로 덜 사용되는 용어

## 2. VPN (Virtual Private Network)

### 기본 개념
- 공유 공인 네트워크(주로 인터넷)를 통한 가상 암호화 터널 구성
- 물리적 전용선 대비 저렴한 비용
- 데이터 기밀성을 위한 암호화 제공

### VPN 유형
1. Site-to-Site VPN
- 사무실 간 영구적 연결
- 라우터/방화벽에서 종단 처리
- 일반적으로 IPsec 프로토콜 사용
- 최종 사용자 장비 설정 불필요

2. Remote Access VPN
- 개별 사용자의 원격 접속용
- 사용자 장치에 VPN 클라이언트 소프트웨어 설치 필요
- SSL/TLS 또는 IPsec 사용
- 예: Cisco AnyConnect

### Site-to-Site VPN 구현 방식
1. IPsec 터널
- 개방형 표준, 다양한 벤더 장비 간 호환
- 멀티캐스트 미지원
- 정적 라우팅만 가능

2. GRE over IPsec
- GRE (Generic Routing Encapsulation) 터널에 IPsec 보안 적용
- 멀티캐스트 및 동적 라우팅 프로토콜 지원
- IPsec의 보안성과 GRE의 유연성 결합

3. IPsec VTI (Virtual Tunnel Interface)
- Cisco 전용 기술
- 간단한 구성
- 멀티캐스트 지원

4. DMVPN (Dynamic Multipoint VPN)
- Cisco 전용 기술
- Hub-and-Spoke 구성으로 완전 메시 연결 지원
- 확장성이 우수하며 구성 간소화
- 동적 터널 생성으로 최적 경로 확보

5. FlexVPN
- DMVPN의 차세대 버전
- 향상된 확장성과 유연성

6. GETVPN (Group Encrypted Transport VPN)
- Cisco 전용 기술
- MPLS 환경에서 사용
- 중앙집중식 키/정책 관리

## 3. MPLS (MultiProtocol Label Switching)

- Note: ISP에서 제공하는 VPN, 공용 회선 공유하여 가격이 싸고, 가입자 간 논리적 분리를 제공한다.  
    - Label이라는 IP 주소보다 단순한 정보를 사용해서 라우터 경로를 구성한다.  
    - PE 시작 시 IP 확인 후 Label을 부착 -> P에서 Label 정보를 보고 다른 P로 이동 -> 나가는 PE에서 Label 제거 및 IP로 전달
        - P to P에선 각 라우터마다 Swap이 발생는 방식 or PHP 최적화로 Swap이 발생하지 않는 방식 등이 있음.
    - https://www.cloudflare.com/ko-kr/learning/network-layer/what-is-mpls/
    https://louis-j.tistory.com/entry/IP-MPLS-MPLS-%EC%99%84%EC%A0%84-%EC%A0%95%EB%B3%B5-%ED%98%84%EB%8C%80-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC%EC%9D%98-%ED%95%B5%EC%8B%AC-%EA%B8%B0%EC%88%A0%EC%9D%84-%ED%8C%8C%ED%97%A4%EC%B9%98%EB%8B%A4
    - http://www.ktword.co.kr/test/view/view.php?m_temp1=2508&id=461
    - https://catsbi.oopy.io/75315c4f-20d7-4196-a239-363f374f7727

### MPLS VPN 개요
- 서비스 제공자의 공유 인프라를 통한 고객 간 분리된 통신
- SLA (Service Level Agreement) 기반 서비스 품질 보장
- 일반 인터넷 VPN 대비 안정적인 서비스 품질

### MPLS 구성요소
1. PE (Provider Edge) 라우터
- 고객 네트워크와 직접 연결
- MPLS VPN 서비스 제공 경계점

2. P (Provider) 라우터
- MPLS 코어 네트워크 구성
- 레이블 기반 패킷 전송 담당

3. CE (Customer Edge) 라우터
- 고객 측 라우터
- PE와 직접 연결

### MPLS VPN 유형
1. Layer 3 VPN
특징
- PE와 CE 라우터가 서로 라우팅 정보를 교환
- 마치 직접 연결된 라우터처럼 동작
- 각 사이트는 자신만의 IP 주소 체계 사용 가능

예시: `본사(10.1.0.0/16) ←→ MPLS망 ←→ 지사(192.168.1.0/24)`
- 서로 다른 IP 대역 사용 가능
- 라우팅 프로토콜로 경로 정보 교환

2. Layer 2 VPN
- VPLS (Virtual Private LAN Service)
  - 멀티포인트 L2 연결
    - 여러 지점을 하나의 거대한 스위치로 연결한 것처럼 동작
  - 단일 브로드캐스트 도메인 구성
- VPWS (Virtual Private Wire Service)
  - 포인트-투-포인트 L2 연결
    - 두 지점을 직접 케이블로 연결한 것처럼 동작
  - pseudowire 기술 사용

## 4. 전용회선 (Leased Line)

### 특징
- 두 지점 간 전용 물리적 연결
- 고정 대역폭 보장
- 대칭적 업로드/다운로드 속도
- 높은 신뢰성과 보안성
- SLA 기반 서비스 품질 보장

### 대역폭 옵션
1. 북미 지역
- T1: 1.544 Mbps
- T2: 6.312 Mbps
- T3: 44.736 Mbps

2. 유럽/기타 지역
- E1: 2.048 Mbps
- E2: 8.448 Mbps
- E3: 34.368 Mbps

### 장단점
장점:
- 전용 대역폭 보장
- 높은 보안성
- SLA 보장
- 안정적인 성능

단점:
- 높은 비용
- 긴 구축 기간
- 확장성 제한

## 5. 기타 WAN 연결 옵션

### 광케이블 기반 서비스
1. SONET/SDH
- SONET: 북미 표준
- SDH: 국제 표준
- 고속 광전송 네트워크 구현

2. DWDM (Dense Wavelength Division Multiplexing)
- 단일 광섬유로 다중 광신호 전송
- 높은 대역폭 효율성
- 백본(Backbone) 네트워크에 주로 사용

### 소규모 사무실/가정용 옵션
1. DSL (Digital Subscriber Line)
- 기존 전화선 활용
- 비대칭 속도 특성
- PPPoE 프로토콜 사용

2. Cable Internet
- 케이블 TV 망 활용
- 공유 대역폭 특성

3. 4G/5G 무선
- 이동통신망 활용
- 백업 회선으로 활용 가능

## 6. WAN 토폴로지

### 주요 토폴로지 유형
1. Hub-and-Spoke (Star)
- 중앙 집중형 구조
- 단순한 구성
- 중앙 보안 정책 적용 용이
- 단일 장애점 위험

2. Dual Hub-and-Spoke
- 이중화된 허브 구성
- 향상된 가용성
- 높은 구축 비용

3. Full Mesh
- 모든 지점 간 직접 연결
- 최적의 트래픽 경로
- 높은 구축/운영 비용
- 복잡한 구성

4. Partial Mesh
- 선택적 직접 연결
- 비용과 성능의 균형
- 중요 지점 간 직접 경로 제공

### 인터넷 연결 이중화 옵션
1. Single-homed
- 단일 ISP, 단일 회선
- 단순한 구성
- 단일 장애점 존재

2. Dual-homed
- 단일 ISP, 이중 회선
- 회선 레벨 이중화

3. Multi-homed
- 복수 ISP, 단일 회선
- ISP 레벨 이중화

4. Dual Multi-homed
- 복수 ISP, 이중 회선
- 최고 수준의 이중화
- 복잡한 구성과 높은 비용

## 7. WAN 인터페이스 카드

- Note: 여담 파트, 지원 라우터가 다르므로 사용에 주의하라는 내용.

### 주요 유형
1. 이더넷 인터페이스
- 기본 온보드 포트
- 추가 모듈 장착 가능

2. 시리얼 인터페이스
- WIC-2T: 구형 플랫폼용
- HWIC-2T: 신형 플랫폼용

3. T1/E1 인터페이스
- NIM-2MFT-T1/E1
- 음성/데이터 통합 지원

### 선택 시 고려사항
- 라우터 플랫폼 호환성
- 필요한 포트 수와 유형
- 대역폭 요구사항
- 향후 확장성

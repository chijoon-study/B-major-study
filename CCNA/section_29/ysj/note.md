## Section 29 정리

## NAT(Network Address Translation)

### 1. IPv4 주소 고갈 문제

##### IPv4의 한계
- IPv4는 32비트 주소 체계로 약 43억 개의 IP 주소 제공
- 초기 설계 시 이정도면 충분할 것으로 예상했으나 실제로는 부족
- 개인당 여러 기기(노트북, 모바일, 태블릿 등) 사용으로 수요 급증
- 프로토콜의 비효율적인 주소 공간 사용으로 실제 사용 가능한 주소 수는 더 적음

##### 해결 방안
1. **IPv6 개발**
   - 128비트 주소 체계 사용 (IPv4의 4배)
   - IPv4보다 28배 많은 주소 공간 제공
   - 주소 공간 고갈 문제 근본적 해결
   - 문제점: IPv4와 역호환되지 않아 전환이 어려움

2. **NAT 도입**
   - IPv6로의 전환 전까지 임시 해결책으로 도입
   - 실제로는 장기적인 해결책이 됨
   - 내부 네트워크에서 사설 IP 사용, 외부 통신 시 공인 IP로 변환

#### 2. 사설 IP 주소 (RFC1918)

##### 사설 IP 주소 범위
- **Class A**: 10.0.0.0 - 10.255.255.255 (10.0.0.0/8)
- **Class B**: 172.16.0.0 - 172.31.255.255 (172.16.0.0/12)
- **Class C**: 192.168.0.0 - 192.168.255.255 (192.168.0.0/16)

##### 특징
- 인터넷에서 라우팅 불가
- 내부 네트워크에서만 사용
- 공인 IP 주소 비용 절감
- 보안상 이점 제공 (외부에서 직접 접근 불가)

#### 3. NAT 유형

##### 1. 정적 NAT (Static NAT)
- 공인 IP와 사설 IP 간 1:1 영구 매핑
- 주요 용도: 웹 서버, 메일 서버 등 외부 접속이 필요한 서버
- 양방향 통신 지원

##### 2. 동적 NAT (Dynamic NAT)
- 공인 IP 주소 풀 사용
- 선착순으로 IP 주소 할당
- 풀의 주소가 모두 사용되면 새로운 연결 불가
- 일반적으로 수신 연결을 허용하지 않는 내부 호스트용

##### 3. PAT (Port Address Translation)
- 하나의 공인 IP로 다수의 내부 호스트 지원
- IP 주소와 포트 번호로 변환 추적
- 가장 널리 사용되는 방식
- 필요에 따라 공인 IP가 아니라 풀을 인터페이스로 매핑할수도 있음. PAT도 풀을 사용하므로 동일하게 적용 가능하며, 주로 DHCP를 사용해서 IP가 바뀌는 소규모 사무실에서 사용함.
- 특징:
  - 포트 번호로 각 연결 구분
  - 공인 IP 주소 절약
  - DHCP 환경에서도 사용 가능

#### 4. NAT 구성 요소

##### 주소 종류
1. **내부 로컬 주소**: 내부 호스트의 실제 IP 주소
2. **내부 전역 주소**: 외부에서 보는 내부 호스트의 변환된 주소
3. **외부 로컬 주소**: 내부에서 보는 외부 호스트의 주소
4. **외부 전역 주소**: 외부 호스트의 실제 IP 주소

##### 기본 구성 명령어
```
ip nat inside source static [내부IP] [외부IP]
ip nat inside source list [ACL번호] pool [풀이름]
ip nat pool [풀이름] [시작IP] [끝IP] netmask [넷마스크]
ip nat inside source list [ACL번호] interface [인터페이스] overload
```

### NAT 데모 랩

#### 1. 정적 NAT (Static NAT) 구성

##### 시나리오
- 내부 웹서버(10.0.1.10)를 외부에서 접근 가능하도록 공인 IP(203.0.113.3)로 매핑
- 양방향 통신 필요 (외부→내부, 내부→외부)

##### 구성 단계
```bash
# 1. NAT 인터페이스 지정
Router(config)# interface f0/0
Router(config-if)# ip nat outside    # 외부 인터페이스 지정

Router(config)# interface f1/0
Router(config-if)# ip nat inside     # 내부 인터페이스 지정

# 2. 정적 NAT 매핑 설정
Router(config)# ip nat inside source static 10.0.1.10 203.0.113.3
```

##### 확인 명령어
```bash
# NAT 변환 테이블 확인
Router# show ip nat translations

# NAT 동작 실시간 모니터링
Router# debug ip nat
```

#### 2. 동적 NAT (Dynamic NAT) 구성

##### 시나리오
- 내부 네트워크(10.0.2.0/24)의 호스트들이 인터넷 접근
- 공인 IP 풀 사용 (203.0.113.4 - 203.0.113.14)

##### 구성 단계
```bash
# 1. NAT 인터페이스 지정
Router(config)# interface f0/0
Router(config-if)# ip nat outside

Router(config)# interface f2/0
Router(config-if)# ip nat inside

# 2. NAT 풀 생성
Router(config)# ip nat pool Flackbox 203.0.113.4 203.0.113.14 netmask 255.255.255.240

# 3. 변환 대상 네트워크 정의 (ACL)
Router(config)# access-list 1 permit 10.0.2.0 0.0.0.255

# 4. NAT 풀과 ACL 연결
Router(config)# ip nat inside source list 1 pool Flackbox
```

#### 3. PAT (Port Address Translation) 구성

##### 시나리오 1: NAT 풀 사용
- 다수의 내부 호스트가 소수의 공인 IP 공유
- 포트 번호로 각 호스트 구분

##### 구성 단계
```bash
# 1. NAT 인터페이스 지정
Router(config)# interface f0/0
Router(config-if)# ip nat outside

Router(config)# interface f2/0
Router(config-if)# ip nat inside

# 2. NAT 풀 생성
Router(config)# ip nat pool Flackbox 203.0.113.4 203.0.113.6 netmask 255.255.255.240

# 3. 변환 대상 네트워크 정의
Router(config)# access-list 1 permit 10.0.2.0 0.0.0.255

# 4. PAT 설정 (overload 키워드 추가)
Router(config)# ip nat inside source list 1 pool Flackbox overload
```

##### 시나리오 2: 단일 공인 IP (DHCP) 사용
- 소규모 사무실에서 자주 사용
- DHCP로 할당받은 인터페이스 IP 사용

##### 구성 단계
```bash
# 1. NAT 인터페이스 지정
Router(config)# interface f0/0
Router(config-if)# ip address dhcp
Router(config-if)# ip nat outside

Router(config)# interface f2/0
Router(config-if)# ip nat inside

# 2. 변환 대상 네트워크 정의
Router(config)# access-list 1 permit 10.0.2.0 0.0.0.255

# 3. 인터페이스 기반 PAT 설정
Router(config)# ip nat inside source list 1 interface f0/0 overload
```

#### 공통 확인 및 문제해결 명령어

##### 기본 확인
```bash
# NAT 변환 테이블 확인
Router# show ip nat translations

# NAT 통계 확인
Router# show ip nat statistics

# 인터페이스 상태 확인
Router# show ip interface brief
```

##### 문제해결
```bash
# NAT 동작 실시간 모니터링
Router# debug ip nat

# NAT 변환 테이블 초기화
Router# clear ip nat translation *      # 모든 동적 변환 삭제
Router# clear ip nat translation inside [로컬IP] [전역IP] # 특정 변환 삭제
```

##### 작동 확인 테스트
```bash
# 내부→외부 연결 테스트
Host> ping 203.0.113.20

# 외부→내부 연결 테스트 (Static NAT의 경우)
Host> telnet 203.0.113.3 80
```

#### 주의사항
1. 정적 NAT 구성 시 양방향 통신 자동 지원
2. 동적 NAT는 풀의 주소가 모두 사용되면 새로운 연결 불가
3. PAT 사용 시 반드시 overload 키워드 추가
4. DHCP 환경에서는 인터페이스 기반 PAT 권장
5. 변환 테이블 확인 시 빠르게 확인 (엔트리 시간 초과 가능)

---

## show ip nat translations 명령어

#### 1. 명령어의 기본 역할
- NAT 라우터의 현재 활성화된 주소 변환 테이블을 표시
- 모든 NAT 매핑(정적, 동적, PAT)의 실시간 상태 확인 가능
- 문제 해결 시 가장 먼저 확인해야 하는 명령어

#### 2. 출력 결과의 주요 구성 요소

##### 기본 필드 설명
```
Pro  Inside global     Inside local       Outside local    Outside global
---  --------------   ---------------    --------------   ---------------
---  203.0.113.3:4096 10.0.1.10:49165   203.0.113.20:80  203.0.113.20:80
```

- **Pro(Protocol)**: 사용된 프로토콜 (tcp, udp, icmp 등)
- **Inside global**: 외부에 노출되는 내부 호스트의 변환된 주소:포트
- **Inside local**: 내부 호스트의 실제 사설 주소:포트
- **Outside local**: 내부 네트워크에서 보이는 외부 호스트 주소:포트
- **Outside global**: 외부 호스트의 실제 공인 주소:포트

#### 3. NAT 유형별 출력 예시

##### 정적 NAT의 경우
```bash
Router# show ip nat translations
Pro Inside global      Inside local       Outside local     Outside global
--- 203.0.113.3       10.0.1.10          ---               ---
```
- 포트 정보 없음
- 영구적인 1:1 매핑
- Outside 필드는 비어있을 수 있음

##### 동적 NAT의 경우
```bash
Router# show ip nat translations
Pro Inside global      Inside local       Outside local     Outside global
--- 203.0.113.4       10.0.2.10          ---               ---
--- 203.0.113.5       10.0.2.11          ---               ---
```
- 풀에서 할당된 주소 표시
- 일시적인 매핑
- 시간 초과 후 엔트리 자동 삭제

##### PAT의 경우
```bash
Router# show ip nat translations
Pro Inside global         Inside local          Outside local     Outside global
tcp 203.0.113.3:4096     10.0.2.10:49165      203.0.113.20:80   203.0.113.20:80
tcp 203.0.113.3:4097     10.0.2.11:49158      203.0.113.20:80   203.0.113.20:80
```
- 포트 번호까지 표시
- 같은 Inside global 주소에 여러 Inside local 주소 매핑
- 프로토콜 정보 포함

#### 4. 세부 주소 의미 설명

##### Inside Addresses
- **Inside local**: 내부 네트워크에서 실제로 구성된 호스트의 IP 주소
  - 예: `10.0.1.10` - 실제 호스트에 설정된 사설 IP
- **Inside global**: 외부에서 보는 내부 호스트의 변환된 공인 IP 주소
  - 예: `203.0.113.3` - NAT 후 외부에서 보이는 공인 IP

##### Outside Addresses
- **Outside local**: 내부 네트워크에서 보이는 외부 호스트의 주소
  - 일반적으로 Outside global과 동일
- **Outside global**: 외부 호스트의 실제 공인 IP 주소
  - 인터넷상의 실제 목적지 주소

#### 5. 실용적 활용 방법

##### 문제 해결 시나리오
1. **연결 문제 확인**
```bash
Router# show ip nat translations
```
- 예상된 변환이 테이블에 있는지 확인
- 포트 번호가 정상적으로 할당되었는지 검증

2. **변환 상태 초기화**
```bash
Router# clear ip nat translation *
Router# show ip nat translations
```
- 변환 테이블 초기화 후 새로운 연결 시도
- 문제 원인 파악에 도움

3. **실시간 모니터링과 함께 사용**
```bash
Router# debug ip nat
Router# show ip nat translations
```
- 실시간 NAT 동작과 변환 테이블 대조
- 변환 과정의 문제점 파악

#### 6. 주의사항
1. 명령어 실행 시점의 NAT 테이블 상태만 보여줌
2. 동적 변환은 매우 빠르게 시간 초과되어 사라질 수 있음
3. 실제 변환 과정이나 문제를 놓칠 수 있음

## 리뷰

영어로 NAT를 엔 에이 티 라고도 읽고 그냥 보이는 발음 그대로 낱 이라고도 읽는듯.

패킷에 헤더가 있고 그걸 다른 곳에서 지원하는게 아니라, 내부 IP를 외부 IP + 포트로 매핑해서 처리하는 방식임.

즉, 4계층이라고 볼 수 있을 듯?

- 뜬금없지만 기록해두면 좋을거 같아서
   - 3계층: 
      - OS 커널의 네트워크 스택에서 대부분의 3계층 기능 처리
      - 하드웨어(NIC)와 밀접한 연관 - NIC는 1~2계층
   - 4계층: 
      - 전적으로 소프트웨어/OS 수준에서 처리
      - 프로그래밍 가능한 영역
      - 포트 관리, 연결 상태 추적, 세션 관리 등

이전에 본 책에서 인상깊은 부분. 강의에서도 IPv6는 절대 다 소모되지 않는다고 했는데, 이정도면 그렇게 말할만 하지.
> IPv6는 주소당 128비트를 사용해. 따라서 IPv6로 만들 수 있는 주소의 개수는 무려 2의 128제곱인 340, 282,366,920,938,463,463,374,60 7,431,768,211,456개야. 단위로 치면억,조,경,해를 가볍게 넘어 약 ‘340간 2,823구’ 만큼의주소를 사용할 수 있어.
> 얼마나 많은지 감이 잘 오지 않지? 이 숫자가 얼마나 많은 양이냐면, 지구 표면 전체를 1mm^2로 산산이 쪼갰을 때 모든 조각마다 665,570,793,348,866,944개의 주소를 제공할 수 있을 정도야. 엄청나지?
> ref. 읽자마자 IT 전문가가 되는 네트워크 교과서



## Section 27 정리

## 스위치 보안 - 액세스 스위치 관련

이 강의는 네트워크 보안을 강화하기 위해 액세스 스위치에서 사용되는 주요 보안 메커니즘 세 가지—DHCP 스누핑, 동적 ARP 검사 (DAI), 802.1x 인증—에 대해 설명합니다.

### 1. DHCP 스누핑

**문제**  
네트워크에 비인가 DHCP 서버가 존재할 때, 잘못된 IP 주소 및 설정이 사용자 기기에 할당되어 네트워크 연결이 방해될 수 있습니다. 이는 실수로 발생하기도 하고, 악의적인 공격자에 의해 의도적으로 발생할 수도 있습니다.

**해결 방법**  
DHCP 스누핑을 통해 스위치 포트 중 신뢰할 수 있는 포트를 지정하여, 비인가 DHCP 서버로부터 오는 트래픽을 차단할 수 있습니다.
- **구성 방법**  
  1. 스위치에서 `ip dhcp snooping` 명령어를 입력하여 DHCP 스누핑 활성화
  2. 특정 VLAN에서 스누핑을 활성화하려면 `ip dhcp snooping vlan [VLAN 번호]` 입력
  3. 신뢰할 수 있는 포트에서 `ip dhcp snooping trust` 명령어로 설정

### 2. 동적 ARP 검사 (DAI)

**문제**  
공격자가 중간자 공격을 수행하기 위해 ARP 스푸핑을 사용하여, 네트워크 상의 트래픽을 감청하거나 특정 트래픽을 차단하는 상황이 발생할 수 있습니다.

**해결 방법**  
DAI는 ARP 패킷의 유효성을 검사하여 ARP 스푸핑을 방지합니다. 이는 DHCP 스누핑 정보 기반으로 작동합니다.
- **구성 방법**  
  1. DHCP 스누핑을 활성화하고, DAI 구성 전제 조건을 만족시킵니다.
  2. 스위치에서 `ip arp inspection vlan [VLAN 번호]` 명령어로 특정 VLAN에서 DAI 활성화
  3. 신뢰할 수 있는 포트에서 `ip arp inspection trust` 설정

### 3. 802.1x 인증

**문제**  
네트워크 자원에 대한 비인가 접근을 방지해야 할 때, 802.1x 인증을 통해 인증된 사용자만 네트워크에 접속할 수 있도록 할 필요가 있습니다.

**해결 방법**  
802.1x 인증을 통해 사용자가 유효한 ID와 비밀번호로 인증되기 전까지 네트워크 접근을 제한합니다.
- **구성 방법**  
  1. 사용자 기기(요청자)가 802.1x 인증을 지원해야 하며, 스위치(인증자)가 이를 처리할 수 있도록 설정합니다.
  2. 인증 서버(예: Cisco ISE)를 통해 사용자 인증을 수행
  3. 인증 성공 시 VLAN에 매핑되어 일반적인 네트워크 접근이 허용됩니다.

이 외에도 포트 보안 등 다양한 보안 메커니즘이 있으며, 이는 다음 강의에서 다루어질 예정입니다.

## 스위치 보안 - 포트 보안

#### 문제 정의
1. **불필요한 포트 활성화**: 사용되지 않는 포트가 활성화된 경우, 인증되지 않은 사용자가 네트워크에 접근할 수 있음.
2. **무선 액세스 포인트(Access Point, AP) 및 기타 장치 연결**: 인증되지 않은 사용자가 임의로 AP나 스위치를 네트워크에 연결하면 외부 접근 위험이 커짐.
3. **MAC 주소 스푸핑**: 공격자가 허용된 MAC 주소를 모방하여 보안이 무력화될 수 있음.
4. **다수의 MAC 주소 사용 시도**: 하나의 포트에 여러 장치가 연결되어 다수의 MAC 주소가 감지되면 네트워크에 혼선이 발생.

#### 해결 방법
1. **불필요한 포트 비활성화**: 사용되지 않는 포트는 비활성화하여 접근을 차단.
2. **포트 보안 설정**:
   - **MAC 주소 기반 제한**: 포트에 특정 MAC 주소만 허용하도록 설정하여 특정 장치만 네트워크에 접속 가능하게 함.
   - **최대 MAC 주소 수 제한**: 포트에서 허용할 수 있는 최대 MAC 주소 수를 설정하여 다수의 장치 연결 시도를 방지.
3. **위반 모드 설정**:
   - **Shutdown**: 위반 발생 시 포트를 비활성화하여 차단.
   - **Protect**: 위반 트래픽만 폐기하고, 허용된 장치의 트래픽은 유지.
   - **Restrict**: 위반 트래픽을 폐기하고 위반 기록을 남김.
4. **위반 후 인터페이스 복구**:
   - 수동으로 **shutdown 및 no shutdown** 명령어를 사용해 포트를 다시 활성화.
   - 자동 복구 시간 설정으로 error-disabled 상태의 포트를 자동으로 재활성화.
5. **특정 MAC 주소 수동 설정**: 허용된 MAC 주소를 수동으로 추가해 특정 장치에 포트를 고정.

#### 결과
이러한 포트 보안 설정을 통해 네트워크에 대한 무단 접근을 방지하고, 네트워크의 보안과 안정성을 높임.

## Section 34 정리

### Syslog

- Note: Syslog라는 메시지 로깅 형식 표준이 있다.

1. **Syslog 기본 개념**:
   - Syslog는 표준 메시지 로깅 형식으로 Cisco IOS가 따르는 업계 표준.
   - 장치 이벤트 발생 시 로그 메시지가 생성되며, 메시지에는 시퀀스 번호, 타임스탬프, Facility(출처), Severity(심각도), mnemonic(간략 설명), 자세한 설명 등이 포함.

2. **Severity 레벨** (0~7):
   - **0**: Emergency (시스템 사용 불가, 심각)
   - **1**: Alert (즉각 조치 필요)
   - **2**: Critical (심각한 상태)
   - **3**: Error (오류)
   - **4**: Warning (주의 필요)
   - **5**: Notice (정상적이지만 주의 필요)
   - **6**: Informational (정보 제공용)
   - **7**: Debug (디버깅 상세 정보)

3. **Syslog 메시지 저장 위치**:
   - **콘솔 라인**: 기본 활성화, 기본 Severity는 Debug.
   - **가상 터미널 라인(VTY)**: 기본 비활성화.
   - **로깅 버퍼(RAM)**: 기본 활성화.
   - **외부 Syslog 서버**: 로그 중앙 집중화에 사용.

4. **Syslog 설정 방법**:
   - **로깅 활성화/비활성화**:
     - `logging console` / `no logging console` (콘솔 라인)
     - `logging monitor <level>` (VTY 라인)
     - `logging buffered <level>` (버퍼)
   - **외부 서버 로깅**:
     - `logging <서버 IP>` 및 `logging trap <level>`.

5. **Terminal Monitor 명령**:
   - 텔넷/SSH 세션에서 디버깅 메시지를 보기 위해 필요.
   - 명령: `terminal monitor`.

6. **Logging Synchronous**:
   - 명령 입력 중 로그 메시지가 방해되지 않도록 설정.
   - 적용: `line console 0` 및 `line vty 0 15`에서 `logging synchronous`.

7. **Debug 명령 사용 주의**:
   - 실시간 디버깅 정보를 출력.
   - 프로덕션 환경에서 과도한 출력은 장치 성능에 영향을 줄 수 있음.
   - 디버깅 종료: `undebug all`.

8. **Syslog 서버의 장점**:
   - 로그 중앙 집중화.
   - 문제 해결 시 전체 네트워크 로그 분석 가능.
   - SIEM(System Information and Event Management)과 통합해 고급 분석 가능.


### SNMP

#### SNMP(Simple Network Management Protocol)

1. 개요
- 네트워크 모니터링을 위한 개방형 표준 프로토콜
- 라우터, 스위치, 서버 등 대부분의 네트워크 장치에서 사용

2. 구성 요소
- SNMP 매니저(서버/NMS): 정보 수집/정리
- SNMP 에이전트: 관리 장치에서 실행되는 소프트웨어
- MIB(Management Information Base): 장치별 데이터 변수 저장 데이터베이스

3. 동작 방식
- Get: 매니저가 장치에서 정보 수집
- Trap: 장치가 매니저로 정보 푸시
- Set: 매니저가 장치 설정 변경(덜 일반적)

4. 버전
- SNMPv1: 일반 텍스트 인증
- SNMPv2c: 일반 텍스트 인증, 대량 검색 지원
- SNMPv3: 강력한 인증/암호화 지원(권장)

5. 보안 고려사항
- 기본 커뮤니티 문자열(public/private) 사용 금지
- 미사용 장치는 SNMP 비활성화
- 가능하면 SNMPv3 사용
- SNMPv2c 사용 시 커스텀 커뮤니티 문자열 설정

#### SNMPv3 구성

1. 보안 모델
- 유저와 그룹 기반 인증 사용
- Community String 대신 암호화된 인증 방식 도입

2. 보안 레벨
- noAuthnoPriv: 기본 인증만 (유저네임)
- AuthNoPriv: 비밀번호 인증 (암호화)
- AuthPriv: 비밀번호 인증 + 통신 암호화 (권장)

3. 구성 단계

그룹 구성:
```
snmp-server group Flackbox-group v3 priv
```

유저 구성:
```
snmp-server user Flackbox-user Flackbox-group v3 auth sha AUTHPASSWORD priv aes 128 PRIVPASSWORD
```

4. 추가 설정 옵션
- access: NMS 서버 IP 접근 제어
- context: 스위치의 VLAN 접근 제어
- view: MIB 객체 접근 권한 설정
  - read view: 읽기 권한 (기본: 모든 접근)
  - write view: 쓰기 권한 (기본: 접근 불가)
  - notify view: 트랩 알림 설정

5. 암호화 옵션
- 인증: SHA (보안성 높음)
- 암호화: AES 128/192/256 (숫자가 클수록 보안 강화)


### Syslog vs SNMP

1. Syslog vs SNMP
- Syslog: 세분화된 로그 정보 제공, 단방향 푸시 방식
- SNMP: 양방향 통신 가능, 더 다양한 기능성 제공
- 상호 보완적이므로 둘 다 사용 가능
- 대부분의 NMS 서버가 두 프로토콜 모두 지원

2. NMS vs SIEM
- 공통점: 
  - 네트워크 장치의 로그 정보 수집
  - Syslog, SNMP, NetFlow 등 동일한 프로토콜 사용

- 차이점:
  NMS:
  - 네트워크 성능/상태 모니터링 중심
  - 대역폭, 인터페이스 상태 등 네트워크 문제 감지
  - 예시: SolarWinds

  SIEM:
  - 보안 모니터링/분석 중심
  - 인증 실패, 악성코드, 해킹 시도 등 보안 위협 감지
  - 예시: InfoSight

결론: 각 도구가 서로 다른 목적을 가지고 있어 상호 보완적으로 사용 가능

---

Syslog와 SNMP의 기본 개념:

Syslog:
- 장치의 상태, 이벤트, 오류 등을 기록하는 로깅 프로토콜
- 장치에서 Syslog 서버로 단방향 메시지 전송
- 상세한 로그 정보 제공

SNMP (Simple Network Management Protocol):
- 네트워크 장치 모니터링/관리를 위한 표준 프로토콜
- 양방향 통신 지원:
  - Get: 서버가 장치에서 정보 수집
  - Trap: 장치가 서버로 정보 전송
- 장치 상태 모니터링, 구성 변경 등 관리 기능 제공

두 프로토콜은 상호 보완적으로 사용되며, 대부분의 네트워크 관리 시스템에서 둘 다 지원합니다.

### 리뷰

- 후반부라 그런가 자격증에 필요한데 별로 중요하지 않은 부분을 막 넘기는 느낌. 재미도 없고 설명도 빨리빨리 넘긴다고 느낌.
- 자막 어투가 약간 달라진거 같기도 함. 여러 사람이 동시에 번역했으려나...
- 사실 이런것까지 알아야 하나? 하는 생각도 들긴 함. 중반 넘어가면서부터 그런 생각이 계속 있음.
- 일단 마무리는 하고 싶어서 이렇게까지 왔지만, 다음에는 강의에서 다루는 내용이 제한적이라면 짦은 강의로 찾아봐야 할듯.
    - 이게 43시간 짜리인데, 다루는 범위가 "3계층 이하 네트워크 동작 + 네트워크 저수준 인프라 구축"임. 
    - 저 내용이였으면 5~15으로 3주 내외로 끊으면 더 좋을듯.
## Section 19 정리

#### GPT

- https://chatgpt.com/share/6722b884-3244-8009-a3a5-b12055d9e08b

#### IGP 내부 게이트웨이 프로토콜의 기초

~~나에게는 너무 구체적이라 쓸 일 없는 내용이라 GPT로 요약하고 따로 정리 안함.~~



RIP와 EIGRP의 주요 특징과 설정을 체계적으로 비교/정리해드리겠습니다:

- **RIP (Routing Information Protocol)**
  - 특징
    - 거리 벡터 라우팅 프로토콜
    - 최대 홉 카운트 15로 제한 (확장성 제한)
    - 소규모 네트워크에 적합 - 실제론 테스트나 정말 소규모 아니면 거의 사용 안함.
  - 버전별 특징
    - RIPv1
      - 브로드캐스트 방식 (30초마다)
      - VLSM 미지원
      - 레거시 프로토콜
    - RIPv2
      - 멀티캐스트(224.0.0.9) 사용
      - VLSM 지원
      - 인증 기능 제공
  - 기본 설정
    ```
    router rip
    version 2
    network 10.0.0.0
    no auto-summary
    ```

- **EIGRP (Enhanced Interior Gateway Routing Protocol)**
  - 특징
    - Cisco 전용 프로토콜 - 현재는 개방형 표준이나, 타 사의 지원이 적음.
    - 빠른 수렴 지원
    - 제한된 업데이트로 효율적
    - 멀티캐스트 사용
    - 최대 4개 경로 부하 분산

  - AS 번호와 피어링
    - AS 번호로 구분 (같은 번호만 피어링)
    - 예: `router eigrp 100`
    - Network 명령어로 피어링 설정

  - 라우터 ID
    - 수동 설정 또는 자동 선택
    - 루프백 > 물리 인터페이스 순
    - 예: `eigrp router-id 1.1.1.1`

- **공통 검증 명령어**
  - `show ip protocols`: 프로토콜 설정 확인
  - `show ip route`: 라우팅 테이블 확인
  
- **주요 차이점**
  - 확장성: EIGRP > RIP
  - 구성 복잡도: RIP < EIGRP
  - 수렴 속도: EIGRP > RIP
  - 표준화: RIP(표준) vs EIGRP(Cisco 전용)
  - 부하 분산: EIGRP만 가능
  - 네트워크 크기: RIP(소규모), EIGRP(중대형)
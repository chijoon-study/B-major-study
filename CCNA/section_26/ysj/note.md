## Section 26 정리

## EtherChannel의 개요와 구성

이 강의에서는 EtherChannel의 역할과 목적에 대해 설명합니다.

1. **캠퍼스 네트워크 구조**: 
   - PC 등 종단 호스트는 액세스층 스위치에 연결됩니다. 액세스층 스위치는 상위 분배층 스위치로 업링크되고, 분배층 스위치는 코어층 스위치로 연결됩니다. 
   - 종단 호스트는 네트워크 대역폭을 항상 사용하지 않으므로, 적은 수의 업링크로도 충분한 네트워크 성능을 유지할 수 있습니다.
   - 액세스층과 분배층의 초과 가입 비율은 보통 20:1이며, 분배층과 코어층은 4:1이 추천됩니다.

2. **대역폭 관리의 문제점**: 
   - 스패닝 트리는 루프 방지를 위해 다중화된 링크 중 하나만 활성화하고 나머지는 차단합니다. 따라서, 다중 링크 연결 시 대역폭 활용이 비효율적일 수 있습니다.
   - 예를 들어, 두 개의 10Gbps 링크를 연결하더라도 스패닝 트리가 하나를 막아 10Gbps만 사용하게 됩니다.

3. **EtherChannel의 활용**:
   - EtherChannel은 여러 물리적 링크를 하나의 논리적 인터페이스로 묶어 스패닝 트리가 차단하지 않고 모든 링크를 활용하게 합니다.
   - 이를 통해 20Gbps 등의 높은 대역폭을 확보하고 부하 분산과 다중화 기능을 제공합니다.

4. **EtherChannel의 작동 방식**:
   - EtherChannel은 하나의 흐름에 대해 특정 인터페이스를 할당하여 패킷을 부하 분산시키며, 라운드 로빈 방식이 아닌 흐름 단위로 부하를 분산합니다. 이는 패킷의 순서를 유지하여 안정적인 연결을 보장합니다.

5. **EtherChannel 프로토콜 종류**:
   - **LACP** (Link Aggregation Control Protocol): 개방형 표준으로 모든 스위치에서 지원되며, 가장 선호되는 프로토콜입니다.
   - **PAgP** (Port Aggregation Protocol): Cisco 전용으로 사용이 권장되지는 않습니다.
   - **Static**: 정적 프로토콜로 협상이 없으나 설정이 맞으면 포트 채널이 생성됩니다.

6. **EtherChannel 구성 명령어**:
   - `channel-group` 명령어를 통해 각 프로토콜을 지정하며 설정을 합니다.
   - 예를 들어, LACP는 `channel-group 1 mode active`로 설정하고, PAgP는 `channel-group 1 mode desirable`, 정적 프로토콜은 `channel-group 1 mode on`으로 설정합니다.

7. **구성 확인 방법**:
   - `show EtherChannel summary` 명령어로 EtherChannel의 상태를 확인합니다.

## 다중 섀시 EtherChannel 옵션

이 강의는 Cisco 스위치에서 다중 섀시 EtherChannel 옵션에 대해 설명하고 있습니다. Cisco StackWise, Virtual Port Channel(vPC), Virtual Switching System(VSS)과 같은 기술을 사용하여 스위치들 간의 연결을 향상하고 대역폭 활용을 극대화하는 방법을 다룹니다.

강의 요점을 정리해보면 다음과 같습니다:

1. **EtherChannel 개요**: EtherChannel은 다중 물리적 링크를 하나의 논리적 링크로 묶어 대역폭을 늘리고 링크의 안정성을 높이는 기술입니다. 하지만 일반 EtherChannel 설정에서는 스패닝 트리가 일부 링크를 차단하여 대역폭 활용에 제한이 생길 수 있습니다.

2. **다중 섀시(multi-chassis) EtherChannel(MEC)**: 여러 스위치가 연결된 환경에서 단일 포트 채널로 운영하여 스패닝 트리의 루프 차단 문제를 해결합니다. 이로 인해 모든 물리적 링크를 사용 가능하며, 전체 대역폭을 활용할 수 있습니다.

3. **Cisco의 MEC 옵션**:
   - **StackWise**: Catalyst 3750, 3850, 9000 등의 Catalyst 스위치 플랫폼에서 지원되며, 전용 케이블로 여러 스위치를 하나로 스택하여 하나의 스위치처럼 운영합니다.
   - **Virtual Switching System(VSS)**: Catalyst 4500, 6500 스위치에서 지원되며, 스위치를 논리적으로 하나로 통합하여 작동합니다.
   - **Virtual Port Channel(vPC)**: Nexus 스위치에서 지원되며, 독립된 두 스위치를 하나의 포트 채널로 묶어 대역폭 활용을 최적화합니다.

4. **기타 주의 사항**: MEC 설정은 CCNA 시험에서는 기본적인 개념만 다루지만, CCNP 또는 CCNA 트랙의 데이터 센터 과정에서는 구성과 모니터링 방법까지 배웁니다.

이 강의는 Cisco 네트워크의 효율성을 높이기 위한 방법들을 강조하며, 다양한 스위치 플랫폼에서의 MEC 옵션을 비교 설명하고 있습니다.

# 요약 및 리뷰

- EtherChannel은 여러 물리적 링크를 하나의 논리적 링크로 묶어 스패닝 트리가 차단하지 않고 모든 링크를 활용하게 함.

- 엔터프라이즈급 네트워크 스위치는 보통 모듈형 섀시 방식으로 만들어짐.
    - 전원 공급 장치, 팬, 제어 모듈, 라인카드 등을 하나의 큰 케이스에 장착
    - 이 물리적인 케이스를 "섀시"라고 부름
- 여러 개의 물리적 섀시를 하나의 논리적 시스템으로 묶는다는 의미로 Multi-Chassis EtherChannel 이라고 부름


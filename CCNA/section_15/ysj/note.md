## Section 15 정리

#### 부팅 프로세스

- 메모리 종류:
    - ROM (Read Only Memory): 장치가 켜질 때 사용되며, POST(Power On Self Test, 하드웨어 상태 확인) 테스트와 부트스트랩을 담당한다.  IOS 소프트웨어 이미지를 Flash에서 찾고, 실패 시 ROMMON 프롬프트를 보여준다.
    - Flash: IOS 소프트웨어 이미지가 저장되는 장소로, 이동식 CompactFlash 카드로도 사용될 수 있다. 부팅 시 ROM에서 Flash로 부트스트랩이 호출된다.
    - NVRAM (Non-Volatile RAM): startup-config 파일이 저장되어 있으며, 부팅 시 RAM으로 불러와져 실행된다. 이 파일이 없으면 설정 마법사가 호출됩니다. (= 공장초기화 상태이므로)
    - RAM (Random Access Memory): 부팅 중 IOS 이미지와 startup-config가 불러와지는 작업 메모리. 휘발성이기 때문에 전원이 꺼지면 데이터가 사라진다. (의도적으로 롤백?이 쉽도록 이런 구성을 가짐)

- 부팅 과정:
    - 장치 전원이 켜지면 ROM에서 POST 테스트가 실행되고, 부트스트랩이 Flash에서 IOS 이미지를 찾고 로딩한다. (이미지는 압축되어 있음.)
    - IOS는 NVRAM에서 startup-config를 불러와 현재의 running-config로 적용한다.
    - 사용자 설정 변경 시 running-config에 즉시 반영되며, copy running-config startup-config 명령어를 통해 NVRAM에 저장할 수 있다.
- TFTP 서버: 외부 TFTP 서버에서 시스템 이미지나 startup-config를 불러올 수 있지만, 연결이 끊기면 부팅할 수 없으므로 권장되지 않음.

#### 공장 초기화 및 비밀번호 복구

- 공장 초기화 방법
    - 활성화 프롬프트에서 `write erase` 명령 입력 -> `startup-config` 제거됨.
    - 장치 재부팅 후 설정 마법사 실행

- 비밀번호 복구 방법
    - 구성 레지스터 이해
        - 기본 부팅 설정: `0x2102`
        - ROMMON 모드 부팅: `0x2120`
        - NVRAM 무시: `0x2142`
    - 재부팅 시 (주로) Ctrl-Break 조합으로 ROMMON 프롬프트 진입
    - ROMMON에서 `confreg 0x2142` 명령 입력하여 startup-config 무시 설정
    - 장치 재부팅 후 설정 마법사에서 "no" 입력하여 우회
    - `enable` 명령으로 활성화 모드 진입, startup-config를 running-config로 복사
    - 새로운 활성화 비밀번호 설정
    - `config-register 0x2102` 입력하여 정상 부팅 가능하도록 설정
    - `copy run start` 명령으로 변경 사항 저장
    - 내 메모: startup-config에 접속하기 위해 암호가 필요한데, 그걸 우회해서 가져오고, 비밀번호를 새로 설정한다고 보면 됨.
    - 주의 사항
        - startup-config를 running-config로 복사하는 것 잊지 않기
        - 구성 레지스터를 원래 설정으로 되돌리는 것 잊지 않기


#### 시스템 이미지 및 구성의 백업

시스템 이미지(IOS)나 구성(Config)를 백업하는 방법 설명.

- 백업 장소: 외부 FTP, TFTP 서버, USB, 장치의 Flash 메모리에 가능.

- 백업 이유:
    - 시스템 이미지를 TFTP 서버에 백업하면 Cisco 웹사이트에서 다시 다운로드할 필요 없이 복구할 수 있음.
    - 구성 파일을 백업하여 나중에 이전 버전으로 롤백할 수 있음. 단, 파일을 복사하면 병합되므로 아예 교체해야 함.

- 백업 명령어:
    - copy flash tftp: 시스템 이미지를 TFTP 서버에 백업.
    - copy running-config tftp: 실행 중인 구성을 TFTP 서버에 백업.
    - copy startup-config usb: 시작 구성을 USB에 백업.

- 실행 예시:
    - TFTP 서버에 시스템 이미지와 실행 중인 구성 백업 과정 설명.
    - Flash에 백업 후 기존 구성을 복원하는 과정 시연.

- 복원 과정:
    - write erase 명령으로 시작 구성을 삭제한 후, copy flash startup-config 명령으로 백업한 구성 파일을 복원.
    - 재부팅 후 이전 구성이 복원된 상태를 확인.

#### IOS 업그레이드

- 소프트웨어 이미지 다운로드
    - Cisco 웹사이트(https://software.cisco.com)에서 새로운 IOS 소프트웨어 이미지를 다운로드
    - "Software Download" 링크 클릭 후 업그레이드할 장치 모델 검색

- TFTP 서버로 복사
    - 다운로드한 IOS 이미지를 TFTP 서버로 복사
    - TFTP 서버에서 장치의 Flash 메모리로 다운로드

- 기존 이미지 처리
    - Flash에 새로운 이미지 다운로드 후 기존 이미지 삭제 가능
    - 기존 이미지 유지 시 boot system 명령어로 새로운 이미지로 부팅 설정

- 업그레이드 과정 예시
    - 스위치 주소 10.10.10.2에서 TFTP 서버 10.10.10.10의 최신 IOS 이미지 다운로드
    - 현재 실행 중인 소프트웨어 확인: sh flash, sh ver 명령어 사용
    - TFTP 서버에서 최신 이미지(버전 15.0) 선택 후 copy tftp flash 명령어로 다운로드

- 부팅 설정
    - boot system 명령어로 새로운 시스템 이미지 경로 설정
    - copy run start 명령어로 변경 사항 저장 후 reload 명령어로 재부팅
    - 재부팅 후 실행 중인 버전 확인하여 업그레이드 완료 여부 확인

## 리뷰

AI 써서 정리.

나중에도 쓸일이 없는 내용같아서 대충 듣고 넘김.

그나저나 비밀번호 복구 방법에 쓰는 저런걸 보면, 해킹당하기 쉽지 않을까?    
막 영화에서 보는 거처럼 서버 랙에 노트북 연결해가지고 내부 데이터 빼고 그런게 이론상으로는 가능할거같음.

뭔가 이런 강의를 생각한건 아니긴 한데...

일단 끝은 볼 예정.

그래도 맨날 네트워크 인프라를 AWS나 클라우드로만 다루다가, 뭔가 실제로 어떤 식으로 동작하는지 보는거라서 의도치 않게 다른 방향으로 좀 유익한 느낌.


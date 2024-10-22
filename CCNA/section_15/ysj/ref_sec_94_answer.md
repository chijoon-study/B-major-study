이 실습에서는 Cisco 라우터에서 공장 초기화, 비밀번호 복구, 구성 백업, 시스템 이미지 백업 및 복구를 수행합니다. 또한 Cisco 스위치에서 IOS 업그레이드를 수행합니다.

공장 초기화
R1의 실행 중인 구성을 확인합니다. 호스트 이름과 인터페이스가 구성되어 있음을 확인하세요.
R1#sh run
Building configuration...
Current configuration : 696 bytes
!
hostname R1
!
interface GigabitEthernet0/0
ip address 10.10.10.1 255.255.255.0
duplex auto
speed auto
R1을 공장 초기화하고 재부팅합니다.
R1#write erase
Erasing the nvram filesystem will remove all configuration files! Continue? [confirm]
[OK]
Erase of nvram: complete
%SYS-7-NV_BLOCK_INIT: Initialized the geometry of nvram R1#reload
Proceed with reload? [confirm]
라우터가 부팅되는 과정을 지켜봅니다.

라우터가 설정 마법사로 부팅되어야 합니다. 마법사를 종료하고 시작 및 실행 구성이 비어 있는지 확인합니다.

'15 Cisco Device Management Configs.zip' 파일에서 R1의 구성을 다시 붙여넣고 저장합니다.

비밀번호 복구
R1에 enable secret 'Flackbox1'을 설정하고 실행 중인 구성을 저장합니다.

적절한 명령어로 라우터가 다음 재부팅 시 rommon 프롬프트로 부팅되도록 구성하고 라우터를 재부팅합니다.

rommon 모드에서 라우터가 부팅 시 시작 구성을 무시하도록 구성하고 라우터를 재부팅합니다.

라우터가 설정 마법사로 부팅되어야 합니다. 마법사를 종료합니다.

실행 중인 구성과 시작 구성을 보면 어떤 내용이 표시될 것으로 예상하십니까? 이를 확인하세요.

시작 구성을 실행 중인 구성으로 복사합니다. 이 단계를 놓치지 마세요. 그렇지 않으면 라우터가 공장 초기화됩니다!

GigabitEthernet0/0 인터페이스의 상태를 확인합니다. 왜 다운 상태입니까?

GigabitEthernet0/0 인터페이스를 활성화합니다.

enable secret을 제거합니다.

다음 재부팅 시 라우터가 정상적으로 부팅되고 접근할 수 있도록 합니다.

라우터를 재부팅하고 예상된 구성이 있는지 확인합니다.

구성 백업
중요: 파일 이름은 대소문자를 구분합니다 - 정확히 표시된 대로 입력해야 합니다(c2900은 C2900과 다릅니다).

R1의 실행 중인 구성을 플래시에 백업합니다. 백업 파일에 적절한 이름을 사용하세요. 구성이 백업되었는지 확인합니다.

R1 시작 구성을 TFTP 서버에 백업합니다. 백업 파일에 적절한 이름을 사용하세요. 구성이 백업되었는지 확인합니다.

IOS 시스템 이미지 백업 및 복구
R1의 IOS 시스템 이미지를 TFTP 서버에 백업합니다. 구성이 백업되었는지 확인합니다.

플래시에서 시스템 이미지를 삭제하고 재부팅합니다.

인터넷 검색을 사용하여 라우터 모델에 대한 시스템 복구 지침을 찾습니다. TFTP 서버를 사용하여 시스템 이미지를 복구합니다.

IOS 이미지 업그레이드
SW1이 C2960 Software (C2960-LANBASE-M), Version 12.2(25)FX를 실행 중인지 확인합니다.

TFTP 서버를 사용하여 c2960-lanbasek9-mz.150-2.SE4.bin으로 업그레이드합니다.

재부팅하고 스위치가 새로운 소프트웨어 버전을 실행 중인지 확인합니다.
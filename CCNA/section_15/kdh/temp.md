## Cisco Device Memory
Cisco에서 만드는 장치에는 여러 종류의 메모리가 들어간다.  
- ROM
- Flash
- NVRAM
- RAM

각 메모리의 용도를 알아보면
### ROM
장치가 처음 켜질때 ROM을 불러온다.  
ROM에는 두가지 주요 기능이있는데
- POST(Power on Self Test) 
  - 처음켜질때 하드웨어에 문제가없는지 확인
- load bootstrap 
  - flash로부터 IOS 소프트웨어를 불러올 bootstrap 실행
  - 만약 flash에서 IOS 소프트웨어가 안찾아진다면 ROMMON(ROM Monitor) prompt를 커맨드 라인에 보여줌
  - ROMMON 프롬프트는 없어지거나 오염된 IOS 소프트웨어를 복구하는데에 사용됨

### Flash
Cisco는 정기적으로 새로운 소프트웨어를 배포하기에 이를 업그레이드 할 수 있다.  
새로운 소프트웨어를 다운로드해 flash에 복사하게 되면 flash에 두 버전의 소프트웨어가 존재하게 되는데, 이때 기본적으론 처음으로 발견된 IOS를 가져오지만 다른 IOS를 가져오고 싶다면 `boot system`이후 `flash`에서 원하는 IOS의 이름을 입력해 부팅할 수 있다.  

### NVRAM
NVRAM에는 startup-config가 저장되는데, 부팅시에 이를 RAM으로 Load하고 이것이 running-config가 되게 된다.  
`copy running-config startup-config`명령어를 통해 RAM에 있는, 즉 현재 설정해놓은 값을 startup config에 저장할 수 있다.  
이렇게 running config, startup config가 나눠진 이유는 설정중 장치에 이상이 생겨 커맨드라인에 조차 접근할 수 없을때 단순히 재부팅함으로서 문제를 해결할 수 있게하기 위함이다.  

### RAM
작업중 설정값이 저장되는 메모리이다.  


## Factory Reset and Password Recovery
장치의 startup config를 지워버리고 싶다면 `write erase`를 입력하면된다.  
이후 재부팅 시 빈 설정으로 부팅되고 설치 마법사가 실행될것이다.  

장치의 enable 프롬프트에 진입하는데에 비밀번호를 설정할 수 있는데, 전임자가 비밀번호를 알려주지 않고 퇴사하는 등의 이유로 enable 프롬프트에 접근하지 못하는 상황이 생길 수 있다.  
이때 기존 설정값을 유지하면서 비밀번호를 복구하는 방법이 있다.  
전역 설정 프롬프트에서`config-register 0x2120` 장치가 재부팅 되고있을때 `ctrl + break`를 입력하면 ROMMON 프롬프트가 켜지는데 ROMMON 프롬프트에서 `confreg`명령어를 통해 레지스터 값을 수정할 수 있는데 아래와 같은 설정값들이 있다.  
- 0x2102: boot normally
- 0x2120: boot into rommon
- 0x2142: ignore contents of NVRAM

여기서 0x2142를 통해 startup config를 무시하고 부팅하면 빈 설정 값으로 장치가 실행된다.    
이때 기존 startup config가 사라지는건 아니고 무시하는것이므로 enable 프롬프트에 진입한 후 `copy start run`을 통해 기존 설정값을 불러오고 기존 비밀번호를 수정하면된다.  

### password vs secret
추가로 비밀번호에는 password와 secret, 두가지 종류가 있는데 password는 암호화되지 않고 저장되며 secret은 암호화되어 저장된다.  
기존에는 password를 사용했지만 보안상의 문제로 secret이 나오게 되었고, password는 더이상 사용되지 않는다.  
하지만 하위호환을 위해 남아있기는 하다.  


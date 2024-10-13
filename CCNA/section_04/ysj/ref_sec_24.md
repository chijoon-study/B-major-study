# IOS Operating System - Lab Exercises

## English Version

### Exploring User Exec Mode and CLI Command Help

- Notice you are in User Exec mode as indicated by the ‘Router>’ prompt.
- Enter a question mark to explore available commands.

```bash
Router> ?
Exec commands:
  <1-99>  Session number to resume
  connect  Open a terminal connection
  disable  Turn off privileged commands
  disconnect  Disconnect an existing network connection
  enable  Turn on privileged commands
  exit  Exit from the EXEC
  logout  Exit from the EXEC
  ping  Send echo messages
  resume  Resume an active network connection
  show  Show running system information
  ssh  Open a secure shell client connection
  telnet  Open a telnet connection
  terminal  Set terminal line parameters
  traceroute  Trace route to destination
```

- Limited commands are available in User Exec mode. For example, `show run` needs Privileged Exec mode.

```bash
Router> show run
% Invalid input detected at '^' marker.
```

### Viewing Additional Output

- To scroll through additional output, use the Space Bar.

```bash
--More—
```

- You can also check possible options for the `show aaa` command:

```bash
Router# sh aaa ?
local      Show AAA local method options
sessions   Show AAA sessions as seen by AAA Session MIB
user       Show users active in AAA subsystem
```

### Configuration Management

- To drop back to Privilege Exec mode:

```bash
R1(config-if)# end
R1#
```

- View configurations:

```bash
R1# show running-config
Building configuration...
Current configuration : 737 bytes
!
hostname R1
!
Output truncated --
```

- Change the hostname and save configurations:

```bash
R1# config t
R1(config)# hostname RouterX
RouterX(config)#
RouterX# copy run start
Building configuration...
[OK]
```

### Available Show Commands

- To see available show commands, enter:

```bash
Router# sh ?
aaa                        Show AAA values
access-lists              List access lists
arp                       Arp table
...
```

## Korean Version

### 사용자 실행 모드 및 CLI 명령 도움말 탐색하기

- ‘Router>’ 프롬프트에 의해 사용자 실행 모드에 있음을 알 수 있습니다.
- 사용 가능한 명령을 탐색하려면 물음표를 입력합니다.

```bash
Router> ?
Exec commands:
  <1-99>  세션 번호 계속하기
  connect  터미널 연결 열기
  disable  특권 명령 끄기
  disconnect  기존 네트워크 연결 끊기
  enable  특권 명령 켜기
  exit  EXEC 종료
  logout  EXEC 종료
  ping  에코 메시지 보내기
  resume  활성 네트워크 연결 계속하기
  show  실행 중인 시스템 정보 보기
  ssh  보안 셸 클라이언트 연결 열기
  telnet  텔넷 연결 열기
  terminal  터미널 라인 매개변수 설정하기
  traceroute  목적지로의 경로 추적하기
```

- 사용자 실행 모드에서는 제한된 명령만 사용할 수 있습니다. 예를 들어, `show run`은 특권 실행 모드가 필요합니다.

```bash
Router> show run
% 잘못된 입력이 '^' 표시 위치에서 감지되었습니다.
```

### 추가 출력 보기

- 추가 출력을 스크롤하려면 Space Bar를 사용합니다.

```bash
--더 많은 내용--
```

- `show aaa` 명령에 대한 가능한 옵션도 확인할 수 있습니다:

```bash
Router# sh aaa ?
local      AAA 로컬 메서드 옵션 보기
sessions   AAA 세션 보기
user       AAA 서브시스템에서 활성 사용자의 보기
```

### 구성 관리

- 특권 실행 모드로 돌아가려면 다음을 입력합니다:

```bash
R1(config-if)# end
R1#
```

- 구성을 보기:

```bash
R1# show running-config
구성 작성 중...
현재 구성 : 737 바이트
!
hostname R1
!
출력이 잘림 --
```

- 호스트 이름을 변경하고 구성을 저장합니다:

```bash
R1# config t
R1(config)# hostname RouterX
RouterX(config)#
RouterX# copy run start
구성 작성 중...
[OK]
```

### 사용 가능한 show 명령

- 사용 가능한 show 명령을 보려면 입력합니다:

```bash
Router# sh ?
aaa                        AAA 값 보기
access-lists              액세스 목록 표시
arp                       ARP 테이블
...
```
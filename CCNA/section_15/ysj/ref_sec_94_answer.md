답안 키

이 실습에서는 Cisco 라우터에서 공장 초기화, 비밀번호 복구, 구성 백업, 시스템 이미지 백업 및 복구를 수행할 것입니다. 또한 Cisco 스위치에서 IOS 업그레이드를 수행할 것입니다.

공장 초기화

1) R1의 실행 중인 구성을 확인합니다. 호스트 이름과 인터페이스가 구성되어 있음을 주목하세요.
```
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
```
2) R1을 공장 초기화하고 재부팅합니다.
```
R1#write erase
Erasing the nvram filesystem will remove all configuration
files! Continue? [confirm]
[OK]
Erase of nvram: complete
%SYS-7-NV_BLOCK_INIT: Initialized the geometry of nvram
R1#reload
Proceed with reload? [confirm]
```
3) 라우터가 부팅되는 동안 부팅 과정을 지켜봅니다.
```
System Bootstrap, Version 15.1(4)M4, RELEASE SOFTWARE (fc1)

Readonly ROMMON initialized

IOS Image Load Test
___________________

Digitally Signed Release Software

Self decompressing the image :
###########################################################
############### [OK]
```
4) 라우터가 설정 마법사로 부팅되어야 합니다. 마법사를 종료한 다음 시작 구성과 실행 중인 구성이 비어 있는지 확인합니다.
```
--- System Configuration Dialog ---

Continue with configuration dialog? [yes/no]: no

Router>enable
Router#show run
Building configuration...
hostname Router
!
interface GigabitEthernet0/0
no ip address
duplex auto
speed auto
shutdown

Router#show start
startup-config is not present
```
5) '15 Cisco Device Management Configs.zip' 파일에서 R1의 구성을 다시 구성에 붙여넣고 저장합니다.
```
Router#configure terminal
Router(config)#hostname R1
R1(config)#!
R1(config)#interface GigabitEthernet0/0
R1(config-if)# ip address 10.10.10.1 255.255.255.0
R1(config-if)# duplex auto
R1(config-if)# speed auto
R1(config-if)# no shutdown
R1(config-if)#!
R1(config-if)#line con 0
R1(config-line)# exec-timeout 30 0
R1(config-line)#end

R1#copy run start
Destination filename [startup-config]?
Building configuration...
[OK]
```
비밀번호 복구

6) R1에서 enable secret을 'Flackbox1'로 설정하고 실행 중인 구성을 저장합니다.
```
R1(config)#enable secret Flackbox1
R1(config)# do copy run start
Destination filename [startup-config]?
Building configuration...
[OK]
R1(config)#
```
7) 적절한 명령을 사용하여 다음 재부팅 시 라우터가 rommon 프롬프트로 부팅되도록 구성하고 라우터를 재부팅합니다.
```
R1(config)#config-register 0x2120
R1(config)#end
R1#reload
Proceed with reload? [confirm]
```
8) rommon 모드에서 라우터가 부팅 시 시작 구성을 무시하도록 구성하고 라우터를 재부팅합니다.
```
rommon 1 > confreg 0x2142
rommon 2 > reset
```
9) 라우터가 설정 마법사로 부팅되어야 합니다. 마법사를 종료합니다.
```
--- System Configuration Dialog ---
Continue with configuration dialog? [yes/no]: no
```
10) 실행 중인 구성과 시작 구성을 보면 어떤 것이 보일 것으로 예상하십니까? 이를 확인하세요.

라우터가 부팅 시 시작 구성을 로드하지 않았기 때문에 실행 중인 구성은 비어 있어야 합니다. 시작 구성은 변경되지 않은 채로 이전의 모든 구성이 여전히 있어야 합니다.
```
Router#sh run
Building configuration...

hostname Router
!
interface GigabitEthernet0/0
no ip address
duplex auto
speed auto

Router#sh start
!
hostname R1
!
enable secret 5 $1$mERr$J2XZHMOgpVVXdLjC9lYtE1
!
interface GigabitEthernet0/0
ip address 10.10.10.1 255.255.255.0
duplex auto
speed auto
```
11) 시작 구성을 실행 중인 구성으로 복사합니다. 이 단계를 놓치지 마세요. 그렇지 않으면 라우터를 공장 초기화하게 됩니다!
```
Router#copy start run
Destination filename [running-config]?
```
12) GigabitEthernet0/0 인터페이스의 상태를 확인합니다. 왜 다운되어 있습니까?
```
R1#show ip interface brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0 10.10.10.1 YES NVRAM administratively down down
GigabitEthernet0/1 unassigned YES NVRAM administratively down down
GigabitEthernet0/2 unassigned YES NVRAM administratively down down
Vlan1 unassigned YES NVRAM administratively down down

R1#show run
! truncated
interface GigabitEthernet0/0
ip address 10.10.10.1 255.255.255.0
duplex auto
speed auto
shutdown
```
라우터 인터페이스는 기본적으로 종료되어 있습니다. 인터페이스의 시작 구성에 'no shutdown'이 명시적으로 나타나지 않기 때문에, 시작 구성이 실행 중인 구성으로 복사될 때 기본값이 적용되어 인터페이스가 종료 상태가 됩니다.

13) GigabitEthernet0/0 인터페이스를 활성화합니다.
```
R1(config)#interface g0/0
R1(config-if)#no shutdown
```
14) enable secret을 제거합니다.
```
R1(config)#no enable secret
```
15) 다음 재부팅 시 라우터가 정상적으로 재부팅되고 라우터에 접근할 수 있도록 합니다.
```
R1(config)#config-register 0x2102
R1(config)#end
R1#copy run start
Destination filename [startup-config]?
Building configuration...
[OK]
```
16) 라우터를 재부팅하고 예상된 구성이 있는지 확인합니다.
```
R1#reload
Proceed with reload? [confirm]

R1>en
R1#show run
Building configuration...
hostname R1
!
interface GigabitEthernet0/0
ip address 10.10.10.1 255.255.255.0
duplex auto
speed auto

R1#sh ip int brief
Interface IP-Address OK? Method Status Protocol
GigabitEthernet0/0 10.10.10.1 YES NVRAM up up
GigabitEthernet0/1 unassigned YES NVRAM administratively down down
GigabitEthernet0/2 unassigned YES NVRAM administratively down down
Vlan1 unassigned YES NVRAM administratively down down
```
구성 백업

중요: 파일 이름은 대소문자를 구분합니다 - 정확히 보여진 대로 입력해야 합니다(c2900은 C2900과 다릅니다).

17) R1의 실행 중인 구성을 Flash에 백업합니다. 백업 파일에 적절한 이름을 사용하세요. 구성이 백업되었는지 확인합니다.
```
R1#copy run flash
Destination filename [running-config]? Backup-1
Building configuration...
[OK]

R1#show flash

System flash directory:
File Length Name/status
5 728 Backup-1
3 33591768 c2900-universalk9-mz.SPA.151-4.M4.bin
2 28282 sigdef-category.xml
1 227537 sigdef-default.xml
[33848315 bytes used, 221895685 available, 255744000 total]
249856K bytes of processor board System flash (Read/Write)
```
18) R1 시작 구성을 TFTP 서버에 백업합니다. 백업 파일에 적절한 이름을 사용하세요. 구성이 백업되었는지 확인합니다.
```
R1#copy start tftp
Address or name of remote host []? 10.10.10.10
Destination filename [R1-confg]? Backup-2
Writing startup-config....!!
[OK - 698 bytes]
698 bytes copied in 3.007 secs (242 bytes/sec)
```
IOS 시스템 이미지 백업 및 복구

19) R1의 IOS 시스템 이미지를 TFTP 서버에 백업합니다. 구성이 백업되었는지 확인합니다.
```
R1#show flash

System flash directory:
File Length Name/status
5 728 Backup-1
3 33591768 c2900-universalk9-mz.SPA.151-4.M4.bin
2 28282 sigdef-category.xml
1 227537 sigdef-default.xml
[33848315 bytes used, 221895685 available, 255744000 total]
249856K bytes of processor board System flash (Read/Write)

R1#copy flash tftp
Source filename []? c2900-universalk9-mz.SPA.151-4.M4.bin
Address or name of remote host []? 10.10.10.10
Destination filename [c2900-universalk9-mz.SPA.151-
4.M4.bin]?

Writing c2900-universalk9-mz.SPA.151-
4.M4.bin...!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
[OK - 33591768 bytes]
```
IOS 이미지 복구

20) Flash에서 시스템 이미지를 삭제하고 재부팅합니다.

```
R1#delete flash:c2900-universalk9-mz.SPA.151-4.M4.bin
Delete filename [c2900-universalk9-mz.SPA.151-4.M4.bin]? 
Delete flash:/c2900-universalk9-mz.SPA.151-4.M4.bin? 
[confirm]

R1#reload
Proceed with reload? [confirm]
Boot process failed... 
The system is unable to boot automatically. The BOOT 
environment variable needs to be set to a bootable 
image. 
rommon 1 >
```

21) 인터넷 검색을 사용하여 라우터 모델에 대한 시스템 복구 지침을 찾습니다. TFTP 서버를 사용하여 시스템 이미지를 복구합니다.

```
http://www.cisco.com/c/en/us/td/docs/routers/access/1900/software/configuration
/guide/Software_Configuration/appendixCrommon.html은 'Cisco 2900 rommon recovery'를 검색할 때 첫 번째 결과입니다.
```

“Recovering the System Image (tftpdnld)” 섹션으로 이동합니다.

'tftpdnld' 명령에는 rommon 모드에서 명령을 입력할 때 표시되는 내장 도움말이 있습니다:

```
rommon 1 > tftpdnld

Missing or illegal ip address for variable IP_ADDRESS 
Illegal IP address.

usage: tftpdnld 
Use this command for disaster recovery only to recover an image via 
TFTP. 
Monitor variables are used to set up parameters for the transfer. 
(Syntax: "VARIABLE_NAME=value" and use "set" to show current 
variables.) 
"ctrl-c" or "break" stops the transfer before flash erase begins.

The following variables are REQUIRED to be set for tftpdnld: 
IP_ADDRESS: The IP address for this unit 
IP_SUBNET_MASK: The subnet mask for this unit 
DEFAULT_GATEWAY: The default gateway for this unit 
TFTP_SERVER: The IP address of the server to fetch from 
TFTP_FILE: The filename to fetch 

The following variables are OPTIONAL: 
TFTP_VERBOSE: Print setting. 0=quiet, 1=progress(default), 2=verbose 
TFTP_RETRY_COUNT: Retry count for ARP and TFTP (default=7) 
TFTP_TIMEOUT: Overall timeout of operation in seconds (default=7200)
```

이 구성에는 모두 대문자를 사용하세요:

```
rommon 2 > IP_ADDRESS=10.10.10.1 
rommon 3 > IP_SUBNET_MASK=255.255.255.0 
rommon 4 > DEFAULT_GATEWAY=10.10.10.1 
rommon 5 > TFTP_SERVER=10.10.10.10 
rommon 6 > TFTP_FILE=c2900-universalk9-mz.SPA.151-4.M4.bin 
rommon 7 > tftpdnld 

IP_ADDRESS: 10.10.10.1 
IP_SUBNET_MASK: 255.255.255.0 
DEFAULT_GATEWAY: 10.10.10.1 
TFTP_SERVER: 10.10.10.10 
TFTP_FILE: c2900-universalk9-mz.SPA.151-4.M4.bin 
Invoke this command for disaster recovery only.
WARNING: all existing data in all partitions on flash will be lost! 

Do you wish to continue? y/n: [n]: y
```

**IOS 이미지 업그레이드**

22) SW1이 C2960 소프트웨어(C2960-LANBASE-M), 버전 12.2(25)FX를 실행하고 있는지 확인합니다.

```
SW1#sh version
Cisco IOS Software, C2960 Software (C2960-LANBASE-M), Version 12.2(25)FX
```

23) TFTP 서버를 사용하여 c2960-lanbasek9-mz.150-2.SE4.bin으로 업그레이드합니다.

```
SW1#copy tftp flash
Address or name of remote host []? 10.10.10.10
Source filename []? c2960-lanbasek9-mz.150-2.SE4.bin
Destination filename [c2960-lanbasek9-mz.150-2.SE4.bin]? 

Accessing tftp://10.10.10.10/c2960-lanbasek9-mz.150-
2.SE4.bin.... 
Loading c2960-lanbasek9-mz.150-2.SE4.bin from 10.10.10.10:
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
[OK - 4670455 bytes] 

4670455 bytes copied in 3.086 secs (121674 bytes/sec)

SW1#show flash
Directory of flash:/ 

1 -rw- 4414921 <no date> c2960-lanbase-mz.122-25.FX.bin
3 -rw- 4670455 <no date> c2960-lanbasek9-mz.150-2.SE4.bin
2 -rw- 1054 <no date> config.text 

64016384 bytes total (54929954 bytes free) 

SW1#config t
SW1(config)#boot system c2960-lanbasek9-mz.150-2.SE4.bin
SW1(config)#end
SW1#copy run start
```

24) 재부팅하고 스위치가 새 소프트웨어 버전을 실행하고 있는지 확인합니다.

```
SW1#reload
Proceed with reload? [confirm] 

SW1#show version
Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.0(2)SE4, RELEASE SOFTWARE (fc1)
```


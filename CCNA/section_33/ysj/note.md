## Section 33 정리


### Cisco 라우터 및 스위치 기본 보안 설정 요약

1. **접속 모드 및 계층 구조**
   - **사용자 모드**: 제한된 명령어만 사용 가능. (프롬프트: `>`).  
   - **관리자 모드 (Enable 모드)**: 더 많은 명령어 사용 가능. (프롬프트: `#`).  
   - **글로벌 구성 모드**: 장치 설정 수정. (`configure terminal` → 프롬프트 `(config)`).

2. **비밀번호 구성 방법**
   - **콘솔 라인 비밀번호**  
     - 물리적 연결 보호.  
     - 명령어:  
       ```plaintext
       line console 0
       password [비밀번호]
       login
       ```  
   - **VTY 라인 비밀번호 (텔넷/SSH)**  
     - 원격 연결 보호.  
     - 명령어:  
       ```plaintext
       line vty 0 15
       password [비밀번호]
       login
       ```  
   - **활성 프롬프트 비밀번호 (Enable 모드 전환 시 필요)**  
     - 설정 방식:  
       ```plaintext
       enable secret [비밀번호]
       ```  
     - **중요**: `enable secret`은 암호화되며, `enable password`는 평문으로 저장됨.  
     - `enable secret`만 사용하는 것이 최선.  
     - `enable password` 설정이 있다면 `no enable password`로 제거.  
     - 예시:  
       ```plaintext
       enable secret [암호화된 비밀번호]
       no enable password
       ```

3. **비밀번호 암호화**  
   - `service password-encryption`을 사용해 모든 비밀번호를 암호화.  
     - Note: config 설정 파일의 내용을 암호화하여 읽을 수 없게 함. 설정 안하면 sh run에서 사용자 비밀번호가 평문으로 보임. 
   - 명령어:  
     ```plaintext
     service password-encryption
     ```
   - 적용 후 `sh run` 명령을 실행하면 모든 비밀번호가 암호화되어 표시됨.

4. **자동 종료 설정 (Exec Timeout)**  
   - 비활동 시 자동 로그아웃. 기본값: 10분.  
   - 설정 예:  
     ```plaintext
     line console 0
     exec-timeout [분] [초]
     line vty 0 15
     exec-timeout [분] [초]
     ```  
   - 비활성화: `no exec-timeout`.

5. **접속 제한 (ACL 적용)**  
   - 특정 IP에서만 텔넷/SSH 접속 허용.  
   - 명령어:  
     ```plaintext
     access-list 1 permit host [관리자 IP]
     line vty 0 15
     access-class 1 in
     ```

6. **추가 보안 팁**  
   - 라인 수준(콘솔/VTY) 비밀번호와 활성 프롬프트 비밀번호를 모두 설정 권장.  
   - 비밀번호 암호화(`enable secret` + `service password-encryption`)는 기본 설정.  
   - 모든 설정 변경 후 반드시 저장(`write memory` 또는 `copy running-config startup-config`).  

### 사용자 명과 관리자 레벨

1. **라인 레벨 보안**  
   - **콘솔 및 VTY 비밀번호 구성**  
     - 단점: 같은 비밀번호를 사용하면 모든 관리자가 동일한 권한을 가짐.  
     - 명령어 예:  
       ```plaintext
       line console 0
       password [비밀번호]
       login
       line vty 0 15
       password [비밀번호]
       login
       ```  

2. **사용자별 계정 및 비밀번호 구성**  
   - 각 사용자마다 사용자명과 비밀번호를 개별 지정 가능.  
   - 명령어 예:  
     ```plaintext
     username [사용자명] secret [비밀번호]
     line console 0
     login local
     line vty 0 15
     login local
     ```  

3. **관리자 레벨 (Privilege Level)**
   - **레벨 0**: 로그아웃, 활성화, 도움말 등 기본 명령만 사용 가능.  
   - **레벨 1 (기본)**: 읽기 전용 명령 사용 가능.  
   - **레벨 15**: 모든 명령 사용 가능.  
   - 사용자 계정에 특정 레벨 지정 가능:  
     ```plaintext
     username [사용자명] privilege [레벨] secret [비밀번호]
     ```  
     

4. **명령어의 관리자 레벨 변경**  
   - 특정 명령어에 관리자 레벨을 할당 가능.  
   - 명령어 예:  
     ```plaintext
     privilege exec level [레벨] [명령어]
     ```  

5. **활성화 비밀번호에 레벨 지정**  
   - 기본 활성화 비밀번호는 레벨 15에만 적용.  
   - 특정 레벨에 비밀번호 지정 가능:  
     ```plaintext
     enable secret level [레벨] [비밀번호]
     ```  


### **SSH 보안 구성**
- 텔넷은 트래픽이 암호화되지 않아 취약하므로 **SSH 사용 권장.**
- Note: 텔넷은 허용하지 않고, SSH만 사용하는게 안전
- SSH 설정 절차:
  1. 도메인 이름 설정: `ip domain-name example.com`
  2. 인증서 생성: `crypto key generate rsa` (최소 768비트 권장).
  3. VTY 라인에 SSH 전용 입력값 설정: `transport input ssh`.
  4. 로컬 사용자 계정 사용 설정: `login local`.
  5. SSH 버전2 활성화: `ip ssh version 2`.
- SSH 접속: 
  - Linux: `ssh -l username IP`.
  - Windows: PuTTY 사용.

### **AAA 개념 및 필요성**  
- **AAA란**: 인증(Authentication), 권한 검증(Authorization), 계정 관리(Accounting).  
- **기존 로컬 보안의 한계**:  
  - 새 관리자가 들어오거나 나갈 때 모든 라우터와 스위치에 수동으로 사용자 계정을 추가/삭제해야 함.  
  - 라인 레벨 비밀번호 변경 시 모든 장치에서 설정 변경 필요.  
- **AAA 서버 도입 장점**:  
  - 보안 중앙화.  
  - 사용자 인증, 권한, 비밀번호 관리가 중앙 서버에서 이루어짐.  
  - 장치별 수동 관리 필요성 제거.  
  - Note: 서버라는 이름에서 알 수 있듯이, 네트워크에서 특정 역할을 수행하는 독립적인 HOST이다.

**AAA 기능 및 프로토콜**  
- **인증(Authentication)**: 사용자 이름과 비밀번호로 본인 확인.  
- **권한 검증(Authorization)**: 사용자가 수행 가능한 작업을 결정.  
- **계정 관리(Accounting)**: 사용자가 실행한 명령어 및 활동 추적.  
- **AAA 주요 프로토콜**:  
  - **RADIUS**: VPN 등 유저 레벨 서비스에 적합.  
  - **TACACS+**: 관리자 권한 제어 및 세부 명령 제어 가능.  

**AAA 서버와 액티브 디렉토리 통합**  
  - Note 액티브 디렉토리: MS(윈도우)의 사용자 정보 관리 DB, Cisco의 AAA 서버와 별도이나. 관리 및 보안 측면에서 하나로 통합하는게 유리함.
- **장점**:  
  - 하나의 사용자 이름과 비밀번호로 모든 장치 접근 가능.  
  - Cisco 명령어 권한 제어(Cisco AAA 서버)와 Windows 로그인 통합 가능.  
- **통합 과정**:  
  - 라우터가 AAA 서버와 통신해 사용자 정보를 확인.  
  - AAA 서버가 LDAP를 사용해 액티브 디렉토리와 통신.  
  - 도메인 컨트롤러가 그룹 정보를 제공해 권한 부여.  

**AAA 서버 구성 방식**  
- **기본 설정**:  
  - `aaa new-model`: AAA 활성화.  
  - `radius-server host [IP] key [비밀번호]`: RADIUS 서버 추가.  
  - `aaa authentication login default group radius local`: RADIUS 인증 우선, 로컬 사용자 명 대체 옵션 설정.  
- **백업 사용자 계정 설정**:  
  - `username [이름] password [비밀번호]`: AAA 서버 연결 실패 시 사용할 로컬 계정 추가.  
- **RADIUS 및 TACACS+ 새로운 구성 방식**:  
  - 각각 `radius-server`와 `tacacs-server` 명령어 사용.  
  - 서버 그룹 생성 및 우선순위 지정 가능.  

**운영 환경에서의 활용 예**  
- **글로벌 구성**:  
  - 로그인 배너: "관리자 전용" 등의 메시지 표시.  
  - Exec 배너: 인증된 관리자가 아닌 경우 로그아웃 경고 메시지 제공.  
- **보안 유지**:  
  - 중앙 관리로 계정과 권한 변경 시 빠른 적용 가능.  
  - 사용자 활동 추적으로 문제 발생 시 원인 추적 용이.  

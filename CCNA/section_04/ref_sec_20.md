## 한국어 버전

### IOS 명령어 계층 구조

| 모드 | 프롬프트 | 설명 |
|------|----------|------|
| 사용자 실행 | `hostname>` | 기본 사용자 모드 |
| 특권 실행 | `hostname#` | 관리자 모드 ('Enable') |
| 전역 구성 | `hostname(config)#` | 전역 구성 모드 ('Configure Terminal') |
| 인터페이스 구성 | `hostname(config-if)#` | 인터페이스 구성 모드 ('Interface (x)') |

- `Exit`: 한 단계 아래로 내려갑니다.
- `End`: 어느 레벨에서든 특권 실행 모드로 돌아갑니다.

### 명령어 축약

- 명령어의 축약된 버전을 입력할 수 있습니다.
- 예: 'enable' 대신 'en'
- 입력한 내용에 대해 가능한 일치 항목이 하나만 있어야 축약이 성공합니다.

### 상황별 도움말

- 물음표(?)를 입력하여 도움말에 액세스할 수 있습니다.
- `sh?`: 'sh'로 시작하는 모든 명령어 표시
- `show ?`: 'show' 명령어에 사용 가능한 모든 키워드 옵션 표시
- `show ip ?`: 'show ip' 명령어에 사용 가능한 모든 키워드 옵션 표시

### 커서 이동

- Backspace: 이전 문자 삭제
- 화살표 키 (< 및 >): 커서를 좌우로 한 문자씩 이동
- Ctrl-A: 커서를 줄의 시작으로 이동
- Ctrl-U: 전체 줄 삭제

### 명령어 기록

- 위아래 화살표 (^ 및 v): 동일한 계층에서 이전에 입력한 명령어를 순환합니다.

### 명령어 출력 표시

- Enter: 'show' 명령어 출력을 한 줄씩 스크롤하여 표시
- Spacebar: 페이지 단위로 표시
- Ctrl-C: 'show' 명령어 출력을 중단하고 명령 프롬프트로 돌아감

### 파이프 명령어 예시

```
show running-config interface FastEthernet0/0
show running-config | begin FastEthernet0/0
show running-config | include FastEthernet0/0
show running-config | exclude FastEthernet0/0
show running-config | section interface
```

## English Version

### IOS Command Hierarchy

| Mode | Prompt | Description |
|------|--------|-------------|
| User Exec | `hostname>` | Basic user mode |
| Privileged Exec | `hostname#` | Administrator mode ('Enable') |
| Global Configuration | `hostname(config)#` | Global configuration mode ('Configure Terminal') |
| Interface Configuration | `hostname(config-if)#` | Interface configuration mode ('Interface (x)') |

- `Exit`: Drops back down one level
- `End`: Returns to Privileged Exec mode from any level

### Command Abbreviation

- You can enter an abbreviated version of a command
- Example: 'en' instead of 'enable'
- Abbreviation succeeds only if there's one possible match for what you typed

### Context Sensitive Help

- Enter a question mark to access Help
- `sh?`: Shows all commands that begin with 'sh'
- `show ?`: Shows all available keyword options for the 'show' command
- `show ip ?`: Shows all available keyword options for the 'show ip' command

### Moving the Cursor

- Backspace: Deletes the previous character
- Arrow keys (< and >): Moves the cursor left and right one character at a time
- Ctrl-A: Moves the cursor to the beginning of the line
- Ctrl-U: Deletes the whole line

### Command History

- Up and down arrows (^ and v): Cycles through previously entered commands at the same level in the hierarchy

### Showing Command Output

- Enter: Shows 'show' command output line by line
- Spacebar: Shows output page by page
- Ctrl-C: Breaks out of the show command output and returns to the command prompt

### Piped Command Examples

```
show running-config interface FastEthernet0/0
show running-config | begin FastEthernet0/0
show running-config | include FastEthernet0/0
show running-config | exclude FastEthernet0/0
show running-config | section interface
```

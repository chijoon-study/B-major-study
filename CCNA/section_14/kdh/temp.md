## speed, duplex
인터페이스에서의 속도와 이중화는 매우 중요하다.  
두 포트간 이중화와 속도를 동일하게 맞춰주지 않으면 인터페이스가 종료되거나 속도가 매우 느려지기 때문이다.  
만약 두 포트의 속도를 다르게 설정하면 인터페이스가 down되어버린다.  
이중화를 다르게 설정하면 인터페이스가 down되지는 않지만 충돌이 매우 자주 일어나므로 속도가 현저히 떨어진다.  


## show ip interface brief
`sh ip int b`를 했을때 나오는 결과의 status와 protocol부분을 보고 어느 문제인지 확인할 수 있다.  
이전 섹션의 과제에도 나왔던 administratively down으로 돼있다면 `no shutdown`을 통해 인터페이스를 활성화해주어야한다.  
관리자는 인터페이스를 임의로 on/off 시킬 수 있다.  

만약 down/down이라면 1계층 이슈이다.  
케이블 연결이 안돼있거나, 반대쪽 장치가 꺼져있거나, 반대쪽 인터페이스가 꺼져있거나.  

만약 up/down이라면 2계층 이슈이다.  
위에서 언급한 속도의 mismatch가 이를 유발한다.  


## cdp, lldp
lldp(link layer discovery protocol)은 cdp(cisco discovery protocol)의 국제표준버전이다.(cdp가 더 일찍 나왔다.)  
cdp는 접속한 장치에 연결된 장치들의 정보를 알려준다.  
명령어는 `show cdp` `show cdp neighbors` `show cdp neighbors detail`이고 `cdp run` `no cdp run` `no cdp enable`를 통해 전역이나 특정 인터페이스에서 활성화/비활성화가 가능하다.  
lldp또한 동일하고 위 명령어에서 cdp만 lldp로 변경하면 되지만, 결과에서 가상 보조 인터페이스를 보여주지 않지만 리눅스 서버를 보여주고, 비활성화에서 `no lldp transmit` `no lldp receive` lldp 정보를 비활성화할때 송/수신 을 정할 수 있다.  
또한 cdp는 기본적으로 활성화 돼있지만 lldp는 버전에따라 기본 활성화 여부가 다르다.  

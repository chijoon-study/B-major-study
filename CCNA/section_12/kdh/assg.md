## configure the routers as DNS Clients
강의에서 나온 명령어를 모든 라우터에서 입력해주었다.
1. `en`
2. `conf t`
3. `ip domain-lookup`
4. `ip name-server 10.10.10.10`

ping을 사용해 서로서로 IP주소가아닌 R1,R2,R3를 통해서도 요청이 가는 것을 확인함


## Examine the ARP cache on the routers
R1에서 `sh arp`를 입력했을때 R3는 보이지 않는다.  

R1과 R3가 R2를 통해 나눠져있기 때문으로 예상 
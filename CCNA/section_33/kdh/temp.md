## cisco device security
씨스코 장치에서 보안도 중요하다.  
대표적으론 일전에 배웠던 password, secret이 있다.  
말했듯이 최근엔 secret만 사용하면된다.  
각 장치마다 전부 secret을 설정해주면 이후 유지보수에 정말 귀찮아지니 따로 AAA서버를 둔다.  

콘솔케이블로 연결할때는 상관없겠지만 원격으로 라우터에 접근할땐 중간에 스니핑을 당할 수도있다.  
라우터에 원격으로 접근하는 방법은 telnet, ssh가 있는데 telnet은 plain text로 통신하므로 스니핑 당할 시 secret도 유출될 수 있다.  
ssh는 데이터를 암호화해 통신하므로 안전하다.  

## OSPF process ID
![](src/OSPF_process_ID.png)
OSPF에는 process ID라는 것이 존재한다.  
라우터에서 OSPF 구성시  `router ospf {process ID}`라는 명령어를 입력하게 되는데 process ID는 로컬, 즉 한 라우터 내에서만 영향을 끼친다.  
이게 무슨말이냐하면 위 사진에서 R2는 R1, R3와 정상적으로 인접성을 이룬다.  
process ID가 서로 다르지만 상관없기 때문이다.  
하지만 로컬 내에선 process ID가 다르면 다른 인스턴스를 사용한다는것이고 데이터베이스도 공유하지 않게 되는데 때문에 위 사진에서 R1과 R3는 서로의 정보를 학습하지 못하게 된다.  
R2의 두 인터페이스간의 process ID가 다르므로 서로의 데이터베이스가 공유되지 않는데 각 데이터베이스에 따로 R1과 R3의 네트워크 정보가 담겨있기 때문이다.  

## route injection


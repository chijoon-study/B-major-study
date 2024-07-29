> Hey I just met you  
The network’s laggy  
But here’s my data  
So store it maybe  


## fault and partial failure
싱글 컴퓨터 환경에서는 두가지 상황밖에 없다.  
- 정상 작동
- 작동 안함

작동안함의 경우 대개 소프트웨어의 문제이다.  
컴퓨터는 같은 입력이오면 같은 결과를 뱉을 뿐이기 때문이다.  
하지만 분산 컴퓨팅 환경에서는 다르다.  
> “In my limited experience I’ve dealt with long-lived network partitions in a single data center (DC), PDU [power distribution unit] failures, switch failures, accidental power cycles of whole racks, whole-DC backbone failures, whole-DC power failures, and a hypoglycemic driver smashing his Ford pickup truck into a DC’s HVAC [heating, ventilation, and air conditioning] system.  
> And I’m not even an ops guy.   
> -- Coda Hale”

정말 어떤 방식으로든 문제가 발생할 수 있고, 더 큰 문제는 이 것이 서비스의 완전한 에러가 아닌 부분적으로만 발생되게 된다는 것이다.  
때문에 문제를 인식하는 것조차 어려울 수 있다.  
때문에 정말 비관적으로 당연히 문제가 발생할 것이라 가정하고 이에 대응하는 소프트웨어 레벨에서의 설계를 해두는 것이 좋다.  

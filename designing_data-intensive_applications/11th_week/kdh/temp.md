## in my experience ..
필자는 "내 경험상 99%의 상황에선 x면 충분하더라"는 기술 x의 유용성보다는 화자의 경력을 나타내는 말이라고 한다.

## Derived data versus distributed transactions
분산 트랜잭션과 derived data system은 비슷한 목표를 가졌지만 수단이 다르다.   
분산 트랜잭션은 보통 linearlizability를 동반하고 derived data system은 eventually consistency이다.  
ddia의 필자는 분산트랜잭션은 구린 fault tolerance를 가졌다고 생각하고 더 좋은 프로토콜이 나올 수 있을거라 기대하지만 이는 단시간 내에 이루어지기 어렵다고 생각한다.  
때문에 필자가 기대하는 유토피아가 오기전까진 참고 eventual consistency를 필수 불가결하게 사용해야한다고 한다.

eventual consistency를 사용할 경우 어쩔 수 없이 인과 문제가 생길 수 있다.  
하지만 11장에서도 말했지만 사실 서로 관계가 없는 이벤트끼리는 인과 관계를 보장해줄 필요가 없다.  
그럼에도 현재로서는 모든 이벤트가 인과 관계를 보장하기 위한 시스템에 의해 불필요한 병목을 겪거나, 전부 인과 관계를 무시해 문제가 발생할 수 있는 두 방법밖에 없다.  
필자는 아마도 시간이 지나면 모든 이벤트가 인과 관계를 보장하기 위한 시스템에 병목을 겪지 않으며 인과 관계가 있는 데이터간의 순서는 올바르게 유지할 수 있는 앱 개발 패턴이 등장할 거라 기대한다.  


## linearizability
공통적으로 사용되는 가자 강한 일관성 모델중 하나이다.  
클라이언트 측에서 단 하나의 DB 복제본만 있다고 생각하게 끔 하는 것이 목적이다.(하나의 복제본이면 총 두개의 DB를 말하는건가??)  

말로만 들으면 조금 모호하다. 실제 예시를 통해 알아보자.  
![](linearizability_1.png)
클라이언트 측에서 생각했을때 위 사진은 전혀 모호하지 않고 정확하다.  
그저 단하나만 정해주면 된다.  
write 중의 read를 0으로 반환해줄지 1로 반환해줄지.  
이를 linearizability에서는 다음과 같이 정한다.  
![](linearizability_2.png)
write중에 어떤 replica가 write중인 값을 읽었다면 다른 모든 replica도 write중인 가장 최신값으로 읽는다.  
미래에 write연산이 실패할지는 고려하지 않는다.  
만약 위 사진에서 A가 0으로 읽었다면 B는 0을 반환해도 되고 1을 반환해도 되지만, 이전 요청인 A가 1을 반환해줘버렸으면 무조건 1을 반환해줘야한다.  

이러한 특성은 다음과 같은 상황을 해결해준다.  
![](linearizability_case.png)
Bob은 Alice보다 늦게 요청을 보냈음에도 더 오래된 값을 보고 있다.  
하지만 위의 linearizability대로라면 그런일은 일어날 수 없다.  
때문에 recency guarantee라고 불리기도 한다.  
linearizability에서는 무조건 모든 연산을 atomic 연산으로보고 여러 연산을 하나로 묶지 않기에(transaction) 트랜잭션이 보장해주던 write-skew같은 문제는 해결해주지 않는다.  

> 근데 여기서 하나 의문인 것이  
> 문제상황같은게 발생하는 이유가 network delay로 인한 replication lag때문인데  
> 다른 replica에서 가장 최신값을 보여줬는지 아닌지를 알려주는 것도 결국 network를 통해 전해줘야 하는데.. 이 뭔..  
> 아직 linearizability를 다 읽은건 아니라 이후에 설명할 수도 있긴한데  
 
이런 linearizability가 필요한 상황은 사실 정의할 수 있다.  
바로소통 하는 두 개체간에 또 다른 채널이 있을때다.  
위의 문제 상황을 생각해보자 Alice가 만약 없었다면 Bob은 본인이 보고 있는 화면이 이상하다 느꼈을까?  
여러번 새로고침하다가 결국엔 경기 결과를 보게 됐을거다.  
하지만 기존 두 객체(Bob과 서버)에 새로운 채널(Bob과 Alice간의 대화)이 추가 됐기에 문제 상황이 된 것이다.  

![](when_linearizability_useful.png)
위 상황에선 아직 file storage에 실제로 이미지가 업데이트 되지 않았을때 image resizer가 이미지를 fetch하는 문제가 발생할 수 있다.  
이 또한 기존 두 객체(web server, image resizer)사이에 추가적인 채널(message queue)이 존재하기 때문이다.   

하지만 대부분의 시스템과 RAM조차 이러한 linearizability를 구현하지 않는다.  
구현상 linerizability와 성능은 양립할 수 없기 때문이다.


## ordering 
느꼈겟지만 이벤트의 순서관련해서 이 책에서 매우 반복적으로 다룬다.  
그리고 이는 이 "순서"라는 것이 중요하다는 것을 암시한다.  
이 순서가 중요한 이유중 하나는 순서가 인과를 관리하기 때문이다.

이전에 알아봤던 예시로 정신분열증이 있거나 미래를 보는 것이 아닌 이상 인간은 직관적으로 당연히 질문이 먼저 나오고 그 이후에 답변이 나올 거라 생각한다.  
하지만 replica에서 만약 질문 이벤트와 답변 이벤트의 순서가 바뀌는 일은 충분히 일어날 수 있는 일이다.


## total order vs partial order
이벤트 순서에는 두가지 종류가 있다. total order, partial order.  
사실 두 종류라고 보기에는 애매한게 total order아래 partial order가 있다. total order가 보장되면 partial order도 보장된다는 뜻이다.  

그래서 total order랑 partial order가 뭐냐하면 total order는 Linearizable한 시스템처럼 모든 이벤트가 하나의 timeline에서 일어난다.  
동시에 일어나는 이벤트는 없고 무조건 한 이벤트는 어느 이벤트의 뒤에 일어난다.

partial order는 대부분 사용해봤을 git을 생각하면 쉽다.  
이벤트들은 branch, merge된다.  
5장에서 알아봤듯이 이벤트는 총 3가지 종류로 나눠진다. 
- a happened before b
- b happened before a
- happen concurrently

어느 이벤트들은 서로 인과관계가 있을 수도 있고, 어느 이벤트들은 단순히 동시에만 일어날 수도 있다.  
git에서도 같은 파일을 작업하는 경우에 브랜치를 새로 파서 이후에 merge하고, 혼자하고 있는 작업에선 원래하던 브랜치에서 계속 작업하면 된다.  
그리고 이는 결국 하나의 timeline인 main branch로 모인다.  
때문에 total order아래에 partial order가 있다고 한 것이다.  

사실 linearizability를 요구하는 시스템, 즉 total order가 보장되어야하는 시스템은 사실 partial order만 보장되도 충분하다.  
위에서 말했듯이 linearizability를 구현할 경우 성능이 매우 떨어지기 때문에 실제 시스템들은 훨씬 구현상 효율적인 partial order를 보장하게끔 구현한다.  


## sequence number ordering
위에서 이야기한 두 이벤트 간의 인과관계를 결정하는데에 쓰이는 방법이 쓰기전 읽은 데이터의 버전을 확인하는 것이다.  
작동 방식은 5장에서 다뤘었으니 넘어가고, "데이터의 버전"에 좀더 집중해보자면,  
만약 싱글리더 방식을 사용한다면 단순히 리더가 logical timestamp를 사용해 버전을 1씩증가시키면 될 것이다.  
하지만 멀티리더나 리더리스 방식을 사용한다면 좀 복잡해진다.  

뭐 노드에 미리 버전 범위 할당, 물리적 timestamp 등등 방법이 있지만 전부 하나씩 문제가 있고, 주로 쓰이는 방법은 lamport timestamp이다.  
![](lamport_timestamp.png)

(counter, node_identifier)로 버전이 이루어져있고, 두 타임스탬프를 비교할때 카운터를 먼저비교하고 이후에 node id를 비교한다.  
클라이언트와 노드는 maximum counter즉 가장 최신버전의 번호를 기억하고있는다.  
그리고 요청시 만약 클라이언트의 maximum counter가 노드의 maximum counter보다 크다면 노드의 maximum counter를 최신 버전으로 업데이트하고 vice versa.  
> 그러면 위 사진에서 a가 write max=1 을 node2가 아니라 node1에 했다면   
> node1의 데이터는 (2,1)로 쓰일테고 그러면 (4,2)보다 늦게 쓰였지만 더 옛날값이 되게 되는데..  

하지만 이렇게 데이터의 버전을 정해주는 것으로 모든 분산시스템의 문제를 해결해주는 것은 아니다.  
계정 생성중에 닉네임 중복확인하는 케이스를 생각해보자,  
동시에 같은 닉네임으로 생성했다. 이후에 타임스탬프를 확인해 더 높은값의 데이터를 삭제하고 실패한것으로 처리했다.  
정상적인가? 보통 계정을 생성하고있다하면 현재, 지금 당장 닉네임이 중복되지 않는지 확인하고 만약 중복됐다면 계정이 생성되면 안된다. 계정을 생성한 이후에 계정을 삭제하는 것이 아니라.  
하지만 만약 지금당장 같은 닉네임으로 생성하고있는 트랜잭션이 있는지 확인하려면 모든 노드를 확인해야하고 매 요청 이 과정을 거쳐야한다면 성능상의 비용이 너무 비싸다.  


## Distributed Transactions and Consensus
합의알고리즘은 매우 중요하다. 또한 사실 어떠한 문제도 발생하지 않는 상황이라면(네트워크 lag, node failure 등등) 매우 간단하다.  
하지만 당연히 분산시스템에서 문제가 발생하는건 당연지사이고 합의알고리즘이 간단하다는 신념위에 지어진 시스템들은 대부분 고장이났다.  

사실 FLP결과에 따르면 노드가 고장날 수 있는 환경에서는(분산시스템의 일반적인 환경) 항상 합의를 이룰수 있는 알고리즘이 절대 없다는 것이 증명됐다.  
그럼 이번 챕터에선 뭘하냐? 사실 FLP가 증명된 조건은 정말 빡빡한 조건, 타임아웃이나 시간을 사용할 수 없는 결정론적인 알고리즘을 가정했기에 불가능하단 것이다.  
때문에 현실에선 어떻게 합의알고리즘에 도달했는지를 이번챕터에서 알아볼 것이다.  


### 2PC
합의 알고리즘 중 가장먼저 알아볼 것은 2PC(2-phase-commit)이다.
![](2PC.png)
말그대로 커밋을 두 단계로 나누는 방식인데, coordinator가 필요하다.  
1. 트랜잭션이 실행될 노드(participant)에 트랜잭션을 실행시킨다.  
2. participant로부터 커밋이 가능한지 여부를 물어본다.(prepare 단계) 만약 yes라면 해당 트랜잭션을 participant는 이후에 그 어떤 문제가 발생해도 직접 abort 할 수 없다.
3. 만약 모든 응답이 yes라면 commit하고 하나라도 no라면 abort한다.

만약 prepare단계에서 participant에 문제가 생길 경우 어짜피 coordinator가 abort할 것이고  
commit 단계에서 문제가 participant에 문제가 생길 경우 coordinator가 무한으로 retry한다.  

coordinator에 문제가 생기는 경우는 in-doubt 또는 uncertain 말그대로 불확실한 상황에 빠지게 되는데, 이때는 coordinator가 되살아나 retry하기 전까지 participant는 무한 대기 상태에 빠진다.  
또한 되살아날때 retry하기 위해 2PC작동방식의 2번째 단계에서 commit or abort요청을 보내기전에 coordinator에 어떤 결정을했었는지 기록해둔다.  

하지만 2PC의 영향을 받는 모든 시스템은 2PC를 따라야한다.  
예를 들어 트랜잭션 성공시 이메일을 보내는 시스템이 있다면 coordinator의 무한 retry동안 이메일서버로는 계속 메일을 보내지만 트랜잭션은 계속 실패하는 상황이 생길 수 있다.  
이를 exactly-once 문제라고도 부르는데 이는 11장에서 좀더 알아볼 것


### in-doubt lock
데이터 일관성 보장을(dirty write, 2PL) 위해 트랜잭션중에는 다루는 객체에 lock이 걸린다.  
in-doubt상태에서는 트랜잭션이 끝나지 않고 계속 lock을 걸고 있기에 문제가 생길 수 있다.  

하지만 분산 트랜잭션 중 고아 트랜잭션이 생길 수 있다.(coordinator가 트랜잭션의 존재를 잊음)  
이때는 관리자가 직접 abort나 commit을 해주어야하는데 이는 매우 귀찮고 고된 작업이다.  
때문에 participant가 단독으로 abort나 commit하는 휴리스틱 결정이라는 방법이 있는데, 이는 atomicity를 해칠 수 있으므로 정말 재앙적인 상황에서만 조심스럽게 사용된다.  



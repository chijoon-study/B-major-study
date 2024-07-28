## 재시도
에러 핸들링에서 재시도는 간단하고 효과적인 방법이지만 완벽하지는 않다.  

예를 들어 서버에서는 요청 처리가 성공했지만 성공했다는 정보를 보내는 과정에서 네트워크 에러가 생기면 클라이언트는 해당 요청이 실패했다고 생각하게 되고 재시도릃 하게 된다.  
이 경우 같은 요청이 두번 발생하는 것이므로 예상하지 않은 결과가 나올 수 있다.  
때문에 이 경우 '멱등성'을 지켜주도록 애플리케이션 레벨에서 설계해두는 것이 좋다.

더 많은 케이스가 있지만 하나 더 알아보자면  
과부하 때문에 요청이 실패한 경우 재시도는 과부하 상태를 더 악화시킬 수도 있다.  
때문에 재시도 최대 횟수를 정해 놓는 것도 좋은 방법이다.


## weak isolation
가장 강한 isolation 레벨에는 serializable이 있다.  
모든 트랜잭션을 한 time에 하나만 처리 한다는 의미이다.  
하지만 이는 매우 비싼 성능 비용을 요구하기에 현실적으론 잘 쓰이지 않는다.  
때문에 이보다는 조금 완화된 isolation레벨들이 존재한다.  
하지만 serializable비해 동시성 문제가 일어날 수 있다.  
때문에 여러 종류의 weak isolation에 대해 알아보고 무엇이 현재 애플리케이션에 적절한지 판단할 수 있어야한다.  

### read committed
첫번째로는 read committed이다.  
read committed가 보장하는 것은 아래와 같다.  
- DB로부터 읽기를 할 때 commit된 데이터만 읽는다. (no dirty reads)
- DB로부터 쓰기를 할 때 commit된 데이터만 덮어쓴다. (no dirty writes)

read-committed도 skew가 발생할 수 있는데 아래와 같은 경우이다.  
![](./read-committed-skew.png)

이러한 문제는 오랜시간이 걸리는 쿼리나(대개 분석용 쿼리) 백업에서 치명적일 수 있다.  
백업또는 무거운 쿼리중에도 DB에는 계속 쓰기가 발생할 수 있고 그럴 경우   
백업본에는 어느 부분은 old data 어느 부분은 new data가 있을 것이고    
분석용 쿼리의 결과는 뒤죽박죽 섞여있을 것이다.  
이런 문제를 해결할 매커니즘이 snapshot isolation이다

snapshot isolation은 MVCC(multi version concurrency control)기법을 기반으로 구현된다.  
MVCC는 객체의 여러버전을 유지하는 방법이다.  
트랜잭션 별로 incrementing ID가 있고 본인 ID보다 높은 ID가 수정한 row를 읽을 경우 이전 버전을 찾아간다.  

### lost update 
위 방법들은 모두 read-only쿼리와 concurrency write간의 동시성 문제를 해결하는 방법이었다.  
하지만 만약 쓰기를 하는 두 트랜잭션간의 동시성 문제가 발생한다면?  
이 경우엔 단순히 읽었을때 어떤 값이 나오느냐 말고도 본인이 write한 정보가 사라질 수 있다.  

가장 간단한 방법은 lock이다.  
애플리케이션에서 객체를 명시적으로 lock걸고 만약 다른 트랜잭션에서 같은 객체를 읽으려하면 read-modift-write 사이클이 끝날때까지 기다리도록 한다.  

또 다른 방법은 compare-and-set이다.  
```sql
UPDATE wiki_pages SET content = 'new content'
  WHERE id = 1234 AND content = 'old content';
```
쿼리의 where clause를 보면 content = 'old content'가 있다.  
즉 read단계에서 읽은 값이 변경된적이 없을때만 위 쿼리가 실행되는 것이다.  
하지만 이도 동시성 문제가 발생할 수 있는데, 다른 쓰기가 진행 중에는 위 조건이 참일 수 있기 때문이다.  

동시성 문제는 복제 DB환경에서 더 복잡해지는데  
위에서 설명한 두 방법은 최신 복사본이 하나만 있다고 가정할때 가능한 방법이기 때문이다.  
때문에 복제 DB환경에서는 처음부터 동시 쓰기를 막는것이 아니라(사실상 불가능) 허용한 이후에 동시 쓰기가 감지 됐을 경우 애플리케이션 코드나 특별한 데이터 구조를 통해 해결한다.  

atomic operation(수정을 read-modify-write의 사이클로 보는 것이 아닌 하나의 update연산으로 보는 것)이 update가 가환 연산일 경우 복제 DB환경에서 유효할 수 있다.  
Riak에서는 값이 동시에 update돼었을 경우 자동적으로 두 update 연산을 병합해 update lost를 막는다.  
당연히 가환 연산이 아니라 LWW 연산의 경우 불가능하다.  
어떤 연산이 먼저 실행됐는지 알 수 없기 때문이다.([이러면 또 이전의 동시성 문제 해결로.. ](../../4th_week/kdh/temp.md))


## serializability
동시성 문제를 해결하기위해 여러 isolation level에 대해 알아보았지만, 위 방법들로도 결국에는 막을 수 없는 동시성 문제도 존재하고, 본인 애플리케이션이 어느 isolation level에 적합한지 판단하는 것도 정말 어려운 일이다.  
때문에 많은 연구자들은 결국에 가장 간단한 답변으로 serializability를 사용하라고 한다.  
serializability는 간단히 모든 동시성 문제의 발생 가능성을 막는 것이다.  
애초에 트랜잭션이 동시에 수행되지 않도록 하는 것이니.  
하지만 그럼에도 대부분의 애플리케이션이 serializability를 사용하지 않는다.  
왜 사용하지 않는지 또 serializability의 구현방법에 대해 알아보자.  
대부분의 DB는 serializability를 세가지 기술중 하나를 통해 제공한다.  
- Actual serial Execution
- Two-Phase Locking (2PL)
- Serializable Snapshot Isolation (SSL)


### Actual Serial Execution
Actual Serial Execution은 정말 말그대로 싱글스레드에서만 트랜잭션을 수행하는 것으로 구현한다.  
간단명료한 아이디어이다.  
하지만 좋은 성능을 위해 멀티스레드가 필수적이라고 지난 30년간 고려 돼왔지만 최근에 들어서는 싱글스레드 방식도 실현 가능하다고 평가 돼고 있다.  
이는 RAM의 폭발적인 성장과 OLTP(대개 작고 짧은 쓰기), OLAP(read only 트랜잭션) 트랜잭션의 이해도가 높아짐 덕분이다.  

하지만 그럼에도 성능상에 단점은 분명하고 위 방법을 사용하려면 아래 조건이 충족되어야 한다.
- 단일 CPU코어에서 처리할 수 있을정도의 낮은 쓰기 처리량
- 여러 파티션에 접근하는 트랜잭션이 있으면 안됨


### 2PL
2PL은 lock이 좀더 깐깐해진 느낌이다.  
snapshot isolation에서 읽기가 다른 쓰기를 block하지 않고 그 역도 동일하다면, 2PL에서는 
- 같은 객체에 대해서 다른 트랜잭션이 read중이라면 write할 수 없음
- 같은 객체에 대해서 다른 트랜잭션이 write중이라면 read할 수 없음


근데 동시성 문제가 가장 쉽게 일어나는 write중 write는 가능한건가보니 안된다고함 
https://chatgpt.com/c/fd7131d8-87eb-4d24-9311-e2b1438a4b55


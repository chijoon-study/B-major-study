## 03장. 저장소와 검색

별로 막 인상깊은 부분은 없어서, 후기 위주로 이야기

1. LSM Tree, B Tree를 설명하는데, 자료구조 자체라기보다는 DBMS에서 어떻게 사용되는지 다룬다.
    - 자료구조와 그 응용이나 확장이라고 봐야 할 것 같은데, LSM Tree, B Tree가 전부 이런 식으로 사용되는 것처럼 설명되는거 같아 아쉽다.
    - 근데 뭐... LSM Tree만 해도 태생이 DBMS에서 사용되기 위한 걸로 알아서, 별로 구분하는게 의미 없을 것 같기도 하다.

2. LSM Tree는 저쟝 효율성이 좋지만, 전체적인 용량 차이는 더 클 수도 있다고 생각한다. (효율성 != 적은 용량)
    - LSM Tree가 순차적으로 저장되고, compaction을 수행하므로 저장 효율성이 좋은건 맞지만, 중복이 발생한다.
    - B Tree는 페이징 방식에 Random I/O라 저쟝 효율성이 낮지만, 중복이 발생하지 않고, 수정하는 방식이다.
    - 둘 다 지원하는 유명한 DBMS가 내가 알기로는 없고, NoSQL(DocumentDB)와 RDBMS(정규화)가 쌓이는 데이터의 절대적인 크기가 달라서 별 의미가 없을 수도 있음.

3. Sequential I/O와 Random I/O
    - LSM Tree랑 B Tree의 효율성 설명할 때 중요한 개념이라고 생각하는데, 설명을 안 해줘서 좀 아쉬움.
    - 읽기/쓰기 모든 부분에서 LSM Tree는 Sequential I/O 위주인 반면, B Tree는 Random I/O이다.
    - 아마 이후 장에서 나올수도 있는데, 찾아보면 좋을듯.
    - [내가 관련해서 정리한거](https://github.com/YangSiJun528/memory/blob/master/notes/series/cs_bookmark/DataBase%20-%20RDB,%20NoSQL,%20index%20%EB%93%B1.md#btree-%EC%9D%B8%EB%8D%B1%EC%8A%A4%EA%B0%80-%EB%8A%90%EB%A6%B0-%EC%9D%B4%EC%9C%A0)


# 추가

이야기하면서 추가로 이야기한 내용.

inmemoryDB 조회 속도 빠른 이유 != 메모리에 데이터를 저장하기 때문
왜? 디스크 DB도 메모리 캐싱하기 떄문.

실제 빠른 이유: **디스크 관리 관련 오버헤드 없음** + 연산 속도 빠름 + (redis: 싱글 스레드로 인한 락 오버헤드 X) 
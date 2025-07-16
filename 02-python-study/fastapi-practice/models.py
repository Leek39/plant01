# Flask 의존성 없이 순수 SQLAlchemy 사용
from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone

# ===== 1. 기본 클래스 생성 =====
# 모든 모델의 부모 클래스를 만듭니다
# Spring Boot JPA의 @Entity 기본 기능과 비슷합니다
Base = declarative_base()

# Spring Boot JPA 비교:
# @Entity
# public class Todo extends BaseEntity {

# ===== 2. 데이터베이스 모델 정의 =====
class Todo(Base):
    """
    순수 SQLAlchemy를 사용한 Todo 모델
    
    Flask-SQLAlchemy와의 주요 차이점:
    - Base를 상속 (db.Model이 아님)
    - Column()을 직접 사용 (db.Column이 아님)
    - Flask 컨텍스트 불필요
    """

    # 테이블 이름 지정 (필수!)
    __tablename__ = 'todos'

    # 기본키 + 자동증가
    # Spring Boot JPA 비교: @Id @GeneratedValue
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 문자열 컬럼 (최대길이 200, 필수값)
    # Spring Boot JPA 비교: @Column(nullable = false, length = 200)
    title = Column(String(200), nullable=False)

    # 불린 컬럼 (기본값 False)
    # Spring Boot JPA 비교: @Column(nullable = false)
    # private Boolean completed = false;
    completed = Column(Boolean, nullable=False, default=False)

    # 시간 컬럼들 (UTC 시간대 사용)
    # Spring Boot JPA 비교: @CreatedDate, @LastModifiedDate
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)  # 생성 시점 자동 설정
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)  # 수정 시점 자동 업데이트
    )

    def __repr__(self):
        """
        객체를 문자열로 표현 (디버깅용)
        Java의 toString() 메소드와 같은 역할
        """
        return f'<Todo {self.id}: {self.title}>'

    def to_dict(self):
        """
        모델을 딕셔너리로 변환 (JSON 응답용)
        Spring Boot의 @JsonSerialize 또는 수동 DTO 변환과 같음
        """
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# ===== 3. 데이터베이스 연결 설정 =====
# 데이터베이스 URL 설정
# Spring Boot 비교: application.properties의 spring.datasource.url
DATABASE_URL = "sqlite:///todos.db"

# 데이터베이스 엔진 생성
# Spring Boot 비교: DataSource 설정
engine = create_engine(
    DATABASE_URL,
    echo=True  # True로 설정하면 SQL 쿼리 로그 출력 (spring.jpa.show-sql=true와 같음)
)

# 세션 팩토리 생성
# Spring Boot 비교: EntityManagerFactory
SessionLocal = sessionmaker(
    autocommit=False,  # 수동 트랜잭션 제어
    autoflush=False,   # 수동 플러시 제어
    bind=engine        # 우리가 만든 엔진에 연결
)

# ===== 4. 데이터베이스 테이블 생성 =====
# 모델에 정의된 모든 테이블을 생성
# Spring Boot 비교: spring.jpa.hibernate.ddl-auto=create-drop
Base.metadata.create_all(bind=engine)

# ===== 5. 데이터베이스 세션 관리 =====
def get_db():
    """
    FastAPI용 데이터베이스 세션 의존성
    Spring Boot 비교: @Autowired EntityManager
    
    FastAPI 엔드포인트에서 사용법:
    @app.get("/todos")
    def get_todos(db: Session = Depends(get_db)):
        return db.query(Todo).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
1. **SQLAlchemy 핵심 구성요소**:
   - Base: 모든 모델의 기본 클래스
   - Column: 데이터베이스 컬럼 정의
   - Engine: 데이터베이스 연결 관리자
   - Session: 데이터베이스 트랜잭션 관리자

2. **데이터 타입들**:
   - Integer: MySQL INT, PostgreSQL INTEGER
   - String(n): MySQL VARCHAR(n), PostgreSQL VARCHAR(n)
   - Boolean: MySQL BOOLEAN, PostgreSQL BOOLEAN
   - DateTime: MySQL DATETIME, PostgreSQL TIMESTAMP

3. **제약조건들**:
   - primary_key=True: 기본키 제약조건
   - nullable=False: NOT NULL 제약조건
   - default=값: 기본값 설정
   - autoincrement=True: 기본키 자동증가

4. **세션 관리 방법**:
   - SessionLocal(): 새 세션 생성
   - session.query(Model): 데이터 조회
   - session.add(객체): 데이터 추가
   - session.commit(): 변경사항 저장
   - session.rollback(): 변경사항 취소
   - session.close(): 연결 종료

5. **Flask-SQLAlchemy에서 마이그레이션**:
   - db.Model → Base
   - db.Column → Column
   - db.session → SessionLocal()
   - Flask app context → 직접 세션 관리
"""
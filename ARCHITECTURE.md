# 헥사고날 아키텍처 (Hexagonal Architecture)

이 프로젝트는 헥사고날 아키텍처(Ports and Adapters 패턴)로 구조화되어 있습니다.

## 아키텍처 개요

헥사고날 아키텍처는 비즈니스 로직을 외부 의존성으로부터 분리하여 유지보수성, 테스트 용이성, 확장성을 향상시키는 아키텍처 패턴입니다.

## 디렉토리 구조

```
app/
├── domain/                          # 도메인 계층 (핵심 비즈니스 로직)
│   ├── entities/                    # 도메인 엔티티
│   │   └── todo.py                 # Todo 엔티티 (비즈니스 규칙 포함)
│   ├── repositories/               # 레포지토리 인터페이스 (Ports)
│   │   └── todo_repository.py      # TodoRepository 인터페이스
│   └── exceptions.py               # 도메인 예외
│
├── application/                     # 애플리케이션 계층 (유즈케이스)
│   ├── dtos/                       # 데이터 전송 객체
│   │   └── todo_dto.py            # Todo DTO
│   └── use_cases/                  # 유즈케이스 (비즈니스 플로우)
│       ├── create_todo.py         # Todo 생성
│       ├── get_todo.py            # Todo 조회
│       ├── list_todos.py          # Todo 목록 조회
│       └── delete_todo.py         # Todo 삭제
│
├── adapters/                        # 어댑터 계층
│   ├── inbound/                    # Primary Adapters (입력 어댑터)
│   │   └── api/                    # REST API 어댑터
│   │       ├── todos.py           # API 엔드포인트
│   │       └── schemas.py         # Marshmallow 스키마
│   └── outbound/                   # Secondary Adapters (출력 어댑터)
│       └── persistence/            # 데이터베이스 어댑터
│           ├── models.py          # SQLAlchemy 모델
│           └── todo_repository.py # TodoRepository 구현
│
└── infrastructure/                  # 인프라 계층
    ├── config.py                   # 애플리케이션 설정
    ├── database.py                 # 데이터베이스 설정
    ├── extensions.py               # Flask 확장
    └── container.py                # 의존성 주입 컨테이너
```

## 계층별 설명

### 1. Domain Layer (도메인 계층)

**목적**: 핵심 비즈니스 로직과 규칙을 포함합니다. 외부 의존성이 전혀 없는 순수한 Python 코드입니다.

**구성 요소**:
- **Entities** (`domain/entities/`): 비즈니스 개념을 표현하는 도메인 객체
  - `Todo`: 비즈니스 규칙 검증 및 행위를 포함하는 도메인 엔티티

- **Repository Interfaces** (`domain/repositories/`): 데이터 접근을 위한 추상 인터페이스 (Ports)
  - `TodoRepository`: Todo 데이터 접근을 위한 인터페이스

- **Domain Exceptions** (`domain/exceptions.py`): 도메인 특화 예외
  - `TodoNotFoundException`: Todo를 찾을 수 없을 때
  - `PermissionDeniedException`: 권한이 없을 때
  - `ValidationException`: 검증 실패 시

**원칙**:
- 프레임워크나 라이브러리에 의존하지 않음
- 순수 비즈니스 로직만 포함
- 외부 계층에서 이 계층을 의존함 (의존성 역전)

### 2. Application Layer (애플리케이션 계층)

**목적**: 비즈니스 유즈케이스를 구현합니다. 도메인 엔티티를 조율하여 특정 비즈니스 플로우를 실행합니다.

**구성 요소**:
- **Use Cases** (`application/use_cases/`): 애플리케이션의 비즈니스 플로우
  - `CreateTodoUseCase`: Todo 생성 플로우
  - `GetTodoUseCase`: Todo 조회 플로우
  - `ListTodosUseCase`: Todo 목록 조회 플로우
  - `DeleteTodoUseCase`: Todo 삭제 플로우

- **DTOs** (`application/dtos/`): 계층 간 데이터 전송 객체
  - `CreateTodoDTO`: Todo 생성 요청 데이터
  - `TodoDTO`: Todo 응답 데이터

**원칙**:
- 도메인 계층에만 의존
- 외부 기술(DB, 프레임워크 등)에 직접 의존하지 않음
- Repository 인터페이스를 통해 데이터 접근

### 3. Adapters Layer (어댑터 계층)

**목적**: 외부 세계와 애플리케이션을 연결합니다.

#### 3.1 Inbound Adapters (Primary Adapters)

외부에서 애플리케이션으로 들어오는 요청을 처리합니다.

**구성 요소**:
- **REST API** (`adapters/inbound/api/`):
  - `todos.py`: HTTP 엔드포인트, 유즈케이스 호출
  - `schemas.py`: 요청/응답 직렬화

**역할**:
- HTTP 요청을 받아 DTO로 변환
- 유즈케이스 실행
- 결과를 HTTP 응답으로 변환

#### 3.2 Outbound Adapters (Secondary Adapters)

애플리케이션에서 외부로 나가는 요청을 처리합니다.

**구성 요소**:
- **Persistence** (`adapters/outbound/persistence/`):
  - `models.py`: SQLAlchemy 데이터베이스 모델
  - `todo_repository.py`: TodoRepository 인터페이스 구현

**역할**:
- 도메인 엔티티와 데이터베이스 모델 간 변환
- Repository 인터페이스 구현

### 4. Infrastructure Layer (인프라 계층)

**목적**: 기술적 세부사항과 애플리케이션 설정을 관리합니다.

**구성 요소**:
- `config.py`: 환경별 설정
- `database.py`: SQLAlchemy 초기화
- `extensions.py`: Flask 확장 (CORS, Marshmallow, Migrate)
- `container.py`: 의존성 주입 컨테이너

## 의존성 규칙

```
┌─────────────────────────────────────────┐
│         Adapters (Inbound)              │
│       REST API, CLI, etc.               │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│      Application (Use Cases)            │
│                                         │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│       Domain (Entities)                 │
│    Business Logic & Rules               │
└──────────────┬──────────────────────────┘
               ↑
               │
┌──────────────┴──────────────────────────┐
│      Adapters (Outbound)                │
│    Database, External APIs, etc.        │
└─────────────────────────────────────────┘
```

**핵심 원칙**:
1. **Domain Layer**: 어떤 계층에도 의존하지 않음
2. **Application Layer**: Domain에만 의존
3. **Adapters Layer**: Application과 Domain에 의존
4. **Infrastructure Layer**: 모든 계층을 연결

## 의존성 주입 (Dependency Injection)

`infrastructure/container.py`에서 의존성을 관리합니다:

```python
from app.infrastructure.container import get_todo_repository

# 유즈케이스에 레포지토리 주입
use_case = CreateTodoUseCase(get_todo_repository())
result = use_case.execute(dto)
```

## 데이터 흐름 예시

### Todo 생성 요청 흐름:

1. **HTTP 요청** → `adapters/inbound/api/todos.py:create_todo()`
2. **DTO 생성** → `CreateTodoDTO` 생성
3. **유즈케이스 실행** → `CreateTodoUseCase.execute(dto)`
4. **도메인 엔티티 생성** → `Todo` 엔티티 생성 (비즈니스 규칙 검증)
5. **레포지토리 저장** → `TodoRepository.save(todo)` 호출
6. **데이터베이스 저장** → `SQLAlchemyTodoRepository` 구현체가 실행
7. **DTO 변환** → 도메인 엔티티를 `TodoDTO`로 변환
8. **HTTP 응답** → JSON으로 직렬화하여 응답

## 장점

### 1. 테스트 용이성
- 도메인 로직을 독립적으로 테스트 가능
- Mock 객체를 사용한 유즈케이스 테스트 용이
- 어댑터를 쉽게 교체 가능

### 2. 유지보수성
- 관심사의 명확한 분리
- 비즈니스 로직이 프레임워크로부터 독립적
- 각 계층의 책임이 명확

### 3. 확장성
- 새로운 어댑터 추가 용이 (예: GraphQL, gRPC)
- 데이터베이스 교체 용이 (SQLAlchemy → MongoDB)
- 비즈니스 로직 재사용 가능

### 4. 의존성 역전
- 비즈니스 로직이 인프라에 의존하지 않음
- 인프라가 비즈니스 로직에 의존
- 핵심 로직의 안정성 향상

## 마이그레이션 가이드

### 기존 코드에서 변경된 사항:

1. **모델 임포트**:
   ```python
   # 기존
   from app.models import Todo

   # 새로운 (권장)
   from app.adapters.outbound.persistence.models import TodoModel
   # 또는 도메인 엔티티
   from app.domain.entities import Todo
   ```

2. **API 엔드포인트**:
   ```python
   # 기존
   from app.api import api

   # 새로운 (권장)
   from app.adapters.inbound.api import api
   ```

3. **설정 임포트**:
   ```python
   # 기존
   from app.config import config

   # 새로운 (권장)
   from app.infrastructure.config import config
   ```

**참고**: 기존 임포트 경로도 backward compatibility를 위해 유지되지만, 새로운 경로 사용을 권장합니다.

## 모범 사례

### 1. 새로운 기능 추가 시:

1. **도메인 엔티티** 정의 (`domain/entities/`)
2. **Repository 인터페이스** 정의 (`domain/repositories/`)
3. **유즈케이스** 구현 (`application/use_cases/`)
4. **레포지토리 구현** (`adapters/outbound/persistence/`)
5. **API 엔드포인트** 추가 (`adapters/inbound/api/`)

### 2. 테스트 작성:

```python
# 도메인 엔티티 테스트 (외부 의존성 없음)
def test_todo_validation():
    with pytest.raises(ValueError):
        Todo(title="", user_id=1)

# 유즈케이스 테스트 (Mock Repository 사용)
def test_create_todo_use_case():
    mock_repo = Mock(spec=TodoRepository)
    use_case = CreateTodoUseCase(mock_repo)
    # ...
```

### 3. 비즈니스 규칙:

- **도메인 엔티티에** 비즈니스 규칙 구현
- **유즈케이스에** 비즈니스 플로우 구현
- **어댑터에** 기술적 세부사항만 구현

## 추가 리소스

- [Hexagonal Architecture 원문](https://alistair.cockburn.us/hexagonal-architecture/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Ports and Adapters Pattern](https://herbertograca.com/2017/11/16/explicit-architecture-01-ddd-hexagonal-onion-clean-cqrs-how-i-put-it-all-together/)

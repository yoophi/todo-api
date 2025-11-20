# Todo API

헥사고날 아키텍처 패턴으로 구조화된 Todo API REST API 샘플입니다.

## Requirements

- Python 3.9+
- PostgreSQL
- uv (의존성 관리)

## Tech Stack

- **Framework**: Flask 3.1.2
- **Database**: PostgreSQL (via psycopg2-binary)
- **ORM**: SQLAlchemy 2.0.44, Flask-SQLAlchemy 3.1.1
- **Migration**: Flask-Migrate 4.1.0
- **Serialization**: Flask-Marshmallow 1.3.0, Marshmallow-SQLAlchemy 1.0.0
- **API Documentation**: Flask-Swagger 0.2.14
- **CORS**: Flask-CORS 6.0.1
- **Architecture**: Hexagonal Architecture (Ports and Adapters)

## Architecture

이 프로젝트는 **헥사고날 아키텍처(Hexagonal Architecture)** 패턴으로 구조화되어 있습니다.

자세한 아키텍처 설명은 [ARCHITECTURE.md](ARCHITECTURE.md)를 참조하세요.

## Project Structure

```
todo-api/
├── app/                                # 메인 애플리케이션 패키지
│   ├── __init__.py                    # Flask 앱 팩토리 (create_app)
│   │
│   ├── domain/                        # 도메인 계층 (핵심 비즈니스 로직)
│   │   ├── entities/                  # 도메인 엔티티
│   │   │   └── todo.py               # Todo 엔티티 (비즈니스 규칙)
│   │   ├── repositories/             # Repository 인터페이스 (Ports)
│   │   │   └── todo_repository.py    # TodoRepository 인터페이스
│   │   └── exceptions.py             # 도메인 예외
│   │
│   ├── application/                   # 애플리케이션 계층 (유즈케이스)
│   │   ├── dtos/                     # 데이터 전송 객체
│   │   │   └── todo_dto.py          # Todo DTO
│   │   └── use_cases/                # 비즈니스 플로우
│   │       ├── create_todo.py       # Todo 생성 유즈케이스
│   │       ├── get_todo.py          # Todo 조회 유즈케이스
│   │       ├── list_todos.py        # Todo 목록 유즈케이스
│   │       └── delete_todo.py       # Todo 삭제 유즈케이스
│   │
│   ├── adapters/                      # 어댑터 계층
│   │   ├── inbound/                  # Primary Adapters (입력)
│   │   │   └── api/                  # REST API 어댑터
│   │   │       ├── todos.py         # API 엔드포인트
│   │   │       └── schemas.py       # Marshmallow 스키마
│   │   └── outbound/                 # Secondary Adapters (출력)
│   │       └── persistence/          # 데이터베이스 어댑터
│   │           ├── models.py        # SQLAlchemy 모델
│   │           └── todo_repository.py # Repository 구현
│   │
│   ├── infrastructure/                # 인프라 계층
│   │   ├── config.py                 # 환경별 설정
│   │   ├── database.py               # SQLAlchemy 인스턴스
│   │   ├── extensions.py             # Flask 확장
│   │   └── container.py              # 의존성 주입 컨테이너
│   │
│   ├── views/                         # 기본 뷰
│   ├── swagger/                       # Swagger 문서
│   ├── commands/                      # Flask CLI 명령어
│   └── __meta__.py                    # 메타데이터
│
├── migrations/                        # Alembic 마이그레이션
├── openspec/                          # 프로젝트 문서 및 명세
├── ARCHITECTURE.md                    # 아키텍처 상세 문서
├── pyproject.toml                     # 프로젝트 설정 및 의존성 (uv)
├── uv.lock                            # 의존성 잠금 파일 (uv)
└── README.md
```

### 아키텍처 계층

1. **Domain Layer**: 비즈니스 로직과 규칙 (외부 의존성 없음)
2. **Application Layer**: 유즈케이스 구현
3. **Adapters Layer**: 외부 세계와의 연결 (API, Database)
4. **Infrastructure Layer**: 기술적 세부사항 및 설정

## Environment Variables

다음 환경 변수를 설정하여 데이터베이스 연결을 구성할 수 있습니다:

- `DB_HOST` (default: `localhost`)
- `DB_PORT` (default: `5432`)
- `DB_USER` (default: `user`)
- `DB_PASSWORD` (default: `password`)
- `DB_DATABASE` (default: `todos`)

추가 환경 변수:
- `SECRET_KEY`: Flask 시크릿 키
- `DEV_DATABASE_URL`: Development 환경 데이터베이스 URL
- `TEST_DATABASE_URL`: Testing 환경 데이터베이스 URL (default: SQLite in-memory)
- `DATABASE_URL`: Production 환경 데이터베이스 URL

## API Endpoints

### Todo API (`/api/todos`)

- `GET /api/todos` - Todo 목록 조회
- `GET /api/todos/<id>` - 특정 Todo 조회
- `POST /api/todos` - 새 Todo 생성
  - Headers: `user-id` (required)
  - Body: `{ "title": "string", "priority": number }`
- `DELETE /api/todos/<id>` - Todo 삭제
  - Headers: `user-id` (required)

### Documentation

- `/swagger` - Swagger UI를 통한 API 문서

## Database Model

### Todo
- `id` (Integer, Primary Key)
- `title` (String, 255자)
- `priority` (Integer, default: 3)
- `user_id` (Integer, required)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Configuration Profiles

프로젝트는 다양한 환경을 위한 설정 프로필을 제공합니다:

- **Development**: 디버그 모드, SQL 쿼리 로깅
- **Testing**: SQLite 인메모리 DB
- **Production**: 프로덕션 환경
- **Docker**: 컨테이너 환경, stderr 로깅
- **Unix**: Unix 시스템, syslog 핸들러

## Installation

```bash
# uv 설치 (없는 경우)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치 및 가상환경 생성
uv sync

# 가상환경 활성화
source .venv/bin/activate

# 또는 uv run을 사용하여 명령 실행
# uv run flask run
```

## Database Setup

```bash
# 데이터베이스 마이그레이션 초기화 (이미 완료됨)
uv run flask db init

# 마이그레이션 실행
uv run flask db upgrade
```

## Running the Application

```bash
# Development 모드 (가상환경 활성화 후)
flask run

# 또는 uv run 사용 (가상환경 활성화 없이)
uv run flask run

# 특정 설정으로 실행
export FLASK_ENV=development
uv run flask run
```

## Architecture Benefits

헥사고날 아키텍처를 사용하여 다음과 같은 이점을 얻습니다:

- ✅ **테스트 용이성**: 비즈니스 로직을 독립적으로 테스트 가능
- ✅ **유지보수성**: 관심사의 명확한 분리로 코드 이해와 수정이 용이
- ✅ **확장성**: 새로운 어댑터 추가가 쉬움 (GraphQL, gRPC 등)
- ✅ **독립성**: 프레임워크/데이터베이스 교체가 용이
- ✅ **재사용성**: 도메인 로직을 다양한 환경에서 재사용 가능

## TODO

- [ ] tests 추가
- [ ] Docker Build 추가
- [ ] `docker-compose` 환경 추가
- [ ] `seed-data` command 추가
- [ ] 다양한 데이터 저장소 지원 (MongoDB, Redis 등)
- [x] 헥사고날 아키텍처로 리팩토링 
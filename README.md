# Todo API

아주 평범한 Todo API 를 제공하는 REST API 샘플입니다.

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

## Project Structure

```
todo-api/
├── app/                        # 메인 애플리케이션 패키지
│   ├── __init__.py            # Flask 앱 팩토리 (create_app)
│   ├── __meta__.py            # 메타데이터
│   ├── config.py              # 환경별 설정 (Development, Testing, Production, Docker, Unix)
│   ├── database.py            # SQLAlchemy 인스턴스
│   ├── extensions.py          # Flask 확장 (CORS, Marshmallow, Migrate)
│   ├── exceptions.py          # 커스텀 예외
│   ├── schema.py              # Marshmallow 스키마 (TodoSchema)
│   ├── api/                   # REST API 엔드포인트
│   │   ├── __init__.py        # API Blueprint
│   │   └── todos.py           # Todo CRUD API
│   ├── models/                # 데이터베이스 모델
│   │   └── __init__.py        # Todo 모델
│   ├── views/                 # 기본 뷰
│   │   └── __init__.py        # 메인 Blueprint
│   ├── swagger/               # Swagger 문서
│   │   └── __init__.py
│   └── commands/              # Flask CLI 명령어
│       └── __init__.py
├── migrations/                # Alembic 마이그레이션
│   ├── env.py
│   ├── alembic.ini
│   └── versions/
├── openspec/                  # 프로젝트 문서 및 명세
│   ├── project.md
│   ├── AGENTS.md
│   └── changes/
├── pyproject.toml             # 프로젝트 설정 및 의존성 (uv)
├── uv.lock                    # 의존성 잠금 파일 (uv)
└── README.md
```

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
flask db init

# 마이그레이션 실행
flask db upgrade
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

## TODO

- [ ] tests 추가
- [ ] Docker Build 추가
- [ ] `docker-compose` 환경 추가
- [ ] `seed-data` command 추가
- [ ] 다양한 데이터 저장소 지원 
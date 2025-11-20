from flask import jsonify, request

from app.adapters.inbound.api import api
from app.adapters.inbound.api.schemas import CreateTodoSchema, TodoSchema
from app.application.dtos import CreateTodoDTO
from app.application.use_cases import (
    CreateTodoUseCase,
    DeleteTodoUseCase,
    GetTodoUseCase,
    ListTodosUseCase,
)
from app.domain.exceptions import (
    PermissionDeniedException,
    TodoNotFoundException,
    ValidationException,
)
from app.infrastructure.container import get_todo_repository


@api.route('/todos')
def todo_list():
    """
    Get Todo List
    사용자의 Todo 목록을 가져온다.
    ---
    tags:
      - todo
    responses:
      200:
        description: OK
        schema:
          type: array
          items:
            $ref: '#/definitions/Todo'
    """
    # 유즈케이스 생성
    use_case = ListTodosUseCase(get_todo_repository())

    # 유즈케이스 실행
    todos = use_case.execute()

    # DTO를 딕셔너리로 변환
    result = [
        {
            'id': todo.id,
            'title': todo.title,
            'priority': todo.priority,
            'user_id': todo.user_id,
            'created_at': todo.created_at.isoformat(),
            'updated_at': todo.updated_at.isoformat(),
        }
        for todo in todos
    ]

    return jsonify(result)


@api.route('/todos/<int:id>')
def todo_item(id):
    """
    Get Todo
    사용자의 Todo 항목을 가져온다.
    ---
    tags:
      - todo
    parameters:
      - name: id
        description: Todo.id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: OK
        schema:
          $ref: '#/definitions/Todo'
      404:
        description: Not Found
    """
    try:
        # 유즈케이스 생성
        use_case = GetTodoUseCase(get_todo_repository())

        # 유즈케이스 실행
        todo = use_case.execute(id)

        # DTO를 딕셔너리로 변환
        result = {
            'id': todo.id,
            'title': todo.title,
            'priority': todo.priority,
            'user_id': todo.user_id,
            'created_at': todo.created_at.isoformat(),
            'updated_at': todo.updated_at.isoformat(),
        }

        return jsonify(result)

    except TodoNotFoundException:
        return jsonify(message="not found"), 404


@api.route('/todos', methods=['POST'])
def create_todo():
    """
    Create Todo
    새로운 Todo를 생성한다.
    ---
    tags:
      - todo
    parameters:
      - name: body
        in: body
        description: 새로 생성할 Todo Data
        schema:
          type: object
          properties:
            title:
              type: string
            priority:
              type: integer
              default: 3
        required: true
      - name: user-id
        description: User.id
        in: header
        type: integer
        required: true
    responses:
      200:
        description: OK
      400:
        description: Bad Request
    """
    try:
        # 요청 데이터 파싱
        payload = request.json
        user_id = request.headers.get('user-id')

        if not user_id:
            return jsonify(error=True, message='user-id header is required'), 400

        # DTO 생성
        dto = CreateTodoDTO(
            title=payload.get('title'),
            user_id=int(user_id),
            priority=payload.get('priority', 3)
        )

        # 유즈케이스 생성 및 실행
        use_case = CreateTodoUseCase(get_todo_repository())
        todo = use_case.execute(dto)

        return jsonify(message="todo created", id=todo.id), 201

    except (ValueError, ValidationException) as e:
        return jsonify(error=True, message=str(e)), 400


@api.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    """
    Delete Todo
    해당 Todo 삭제
    ---
    parameters:
      - name: id
        description: Todo.id
        in: path
        type: integer
        required: true
      - name: user-id
        description: User.id
        in: header
        type: integer
        required: true
    tags:
      - todo
    responses:
      200:
        description: OK
      401:
        description: Permission Denied
      404:
        description: Not Found
    """
    try:
        user_id = request.headers.get('user-id')

        if not user_id:
            return jsonify(error=True, message='user-id header is required'), 400

        # 유즈케이스 생성 및 실행
        use_case = DeleteTodoUseCase(get_todo_repository())
        use_case.execute(id, int(user_id))

        return jsonify(message='todo deleted'), 200

    except TodoNotFoundException:
        return jsonify(message='not found'), 404

    except PermissionDeniedException as e:
        return jsonify(error=True, message=str(e)), 401

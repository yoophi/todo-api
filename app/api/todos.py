from dependency_injector.wiring import inject, Provide
from flask import jsonify, request

from app.api import api
from app.containers import Container
from app.schema import TodoSchema
from app.exceptions import TodoNotFound
from app.service.todo import TodoService


@api.route('/todos')
@inject
def todo_list(todo_service: TodoService = Provide[Container.todo_service]):
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
    items = todo_service.get_todo_list()
    rv = TodoSchema(many=True).dump(items)

    return jsonify(rv)


@api.route('/todos/<int:id>')
@inject
def todo_item(id, todo_service=Provide[Container.todo_service]):
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
    """
    item = todo_service.get_todo_detail(id)
    if not item:
        return jsonify(message="not found"), 404

    return TodoSchema().dump(item)


@api.route('/todos', methods=['POST', ])
@inject
def create_todo(todo_service=Provide[Container.todo_service]):
    """
    Get Todo
    사용자의 Todo 항목을 가져온다.
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
              default: 1
        required: true
      - name: user_id
        description: User.id
        in: header
        type: integer
        required: true
    responses:
      200:
        description: OK
    """
    payload = request.json
    user_id = request.headers.get('user-id')
    todo_service.add_todo(
        title=payload.get('title'),
        priority=payload.get('priority'),
        user_id=user_id,
    )

    return jsonify(message="todo created"), 200


@api.route('/todos/<int:id>', methods=['DELETE', ])
@inject
def delete_todo(id, todo_service=Provide[Container.todo_service]):
    """
    해당 Todo 삭제
    ---
    parameters:
      - name: id
        description: Todo.id
        in: path
        type: integer
        required: true
      - name: user_id
        description: User.id
        in: header
        type: integer
        required: true
    tags:
      - todo
    responses:
      '200':
        description: OK
    """
    user_id = int(request.headers.get('user-id', 0))
    try:
        todo_service.remove_todo(id=id, user_id=user_id)
    except TodoNotFound:
        return jsonify(message='not found'), 404
    except PermissionError:
        return jsonify(message='permission denied'), 401
    except Exception as e:
        return jsonify(message=str(e)), 500

    return jsonify(result='todo deleted'), 200


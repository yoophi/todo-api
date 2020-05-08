from flask import jsonify, request

from app.api import api
from app.database import db
from app.models import Todo
from app.schema import TodoSchema


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
    items = db.session.query(Todo).all()
    rv = TodoSchema(many=True).dump(items)

    return jsonify(rv)


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
    """

    item = db.session.query(Todo).get(id)
    if not item:
        return jsonify(message="not found"), 404

    return TodoSchema().dump(item)


@api.route('/todos', methods=['POST', ])
def create_todo():
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
    todo = Todo(
        title=payload.get('title'),
        priority=payload.get('priority'),
        user_id=user_id,
    )
    db.session.add(todo)
    db.session.commit()

    return jsonify(message="todo created"), 200


@api.route('/todos/<int:id>', methods=['DELETE', ])
def delete_todo(id):
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
    todo = db.session.query(Todo).get(id)
    if not todo:
        return jsonify(message='not found'), 404

    if todo.user_id != user_id:
        return jsonify(error=True, message='permission denied'), 401

    db.session.delete(todo)
    db.session.commit()

    return jsonify(result='todo deleted'), 200

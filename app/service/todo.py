from app.database import db
from app.exceptions import TodoNotFound
from app.models import Todo


class TodoService:
    def add_todo(self, title, priority, user_id):
        todo = Todo(
            title=title,
            priority=priority,
            user_id=user_id,
        )
        db.session.add(todo)
        db.session.commit()
        return todo

    def get_todo_list(self):
        return db.session.query(Todo).all()

    def get_todo_detail(self, id):
        return db.session.query(Todo).get(id)

    def remove_todo(self, id, user_id):
        todo = db.session.query(Todo).get(id)
        if not todo:
            raise TodoNotFound()

        if todo.user_id != user_id:
            raise PermissionError()

        db.session.delete(todo)
        db.session.commit()
        return True

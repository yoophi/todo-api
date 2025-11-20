from marshmallow import Schema, fields

from app.infrastructure.extensions import ma


class TodoSchema(ma.Schema):
    """
    Todo Marshmallow 스키마

    API 요청/응답 직렬화를 위한 스키마입니다.
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    priority = fields.Int(load_default=3)
    user_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = ('id', 'title', 'priority', 'user_id', 'created_at', 'updated_at')


class CreateTodoSchema(Schema):
    """Todo 생성 요청 스키마"""
    title = fields.Str(required=True)
    priority = fields.Int(load_default=3)

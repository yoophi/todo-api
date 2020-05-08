from app.extensions import ma
from app.swagger import swagger_definition


@swagger_definition
class TodoSchema(ma.Schema):
    """
    Todo
    ---
    type: "object"
    properties:
      id:
        type: "integer"
        format: "int64"
      title:
        type: "string"
      priority:
        type: "integer"
        format: "int64"
      user_id:
        type: "integer"
        format: "int64"
      created_at:
        type: "string"
        format: "date-time"
      updated_at:
        type: "string"
        format: "date-time"
    """

    class Meta:
        fields = (
            "id",
            "title", "priority",
            "user_id",
            "created_at", "updated_at",
        )


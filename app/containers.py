from dependency_injector import containers, providers

from app.service import todo


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app.api.todos"])

    todo_service = providers.Factory(
        todo.TodoService,
    )

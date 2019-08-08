from django.apps import AppConfig


class TodoConfig(AppConfig):
    name = 'foo.todo'

    def ready(self):
        import foo.todo.signals
from django.db import models


class Todo(models.Model):
    content = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.content} [{' ' if not self.completed else 'x'}]"
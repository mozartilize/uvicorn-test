from django.conf.urls import url

from .consumers import TodoConsumer


websocket_urlpatterns = [
    url(r'^ws/todos$', TodoConsumer),
]

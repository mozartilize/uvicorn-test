# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import foo.todo.websocket_routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': URLRouter(
        foo.todo.websocket_routing.websocket_urlpatterns
    ),
})

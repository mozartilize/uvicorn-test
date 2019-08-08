import socket
from wsproto import WSConnection
from wsproto.connection import ConnectionType
from wsproto.events import (
    AcceptConnection,
    CloseConnection,
    Message,
    Request,
    TextMessage,
    Ping,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Todo

RECEIVE_BYTES = 4096


def net_send(out_data: bytes, conn: socket.socket) -> None:
    """ Write pending data from websocket to network. """
    print("Sending {} bytes".format(len(out_data)))
    conn.send(out_data)


def net_recv(ws: WSConnection, conn: socket.socket) -> None:
    """ Read pending data from network into websocket. """
    in_data = conn.recv(RECEIVE_BYTES)
    if not in_data:
        # A receive of zero bytes indicates the TCP socket has been closed. We
        # need to pass None to wsproto to update its internal state.
        print("Received 0 bytes (connection closed)")
        ws.receive_data(None)
    else:
        print("Received {} bytes".format(len(in_data)))
        ws.receive_data(in_data)


def handle_events(ws: WSConnection) -> None:
    for event in ws.events():
        if isinstance(event, AcceptConnection):
            print("WebSocket negotiation complete")
        elif isinstance(event, TextMessage):
            print("Received message: {}".format(event.data))
        elif isinstance(event, Ping):
            print("Received ping: {}".format(event))
        else:
            raise Exception("Do not know how to handle event: " + str(event))


@receiver(post_save, sender=Todo)
def handle_todo_post_save(sender, instance, created, **kwargs):
    if not hasattr(sender, 'APP_PORT'):
        return
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(('localhost', int(sender.APP_PORT)))

    ws = WSConnection(ConnectionType.CLIENT)
    print("hello")
    net_send(
        ws.send(Request(
            host=f"localhost:{sender.APP_PORT}",
            target=f"ws/todos")),
        conn
    )
    net_recv(ws, conn)
    handle_events(ws)

    net_send(ws.send(Message(data=str(instance.pk))), conn)
    net_recv(ws, conn)
    handle_events(ws)

    net_send(ws.send(CloseConnection(code=1000)), conn)
    net_recv(ws, conn)
    conn.shutdown(socket.SHUT_WR)
    net_recv(ws, conn)

    del sender.APP_PORT
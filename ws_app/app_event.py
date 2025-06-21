import socketio


class AppEventNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace=None):
        super().__init__(namespace)

    async def on_connect(self, sid, environ):
        print(f"Client connected: {sid}")

    async def on_disconnect(self, sid):
        print(f"Client disconnected: {sid}")

    async def on_message(self, sid, data):
        print(f"Message from {sid}: {data}")
        await self.emit('response', {'data': 'Message received'}, room=sid)

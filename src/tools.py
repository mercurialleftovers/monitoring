from fastapi import WebSocket


class WSManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        # now ws connection is opened
        self.active_connections.append(ws)

    async def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

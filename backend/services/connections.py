from starlette.websockets import WebSocket


class ConnectionManager:
    """Класс для управления подключениями пользователей."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Реализиует логику подключения пользователей к игре. Если уже 2 и больше подключений, то последующие обрубает
        Если подключений 0, только возвращает ответ на клиент, что ожидается подключение второго игрока.
        При подлкючении второго игрока, возвращает ответ на клиент, что игра началась и ходит первый подключивщийся игрок"""
        if len(self.active_connections) >= 2:
            await websocket.accept()
            await websocket.close(code=4000, reason='Too many connections')
        if len(self.active_connections) == 0:
            await websocket.accept()
            self.active_connections.append(websocket)
            await websocket.send_json(
                {
                    "init": True,
                    "player": "X",
                    "message": "Awaiting second player",
                }
            )
        else:
            await websocket.accept()
            self.active_connections.append(websocket)
            await websocket.send_json(
                {
                    "init": True,
                    "player": "O",
                    "message": "Ok, all in rooom. Let's go! Now PlayerX turn!",
                }
            )

            await self.active_connections[0].send_json(
                {
                    "init": True,
                    "player": "X",
                    "message": "Player X your turn!"
                }
            )

    def disconnect(self, websocket: WebSocket):
        """Отключает пользователя"""
        self.active_connections.remove(websocket)

    async def broadcast_without_active_player(self, message: dict, websocket: WebSocket):
        """Отправляет сообщение второму игроку"""
        for connection in self.active_connections:
            if connection != websocket:
                await connection.send_json(message)

    async def broadcast(self, message: dict):
        """Отправляет сообщение второму игроку"""
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()

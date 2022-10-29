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

    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Отправляет персональное сообщение игроку чей сейчас ход"""
        await websocket.send_text(message)

    async def broadcast_without_active_player(self, message: dict, websoket: WebSocket):
        """Отправляет сообщение второму игроку"""
        for connenction in self.active_connections:
            if connenction != websoket:
                await connenction.send_json(message)


manager = ConnectionManager()

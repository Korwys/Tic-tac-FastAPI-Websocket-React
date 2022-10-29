from starlette.websockets import WebSocket

from services.connections import manager

board = [
    None, None, None,
    None, None, None,
    None, None, None
]


def check_board() -> str:
    """Проверяет выполнено ли условие на победу или ничью и возвращает ответ."""
    combinations = board[0] == board[1] == board[2] is not None or \
                   board[3] == board[4] == board[5] is not None or \
                   board[6] == board[7] == board[8] is not None or \
                   board[0] == board[3] == board[6] is not None or \
                   board[1] == board[4] == board[7] is not None or \
                   board[2] == board[5] == board[8] is not None or \
                   board[0] == board[4] == board[8] is not None or \
                   board[2] == board[4] == board[6] is not None

    if combinations:
        return 'Win'
    elif None not in board:
        return 'Draw'
    else:
        return 'Move'


def change_board_cell(indx: int, player: str) -> list:
    """Меняет ячейку на доске на символ игрока"""
    board[indx] = player
    return board


async def update_board(data: dict, websoket: WebSocket) -> None:
    """После проверок возвращает ответ клиенту."""
    indx = int(data['cell']) - 1
    change_board_cell(indx, data['player'])
    if check_board() == 'Win':
        send_data = {
            "init": False,
            "player": data['player'],
            "message": "You Win",
            "cell": data['cell']
        }
        await websoket.send_json(send_data)
        await manager.broadcast_without_active_player({"info": True, "cell": data['cell'], 'player': data['player']},
                                                      websoket)
    elif check_board() == 'Draw':
        send_data = {
            "init": False,
            "player": data['player'],
            "message": "Draw",
            "cell": data['cell']
        }
        await manager.broadcast(send_data)
    else:
        send_data = {
            "init": False,
            "player": data['player'],
            "message": "Next",
            "cell": data['cell']
        }
        await manager.broadcast(send_data)

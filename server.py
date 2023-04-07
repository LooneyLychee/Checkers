from _thread import *
from game import ServerGame, Answer
from logic.position import Position
from logic.board import CheckersVariant, Color
from enum import Enum
from multiprocessing.connection import Listener
import socket

class Status(Enum):
    STARTED = 0
    FINISHED = 1


server = socket.gethostbyname(socket.gethostname())
port = 5555
print(server)
s = Listener((server, port))

print("Waiting for connection, Server STARTED")

polish_player = 1
classic_player = 1


games = {}
games_status = {}

polish_game_id = 0
classic_game_id = 1


def threaded_client(conn, player, game_ID):
    conn.send(str(player))
    while True:
        try:
            data = conn.recv()
            if game_ID in games:
                game = games[game_ID]
                if not data:
                    print("Not data")
                    break
                else:
                    player_color = Color(player)
                    if data == "no":
                        game.answer(player_color, Answer.NO)
                    elif data == "yes":
                        game.answer(player_color, Answer.YES)
                    elif data == "give_up":
                        game.give_up(player_color)
                    elif data == "tie":
                        game.tie(player_color)
                    elif data != "get_game":
                        position = Position(data)
                        game.pick_a_piece(position, player_color)
                        game.make_a_move(position, player_color)

                    conn.send(game.to_client)
            else:
                print("game dont exist")
                break
        except:
            print("conn failed")
            break

    if game_ID in games_status:
        print("game over")
        game_status = games_status[game_ID]
        if game_status == Status.STARTED:
            games_status[game_ID] = Status.FINISHED
        elif game_status == Status.FINISHED:
            try:
                del games[game_ID]
                del games_status[game_ID]
            except:
                pass
    else:
        print("player quite before game started")
        if games[game_ID].checkers_variant == CheckersVariant.CLASSIC:
            global classic_player
            classic_player = 1
        else:
            global polish_player
            polish_player = 1

        try:
            del games[game_ID]
        except:
            pass

    conn.close()


while True:
    conn = s.accept()
    print("Connected")

    data = conn.recv()
    checkers_variant = CheckersVariant(int(data))

    if checkers_variant == CheckersVariant.CLASSIC:
        if classic_player == 1:
            games[classic_game_id] = ServerGame(CheckersVariant.CLASSIC)
            print("Creating a new classic game...")

        start_new_thread(threaded_client, (conn, classic_player, classic_game_id))

        if classic_player == 1:
            classic_player -= 1
        else:
            games[classic_game_id].connected()
            games_status[classic_game_id] = Status.STARTED
            classic_player = 1
            classic_game_id = max(classic_game_id, polish_game_id) + 1
    else:
        if polish_player == 1:
            games[polish_game_id] = ServerGame(CheckersVariant.POLISH)
            print("Creating a new polish game...")

        start_new_thread(threaded_client, (conn, polish_player, polish_game_id))

        if polish_player == 1:
            polish_player -= 1
        else:
            games[polish_game_id].connected()
            games_status[polish_game_id] = Status.STARTED
            polish_player = 1
            polish_game_id = max(classic_game_id, polish_game_id) + 1

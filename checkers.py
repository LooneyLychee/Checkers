import pygame
from front.menu import MenuScreen
from network import Network
from game import ClientGame
from front.info_screen import WaitingScreen, EndScreen, TieScreen, Message
from logic.board import *
from front.properties import Size

pygame.init()
win = pygame.display.set_mode(Size.WINDOW_SIZE.value)
pygame.display.set_caption("Checkers")


def start_game(checkers_variant):
    run = True

    n = Network(str(checkers_variant.value))
    player = int(n.get_p())

    print("You are player", player)

    game = ClientGame(checkers_variant, Color(player))
    waiting_screen = WaitingScreen()
    tie_screen = None
    while run:
        try:
            from_server = n.send("get_game")
            game.actualize(from_server)
            if game.from_server.end or game.from_server.tie:
                break
        except:
            print("not game")
            break

        if game.from_server.questioning is None:
            tie_screen = None
        elif tie_screen is None:
            if game.from_server.questioning == Color(player):
                tie_screen = TieScreen(Message.QUESTIONING)
            else:
                tie_screen = TieScreen(Message.RESPONDING)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                n.send("give_up")
                pygame.quit()
                return False

            if game.from_server.questioning is None:
                button = game.game_screen.get_button(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP and button is not None:
                    if button.caption == "Give Up":
                        n.send("give_up")
                        break
                    else:
                        n.send("tie")
            else:
                button = tie_screen.get_button(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONUP and button is not None:
                    if button.caption == "YES":
                        n.send("yes")
                        break
                    else:
                        n.send("no")

            if game.from_server.player_turn == Color(player) and game.from_server.end is not None:
                if event.type == pygame.MOUSEBUTTONUP:
                    coordinators = pygame.mouse.get_pos()
                    position = game.game_screen.board.get_position(coordinators)
                    if position is not None:
                        n.send(str(position))

        if game.from_server.connected:
            game.game_screen.draw(win, tie_screen)
        else:
            waiting_screen.draw(win)

    if game.from_server.end or game.from_server.tie:
        run = end_screen(game.from_server.winner, player)

    return run


def end_screen(winner, player):
    result = EndScreen.get_result(Color(player), winner)

    screen = EndScreen(result)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            button = screen.get_button(pygame.mouse.get_pos())
            if button is not None and event.type == pygame.MOUSEBUTTONUP:
                return True

        screen.draw(win)


def menu_screen():
    menu = MenuScreen()

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                break

            button = menu.get_button(pygame.mouse.get_pos())
            if button is not None and event.type == pygame.MOUSEBUTTONUP:
                if button.caption == "CLASSIC":
                    run = start_game(CheckersVariant.CLASSIC)
                else:
                    run = start_game(CheckersVariant.POLISH)
                if not run:
                    break
        if run:
            menu.draw(win)


menu_screen()

from ex12 import game
from ex12 import screen

if __name__ == '__main__':
    game = game.Game()
    screen = screen.Screen(game)
    screen.run()

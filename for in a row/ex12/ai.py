from . import game
import random

COLS = [0, 1, 2, 3, 4, 5, 6]

class AI:
    """
    receives a game and returns a legal move when called.
    """
    def __init__(self, game, player):
        self.game = game
        self.cols = COLS

    def find_legal_move(self, timeout=None):
        """
        if the game is not over yet, returns a random move. if column if full,
        tries again.
        """
        if self.game.get_winner() is None:
            self.coice = random.choice(self.cols)
            if self.game.get_player_at(0, self.coice):
                self.find_legal_move()
            return self.coice
        else:
            raise Exception("No possible AI moves.")


    def get_last_found_move(self):
        pass

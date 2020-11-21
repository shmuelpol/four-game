COLUMN_LENGTH = 6
ROW_LENGTH = 7
COLS = [0, 1, 2, 3, 4, 5, 6]
ROWS = [0, 1, 2, 3, 4, 5]
MAX = COLUMN_LENGTH * ROW_LENGTH

SEQ = 4  # desired sequence length.

UP = (0, 1)
RIGHT = (1, 0)
UPRIGHT = (1, 1)
DOWNRIGHT = (1, -1)

class Game:
    """
    four in a row logic, follows API.
    additional methods: clean board, end game.
    """

    def __init__(self):
        """
        initializes game.
        """
        self.game_on = True  # a flag for turning the game on and off.
        self.__column_length = COLUMN_LENGTH
        self.__row_length = ROW_LENGTH
        self.__cols = COLS
        self.clean_board()

    def get_data(self, data):
        """
        a get function.
        """
        if data == "column_length":
            return self.__column_length
        elif data == "row_length":
            return self.__row_length
        elif data == "cols":
            return self.__cols
        elif data == "last_move":
            return  self.__last_move

    def clean_board(self):
        """
        cleans board, or creates it if non existent.
        """
        board = []
        for row in range(COLUMN_LENGTH):
            board.append([0] * ROW_LENGTH)
        self.__board = board
        self.__player1_coins = []
        self.__player2_coins = []
        self.__moves = 0

    def end_game(self, winner):
        """
        ends a single game. game_on can be restarted from outside.
        """
        if winner is None:
            return
        self.game_on = False
        self.clean_board()


    def make_move(self, column):
        """
        adds a move to the board and to the relevant player list.
        if move is illegal, raises exception.
        :param column: int in range of row length.
        """
        if column not in COLS or not self.game_on:
            raise Exception("Illegal move.")

        for row in range(COLUMN_LENGTH)[::-1]:
            if self.__board[row][column] == 0:
                player = self.get_current_player()
                self.__board[row][column] = player
                self.__add_move_to_list(row, column)
                self.__moves += 1
                self.__last_move = (row, column, player)
                return True
        raise Exception("Illegal move.")  # column is full.

    def __add_move_to_list(self, row, col):
        """
        keeps track of each player's coins, for get winner functionality.
        """
        if self.get_current_player() == 1:
            self.__player1_coins.append([row, col])
        else:
            self.__player2_coins.append([row, col])

    def __check_seq(self, player, coin, coin_list, length, step):
        """
        a recursive helper for get winner.
        :param step: direction.
        :param length: length left for sequence.
        :param coin: current coin in sequence.
        """
        if length == 1:  # base case.
            coin_list = coin_list + [coin]
            self.winner_coins = coin_list  # saves winning coins for the screen
            return True

        # else, if a sequence is found, continues in same direction:
        if [coin[0] + step[0], coin[1] + step[1]] in player[0]:
            return self.__check_seq(player,
                                    (coin[0] + step[0], coin[1] + step[1]),
                                    coin_list + [coin], length - 1, step)
        return False

    def get_winner(self):
        """
        checks for winner in the game, using players coin lists.
        :return: winner if found, 0 if game ended without a winner,
        None if game has not ended. (and therefore also functions as should_end
        flag)
        """
        for coin_list in [(self.__player1_coins, 1), (self.__player2_coins, 2)]:
            for coin in coin_list[0]:
                if self.__check_seq(coin_list, coin, [], SEQ, UP) or\
                        self.__check_seq(coin_list, coin, [], SEQ, UPRIGHT) or\
                        self.__check_seq( coin_list, coin, [], SEQ, RIGHT) or\
                        self.__check_seq(coin_list, coin, [], SEQ, DOWNRIGHT):
                    return coin_list[1]  # returns player
        if self.__moves == MAX:
            return 0

    def get_player_at(self, row, col):
        """
        returns player at a cell, 0 if cell is empty.
        raises exception if illegal cell is received.
        """
        if row not in ROWS or col not in COLS:
            raise Exception("Illegal location.")
        if self.__board[row][col] == 1:
            return 1
        elif self.__board[row][col] == 2:
            return 2

    def get_current_player(self):
        """
        :return: current player at the game.
        """
        if self.__moves % 2 == 0:
            return 1
        else:
            return 2

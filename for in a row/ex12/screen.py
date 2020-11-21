import tkinter as tk
from PIL import ImageTk, Image
from .ai import AI

class Screen():
    """
    creates GUI, receives user input and deliver it to game, and runs
    the game accordingly. along with user's moves, also manages ai moves if
    necessary.
    """
    def __init__(self, game):
        """
        initializes screen.
        """
        self.__game = game
        self.__init_root()
        self.__init_board()
        self.__init_start()

    def run(self):
        """
        after initialization, runs the game.
        """
        self.__root.mainloop()

    def __exit_game(self, event):
        """
        closes GUI.
        """
        self.__root.destroy()

    def __init_root(self):
        """
        initializes GUI.
        """
        self.__root = tk.Tk()
        self.__root.title("Game of Coins")
        self.__root.geometry("850x570")
        self.__root.resizable(0, 0)

    def __init_board(self):
        """
        draws a clean board on the screen, including a background and an exit
        button.
        """
        self.__bg_img = ImageTk.PhotoImage(Image.open("ex12/ex12.png"))
        self.__bg = tk.Label(self.__root, image=self.__bg_img)
        self.__bg.pack()

        self.__exit_img = ImageTk.PhotoImage(Image.open("ex12/exit.png"))
        self.__exit = tk.Button(self.__bg, image=self.__exit_img, bg="black")
        self.__exit.place(relx=0.79, rely=0.005)
        self.__exit.bind("<Button-1>", self.__exit_game)

        self.__board = tk.Label(self.__bg, bg="black")
        self.__coin = ImageTk.PhotoImage(Image.open("ex12/coin.png"))
        self.__rcoin = ImageTk.PhotoImage(Image.open("ex12/rcoin.png"))
        self.__bcoin = ImageTk.PhotoImage(Image.open("ex12/bcoin.png"))
        self.__clean_board()

    def __clean_board(self):
        """
        crates a clean board, and cleans the game's board record.
        """
        self.__spots = [[] for row in range(self.__game.get_data("column_length"))]
        for row in range(self.__game.get_data("column_length")):
            for column in range(self.__game.get_data("row_length")):
                spot = tk.Button(self.__board, image=self.__coin, bg="black")
                spot.grid(row=row, column=column)
                spot.bind("<Button-1>", self.__spot_pressed(row, column))
                self.__spots[row].append(spot)
        self.__game.clean_board()

    def __init_start(self):
        """
        draws start screen, including four options.
        """
        self.__robot1 = ImageTk.PhotoImage(Image.open("ex12/robot1.png"))
        self.__robot2 = ImageTk.PhotoImage(Image.open("ex12/robot2.png"))
        self.__humans = ImageTk.PhotoImage(Image.open("ex12/humans.png"))
        self.__robots = ImageTk.PhotoImage(Image.open("ex12/robots.png"))
        self.__button1 = tk.Button(self.__bg, image=self.__robot1, bg="black")
        self.__button2 = tk.Button(self.__bg, image=self.__robots, bg="black")
        self.__button3 = tk.Button(self.__bg, image=self.__robot2, bg="black")
        self.__button4 = tk.Button(self.__bg, image=self.__humans, bg="black")
        self.__button1.place(relx=0.5, rely=0.15)
        self.__button3.place(relx=0.5, rely=0.55)
        self.__button2.place(relx=0.09, rely=0.55)
        self.__button4.place(relx=0.09, rely=0.15)
        self.__button1.bind("<Button-1>", self.__ai_player)
        self.__button2.bind("<Button-1>", self.__two_ai)
        self.__button3.bind("<Button-1>", self.__player_ai)
        self.__button4.bind("<Button-1>", self.__two_players)

    def __start_game(self):
        """
        removes starting screen, and places the board on the screen.
        """
        self.__button1.destroy()
        self.__button2.destroy()
        self.__button3.destroy()
        self.__button4.destroy()
        self.__board.place(relx=0.5, rely=0.48, anchor="center")

    def __spot_pressed(self, i, j):
        """
        a function for board initializing. creates a matching function for
        a given cell, which is attached to the relevant button.
        """
        def re(event):
            """
            user input function. activated when a button is pressed.
            if move is valid, makes the move. if necessary, preforms
            the following ai move.
            """
            if self.__player != "both" and\
                    self.__player != self.__game.get_current_player():
                return  # not player's turn.

            else:
                try:
                    self.__game.make_move(j)  # player's move.
                    self.__add_coin(*self.__game.get_data("last_move"))

                    if (self.__player == 1 or self.__player == 2) and\
                            self.__game.get_winner() is None:  # play ai move.
                        self.__game.make_move(self.__ai.find_legal_move())
                        self.__add_coin(*self.__game.get_data("last_move"))
                except:
                    pass

            # check for winner
            self.__should_end()

        return re

    def __add_coin(self, i, j, player):
        """
        draws a coin on the board
        :param i: row
        :param j: column
        :param player: which player coin to draw.
        """
        if player == 1:
            color = self.__rcoin
        else:
            color = self.__bcoin
        self.__spots[i][j].configure(image=color)

    def __should_end(self):
        """
        checks if a game should end, shows end message if True.
        """
        winner = self.__game.get_winner()
        if winner is None:
            return

        if winner == 0:
            self.__end_img = ImageTk.PhotoImage(
                Image.open("ex12/tie.png"))
        elif winner == 1:
            self.__show_winner_coins()
            self.__end_img = ImageTk.PhotoImage(
                Image.open("ex12/player1win.png"))
        else:  # winner == 2
            self.__show_winner_coins()
            self.__end_img = ImageTk.PhotoImage(
                Image.open("ex12/player2win.png"))

        self.__end = tk.Button(self.__root, image=self.__end_img, bg="black",
                               command=self.__restart_game)
        self.__end.place(relx=0.32, rely=0.85)
        self.__game.game_on = False # prevents any more moves during end message

    def __restart_game(self):
        """
        after clicking on end message, restarts game.
        """
        self.__game.game_on = True
        self.__end.destroy()
        self.__bg.destroy()
        self.__init_board()
        self.__init_start()

    def __show_winner_coins(self):
        """
        shows the winner coins
        """
        winner = self.__game.get_winner()
        coin_list = self.__game.winner_coins
        if winner == 1:
            self.__win_img = ImageTk.PhotoImage(Image.open("ex12/rcoinwin.png"))
        else:
            self.__win_img = ImageTk.PhotoImage(Image.open("ex12/bcoinwin.png"))
        for winner_coin in coin_list:
            self.__spots[winner_coin[0]][winner_coin[1]].configure(
                image=self.__win_img)

    #  main buttons functions - running the game according to user's choice:
    def __two_players(self, event):
        """
        both player are humans.
        """
        self.__player = "both"
        self.__start_game()

    def __ai_player(self, event):
        """
        ai plays first.
        """
        self.__player = 2
        self.__ai = AI(self.__game, 1)
        self.__game.make_move(self.__ai.find_legal_move())
        self.__add_coin(*self.__game.get_data("last_move"))
        self.__start_game()

    def __player_ai(self, event):
        """
        human plays first.
        """
        self.__player = 1
        self.__ai = AI(self.__game, 2)
        self.__start_game()

    def __two_ai(self, event):
        """
        tow ai playing against each other.
        """
        self.__player = None
        self.__ai1 = AI(self.__game, 1)
        self.__ai2 = AI(self.__game, 2)
        self.__start_game()
        self.__play_two_ai()

    def __play_two_ai(self):
        """
        while game has not ended, preforms ai moves.
        """
        if self.__game.game_on:
            self.__ai1, self.__ai2 = self.__ai2, self.__ai1
            try:
                move = self.__ai2.find_legal_move()
                self.__game.make_move(move)
                self.__root.after(30, self.__play_two_ai)
                self.__add_coin(*self.__game.get_data("last_move"))
                self.__should_end()
            except:
                pass

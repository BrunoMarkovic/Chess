import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import PhotoImage
import config
import chess
from PIL import Image, ImageTk

class chessGame:
    def __init__(self):
        self.board = chess.board()
        self.white = self.board.get_white_player()
        self.black = self.board.get_black_player()
        self.images = {}
        self.playerTurn = self.white
        self.legal_move_positions = []
        self.LastPieceCliecked = None
        self.lastPieceMoved = None
        self.noOfMovesWithoutCaptureOrPawnMove = 0
        self.white_Draw_Call = False
        self.black_Draw_Call = False
        #self.positions = {}

        self.root = tk.Tk()
        self.root.title("Chess")
        self.root.geometry(str(config.HEIGHT) + "x" + str(config.WIDTH))
        self.root.minsize(770, 500)
        #self.root.config(background="white")

        self.menubar = tk.Menu(self.root)
        self.resign = tk.Menu(self.menubar, tearoff=0)
        self.resign.add_command(label="resign", command=lambda: self.resign_Call())
        self.resign.add_command(label="draw", command=lambda: self.draw_Call())
        self.menubar.add_cascade(menu=self.resign, label="End Game Options")
        self.root.config(menu=self.menubar)



        self.root.grid_rowconfigure(0, weight=1)

        self.root.grid_columnconfigure(0, weight=1)

        self.numOfRows = config.NOFROWS
        self.numOfCollumns = config.NOFCOLLUMNS

        self.buttons = {}

        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.config(padx=3, pady=3) #mogu dodat relif = tk.RAISED
        self.buttonFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        for i in range(self.numOfCollumns):
            self.buttonFrame.columnconfigure(i, weight=1, minsize=25)

        for i in range(self.numOfRows):
            self.buttonFrame.rowconfigure(i, weight=1, minsize=25)
        for i in range(self.numOfRows):
            for j in range(self.numOfCollumns):
                if (i + j) % 2 == 0:
                    btn1 = tk.Label(self.buttonFrame, font=("Arial", 18), bd=1, padx=0, pady=0, bg=chessGame.rgb_to_hex(236,236,211))
                else:
                    btn1 = tk.Label(self.buttonFrame, font=("Arial", 18), bd=1, padx=0, pady=0, bg=chessGame.rgb_to_hex(121,148,89))
                #btn1 = tk.Button(self.buttonFrame, font=("Arial", 18), bd=0, padx=0, pady=0, width=4, height=2, highlightbackground='darkgrey',highlightthickness=0,activebackground="lightgrey")
                btn1.grid(row=i, column=j, sticky=tk.N+tk.S+tk.E+tk.W)
                self.buttons[f'{i}button{j}'] = btn1
                btn1.bind('<Button-1>', lambda event, x=j, y=i, b=self.buttons[f'{i}button{j}']: self.buttonClicked(x, y, b))


        self.getImages()
        self.updateBoard()
        self.root.mainloop()


    def changeTurn(self):
        if self.playerTurn == self.white:
            self.playerTurn = self.black
        else:
            self.playerTurn = self.white

    def buttonClicked(self, x, y, button):
        #print(f'Button clicked at {x}, {y}')
        #print(self.legal_move_positions)
        #print(f'Player turn: {self.playerTurn.color}')
        #print(f'Last piece clicked: {self.LastPieceCliecked}')
        onBoard = self.board.is_anyPiece_atBoard_Player(x,y)
        whoseFigure = None
        if onBoard != None:
            whoseFigure = onBoard[1]
            Piece = onBoard[0]
            if whoseFigure == self.playerTurn:
                self.LastPieceCliecked = Piece
                self.clear_legal_move_highlights()
                self.legal_move_positions = self.board.legal_moves(Piece, whoseFigure)
                if self.lastPieceMoved != None:
                    if self.elPassant() != None:
                        self.legal_move_positions.append(self.elPassant())
                #print(self.legal_move_positions)
                self.highlight_legal_moves(self.legal_move_positions)
            else:
                if self.LastPieceCliecked != None:
                    if (x,y) in self.legal_move_positions:
                        noOfOtherPlayerPieces = len(self.otherPlayer().pieces)

                        is_ElPassant = None
                        if self.lastPieceMoved != None:
                            is_ElPassant = self.elPassant()
                        if is_ElPassant != None and (x,y) == is_ElPassant:
                            self.board.elPassant(self.lastPieceMoved, self.LastPieceCliecked, self.playerTurn)
                        else:
                            self.board.move_piece(self.LastPieceCliecked.x, self.LastPieceCliecked.y, x, y, self.playerTurn)
                        self.lastPieceMoved = self.LastPieceCliecked

                        self.check_if_game_Ended(noOfOtherPlayerPieces)
                        if self.LastPieceCliecked.get_type() == "pawn" and ((y == 7 and self.playerTurn == self.white) or (y == 0 and self.playerTurn == self.black)):
                            self.pawnPromotion(x,y, self.playerTurn.color)
                        self.updateBoard()
                        self.changeTurn()

                self.LastPieceCliecked = None
                if self.legal_move_positions != []:
                    self.clear_legal_move_highlights()

        else:
            if self.legal_move_positions != []:
                if (x,y) in self.legal_move_positions:
                    noOfOtherPlayerPieces = len(self.otherPlayer().pieces)
                    is_ElPassant = None
                    if self.lastPieceMoved != None:
                        is_ElPassant = self.elPassant()
                    if is_ElPassant != None and (x, y) == is_ElPassant:
                        self.board.elPassant(self.lastPieceMoved, self.LastPieceCliecked, self.playerTurn)
                    else:
                        self.board.move_piece(self.LastPieceCliecked.x, self.LastPieceCliecked.y, x, y, self.playerTurn)
                    self.lastPieceMoved = self.LastPieceCliecked
                    self.check_if_game_Ended(noOfOtherPlayerPieces)
                    if self.LastPieceCliecked.get_type() == "pawn" and (
                            (y == 7 and self.playerTurn == self.white) or (y == 0 and self.playerTurn == self.black)):
                        self.pawnPromotion(x,y, self.playerTurn.color)


                    #print(f'Trying to move piece from {self.LastPieceCliecked.x}, {self.LastPieceCliecked.y} to {x}, {y}, count: {self.noOfMovesWithoutCaptureOrPawnMove}')
                    self.updateBoard()
                    self.changeTurn()
            else:
                #print(f'{(x,y)} is not in {self.legal_move_positions}')
                self.LastPieceCliecked = None
            self.clear_legal_move_highlights()





        #print(f'Button clicked at {x}, {y}')

    @staticmethod
    def rgb_to_hex(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'


    def resign_Call(self):
        if self.playerTurn == self.white:
            messagebox.showinfo("Game Over", "Black wins!")
            self.root.quit()
        else:
            messagebox.showinfo("Game Over", "White wins!")
            self.root.quit()

    def draw_Call(self):
        if self.playerTurn == self.white:
            if self.white_Draw_Call == False:
                self.white_Draw_Call = True
        if self.playerTurn == self.black:
            if self.black_Draw_Call == False:
                self.black_Draw_Call = True
        if self.white_Draw_Call == True and self.black_Draw_Call == True:
            messagebox.showinfo("Game Over", "Game is draw")
            self.root.quit()




    def pawnPromotion(self, x, y, player_color):
        self.promotion_window = tk.Toplevel(self.root)
        self.promotion_window.title("Pawn Promotion")
        self.promotion_window.geometry("400x150")

        promotion_label = tk.Label(self.promotion_window, text="Select a piece to promote your pawn:",
                                   font=("Arial", 12))
        promotion_label.pack(side=tk.TOP, pady=10)


        button_frame = tk.Frame(self.promotion_window)
        button_frame.pack(side=tk.TOP)


        pieces = ["queen", "rock", "bishop", "knight"]
        piece_buttons = {}


        for col, piece in enumerate(pieces):
            img_path = f'images/{player_color}-{piece}.png'
            img = Image.open(img_path).convert('RGBA')
            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)

            # Create a button with the piece's image
            piece_button = tk.Button(button_frame, image=tk_img,
                                     command=lambda p=piece: self.promote_pawn(p, x, y, player_color))
            piece_button.image = tk_img
            piece_button.grid(row=0, column=col, padx=10)

            piece_buttons[piece] = piece_button

    def elPassant(self):
        if self.playerTurn.color == "white":
            if self.lastPieceMoved.get_type() == "pawn" and self.lastPieceMoved.y == 4 and self.LastPieceCliecked.y == 4:
                if self.lastPieceMoved.moved_Two == True and (self.LastPieceCliecked.x == self.lastPieceMoved.x + 1 or self.LastPieceCliecked.x == self.lastPieceMoved.x - 1):
                    return (self.lastPieceMoved.x, self.lastPieceMoved.y + 1)
            else:
                return None
        elif self.playerTurn.color == "black":
            if self.lastPieceMoved.get_type() == "pawn" and self.lastPieceMoved.y == 3 and self.LastPieceCliecked.y == 3:
                if self.lastPieceMoved.moved_Two == True and (self.LastPieceCliecked.x == self.lastPieceMoved.x + 1 or self.LastPieceCliecked.x == self.lastPieceMoved.x - 1):
                    return (self.lastPieceMoved.x, self.lastPieceMoved.y - 1)
        else:
            return None


    def promote_pawn(self, role,x,y, color):
        one_being_promoted = self.board.is_any_piece_atBoard(x, y)
        print(f"Promoting {one_being_promoted} to {role}")
        self.board.promote_pawn(color, one_being_promoted, role)
        self.updateBoard()
        self.promotion_window.destroy()
        self.root.deiconify()

    def getImages(self):
        cell_width = int(self.root.winfo_width() / self.numOfCollumns) - 2
        cell_height = int(self.root.winfo_height() / self.numOfRows) - 2

        for player in self.board.players:
            for piece in player.pieces:
                color = player.color
                img_path = f'images/{color}-{piece.get_type()}.png'
                try:
                    img = Image.open(img_path).convert('RGBA')
                    img = img.resize((cell_width, cell_height), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(img)
                    # Store the resized image with its piece type and color as key
                    self.images[f'{piece.get_type()}-{color}'] = tk_img
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")

    def otherPlayer(self):
        if self.playerTurn == self.white:
            return self.black
        else:
            return self.white



    def updateBoard(self):
        #cell_width = int(self.root.winfo_width() / self.numOfCollumns)
        #cell_height = int(self.root.winfo_height() / self.numOfRows)

        for i in range(self.numOfRows):
            for j in range(self.numOfCollumns):
                piece_info = self.board.is_anyPiece_atBoard_Player(i, j)
                if piece_info is not None:
                    piece = piece_info[0]
                    player = piece_info[1]
                    color = player.color

                    img_key = f'{piece.get_type()}-{color}'
                    self.buttons[f'{j}button{i}'].config(image=self.images[img_key])



                else:
                    self.buttons[f'{j}button{i}'].config(image='')


    def highlight_legal_moves(self, legalMoves):
        for move in legalMoves:
            to_x, to_y = move[0], move[1]


            if (to_x + to_y) % 2 == 0:
                self.buttons[f'{to_y}button{to_x}'].config(
                    bg=chessGame.rgb_to_hex(194, 226, 160))
            else:
                self.buttons[f'{to_y}button{to_x}'].config(
                    bg=chessGame.rgb_to_hex(139, 188, 98))




    def check_if_game_Ended(self, noOfOtherPlayerPieces):
        if self.board.check_mate(self.otherPlayer()):
            messagebox.showinfo("Game Over", f"Checkmate! {self.playerTurn.color} wins!")
            self.root.quit()
        elif self.board.is_stalemate(self.otherPlayer()):
            messagebox.showinfo("Game Over", "Stalemate! Game is draw")
            self.root.quit()
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Insufficient material! Game is draw")
            self.root.quit()

        if len(self.otherPlayer().pieces) == (noOfOtherPlayerPieces - 1) or self.LastPieceCliecked.get_type() == "pawn":
            self.noOfMovesWithoutCaptureOrPawnMove = 0
        else:
            self.noOfMovesWithoutCaptureOrPawnMove += 1
            if self.noOfMovesWithoutCaptureOrPawnMove == 50:
                messagebox.showinfo("Game Over", "50 moves without capture or pawn move, game is draw")
                self.root.quit()



    def clear_legal_move_highlights(self):

        for pos in self.legal_move_positions:
            x, y = pos

            if (x + y) % 2 == 0:
                self.buttons[f'{y}button{x}'].config(bg=chessGame.rgb_to_hex(236, 236, 211))
            else:
                self.buttons[f'{y}button{x}'].config(bg=chessGame.rgb_to_hex(121, 148, 89))


        self.legal_move_positions.clear()

chessGame()
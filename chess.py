import copy

class piece:

    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.type = "piece"


    def is_direction_valid(self, x, y):
        pass

    def move(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y


    def get_type(self):
        return self.type

    @staticmethod
    def is_valid_move(x, y):
        return x >= 0 and x < 8 and y >= 0 and y < 8

    def __str__(self):
        return self.type + " at position " + str(self.x) + ", " + str(self.y)

class pawn(piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hasMoved = False
        self.moved_Two = False
        self.type = "pawn"


    def is_direction_valid(self, x, y, color):
        if color == "black":
            if (y == self.y - 1 or (y == self.y - 2 and not self.hasMoved)) and x == self.x and self.is_valid_move(x, y) or ((self.x - 1 == x or self.x + 1 == x) and y == self.y - 1):
                return True
        elif color == "white":
            if (y == self.y + 1 or (y == self.y + 2 and not self.hasMoved)) and x == self.x and self.is_valid_move(x, y) or ((self.x - 1 == x or self.x + 1 == x) and y == self.y + 1):
                return True
        return False
    def move(self, x, y, color):
        if self.is_direction_valid(x, y, color):
            if self.x == x and abs(self.y - y) == 2:
                self.moved_Two = True
            self.x = x
            self.y = y
            self.hasMoved = True
        else:
            print("Invalid move")

    def elPassant_move(self, x,y):
        self.x = x
        self.y = y


class rock(piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hasMoved = False
        self.type = "rock"


    def is_direction_valid(self, x, y):
        if(x != self.x and y != self.y) or (x == self.x and y == self.y) or not self.is_valid_move(x, y):
            return False
        return True
    def move(self, x, y):
        if self.is_direction_valid(x, y):
            self.x = x
            self.y = y
            self.hasMoved = True
        else:
            print("Invalid move")

    def castle_move(self, x, y):
        if abs(x - self.x) == 2 and y == self.y or abs(x - self.x) == 3 and y == self.y:
            self.x = x
            self.y = y
            self.hasMoved = True
        else:
            print("Invalid move")


class bishop(piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "bishop"

    def is_direction_valid(self, x, y):
        if abs(x - self.x) != abs(y - self.y) or not self.is_valid_move(x, y):
            return False
        return True


    def move(self, x, y):
        if self.is_direction_valid(x, y):
            self.x = x
            self.y = y
        else:
            print("Invalid move")

class knight(piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "knight"

    def is_direction_valid(self, x, y):
        if (abs(x - self.x) != 2 or abs(y - self.y) != 1) and (abs(x - self.x) != 1 or abs(y - self.y) != 2) or not self.is_valid_move(x, y):
            return False
        return True

    def move(self, x, y):
        if self.is_direction_valid(x, y):
            self.x = x
            self.y = y
        else:
            print("Invalid move")

class queen(piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "queen"

    def is_direction_valid(self, x, y):
        if (abs(x - self.x) != abs(y - self.y) and x != self.x and y != self.y) or not self.is_valid_move(x, y) and (x == self.x and y == self.y):
            return False
        return True
    def move(self, x, y):
        if self.is_direction_valid(x, y):
            self.x = x
            self.y = y
        else:
            print("Invalid move")

class king(piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hasMoved = False
        self.type = "king"

    def is_direction_valid(self, x, y):
        if (abs(x - self.x) > 1 or abs(y - self.y) > 1) or not self.is_valid_move(x, y):
            return False
        return True

    def castle_move(self, x, y):
            self.x = x
            self.y = y
            self.hasMoved = True

    def move(self, x, y):
        if self.is_direction_valid(x, y):
            self.x = x
            self.y = y
            self.hasMoved = True
        else:
            print("Invalid move")
        '''
        self.x = x
        self.y = y
        '''

class player:
    def __init__(self, color):
        self.pieces = []
        self.color = color
        if self.color == "white":
            self.pieces.append(rock(0, 0))
            self.pieces.append(knight(1, 0))
            self.pieces.append(bishop(2, 0))
            self.pieces.append(queen(3, 0))
            self.pieces.append(king(4, 0))
            self.pieces.append(bishop(5, 0))
            self.pieces.append(knight(6, 0))
            self.pieces.append(rock(7, 0))
            for i in range(8):
                self.pieces.append(pawn(i, 1))
        else:
            self.pieces.append(rock(0, 7))
            self.pieces.append(knight(1, 7))
            self.pieces.append(bishop(2, 7))
            self.pieces.append(queen(3, 7))
            self.pieces.append(king(4, 7))
            self.pieces.append(bishop(5, 7))
            self.pieces.append(knight(6, 7))
            self.pieces.append(rock(7, 7))
            for i in range(8):
                self.pieces.append(pawn(i, 6))

    def is_any_piece_at(self, x, y):
        for piece in self.pieces:
            if piece.get_position() == (x, y):
                return piece
        return None

    def move_piece(self, x, y, new_x, new_y):
        piece = self.is_any_piece_at(x, y)
        if piece is None:
            print("No piece at position " + str(x) + ", " + str(y))
        else:
            piece.move(new_x, new_y)

    def addPiece(self, piece):
        self.pieces.append(piece)

    def removePiece(self, piece):
        self.pieces.remove(piece)

    def print_pieces(self):
        for piece in self.pieces:
            print(piece)


class board:

    def __init__(self):
        self.players = []
        self.players.append(player("white"))
        self.players.append(player("black"))

    def get_white_player(self):
        return self.players[0]

    def promote_pawn(self, color, piece, role):
        player = self.get_player(color)
        if role == "queen":
            player.removePiece(piece)
            player.addPiece(queen(piece.get_position()[0], piece.get_position()[1]))
        elif role == "rock":
            player.removePiece(piece)
            player.addPiece(rock(piece.get_position()[0], piece.get_position()[1]))
        elif role == "bishop":
            player.removePiece(piece)
            player.addPiece(bishop(piece.get_position()[0], piece.get_position()[1]))
        elif role == "knight":
            player.removePiece(piece)
            player.addPiece(knight(piece.get_position()[0], piece.get_position()[1]))

    def get_black_player(self):
        return self.players[1]

    def does_player_have_two_knights(self, player):
        count = 0
        for piece in player.pieces:
            if piece.get_type() == "knight":
                count += 1
        return count == 2


    def does_playerhave_material(self, player):
        if len(player.pieces) > 2:
            return True
        else:
            if len(player.pieces) == 1:
                return False
            elif len(player.pieces) == 2:
                if player.pieces[0].get_type() == "bishop" or player.pieces[1].get_type() == "bishop":
                    return False
                elif player.pieces[0].get_type() == "knight" or player.pieces[1].get_type() == "knight":
                    return False
        return True

    def is_insufficient_material(self):
        if len(self.get_white_player().pieces) > 3 or len(self.get_black_player().pieces) > 3:
            return False
        if len(self.get_white_player().pieces) == 3 and len(self.get_black_player().pieces) == 1 and self.does_player_have_two_knights(self.get_white_player()):
            return True
        elif len(self.get_white_player().pieces) == 1 and len(self.get_black_player().pieces) == 3 and self.does_player_have_two_knights(self.get_black_player()):
            return True
        if len(self.get_white_player().pieces) > 2 or len(self.get_black_player().pieces) > 2:
            return False
        if not self.does_playerhave_material(self.get_white_player()) and not self.does_playerhave_material(self.get_black_player()):
            return True
        return False





    def elPassant(self, pieceEaten, pieceEating, player):
        self.other_Player(player).removePiece(pieceEaten)
        if player.color == "black":
            pieceEating.elPassant_move(pieceEaten.get_position()[0], pieceEating.get_position()[1] - 1)
        elif player.color == "white":
            pieceEating.elPassant_move(pieceEaten.get_position()[0], pieceEating.get_position()[1] + 1)

    def get_player(self, color):
        for player in self.players:
            if player.color == color:
                return player

    def is_any_piece_atBoard(self, x, y):
        for player in self.players:
            if player.is_any_piece_at(x, y) is not None:
                return player.is_any_piece_at(x, y)
        return None

    def is_anyPiece_atBoard_Player(self,x,y):
        for player in self.players:
            if player.is_any_piece_at(x,y) is not None:
                return (player.is_any_piece_at(x,y),player)
        return None


    def add_piece(self, piece, player):
        player.addPiece(piece)

    def remove_piece(self, piece, player):
        player.removePiece(piece)

    def remove_piece_cordinates(self, x, y):
        for player in self.players:
            piece = player.is_any_piece_at(x, y)
            if piece is not None:
                player.removePiece(piece)
                return piece
        return None


    def other_Player(self, player):
        for otherPlayer in self.players:
            if otherPlayer != player:
                return otherPlayer

    def is_my_piece_at(self, player, x, y):
        return player.is_any_piece_at(x, y) is not None

    def is_any_piece_at_path(self, piece, ex, ey):
        if piece.get_type() == "rock":
            found = False
            px = piece.get_position()[0]
            py = piece.get_position()[1]
            if px == ex:
                for i in range(min(py, ey) + 1, max(py, ey)):
                    if piece.is_valid_move(px, i) and self.is_any_piece_atBoard(px, i) is not None:
                        found = True
                        break
                if found:
                    return True
            elif py == ey:
                found = False
                for i in range(min(px, ex) + 1, max(px, ex)):
                    if piece.is_valid_move(i, py) and self.is_any_piece_atBoard(i, py) is not None:
                        found = True
                        break
                if found:
                    return True
            else:
                return True
        elif piece.get_type() == "bishop":
            found = False
            px = piece.get_position()[0]
            py = piece.get_position()[1]
            if abs(px - ex) == abs(py - ey):
                found = False
                for i in range(1, abs(px - ex)):
                    if px > ex and py > ey:
                        if piece.is_valid_move(px - i, py - i) and self.is_any_piece_atBoard(px - i, py - i) is not None :
                            found = True
                            break
                    elif px < ex and py < ey:
                        if piece.is_valid_move(px + i, py + i) and self.is_any_piece_atBoard(px + i, py + i) is not None:
                            found = True
                            break
                    elif px > ex and py < ey:
                        if piece.is_valid_move(px - i, py + i) and self.is_any_piece_atBoard(px - i, py + i) is not None:
                            found = True
                            break
                    elif px < ex and py > ey:
                        if piece.is_valid_move(px + i, py - i) and self.is_any_piece_atBoard(px + i, py - i) is not None:
                            found = True
                            break
                if found:
                    return True
            else:
                return True
        elif piece.get_type() == "queen":
            found = False
            px = piece.get_position()[0]
            py = piece.get_position()[1]
            if px == ex:
                for i in range(min(py, ey) + 1, max(py, ey)):
                    if piece.is_valid_move(px, i) and self.is_any_piece_atBoard(px, i) is not None:
                        found = True
                        break
                if found:
                    return True
            elif py == ey:
                found = False
                for i in range(min(px, ex) + 1, max(px, ex)):
                    if piece.is_valid_move(i, py) and self.is_any_piece_atBoard(i, py) is not None:
                        found = True
                        break
                if found:
                    return True
            elif abs(px - ex) == abs(py - ey):
                found = False
                for i in range(1, abs(px - ex)):
                    if px > ex and py > ey:
                        if piece.is_valid_move(px - i, py - i) and self.is_any_piece_atBoard(px - i, py - i) is not None :
                            found = True
                            break
                    elif px < ex and py < ey:
                        if piece.is_valid_move(px + i, py + i) and self.is_any_piece_atBoard(px + i, py + i) is not None:
                            found = True
                            break
                    elif px > ex and py < ey:
                        if piece.is_valid_move(px - i, py + i) and self.is_any_piece_atBoard(px - i, py + i) is not None:
                            found = True
                            break
                    elif px < ex and py > ey:
                        if piece.is_valid_move(px + i, py - i) and self.is_any_piece_atBoard(px + i, py - i) is not None:
                            found = True
                            break
                if found:
                    return True
            else:
                return True
        return False




    def didCheckOcure(self, player):
        king = None
        for piece in player.pieces:
            if piece.get_type() == "king":
                king = piece
                break
        ex = king.get_position()[0]
        ey = king.get_position()[1]
        color = player.color
        for otherPlayer in self.players:
            if otherPlayer != player:
                for piece in otherPlayer.pieces:
                    if piece.get_type() == "queen" or piece.get_type() == "rock" or piece.get_type() == "bishop":
                        if not self.is_any_piece_at_path(piece, ex, ey):
                            return True # msm da ode nebi trebalo returnat nego samo nastavit dalje u iducu iteraciju
                    elif piece.get_type() == "knight":
                        found = False
                        px = piece.get_position()[0]
                        py = piece.get_position()[1]
                        if (abs(px - ex) == 2 and abs(py - ey) == 1) or (abs(px - ex) == 1 and abs(py - ey) == 2):
                            return True
                    elif piece.get_type() == "pawn":
                        found = False
                        px = piece.get_position()[0]
                        py = piece.get_position()[1]
                        if color == "black":
                            if (py == ey - 1 and (px == ex - 1 or px == ex + 1)):
                                return True
                        elif color == "white":
                            if (py == ey + 1 and (px == ex - 1 or px == ex + 1)):
                                return True
        return False


    def did_User_Make_Check(self, player):
        otherPlayer = self.other_Player(player)
        return self.didCheckOcure(otherPlayer)

    def do_castling(self, player, side):
        if side == 0:
            if player.color == "white":
                player.is_any_piece_at(4, 0).castle_move(6, 0)
                player.is_any_piece_at(7, 0).castle_move(5, 0)
            elif player.color == "black":
                player.is_any_piece_at(4, 7).castle_move(6, 7)
                player.is_any_piece_at(7, 7).castle_move(5, 7)
        elif side == 1:
            if player.color == "white":
                player.is_any_piece_at(4, 0).castle_move(2, 0)
                player.is_any_piece_at(0, 0).castle_move(3, 0)
            elif player.color == "black":
                player.is_any_piece_at(4, 7).castle_move(2, 7)
                player.is_any_piece_at(0, 7).castle_move(3, 7)

    def move_piece(self, x, y, new_x, new_y, player, jeliProvjera = False, isSpecialMove = False): # jeli provjera mi sluzi samo da mogu provjeravat za check mate ||| isSpecialMove sluzi za castling

        didIEat = False
        doINeedToReverseHasMoved = False
        oneTheatIsEaten = None
        piece = player.is_any_piece_at(x, y)
        if not isSpecialMove:
            if player.color == "white":
                if x == 4 and y == 0:
                    if player.is_any_piece_at(x,y).get_type() == "king":
                        if new_x == 6 and new_y == 0:
                            if self.is_castle_possible(player, 0):
                                self.do_castling(player, 0)
                                isSpecialMove = True
                                return
                        elif new_x == 2 and new_y == 0:
                            if self.is_castle_possible(player, 1):
                                self.do_castling(player, 1)
                                isSpecialMove = True
                                return
            elif player.color == "black":
                if x == 4 and y == 7:
                    if player.is_any_piece_at(x,y).get_type() == "king":
                        if new_x == 6 and new_y == 7:
                            if self.is_castle_possible(player, 0):
                                self.do_castling(player, 0)
                                isSpecialMove = True
                                return
                        elif new_x == 2 and new_y == 7:
                            if self.is_castle_possible(player, 1):
                                self.do_castling(player, 1)
                                isSpecialMove = True
                                return




        if piece is None:
            print("No piece at position " + str(x) + ", " + str(y))
        else:
            if piece.get_type() == "pawn":
                if not piece.is_direction_valid(new_x, new_y, player.color):
                    print("Invalid move")
                    return
            else:
                if not piece.is_direction_valid(new_x, new_y) and not isSpecialMove:
                    print("Invalid move")
                    return

            # MORAMO PROVJERITI DA LI JE POTEZ VALIDAN, ne smi niko biti na putu niti smije na tom polju biti iste boje
            # treba dodatno provjeriti ako je pawn da li je prvi potez i da li se krece naprijed i ima li neko na putu, i ima li neko na polju di zeli ic nebitno nas ili njihov
            # ne smi se kralj kretati u polje gdje je moguc napad
            # ne smi se nista pokrenit ako ce time nastat sah za igraca koji je na potezu
            if piece.get_type() == "pawn":
                # provjera jel iko ima na polju di zelimo ic ++
                # provjera jel jel iko ima na putu ako se krecemo dva polja ++
                # provjera jel protivnicka figura na dijagonali ako se krecemo dijametralno ++
                #  provjera ako ima neki protivnicki pawn na dijagonali da li je to en passant
                didAte = False
                didInvaltiMove = False
                if ((new_x - 1 == x or new_x + 1 == x) and new_y == y - 1 and player.color == "black") or (
                        (new_x - 1 == x or new_x + 1 == x) and new_y == y + 1 and player.color == "white"):
                    if not self.is_my_piece_at(self.other_Player(player), new_x, new_y):
                        print("Invalid move")
                        didInvaltiMove = True
                    else:
                        didAte = True
                elif self.is_my_piece_at(player, new_x, new_y) or self.is_my_piece_at(self.other_Player(player), new_x, new_y):
                    print("Invalid move")
                    didInvaltiMove = True
                elif ((new_y == y - 2 and not piece.hasMoved) and new_x == x) or ((new_y == y + 2 and not piece.hasMoved) and new_x == x): # ode se u teoriji moze desit da if prode za npr  + 2 sta je bijeli a dole provjerava jel crn i nece se skuzit da je invalidan potez, ali to ce se opet provjerit u move.piece
                    if player.color == "black":
                        if self.is_any_piece_atBoard(x, y - 1) is not None:
                            print("Invalid move")
                            didInvaltiMove = True
                    elif player.color == "white":
                        if self.is_any_piece_atBoard(x, y + 1) is not None:
                            print("Invalid move")
                            didInvaltiMove = True
                if didInvaltiMove:
                    return
                else:
                    if didAte:
                        self.remove_piece(self.is_any_piece_atBoard(new_x, new_y), self.other_Player(player))
                    piece.move(new_x, new_y, player.color)
            else:
                didIEat = False
                if piece.get_type() == "rock" or piece.get_type() == "queen" or piece.get_type() == "bishop":
                    if self.is_any_piece_at_path(piece, new_x, new_y) or self.is_my_piece_at(player, new_x, new_y):
                        print("Invalid move")
                        return
                    if self.is_my_piece_at(self.other_Player(player), new_x, new_y):
                        didIEat = True

                elif piece.get_type() == "knight":
                    if self.is_my_piece_at(player, new_x, new_y):
                        print("Invalid move")
                        return
                    if self.is_my_piece_at(self.other_Player(player), new_x, new_y):
                        didIEat = True
                elif piece.get_type() == "king":
                    if self.is_my_piece_at(player, new_x, new_y):
                        print("Invalid move")
                        return
                    if self.is_my_piece_at(self.other_Player(player), new_x, new_y):
                        didIEat = True
                if didIEat:
                    oneTheatIsEaten = self.is_any_piece_atBoard(new_x, new_y)
                    #print(f'ovaj je pojeden {oneTheatIsEaten}')
                    self.other_Player(player).removePiece(oneTheatIsEaten)

                if piece.get_type() == "king" or piece.get_type() == "rock":
                    if not piece.hasMoved:
                        doINeedToReverseHasMoved = True
                if piece.get_type() == "king" and isSpecialMove:
                    piece.castle_move(new_x, new_y)
                else:
                    piece.move(new_x, new_y) # provjeri ako je special move da pozoven drugu metodu koja ce ga maknit sa starog polja i stavit na novo
            if self.didCheckOcure(player) and not jeliProvjera:
                print("Invalid move")
                if piece.get_type() == "pawn":
                    piece.move(x, y, player.color)
                else:
                    piece.move(x, y)
                    if piece.get_type() == "king" or piece.get_type() == "rock":
                        if doINeedToReverseHasMoved:
                            piece.hasMoved = False
                if didIEat:
                    self.add_piece(oneTheatIsEaten, self.other_Player(player))
                return
            elif self.did_User_Make_Check(player) and not jeliProvjera:
                print("Check")

    def is_castle_possible(self, player, side): # side 0 je short side 1 je long side
        cpy = copy.deepcopy(self)
        cpyPlayer = None
        if player.color == "white":
            cpyPlayer = cpy.get_white_player()
        elif player.color == "black":
            cpyPlayer = cpy.get_black_player()




        piece = None
        if player.color == "white":
            if player.is_any_piece_at(4,0).get_type() != "king":
                return False
            else:
                piece = player.is_any_piece_at(4,0)
        elif player.color == "black":
            if player.is_any_piece_at(4,7).get_type() != "king":
                return False
            else:
                piece = player.is_any_piece_at(4,7)
        else:
            return False


        if player.color == "white":
            if side == 0:
                if piece.get_position() == (4, 0) and not piece.hasMoved and self.is_any_piece_atBoard(5, 0) is None and self.is_any_piece_atBoard(6, 0) is None and player.is_any_piece_at(7, 0) is not None and player.is_any_piece_at(7, 0).get_type() == "rock" and not player.is_any_piece_at(7, 0).hasMoved and not self.didCheckOcure(player):
                    cpy.move_piece(4, 0, 6, 0, cpy.get_player(player.color), True, isSpecialMove=True)
                    if not cpy.didCheckOcure(cpy.get_player(player.color)):
                        cpy.move_piece(6, 0, 5, 0, cpy.get_player(player.color), True, isSpecialMove=True)
                        if not cpy.didCheckOcure(cpy.get_player(player.color)):
                            return True
                        else:
                            return False
                    else :
                        return False
            elif side == 1:
                if piece.get_position() == (4, 0) and not piece.hasMoved and self.is_any_piece_atBoard(3, 0) is None and self.is_any_piece_atBoard(2, 0) is None and self.is_any_piece_atBoard(1, 0) is None and player.is_any_piece_at(0, 0) is not None and player.is_any_piece_at(0, 0).get_type() == "rock" and not player.is_any_piece_at(0, 0).hasMoved and not self.didCheckOcure(player):
                    cpy.move_piece(4, 0, 2, 0, cpy.get_player(player.color), True, isSpecialMove=True)
                    if not cpy.didCheckOcure(cpy.get_player(player.color)):
                        cpy.move_piece(2, 0, 3, 0, cpy.get_player(player.color), True, isSpecialMove=True)
                        if not cpy.didCheckOcure(cpy.get_player(player.color)):
                            return True
                        else:
                            return False
                    else:
                        return False

        elif player.color == "black":
            if side == 0:
                if piece.get_position() == (4, 7) and not piece.hasMoved and self.is_any_piece_atBoard(5, 7) is None and self.is_any_piece_atBoard(6, 7) is None and player.is_any_piece_at(7, 7) is not None and player.is_any_piece_at(7, 7).get_type() == "rock" and not player.is_any_piece_at(7, 7).hasMoved and not self.didCheckOcure(player):
                    cpy.move_piece(4, 7, 6, 7, cpy.get_player(player.color), True, isSpecialMove=True)
                    if not cpy.didCheckOcure(cpy.get_player(player.color)):
                        cpy.move_piece(6, 7, 5, 7, cpy.get_player(player.color), True, isSpecialMove=True)
                        if not cpy.didCheckOcure(cpy.get_player(player.color)):
                            return True
                        else:
                            return False
                    else:
                        return False
            elif side == 1:
                if piece.get_position() == (4, 7) and not piece.hasMoved and self.is_any_piece_atBoard(3, 7) is None and self.is_any_piece_atBoard(2, 7) is None and self.is_any_piece_atBoard(1, 7) is None and player.is_any_piece_at(0, 7) is not None and player.is_any_piece_at(0, 7).get_type() == "rock" and not player.is_any_piece_at(0, 7).hasMoved and not self.didCheckOcure(player):
                    cpy.move_piece(4, 7, 2, 7, cpy.get_player(player.color), True, isSpecialMove=True)
                    if not cpy.didCheckOcure(cpy.get_player(player.color)):
                        cpy.move_piece(2, 7, 3, 7, cpy.get_player(player.color), True, isSpecialMove=True)
                        if not cpy.didCheckOcure(cpy.get_player(player.color)):
                            return True
                        else:
                            return False
                    else:
                        return False
        return False





    def legal_moves(self, piece, player):
        legal_moves = []
        x = piece.get_position()[0]
        y = piece.get_position()[1]
        cpy = copy.deepcopy(self)
        color = player.color
        cpyPlayer = cpy.get_player(color)

        if piece.get_type() == "rock":
            for i in range(8):
                if i != x:
                    if not self.is_any_piece_at_path(piece, i, y) and (self.is_any_piece_atBoard(i, y) is None or self.other_Player(player).is_any_piece_at(i, y) is not None):
                        cpy.move_piece(x, y, i, y, cpy.get_player(color), True)
                        if not cpy.didCheckOcure(cpy.get_player(color)):
                            legal_moves.append((i, y))
                        cpy = copy.deepcopy(self)
                if i != y:
                    if not self.is_any_piece_at_path(piece, x, i) and (self.is_any_piece_atBoard(x, i) is None or self.other_Player(player).is_any_piece_at(x, i) is not None):
                        cpy.move_piece(x, y, x, i, cpy.get_player(color), True)
                        if not cpy.didCheckOcure(cpy.get_player(color)):
                            legal_moves.append((x, i))
                        cpy = copy.deepcopy(self)
        elif piece.get_type() == "bishop":
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x + i, y + i) and (self.is_any_piece_atBoard(x + i, y + i) is None or self.other_Player(player).is_any_piece_at(x + i, y + i)) and piece.is_valid_move(x + i, y + i):
                    cpy.move_piece(x, y, x + i, y + i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x + i, y + i))
                    cpy = copy.deepcopy(self)

                    if self.other_Player(player).is_any_piece_at(x + i, y + i) is not None:
                        break
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x - i, y - i ) and (self.is_any_piece_atBoard(x - i, y - i) is None or self.other_Player(player).is_any_piece_at(x - i, y - i)) and piece.is_valid_move(x - i, y - i):
                    cpy.move_piece(x, y, x - i, y - i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x - i, y - i))
                    cpy = copy.deepcopy(self)
                    if self.other_Player(player).is_any_piece_at(x - i, y - i) is not None:
                        break
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x + i, y - i) and (self.is_any_piece_atBoard(x + i, y - i) is None or self.other_Player(player).is_any_piece_at(x + i, y - i) ) and piece.is_valid_move(x + i, y - i):
                    cpy = copy.deepcopy(self)
                    cpy.move_piece(x, y, x + i, y - i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x + i, y - i))
                    cpy = copy.deepcopy(self)

                    if self.other_Player(player).is_any_piece_at(x + i, y - i) is not None:
                        break
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x - i, y + i) and (self.is_any_piece_atBoard(x - i, y + i) is None or self.other_Player(player).is_any_piece_at(x - i, y + i) ) and piece.is_valid_move(x - i, y + i):
                    cpy = copy.deepcopy(self)
                    cpy.move_piece(x, y, x - i, y + i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x - i, y + i))
                    cpy = copy.deepcopy(self)
                    if self.other_Player(player).is_any_piece_at(x - i, y + i) is not None:
                        break
        elif piece.get_type() == "queen":
            for i in range(8):
                if i != x:
                    if not self.is_any_piece_at_path(piece, i, y) and (self.is_any_piece_atBoard(i, y) is None or self.other_Player(player).is_any_piece_at(i, y) is not None):
                        cpy.move_piece(x, y, i, y, cpy.get_player(color), True)
                        if not cpy.didCheckOcure(cpy.get_player(color)):
                            legal_moves.append((i, y))
                        cpy = copy.deepcopy(self)

                if i != y:
                    if not self.is_any_piece_at_path(piece, x, i) and (self.is_any_piece_atBoard(x, i) is None or self.other_Player(player).is_any_piece_at(x, i) is not None):
                        cpy.move_piece(x, y, x, i, cpy.get_player(color), True)
                        if not cpy.didCheckOcure(cpy.get_player(color)):
                            legal_moves.append((x, i))
                        cpy = copy.deepcopy(self)
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x + i, y + i) and (self.is_any_piece_atBoard(x + i, y + i) is None or self.other_Player(player).is_any_piece_at(x + i, y + i)) and piece.is_valid_move(x + i, y + i):
                    cpy.move_piece(x, y, x + i, y + i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x + i, y + i))
                    cpy = copy.deepcopy(self)
                    if self.other_Player(player).is_any_piece_at(x + i, y + i) is not None:
                        break
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x - i, y - i ) and (self.is_any_piece_atBoard(x - i, y - i) is None or self.other_Player(player).is_any_piece_at(x - i, y - i)) and piece.is_valid_move(x - i, y - i):
                    cpy.move_piece(x, y, x - i, y - i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x - i, y - i))
                    cpy = copy.deepcopy(self)
                    if self.other_Player(player).is_any_piece_at(x - i, y - i) is not None:
                        break
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x + i, y - i) and (self.is_any_piece_atBoard(x + i, y - i) is None or self.other_Player(player).is_any_piece_at(x + i, y - i) ) and piece.is_valid_move(x + i, y - i):
                    cpy.move_piece(x, y, x + i, y - i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x + i, y - i))
                    cpy = copy.deepcopy(self)
                    if self.other_Player(player).is_any_piece_at(x + i, y - i) is not None:
                        break
            for i in range(1,8):
                if not self.is_any_piece_at_path(piece, x - i, y + i) and (self.is_any_piece_atBoard(x - i, y + i) is None or self.other_Player(player).is_any_piece_at(x - i, y + i) ) and piece.is_valid_move(x - i, y + i):
                    cpy.move_piece(x, y, x - i, y + i, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x - i, y + i))
                    cpy = copy.deepcopy(self)
                    if self.other_Player(player).is_any_piece_at(x - i, y + i) is not None:
                        break
        elif piece.get_type() == "king":
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if piece.is_valid_move(x + i, y + j) and (self.is_any_piece_atBoard(x + i, y + j) is None or self.other_Player(player).is_any_piece_at(x + i, y + j) is not None):
                        cpy.move_piece(x, y, x + i, y + j, cpy.get_player(color), True)
                        if not cpy.didCheckOcure(cpy.get_player(color)):
                            legal_moves.append((x + i, y + j))
                        cpy = copy.deepcopy(self)

            if player.color == "white" and not piece.hasMoved and self.is_castle_possible(player, 0):
                legal_moves.append((6, 0))
            elif player.color == "white" and not piece.hasMoved and self.is_castle_possible(player, 1):
                legal_moves.append((2, 0))
            elif player.color == "black" and not piece.hasMoved and self.is_castle_possible(player, 0):
                legal_moves.append((6, 7))
            elif player.color == "black" and not piece.hasMoved and self.is_castle_possible(player, 1):
                legal_moves.append((2, 7))

        elif piece.get_type() == "knight":
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if abs(i) == 2 and abs(j) == 1 or abs(i) == 1 and abs(j) == 2:
                        if piece.is_valid_move(x + i, y + j) and (self.is_any_piece_atBoard(x + i, y + j) is None or self.other_Player(player).is_any_piece_at(x + i, y + j) is not None):
                            cpy.move_piece(x, y, x + i, y + j, cpy.get_player(color), True)
                            if not cpy.didCheckOcure(cpy.get_player(color)):
                                legal_moves.append((x + i, y + j))
                            cpy = copy.deepcopy(self)
        elif piece.get_type() == "pawn":
            # napravit provjeru za en passant i za promjenu u drugu figuru
            if player.color == "black":
                if self.is_any_piece_atBoard(x, y - 1) is None:
                    cpy.move_piece(x, y, x, y - 1, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x, y - 1))
                    cpy = copy.deepcopy(self)
                    if not piece.hasMoved and self.is_any_piece_atBoard(x, y - 2) is None:
                        cpy.move_piece(x, y, x, y - 2, cpy.get_player(color), True)
                        if not cpy.didCheckOcure(cpy.get_player(color)):
                            legal_moves.append((x, y - 2))
                        cpy = copy.deepcopy(self)
                if self.is_any_piece_atBoard(x - 1, y - 1) is not None and self.other_Player(player).is_any_piece_at(x - 1, y - 1) is not None:
                    cpy.move_piece(x, y, x - 1, y - 1, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x - 1, y - 1))
                    cpy = copy.deepcopy(self)
                if self.is_any_piece_atBoard(x + 1, y - 1) is not None and self.other_Player(player).is_any_piece_at(x + 1, y - 1) is not None:
                    cpy.move_piece(x, y, x + 1, y - 1, cpy.get_player(color), True)
                    if not cpy.didCheckOcure(cpy.get_player(color)):
                        legal_moves.append((x + 1, y - 1))
                    cpy = copy.deepcopy(self)
            elif player.color == "white":
                if self.is_any_piece_atBoard(x, y + 1) is None:
                    cpy.move_piece(x, y, x, y + 1, cpy.get_white_player(), True)
                    if not cpy.didCheckOcure(cpy.get_white_player()):
                        legal_moves.append((x, y + 1))
                    cpy = copy.deepcopy(self)
                    if not piece.hasMoved and self.is_any_piece_atBoard(x, y + 2) is None:
                        cpy.move_piece(x, y, x, y + 2, cpy.get_white_player(), True)
                        if not cpy.didCheckOcure(cpy.get_white_player()):
                            legal_moves.append((x, y + 2))
                        cpy = copy.deepcopy(self)
                if self.is_any_piece_atBoard(x - 1, y + 1) is not None and self.other_Player(player).is_any_piece_at(x - 1, y + 1) is not None:
                    cpy.move_piece(x, y, x - 1, y + 1, cpy.get_white_player(), True)
                    if not cpy.didCheckOcure(cpy.get_white_player()):
                        legal_moves.append((x - 1, y + 1))
                    cpy = copy.deepcopy(self)
                if self.is_any_piece_atBoard(x + 1, y + 1) is not None and self.other_Player(player).is_any_piece_at(x + 1, y + 1) is not None:
                    cpy.move_piece(x, y, x + 1, y + 1, cpy.get_white_player(), True)
                    if not cpy.didCheckOcure(cpy.get_white_player()):
                        legal_moves.append((x + 1, y + 1))
                    cpy = copy.deepcopy(self)
        return legal_moves



    def check_mate(self, player):
        color = player.color
        if not self.didCheckOcure(player):
            return False
        for piece in player.pieces:
            for move in self.legal_moves(piece, player):
                x = piece.get_position()[0]
                y = piece.get_position()[1]
                new_x = move[0]
                new_y = move[1]
                cpy = copy.deepcopy(self)
                cpy.move_piece(x, y, new_x, new_y, cpy.get_player(color), True)
                if not cpy.didCheckOcure(cpy.get_player(color)):
                    cpy.move_piece(new_x, new_y, x, y, cpy.get_player(color), True)
                    return False
                cpy.move_piece(new_x, new_y, x, y, cpy.get_player(color), True)
        return True

    def is_stalemate(self, player):
        color = player.color
        if self.didCheckOcure(player):
            return False
        for piece in player.pieces:
            for move in self.legal_moves(piece, player):
                x = piece.get_position()[0]
                y = piece.get_position()[1]
                new_x = move[0]
                new_y = move[1]
                cpy = copy.deepcopy(self)
                cpy.move_piece(x, y, new_x, new_y, cpy.get_player(color), True)
                if not cpy.didCheckOcure(cpy.get_player(color)):
                    return False
        return True
    def print_board(self):
        for i in range(8):
            for j in range(8):
               found = False
               for player in self.players:
                     if player.is_any_piece_at(j, i) is not None:
                          print(player.is_any_piece_at(j, i).get_type()[0], end=" ")
                          found = True
                          break
               if not found:
                     print("-", end=" ")
            print()













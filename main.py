import pygame
import pygame.gfxdraw
pygame.init()
import random
import math
import copy
import time
import ui
width, height = 640, 640
fps = 60
ai_depth = 2
vs_ai = True
both_ai = False
board_width, board_height, board_size = min(width, height), min(width, height), 8
window = pygame.display.set_mode([width, height])
pygame.display.set_caption("LOADING IMAGES")
def draw_board(board_size, board_width, board_height):
    for i in range(board_size):
        for j in range(board_size):
            square_rect = pygame.Rect(j*board_width/board_size, i*board_height/board_size, board_width/board_size, board_height/board_size)
           
            pygame.draw.rect(window, squares[j+(i*board_size)].color, square_rect)



black_attacked_squares = set()
white_attacked_squares = set()

squares_with_squares = []
squares_with_white_squares = []
squares_with_black = []

PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

WHITE = 1
BLACK = 2

CREAM = (255, 220, 190)
BROWN = (170, 119, 87)

BLUE = (96, 128, 196)
LIGHT_BLUE = (215, 225, 255)

GREEN = (90, 196, 120)
LIGHT_GREEN = (205, 255, 225)

GRAY = (142, 142, 142)

LIGHT_GRAY = (225, 225, 225)

SILVER = (128, 128, 172)

LIGHT_SILVER = (225, 225, 255)

COLOR_SCHEME = (SILVER, LIGHT_SILVER)

DARK_SQUARE_COLOR, LIGHT_SQUARE_COLOR = COLOR_SCHEME

LIGHT_SQUARE_SELECTED_COLOR = (LIGHT_SQUARE_COLOR[0]/1.07, LIGHT_SQUARE_COLOR[1]/1.07, LIGHT_SQUARE_COLOR[2]/1.07)
DARK_SQUARE_SELECTED_COLOR = (DARK_SQUARE_COLOR[0]/1.15, DARK_SQUARE_COLOR[1]/1.15, DARK_SQUARE_COLOR[2]/1.15)

LIGHT_SQUARE_CHECK_COLOR = (LIGHT_SQUARE_COLOR[0], LIGHT_SQUARE_COLOR[1]/2, LIGHT_SQUARE_COLOR[2]/2)
DARK_SQUARE_CHECK_COLOR = (DARK_SQUARE_COLOR[0], DARK_SQUARE_COLOR[1]/2, DARK_SQUARE_COLOR[2]/2)
DOT_COLOR = (LIGHT_SQUARE_COLOR[0]/2+DARK_SQUARE_COLOR[0]/2, LIGHT_SQUARE_COLOR[1]/2+DARK_SQUARE_COLOR[1]/2, LIGHT_SQUARE_COLOR[2]/2+DARK_SQUARE_COLOR[2]/2)
turns = 0


def next_square_up(squares, square):
    num = square.x+square.y*board_size
    num -= 8
    if num < 64 and num >= 0:
        return squares[num]
    return None

def next_square_down(squares, square):
    num = square.x+square.y*board_size
    num += 8
    if num < 64 and num >= 0:
        return squares[num]
    return None

def next_square_right(squares, square):
    num = square.x+square.y*board_size
    if square.x < 7:
        num += 1
    else:
        return None
    if num < 64 and num >= 0:
        return squares[num]
    return None

def next_square_left(squares, square):
    num = square.x+square.y*board_size
    if square.x > 0:
        num -= 1
    else:
        return None
    if num < 64 and num >= 0:
        return squares[num]
    return None

def next_square_upright(squares, square):
    square = next_square_up(squares, square)
    if square != None:
        return next_square_right(squares, square)
    return None

def next_square_upleft(squares, square):
    square = next_square_up(squares, square)
    if square != None:
        return next_square_left(squares, square)
    return None

def next_square_downright(squares, square):
    square = next_square_down(squares, square)
    if square != None:
        return next_square_right(squares, square)
    return None

def next_square_downleft(squares, square):
    square = next_square_down(squares, square)
    if square != None:
        return next_square_left(squares, square)
    return None

def check_direction(squares, start, func):
    legals = []
    checking_square = start
    checking_square = func(squares, checking_square)
    while checking_square != None:
        if checking_square.piece != None:
            if checking_square.piece.color == start.piece.color:
                break
            legals.append(checking_square)
            break
        legals.append(checking_square)
        checking_square = func(squares, checking_square)
       
    return legals

def knightable(square, color):
    if square == None:
        return False
    if square.piece == None:
        return True
    if square.piece.color == color:
        return False
    return True

def kingable(square, color):
    if square == None:
        return False
    if square.piece == None:
        return True
    if square.piece.color == color:
        return False
    return True

def get_legal_moves(squares, piece, x, y, check_castling):
    legals = []
    piece_square = squares[x+y*board_size]
    checking_square = piece_square
    if piece.type == ROOK:
        legals += (check_direction(squares, piece_square, next_square_up))
        legals += check_direction(squares, piece_square, next_square_down)
        legals += check_direction(squares, piece_square, next_square_left)
        legals += check_direction(squares, piece_square, next_square_right)

    elif piece.type == BISHOP:
        legals += check_direction(squares, piece_square, next_square_upright)
        legals += check_direction(squares, piece_square, next_square_upleft)
        legals += check_direction(squares, piece_square, next_square_downright)
        legals += check_direction(squares, piece_square, next_square_downleft)

    elif piece.type == QUEEN:
        legals += check_direction(squares, piece_square, next_square_up)
        legals += check_direction(squares, piece_square, next_square_down)
        legals += check_direction(squares, piece_square, next_square_left)
        legals += check_direction(squares, piece_square, next_square_right)
        legals += check_direction(squares, piece_square, next_square_upright)
        legals += check_direction(squares, piece_square, next_square_upleft)
        legals += check_direction(squares, piece_square, next_square_downright)
        legals += check_direction(squares, piece_square, next_square_downleft)

    elif piece.type == PAWN:
        if piece.color == WHITE:
            up1 = next_square_up(squares, piece_square)
            if up1 != None and up1.piece == None:
                legals += [up1]
                if piece_square.y == 6:
                    up2 = next_square_up(squares, up1)
                    if up2 != None and up2.piece == None:
                        legals += [up2]

            upright = next_square_upright(squares, piece_square)
            if upright != None and upright.piece != None:
                if upright.piece.color != piece.color:
                    legals += [upright]

            upleft = next_square_upleft(squares, piece_square)
            if upleft != None and upleft.piece != None:
                if upleft.piece.color != piece.color:
                    legals += [upleft]


            passantright = next_square_right(squares, piece_square)
            if passantright != None and passantright.piece != None and passantright.piece.type == PAWN:
                if passantright.piece.passantable == True:
                    if next_square_up(squares, passantright) != None:
                        legals.append(next_square_up(squares, passantright))

            passantleft = next_square_left(squares, piece_square)
            if passantleft != None and passantleft.piece != None and passantleft.piece.type == PAWN:
                if passantleft.piece.passantable == True:
                    if next_square_up(squares, passantleft) != None:
                        legals.append(next_square_up(squares, passantleft))
                   
        else:
            down1 = next_square_down(squares, piece_square)
            if down1 != None and down1.piece == None:
                legals += [down1]
                if piece_square.y == 1:
                    down2 = next_square_down(squares, down1)
                    if down2 != None and down2.piece == None:
                        legals += [down2]

            downright = next_square_downright(squares, piece_square)
            if downright != None and downright.piece != None:
                if downright.piece.color != piece.color:
                    legals += [downright]

            downleft = next_square_downleft(squares, piece_square)
            if downleft != None and downleft.piece != None:
                if downleft.piece.color != piece.color:
                    legals += [downleft]

            passantright = next_square_right(squares, piece_square)
            if passantright != None and passantright.piece != None and passantright.piece.type == PAWN:
                if passantright.piece.passantable == True:
                    if next_square_down(squares, passantright) != None:
                        legals.append(next_square_down(squares, passantright))

            passantleft = next_square_left(squares, piece_square)
            if passantleft != None and passantleft.piece != None and passantleft.piece.type == PAWN:
                if passantleft.piece.passantable == True:
                    if next_square_down(squares, passantleft) != None:
                        legals.append(next_square_down(squares, passantleft))

    elif piece.type == KNIGHT:
        urr = next_square_upright(squares, piece_square)
        if urr != None:
            urr = next_square_right(squares, urr)
            if knightable(urr, piece.color):
                legals += [urr]

        uru = next_square_upright(squares, piece_square)
        if uru != None:
            uru = next_square_up(squares, uru)
            if knightable(uru, piece.color):
                legals += [uru]

        ull = next_square_upleft(squares, piece_square)
        if ull != None:
            ull = next_square_left(squares, ull)
            if knightable(ull, piece.color):
                legals += [ull]

        ulu = next_square_upleft(squares, piece_square)
        if ulu != None:
            ulu = next_square_up(squares, ulu)
            if knightable(ulu, piece.color):
                legals += [ulu]

       
        drr = next_square_downright(squares, piece_square)
        if drr != None:
            drr = next_square_right(squares, drr)
            if knightable(drr, piece.color):
                legals += [drr]

        drd = next_square_downright(squares, piece_square)
        if drd != None:
            drd = next_square_down(squares, drd)
            if knightable(drd, piece.color):
                legals += [drd]

        dll = next_square_downleft(squares, piece_square)
        if dll != None:
            dll = next_square_left(squares, dll)
            if knightable(dll, piece.color):
                legals += [dll]

        dld = next_square_downleft(squares, piece_square)
        if dld != None:
            dld = next_square_down(squares, dld)
            if knightable(dld, piece.color):
                legals += [dld]

    elif piece.type == KING:
        right = next_square_right(squares, piece_square)
        if kingable(right, piece.color):
            legals += [right]

        upright = next_square_upright(squares, piece_square)
        if kingable(upright, piece.color):
            legals += [upright]

        up = next_square_up(squares, piece_square)
        if kingable(up, piece.color):
            legals += [up]

        upleft = next_square_upleft(squares, piece_square)
        if kingable(upleft, piece.color):
            legals += [upleft]

        left = next_square_left(squares, piece_square)
        if kingable(left, piece.color):
            legals += [left]

        downleft = next_square_downleft(squares, piece_square)
        if kingable(downleft, piece.color):
            legals += [downleft]

        down = next_square_down(squares, piece_square)
        if kingable(down, piece.color):
            legals += [down]

        downright = next_square_downright(squares, piece_square)
        if kingable(downright, piece.color):
            legals += [downright]

        #CASTLING
        if check_castling and not in_check(squares, piece.color):
            rook_short_castle = next_square_right(squares, piece_square)
            if rook_short_castle != None:
                rook_short_castle = next_square_right(squares, rook_short_castle)

            if rook_short_castle != None:
                rook_short_castle = next_square_right(squares, rook_short_castle)

           
            if rook_short_castle != None:
                rook_short_castle = rook_short_castle.piece
           
            if piece.moves == 0 and rook_short_castle != None and rook_short_castle.moves == 0:
                castle_short = next_square_right(squares, piece_square)
               
                if castle_short.piece == None and not would_be_in_check(squares, piece, piece_square, castle_short):
                    castle_short = next_square_right(squares, castle_short)
                    if castle_short.piece == None and not would_be_in_check(squares, piece, piece_square, castle_short):
                        legals.append(castle_short)
                       
            rook_long_castle = next_square_left(squares, piece_square)
            for i in range(3):
                if rook_long_castle != None:
                    rook_long_castle = next_square_left(squares, rook_long_castle)

            if rook_long_castle != None:
                rook_long_castle = rook_long_castle.piece

            if piece.moves == 0 and rook_long_castle != None and rook_long_castle.moves == 0:
                castle_long = next_square_left(squares, piece_square)
               
                if castle_long.piece == None and not would_be_in_check(squares, piece, piece_square, castle_long):
                    castle_long = next_square_left(squares, castle_long)
                    if castle_long.piece == None and not would_be_in_check(squares, piece, piece_square, castle_long):
                        legals.append(castle_long)

           

       
       
           
       
       
   
    return legals
piece_size = (board_width//board_size, board_height//board_size)

def get_value(piece):
    if piece.type == PAWN:
        return 100
    if piece.type == BISHOP:
        return 300

    if piece.type == KNIGHT:
        return 300

    if piece.typ == ROOK:
        return 500

    if piece.type == QUEEN:
        return 900
def order_moves(moves):
    for move in moves:
        moved_piece = move[1]
        target_piece = move[3]
        target_square = move[2]
        if target_piece != None and target_piece.type > moved_piece.type:
            moves.remove(move)
            moves.insert(0, move)
            continue
        if moved_piece.type == KING:
            moves.remove(move)
            moves.append(move)
            continue

        if move[2]%board_size > 1 and move[2]%board_size < 6:
            moves.remove(move)
            moves.insert(0, move)
            continue

        if move[2]/board_size > 1 and move[2]/board_size < 6:
            moves.remove(move)
            moves.insert(0, move)
            continue
    
        
            

large = True
if large:
    white_rook_image = pygame.transform.smoothscale(pygame.image.load("white_rook.png"), piece_size)
    white_pawn_image = pygame.transform.smoothscale(pygame.image.load("white_pawn.png"), piece_size)
    white_knight_image = pygame.transform.smoothscale(pygame.image.load("white_knight.png"), piece_size)
    white_bishop_image = pygame.transform.smoothscale(pygame.image.load("white_bishop.png"), piece_size)
    white_queen_image = pygame.transform.smoothscale(pygame.image.load("white_queen.png"), piece_size)
    white_king_image = pygame.transform.smoothscale(pygame.image.load("white_king.png"), piece_size)

    black_rook_image = pygame.transform.smoothscale(pygame.image.load("black_rook.png"), piece_size)
    black_pawn_image = pygame.transform.smoothscale(pygame.image.load("black_pawn.png"), piece_size)
    black_knight_image = pygame.transform.smoothscale(pygame.image.load("black_knight.png"), piece_size)
    black_bishop_image = pygame.transform.smoothscale(pygame.image.load("black_bishop.png"), piece_size)
    black_queen_image = pygame.transform.smoothscale(pygame.image.load("black_queen.png"), piece_size)
    black_king_image = pygame.transform.smoothscale(pygame.image.load("black_king.png"), piece_size)

else:
    white_rook_image = pygame.transform.smoothscale(pygame.image.load("white_rook_small.png"), piece_size)
    white_pawn_image = pygame.transform.smoothscale(pygame.image.load("white_pawn_small.png"), piece_size)
    white_knight_image = pygame.transform.smoothscale(pygame.image.load("white_knight_small.png"), piece_size)
    white_bishop_image = pygame.transform.smoothscale(pygame.image.load("white_bishop_small.png"), piece_size)
    white_queen_image = pygame.transform.smoothscale(pygame.image.load("white_queen_small.png"), piece_size)
    white_king_image = pygame.transform.smoothscale(pygame.image.load("white_king_small.png"), piece_size)

    black_rook_image = pygame.transform.smoothscale(pygame.image.load("black_rook_small.png"), piece_size)
    black_pawn_image = pygame.transform.smoothscale(pygame.image.load("black_pawn_small.png"), piece_size)
    black_knight_image = pygame.transform.smoothscale(pygame.image.load("black_knight_small.png"), piece_size)
    black_bishop_image = pygame.transform.smoothscale(pygame.image.load("black_bishop_small.png"), piece_size)
    black_queen_image = pygame.transform.smoothscale(pygame.image.load("black_queen_small.png"), piece_size)
    black_king_image = pygame.transform.smoothscale(pygame.image.load("black_king_small.png"), piece_size)
pygame.display.set_caption("CHESS")
class piece():
    def __init__(self, piece_type, piece_color):
        self.type = piece_type
        self.color = piece_color
        self.image = None
        if self.color == WHITE:
            if self.type == ROOK:
                self.image = white_rook_image
            if self.type == PAWN:
                self.image = white_pawn_image
            if self.type == KNIGHT:
                self.image = white_knight_image
            if self.type == BISHOP:
                self.image = white_bishop_image
            if self.type == QUEEN:
                self.image = white_queen_image
            if self.type == KING:
                self.image = white_king_image

        if self.color == BLACK:
            if self.type == ROOK:
                self.image = black_rook_image
            if self.type == PAWN:
                self.image = black_pawn_image
            if self.type == KNIGHT:
                self.image = black_knight_image
            if self.type == BISHOP:
                self.image = black_bishop_image
            if self.type == QUEEN:
                self.image = black_queen_image
            if self.type == KING:
                self.image = black_king_image

        self.moves = 0
        self.passantable = False

class Move():
    def __init__(self, piece_square, piece, move_square, move_square_piece):
        self.piece_square = piece_square
        self.piece = piece
        self.move_square = move_square
        self.move_square_piece = move_square_piece

    def make(self):
        make_move(squares, self.piece_square, self.piece, self.move_square, self.move_square_piece)


    def unmake(self):
        unmake_move(squares, self.piece_square, self.piece, self.move_square, self.move_square_piece)



def make_board():
    for i in range(board_size):
        for j in range(board_size):
            squares.append(square(j, i))

def get_mouse_square(pos):
    x, y = pos
    return (int(x/(board_width/board_size))) + ((int(y/(board_height/board_size)))*board_size)

clock = pygame.time.Clock()

squares = []

held_legals = []

def copy_depth_2(src):
    dst = []
    for item in src:
        dst.append(copy.copy(item))

    return dst
           

time.time()
class square():
    def __init__(self, x, y):
        self.piece = None
        if y == 7:
            if x == 0 or x == 7:
                self.piece = piece(ROOK, WHITE)
            if x == 1 or x == 6:
                self.piece = piece(KNIGHT, WHITE)
            if x == 2 or x == 5:
                self.piece = piece(BISHOP, WHITE)
            if x == 3:
                self.piece = piece(QUEEN, WHITE)
            if x == 4:
                self.piece = piece(KING, WHITE)
        if y == 6:
            self.piece = piece(PAWN, WHITE)
        if y == 1:
            self.piece = piece(PAWN, BLACK)

        if y == 0:
            if x == 0 or x == 7:
                self.piece = piece(ROOK, BLACK)
            if x == 1 or x == 6:
                self.piece = piece(KNIGHT, BLACK)
            if x == 2 or x == 5:
                self.piece = piece(BISHOP, BLACK)
            if x == 3:
                self.piece = piece(QUEEN, BLACK)
            if x == 4:
                self.piece = piece(KING, BLACK)
           
        self.x = x
        self.y = y
        self.color = DARK_SQUARE_COLOR
        if (self.x+self.y)%2 == 0:
            self.color = LIGHT_SQUARE_COLOR

    def draw_piece(self):
        if self.piece != None:
            if self.piece.image != None:
                global board_width
                global board_height
                global board_size
                x = self.x*board_width/board_size
                y = self.y*board_height/board_size
                window.blit(self.piece.image, (x, y))
def get_king(squares, color):
    for square in squares:
        if square.piece != None:
            if square.piece.type == KING and square.piece.color == color:
                return square.x+square.y*board_size
    return None

def in_check(squares2, color):
    king_square = get_king(squares2, color)
   
    if king_square == None:
        return False

   
   
    for thing in squares2:
        if thing.piece != None:
            if thing.piece.color != color:
                #print("piece type: " + str(thing.piece.type))
                #print("Legal moves bruv: " + str(get_legal_moves(squares, thing.piece, thing.x, thing.y)))
                for thing in get_legal_moves(squares2, thing.piece, thing.x, thing.y, False):
                    if thing.x+thing.y*board_size == king_square:
                        return True

    return False

def would_be_in_check(squares, piece, piece_square, move_square):
    move_to_check_for_check = Move(square_num(piece_square), piece, square_num(move_square), move_square.piece)
    move_to_check_for_check.make()
    check = in_check(squares, piece.color)
    move_to_check_for_check.unmake()
    return check
   
make_board()


def get_legals_everything_nums(squares, piece, piece_square):
    moves = get_legal_moves(squares, piece, piece_square.x, piece_square.y, True)
    moves_to_delete = set()
    for i in range(len(moves)):
        moves[i] = moves[i].x+moves[i].y*board_size

    for square in moves:

        #FIX THISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS make it not copy instead make and unmake move
        """
        squares2 = copy_depth_2(squares)
        squares2[square].piece = piece
        squares2[piece_square.x+piece_square.y*board_size].piece = None
       
        if in_check(squares2, piece.color):
            if square in moves:
                moves_to_delete.add(square)
        """

        if would_be_in_check(squares, piece, piece_square, squares[square]):
            moves_to_delete.add(square)
    for move in moves_to_delete:
        moves.remove(move)

    #moves = [move for move in moves if move not in moves_to_delete]
    #TRYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY

           
    return moves
           

def get_all_moves(squares, color):

    moves = []

    for square in squares:
        if square.piece != None and square.piece.color == color:
            for thing in get_legals_everything_nums(squares, square.piece, square):
                moves.append([square_num(square), square.piece, thing, squares[thing].piece])

    return moves
   
def square_num(square):
    return square.x+square.y*board_size

def get_ai_move(squares, color, depth):


    moves = get_all_moves(squares, color)
    best_move = None
    
    if len(moves) > 0:
        best_move = moves[0]

       
        make_move(squares, best_move[0], best_move[1], best_move[2], best_move[3])
        best_move_value = -9999999000000
        unmake_move(squares, best_move[0], best_move[1], best_move[2], best_move[3]) 
        for i in range(len(moves)):
 
            make_move(squares, moves[i][0], moves[i][1], moves[i][2], moves[i][3])
            if color == WHITE:
                rescolor = BLACK
            if color == BLACK:
                rescolor = WHITE
               
           
           

            """
            if depth > 1:
                squares3 = copy_depth_2(squares2)
                best_response = get_ai_move(squares3, rescolor, depth-1)
                move(squares3, best_response[0], best_response[1])
                best_response_value = evaluate_pos(squares3, color)
            """
           
            

            move_value = -search(squares, rescolor, depth-1, -99999999999, 99999999)
            unmake_move(squares, moves[i][0], moves[i][1], moves[i][2], moves[i][3])
           
            if move_value > best_move_value:
                best_move = moves[i]
               
                best_move_value = move_value

            
    if len(moves) > 0:

        if best_move_value > 0:
            print("Eval: " + str(best_move_value/100) + " for black")
        else:
            print("Eval: " + str(-best_move_value/100) + " for white")
    else:
        print("NO MOVES")

    return best_move


def search(squares, color, depth, alpha, beta):
    if depth == 0:
        #print("Search should've returned " + str(evaluate_pos(squares, color)))
        return evaluate_pos(squares, color)

    

    moves = get_all_moves(squares, color)
    order_moves(moves)
    if len(moves) == 0:
        if in_check(squares, color):
            return -9999999
        
        return 0



    for thing in moves:
        make_move(squares, thing[0], thing[1], thing[2], thing[3])
        if color == WHITE:
            rescolor = BLACK
        if color == BLACK:
            rescolor = WHITE
        eval_ = -search(squares, rescolor, depth-1, -beta, -alpha)
        unmake_move(squares, thing[0], thing[1], thing[2], thing[3])

        if eval_ >= beta:
            return beta;
       
        alpha = max(eval_, alpha)

    return alpha
   



def get_best_move(squares, color):
    pass
   



def evaluate_pos(squares, color):
    score = 0
    if color == WHITE:
        score += get_material(squares, WHITE)-get_material(squares, BLACK)
        
        return score
    return get_material(squares, BLACK)-get_material(squares, WHITE)

   
def get_material(squares, color):
    total = 0

    pawn_value = 100
    knight_value = 300
    bishop_value = 300
    rook_value = 500
    queen_value = 900
   
    for square in squares:
        if square.piece != None:
            if square.piece.color == color:
               
                if square.piece.type == PAWN:
                    total += pawn_value

                elif square.piece.type == KNIGHT:
                    total += knight_value
                    total += len(get_legal_moves(squares, square.piece, square.x, square.y, False))*30

                elif square.piece.type == BISHOP:
                    total += bishop_value
                    total += len(get_legal_moves(squares, square.piece, square.x, square.y, False))*20

                elif square.piece.type == ROOK:
                    total += rook_value
                    total += len(get_legal_moves(squares, square.piece, square.x, square.y, False))*15

                elif square.piece.type == QUEEN:
                    total += queen_value
                    total += len(get_legal_moves(squares, square.piece, square.x, square.y, False))*10

    return total
holding_piece = False
held_piece_square = None
held_piece = None
held_piece_moves = []


def make_move(squares, piece_square, piece, square, square_piece):
    piece.moves += 1
    squares[square].piece = squares[piece_square].piece
    squares[piece_square].piece = None
    

def unmake_move(squares, original_square, original_piece, moved_square, moved_square_piece):
    original_piece.moves -= 1
    
    squares[original_square].piece = original_piece
    squares[moved_square].piece = moved_square_piece
    




playing = True
square = squares[get_mouse_square(pygame.mouse.get_pos())]
while playing:
    window.fill((0, 0, 0))
    
    

    ai_start_time = time.time()
    if both_ai:
        if turns % 2 == 0:
            ai_move = get_ai_move(squares, WHITE, ai_depth)
        else:
            ai_move = get_ai_move(squares, BLACK, ai_depth)
        make_move(squares, ai_move[0], ai_move[1], ai_move[2], ai_move[3])
        turns += 1
        
    if turns % 2 == 1 and vs_ai and (not both_ai):
        ai_move = get_ai_move(squares, BLACK, ai_depth)
    
    



        make_move(squares, ai_move[0], ai_move[1], ai_move[2], ai_move[3])
        turns += 1
    if both_ai:
        print("AI TIME: " + str(time.time()-ai_start_time))

               
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                break
            if event.key == pygame.K_DOWN:
                fps = 12
            elif event.key == pygame.K_UP:
                fps = 120
            elif event.key == pygame.K_LEFT:
                fps = 48
            elif event.key == pygame.K_RIGHT:
                fps = 60

   
           
        elif event.type == pygame.MOUSEBUTTONDOWN:
 
            square_clicked = squares[get_mouse_square(pygame.mouse.get_pos())]
            if holding_piece:
                if square_clicked in get_legal_moves(squares, held_piece, held_piece_square.x, held_piece_square.y, True):

                   
                    move_clicked = Move(held_piece_square, held_piece, square_clicked, square_clicked.piece)
                    
                    if not would_be_in_check(squares, held_piece, held_piece_square, square_clicked):
                        king_square = squares[get_king(squares, held_piece.color)]
                        if king_square.color == LIGHT_SQUARE_CHECK_COLOR:
                            king_square.color = LIGHT_SQUARE_COLOR
                        elif king_square.color == DARK_SQUARE_CHECK_COLOR:
                            king_square.color = DARK_SQUARE_COLOR

                        if held_piece.type == KING:

                            if square_num(square_clicked) == square_num(held_piece_square)+2:
                                
                                squares[square_num(square_clicked)-1].piece = squares[square_num(square_clicked)+1].piece
                                squares[square_num(square_clicked)+1].piece = None


                            if square_num(square_clicked) == square_num(held_piece_square)-2:
                                squares[square_num(square_clicked)+1].piece = squares[square_num(square_clicked)-2].piece
                                squares[square_num(square_clicked)-2].piece = None
                               
                        if held_piece.type == PAWN:
                            if square_num(square_clicked)-square_num(held_piece_square) == -7:

                                if square_clicked.piece == None:

                                    squares[square_num(held_piece_square)+1].piece = None

                            elif square_num(square_clicked)-square_num(held_piece_square) == -9:

                                if square_clicked.piece == None:

                                    squares[square_num(held_piece_square)-1].piece = None

                            elif square_num(square_clicked)-square_num(held_piece_square) == 7:

                                if square_clicked.piece == None:

                                    squares[square_num(held_piece_square)-1].piece = None

                            elif square_num(square_clicked)-square_num(held_piece_square) == 9:

                                if square_clicked.piece == None:

                                    squares[square_num(held_piece_square)+1].piece = None

                               


                        square_clicked.piece = held_piece
                        square_clicked.piece.moves += 1
                        for thing in squares:
                            if thing.piece != None:
                                thing.passantable = False

                        if square_clicked.piece.type == PAWN and abs(square_num(square_clicked) - square_num(held_piece_square)) == board_size*2:
                            square_clicked.piece.passantable = True
                           
                        turns += 1
                        held_piece_square.piece = None
                        holding_piece = False
                       

                    else:
                        king_square = squares[get_king(squares, held_piece.color)]
                        if king_square.color == DARK_SQUARE_COLOR:
                            king_square.color = DARK_SQUARE_CHECK_COLOR
                        elif king_square.color == LIGHT_SQUARE_COLOR:
                            king_square.color = LIGHT_SQUARE_CHECK_COLOR
                        holding_piece = False


                #If user is holding a piece and clicks on another, the other piece is now being held instead of just not holding anything
                elif square_clicked.piece != None and square_clicked.piece.color == held_piece_square.piece.color:
                    holding_piece = True
                    held_piece = square_clicked.piece
                    held_piece_square = square_clicked
                   
                else:
                    holding_piece = False
               
               
            else:
                if square_clicked.piece != None:
                    if (turns%2 == 0 and square_clicked.piece.color == WHITE) or (turns%2 == 1 and square_clicked.piece.color == BLACK):
                        holding_piece = True
                        held_piece = square_clicked.piece
                        held_piece_square = square_clicked

            if holding_piece:
                held_piece_moves = get_legals_everything_nums(squares, held_piece, held_piece_square)
               

   
   
    if square.color == DARK_SQUARE_SELECTED_COLOR:
        square.color = DARK_SQUARE_COLOR
    elif square.color == LIGHT_SQUARE_SELECTED_COLOR:
        square.color = LIGHT_SQUARE_COLOR
    square = squares[get_mouse_square(pygame.mouse.get_pos())]
    if square.color == DARK_SQUARE_COLOR:
        square.color = DARK_SQUARE_SELECTED_COLOR
    elif square.color == LIGHT_SQUARE_COLOR:
        square.color = LIGHT_SQUARE_SELECTED_COLOR


       

   

           
               
           
    draw_board(8, board_width, board_height)
    for thing in squares:
        thing.draw_piece()
       
    if holding_piece:
        for i in range(len(held_piece_moves)):
            pos_x, pos_y = (held_piece_moves[i]%8+.5)*(board_width/board_size), (held_piece_moves[i]//8+.5)*(board_width/board_size)
            pygame.gfxdraw.filled_circle(window, int(pos_x), int(pos_y), int(board_width/board_size/5), DOT_COLOR)
            pygame.gfxdraw.aacircle(window, int(pos_x), int(pos_y), int(board_width/board_size/5), DOT_COLOR)
    
    pygame.display.flip()
    if not both_ai:
        clock.tick(fps)
pygame.quit()

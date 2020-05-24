import pygame
import random
import time
import copy

pygame.init()

display = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Russian chess')


class FigureType:
    empty = 0
    white_pawn = 1
    white_king = 2
    black_pawn = 3
    black_king = 4


class Player:
    is_players_move = True
    factor = 0
    final_score = 0
    best_score = 0


class Move:
    def __init__(self):
        self.from_x = 0
        self.from_y = 0
        self.to_x = 0
        self.to_y = 0


class Image:
    black_pawn_image = pygame.image.load('../images/black_pawn.gif')
    white_pawn_image = pygame.image.load('../images/white_pawn.gif')
    white_king_image = pygame.image.load('../images/white_king.gif')
    black_king_image = pygame.image.load('../images/black_king.gif')


def create_initial_board(my_board):
    my_board = []
    for i in range(3):
        my_board.append([])
        for j in range(8):
            if (i + j) % 2 == 0:
                my_board[i].append(FigureType.empty)
            else:
                my_board[i].append(FigureType.black_pawn)

    for i in range(3, 5):
        my_board.append([])
        for j in range(8):
            my_board[i].append(FigureType.empty)

    for i in range(5, 8):
        my_board.append([])
        for j in range(8):
            if (i + j) % 2 == 0:
                my_board[i].append(FigureType.empty)
            else:
                my_board[i].append(FigureType.white_pawn)
    return my_board


def computers_move(board_size, square_size, offsets, max_recursion_depth, my_board, available_moves):
    find_correct_computers_moves(1, (), [], board_size, square_size, offsets, max_recursion_depth, my_board, available_moves)
    if available_moves:
        kh = len(available_moves)
        th = random.randint(0, kh - 1)
        dh = len(available_moves[th])

        for i in range(dh - 1):
            move = Move()
            move.from_x = available_moves[th][i][0]
            move.from_y = available_moves[th][i][1]
            move.to_x = available_moves[th][1 + i][0]
            move.to_y = available_moves[th][1 + i][1]
            make_move(1, move, board_size, square_size, offsets, my_board)
        available_moves = []
        Player.is_players_move = True

    computers_figures_count, players_figures_count = count_of_remaining_figures(board_size, my_board)
    if not players_figures_count or not computers_figures_count or \
        (Player.is_players_move and not find_available_players_moves_all_over_board(board_size, offsets, my_board)) or \
            Player.is_players_move and not computers_move_list(board_size, offsets, my_board):
        run_game()
    pygame.display.update()


def computers_move_list(board_size, offsets, my_board):
    available = find_available_computers_move_all_over_board([], board_size, offsets, my_board)
    if not available:
        available = check_computers_free_moves([], board_size, offsets, my_board)
    return available


def find_correct_computers_moves(curr_recursion_depth, n_available, available, board_size, square_size, offsets, max_recursion_depth, my_board, available_moves):
    if not available:
        available = computers_move_list(board_size, offsets, my_board)

    if available:
        k_board = copy.deepcopy(my_board)
        for ((from_i, from_j), (to_i, to_j)) in available:
            move = Move()
            move.from_x = from_i
            move.from_y = from_j
            move.to_x = to_i
            move.to_y = to_j
            t_available = make_move(0, move, board_size, square_size, offsets, my_board)
            if t_available:
                find_correct_computers_moves(curr_recursion_depth, (n_available + ((from_i, from_j),)), t_available, board_size, square_size, offsets, max_recursion_depth, my_board, available_moves)
            else:
                check_players_move(curr_recursion_depth, [], board_size, square_size, offsets, max_recursion_depth, my_board, available_moves, move)
                if curr_recursion_depth == 1:
                    curr_res = Player.final_score / Player.factor
                    if not available_moves:
                        available_moves = (n_available + ((from_i, from_j), (to_i, to_j)),)
                        Player.best_score = curr_res
                    else:
                        if curr_res == Player.best_score:
                            available_moves += (n_available + ((from_i, from_j), (to_i, to_j)),)
                        if curr_res > Player.best_score:
                            available_moves = ()
                            available_moves = (n_available + ((from_i, from_j), (to_i, to_j)),)
                            Player.best_score = curr_res
                    Player.final_score = 0
                    Player.factor = 0
            my_board = copy.deepcopy(k_board)
    else:
        computers_figures_count, players_figures_count = count_of_remaining_figures(board_size, my_board)
        Player.final_score += computers_figures_count - players_figures_count
        Player.factor += 1


def find_available_players_moves_all_over_board(board_size, offsets, my_board):
    available = find_correct_players_moves([], board_size, offsets, my_board)
    if not available:
        available = check_players_free_moves([], board_size, offsets, my_board)
    return available


def check_players_move(curr_recursion_depth, available, board_size, square_size, offsets, max_recursion_depth, my_board, available_moves, move):
    if not available:
        available = find_available_players_moves_all_over_board(board_size, offsets, my_board)

    if available:
        k_board = copy.deepcopy(my_board)
        for ((move.from_x, move.from_y), (move.to_x, move.to_y)) in available:
            t_available = make_move(0, move, board_size, square_size, offsets, my_board)
            if t_available:
                check_players_move(curr_recursion_depth, t_available, board_size, square_size, offsets, max_recursion_depth, my_board, available_moves, move)
            else:
                if curr_recursion_depth < max_recursion_depth:
                    find_correct_computers_moves(curr_recursion_depth + 1, (), [], board_size, square_size, offsets, max_recursion_depth, my_board, available_moves)
                else:
                    computers_figures_count, players_figures_count = count_of_remaining_figures(board_size, my_board)
                    Player.final_score += computers_figures_count - players_figures_count
                    Player.factor += 1

            my_board = copy.deepcopy(k_board)
    else:
        computers_figures_count, players_figures_count = count_of_remaining_figures(board_size, my_board)
        Player.final_score += computers_figures_count - players_figures_count
        Player.factor += 1


def count_of_remaining_figures(board_size, my_board):
    computers_figures_count = 0
    players_figures_count = 0

    for i in range(board_size):
        for j in range(board_size):
            if my_board[j][i] == FigureType.white_pawn:
                players_figures_count += 1
            elif my_board[j][i] == FigureType.white_king:
                players_figures_count += 2
            elif my_board[j][i] == FigureType.black_pawn:
                computers_figures_count += 1
            elif my_board[j][i] == FigureType.black_king:
                computers_figures_count += 3
    return computers_figures_count, players_figures_count


def players_move(board_size, square_size, offsets, my_board, move):
    Player.is_players_move = False
    available = find_available_players_moves_all_over_board(board_size, offsets, my_board)
    if available:
        if ((move.from_x, move.from_y), (move.to_x, move.to_y)) in available:
            t_available = make_move(1, move, board_size, square_size, offsets, my_board)
            if t_available:
                Player.is_players_move = True
        else:
            Player.is_players_move = True
    draw_surface(board_size, square_size, my_board)


def make_move(need_to_draw, move, board_size, square_size, offsets, my_board):
    if need_to_draw:
        draw_surface(board_size, square_size, my_board)

    if move.to_y == 0 and my_board[move.from_y][move.from_x] == FigureType.white_pawn:
        my_board[move.from_y][move.from_x] = FigureType.white_king

    if move.to_y == board_size - 1 and my_board[move.from_y][move.from_x] == FigureType.black_pawn:
        my_board[move.from_y][move.from_x] = FigureType.black_king

    my_board[move.to_y][move.to_x] = my_board[move.from_y][move.from_x]
    my_board[move.from_y][move.from_x] = 0

    offset_x = offset_y = 1
    if move.from_x < move.to_x:
        offset_x = -1
    if move.from_y < move.to_y:
        offset_y = -1
    x_poz, y_poz = move.to_x, move.to_y
    while (move.from_x != x_poz) or (move.from_y != y_poz):
        x_poz += offset_x
        y_poz += offset_y
        if my_board[y_poz][x_poz] != 0:
            my_board[y_poz][x_poz] = 0
            if need_to_draw:
                draw_surface(board_size, square_size, my_board)
            if my_board[move.to_y][move.to_x] == FigureType.black_pawn or my_board[move.to_y][move.to_x] == FigureType.black_king:
                return find_available_computers_moves_sterting_from_this_cell([], move.to_x, move.to_y, board_size, offsets, my_board)
            elif my_board[move.to_y][move.to_x] == FigureType.white_pawn or my_board[move.to_y][move.to_x] == FigureType.white_king:
                return find_correct_players_movesp([], move.to_x, move.to_y, board_size, offsets, my_board)
    if need_to_draw:
        draw_surface(board_size, square_size, my_board)


def find_available_computers_move_all_over_board(available, board_size, offsets, my_board):
    for y in range(board_size):
        for x in range(board_size):
            available = find_available_computers_moves_sterting_from_this_cell(available, x, y, board_size, offsets, my_board)
    return available


def check_kings_moves(available, x, y, board_size, offsets, my_board):
    for ix, iy in offsets:
        osh = 0
        for i in range(1, board_size):
            if 0 <= y + iy * i < board_size and 0 <= x + ix * i < board_size:
                if osh == 1:
                    available.append(((x, y), (x + ix * i, y + iy * i)))
                if my_board[y + iy * i][x + ix * i] == FigureType.white_pawn or \
                        my_board[y + iy * i][x + ix * i] == FigureType.white_king:
                    osh += 1
                if my_board[y + iy * i][x + ix * i] == FigureType.black_pawn or \
                        my_board[y + iy * i][x + ix * i] == FigureType.black_king or osh == 2:
                    if osh > 0 : available.pop()
                    break
    return available


def find_available_computers_moves_sterting_from_this_cell(available, x, y, board_size, offsets, my_board):
    if my_board[y][x] == FigureType.black_pawn:
        for ix, iy in offsets:
            if 0 <= y + iy + iy < board_size and 0 <= x + ix + ix < board_size:
                if my_board[y + iy][x + ix] == FigureType.white_pawn or \
                        my_board[y + iy][x + ix] == FigureType.white_king:
                    if my_board[y + iy + iy][x + ix + ix] == 0:
                        available.append(((x, y), (x + ix + ix, y + iy + iy)))
    elif my_board[y][x] == FigureType.black_king:
        available = check_kings_moves(available, x, y, board_size, offsets, my_board)
    return available


def check_computers_free_moves(available, board_size, offsets, my_board):
    for y in range(board_size):
        for x in range(board_size):
            if my_board[y][x] == FigureType.black_pawn:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy < board_size and 0 <= x + ix < board_size:
                        if my_board[y + iy][x + ix] == FigureType.empty:
                            available.append(((x, y), (x + ix, y + iy)))
                        if my_board[y + iy][x + ix] == FigureType.white_pawn or \
                                my_board[y + iy][x + ix] == FigureType.white_king:
                            if 0 <= y + iy * 2 < board_size and 0 <= x + ix * 2 < board_size:
                                if my_board[y + iy * 2][x + ix * 2] == FigureType.empty:
                                    available.append(((x, y), (x + ix * 2, y + iy * 2)))
            if my_board[y][x] == FigureType.black_king:
                available = check_kings_moves(available, x, y, board_size, offsets, my_board)
    return available


def find_correct_players_moves(available, board_size, offsets, my_board):
    available = []
    for y in range(board_size):
        for x in range(board_size):
            available = find_correct_players_movesp(available, x, y, board_size, offsets, my_board)
    return available


def find_correct_players_movesp(available, x, y, board_size, offsets, my_board):
    if my_board[y][x] == FigureType.white_pawn:
        for ix, iy in offsets:
            if 0 <= y + iy + iy < board_size and 0 <= x + ix + ix < board_size:
                if my_board[y + iy][x + ix] == FigureType.black_pawn or \
                        my_board[y + iy][x + ix] == FigureType.black_king:
                    if my_board[y + iy + iy][x + ix + ix] == 0:
                        available.append(((x, y), (x + ix + ix, y + iy + iy)))
    if my_board[y][x] == FigureType.white_king:
        available = check_kings_moves(available, x, y, board_size, offsets, my_board)
    return available


def check_players_free_moves(available, board_size, offsets, my_board):
    for y in range(board_size):
        for x in range(board_size):
            if my_board[y][x] == FigureType.white_pawn:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy < board_size and 0 <= x + ix < board_size:
                        if my_board[y + iy][x + ix] == 0:
                            available.append(((x, y), (x + ix, y + iy)))
                        if my_board[y + iy][x + ix] == FigureType.black_pawn or \
                                my_board[y + iy][x + ix] == FigureType.black_king:
                            if 0 <= y + iy * 2 < board_size and 0 <= x + ix * 2 < board_size:
                                if my_board[y + iy * 2][x + ix * 2] == 0:
                                    available.append(((x, y), (x + ix * 2, y + iy * 2)))
            if my_board[y][x] == FigureType.white_king:
                available = check_kings_moves(available, x, y, board_size, offsets, my_board)
    return available


def run_game():
    game = True
    max_recursion_depth = 3
    offsets =[(-1, -1), (-1, 1), (1, -1), (1, 1)]
    board_size = 8
    square_size = 100
    my_board = []
    available_moves = []
    my_board = create_initial_board(my_board)
    draw_surface(board_size, square_size, my_board)
    unselected_square = -1
    move = Move()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // square_size, event.pos[1] // square_size
                curr_square = (x, y)
                curr_figure = my_board[curr_square[1]][curr_square[0]]
                if curr_figure == 1 or curr_figure == 2:
                    move.from_x, move.from_y = x, y
                else:
                    if move.from_x != unselected_square:
                        move.to_x, move.to_y = x, y
                        if Player.is_players_move:
                            players_move(board_size, square_size, offsets, my_board, move)
                            if not Player.is_players_move:
                                time.sleep(0.5)
                                computers_move(board_size, square_size, offsets, max_recursion_depth, my_board, available_moves)
                        move.from_x = unselected_square
        draw_surface(board_size, square_size, my_board)
        pygame.display.update()
        time.sleep(0.5)


def draw_surface(board_size, square_size, my_board):
    display.fill((255, 255, 255))
    d = dict([(FigureType.white_pawn, Image.white_pawn_image), (FigureType.black_pawn, Image.black_pawn_image),
              (FigureType.white_king, Image.white_king_image), (FigureType.black_king, Image.black_king_image)])
    for i in range(board_size):
        for j in range(board_size):
            if (i + j) % 2 == 1:
                pygame.draw.rect(display, (0, 0, 0), (i * square_size, j * square_size, square_size, square_size))
            for key in d.keys():
                if my_board[j][i] == key:
                    display.blit(d[key], (i * square_size, j * square_size))
    pygame.display.update()


run_game()


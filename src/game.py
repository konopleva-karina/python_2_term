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
    from_x = 0
    from_y = 0
    to_x = 0
    to_y = 0
    available_moves = []


class Image:
    black_pawn_image = pygame.image.load('../images/black_pawn.gif')
    white_pawn_image = pygame.image.load('../images/white_pawn.gif')
    white_king_image = pygame.image.load('../images/white_king.gif')
    black_king_image = pygame.image.load('../images/black_king.gif')


class Board:
    @staticmethod
    def create_initial_board():
        board = []
        for i in range(3):
            board.append([])
            for j in range(8):
                if (i + j) % 2 == 0:
                    board[i].append(FigureType.empty)
                else:
                    board[i].append(FigureType.black_pawn)

        for i in range(3, 5):
            board.append([])
            for j in range(8):
                board[i].append(FigureType.empty)

        for i in range(5, 8):
            board.append([])
            for j in range(8):
                if (i + j) % 2 == 0:
                    board[i].append(FigureType.empty)
                else:
                    board[i].append(FigureType.white_pawn)
        return board

    board = []


def computers_move(board_size, square_size, offsets, max_recursion_depth):
    find_correct_computers_moves(1, (), [], board_size, square_size, offsets, max_recursion_depth)
    if Move.available_moves:
        kh = len(Move.available_moves)
        th = random.randint(0, kh - 1)
        dh = len(Move.available_moves[th])

        for i in range(dh - 1):
            make_move(1, Move.available_moves[th][i][0], Move.available_moves[th][i][1], Move.available_moves[th][1 + i][0],
                      Move.available_moves[th][1 + i][1], board_size, square_size, offsets)
        Move.available_moves = []
        Player.is_players_move = True

    computers_figures_count, players_figures_count = count_of_remaining_figures(board_size)
    if not players_figures_count or not computers_figures_count or \
        (Player.is_players_move and not find_available_players_moves_all_over_board(board_size, offsets)) or \
            Player.is_players_move and not computers_move_list(board_size, offsets):
        run_game()
    pygame.display.update()


def computers_move_list(board_size, offsets):
    available = find_available_computers_move_all_over_board([], board_size, offsets)
    if not available:
        available = check_computers_free_moves([], board_size, offsets)
    return available


def find_correct_computers_moves(curr_recursion_depth, n_available, available, board_size, square_size, offsets, max_recursion_depth):
    if not available:
        available = computers_move_list(board_size, offsets)

    if available:
        k_board = copy.deepcopy(Board.board)
        for ((from_i, from_j), (to_i, to_j)) in available:
            t_available = make_move(0, from_i, from_j, to_i, to_j, board_size, square_size, offsets)
            if t_available:
                find_correct_computers_moves(curr_recursion_depth, (n_available + ((from_i, from_j),)), t_available, board_size, square_size, offsets, max_recursion_depth)
            else:
                check_players_move(curr_recursion_depth, [], board_size, square_size, offsets, max_recursion_depth)
                if curr_recursion_depth == 1:
                    curr_res = Player.final_score / Player.factor
                    if not Move.available_moves:
                        Move.available_moves = (n_available + ((from_i, from_j), (to_i, to_j)),)
                        Player.best_score = curr_res
                    else:
                        if curr_res == Player.best_score:
                            Move.available_moves += (n_available + ((from_i, from_j), (to_i, to_j)),)
                        if curr_res > Player.best_score:
                            Move.available_moves = ()
                            Move.available_moves = (n_available + ((from_i, from_j), (to_i, to_j)),)
                            Player.best_score = curr_res
                    Player.final_score = 0
                    Player.factor = 0

            Board.board = copy.deepcopy(k_board)
    else:
        computers_figures_count, players_figures_count = count_of_remaining_figures(board_size)
        Player.final_score += computers_figures_count - players_figures_count
        Player.factor += 1


def find_available_players_moves_all_over_board(board_size, offsets):
    available = find_correct_players_moves([], board_size, offsets)
    if not available:
        available = check_players_free_moves([], board_size, offsets)
    return available


def check_players_move(curr_recursion_depth, available, board_size, square_size, offsets, max_recursion_depth):
    if not available:
        available = find_available_players_moves_all_over_board(board_size, offsets)

    if available:
        k_board = copy.deepcopy(Board.board)
        for ((Move.from_x, Move.from_y), (Move.to_x, Move.to_y)) in available:
            t_available = make_move(0, Move.from_x, Move.from_y, Move.to_x, Move.to_y, board_size, square_size, offsets)
            if t_available:
                check_players_move(curr_recursion_depth, t_available, board_size, square_size, offsets, max_recursion_depth)
            else:
                if curr_recursion_depth < max_recursion_depth:
                    find_correct_computers_moves(curr_recursion_depth + 1, (), [], board_size, square_size, offsets, max_recursion_depth)
                else:
                    computers_figures_count, players_figures_count = count_of_remaining_figures(board_size)
                    Player.final_score += computers_figures_count - players_figures_count
                    Player.factor += 1

            Board.board = copy.deepcopy(k_board)
    else:
        computers_figures_count, players_figures_count = count_of_remaining_figures(board_size)
        Player.final_score += computers_figures_count - players_figures_count
        Player.factor += 1


def count_of_remaining_figures(board_size):
    computers_figures_count = 0
    players_figures_count = 0

    for i in range(board_size):
        for j in range(board_size):
            if Board.board[j][i] == FigureType.white_pawn:
                players_figures_count += 1
            elif Board.board[j][i] == FigureType.white_king:
                players_figures_count += 2
            elif Board.board[j][i] == FigureType.black_pawn:
                computers_figures_count += 1
            elif Board.board[j][i] == FigureType.black_king:
                computers_figures_count += 3
    return computers_figures_count, players_figures_count


def players_move(board_size, square_size, offsets):
    Player.is_players_move = False
    available = find_available_players_moves_all_over_board(board_size, offsets)
    if available:
        if ((Move.from_x, Move.from_y), (Move.to_x, Move.to_y)) in available:
            t_available = make_move(1, Move.from_x, Move.from_y, Move.to_x, Move.to_y, board_size, square_size, offsets)
            if t_available:
                Player.is_players_move = True
        else:
            Player.is_players_move = True
    draw_surface(Board.board, board_size, square_size)


def make_move(need_to_draw, from_x, from_y, to_x, to_y, board_size, square_size, offsets):
    if need_to_draw:
        draw_surface(Board.board, board_size, square_size)

    if to_y == 0 and Board.board[from_y][from_x] == FigureType.white_pawn:
        Board.board[from_y][from_x] = FigureType.white_king

    if to_y == board_size - 1 and Board.board[from_y][from_x] == FigureType.black_pawn:
        Board.board[from_y][from_x] = FigureType.black_king

    Board.board[to_y][to_x] = Board.board[from_y][from_x]
    Board.board[from_y][from_x] = 0

    offset_x = offset_y = 1
    if from_x < to_x:
        offset_x = -1
    if from_y < to_y:
        offset_y = -1
    x_poz, y_poz = to_x, to_y
    while (from_x != x_poz) or (from_y != y_poz):
        x_poz += offset_x
        y_poz += offset_y
        if Board.board[y_poz][x_poz] != 0:
            Board.board[y_poz][x_poz] = 0
            if need_to_draw:
                draw_surface(Board.board, board_size, square_size)
            if Board.board[to_y][to_x] == FigureType.black_pawn or Board.board[to_y][to_x] == FigureType.black_king:
                return find_available_computers_moves_sterting_from_this_cell([], to_x, to_y, board_size, offsets)
            elif Board.board[to_y][to_x] == FigureType.white_pawn or Board.board[to_y][to_x] == FigureType.white_king:
                return find_correct_players_movesp([], to_x, to_y, board_size, offsets)
    if need_to_draw:
        draw_surface(Board.board, board_size, square_size)


def find_available_computers_move_all_over_board(available, board_size, offsets):
    for y in range(board_size):
        for x in range(board_size):
            available = find_available_computers_moves_sterting_from_this_cell(available, x, y, board_size, offsets)
    return available


def check_kings_moves(available, x, y, board_size, offsets):
    for ix, iy in offsets:
        osh = 0
        for i in range(1, board_size):
            if 0 <= y + iy * i < board_size and 0 <= x + ix * i < board_size:
                if osh == 1:
                    available.append(((x, y), (x + ix * i, y + iy * i)))
                if Board.board[y + iy * i][x + ix * i] == FigureType.white_pawn or \
                        Board.board[y + iy * i][x + ix * i] == FigureType.white_king:
                    osh += 1
                if Board.board[y + iy * i][x + ix * i] == FigureType.black_pawn or \
                        Board.board[y + iy * i][x + ix * i] == FigureType.black_king or osh == 2:
                    if osh > 0: available.pop()
                    break
    return available


def find_available_computers_moves_sterting_from_this_cell(available, x, y, board_size, offsets):
    if Board.board[y][x] == FigureType.black_pawn:
        for ix, iy in offsets:
            if 0 <= y + iy + iy < board_size and 0 <= x + ix + ix < board_size:
                if Board.board[y + iy][x + ix] == FigureType.white_pawn or \
                        Board.board[y + iy][x + ix] == FigureType.white_king:
                    if Board.board[y + iy + iy][x + ix + ix] == 0:
                        available.append(((x, y), (x + ix + ix, y + iy + iy)))
    elif Board.board[y][x] == FigureType.black_king:
        available = check_kings_moves(available, x, y, board_size, offsets)
    return available


def check_computers_free_moves(available, board_size, offsets):
    for y in range(board_size):
        for x in range(board_size):
            if Board.board[y][x] == FigureType.black_pawn:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy < board_size and 0 <= x + ix < board_size:
                        if Board.board[y + iy][x + ix] == FigureType.empty:
                            available.append(((x, y), (x + ix, y + iy)))
                        if Board.board[y + iy][x + ix] == FigureType.white_pawn or \
                                Board.board[y + iy][x + ix] == FigureType.white_king:
                            if 0 <= y + iy * 2 < board_size and 0 <= x + ix * 2 < board_size:
                                if Board.board[y + iy * 2][x + ix * 2] == FigureType.empty:
                                    available.append(((x, y), (x + ix * 2, y + iy * 2)))
            if Board.board[y][x] == FigureType.black_king:
                available = check_kings_moves(available, x, y, board_size, offsets)
    return available


def find_correct_players_moves(available, board_size, offsets):
    available = []
    for y in range(board_size):
        for x in range(board_size):
            available = find_correct_players_movesp(available, x, y, board_size, offsets)
    return available


def find_correct_players_movesp(available, x, y, board_size, offsets):
    if Board.board[y][x] == FigureType.white_pawn:
        for ix, iy in offsets:
            if 0 <= y + iy + iy < board_size and 0 <= x + ix + ix < board_size:
                if Board.board[y + iy][x + ix] == FigureType.black_pawn or \
                        Board.board[y + iy][x + ix] == FigureType.black_king:
                    if Board.board[y + iy + iy][x + ix + ix] == 0:
                        available.append(((x, y), (x + ix + ix, y + iy + iy)))
    if Board.board[y][x] == FigureType.white_king:
        available = check_kings_moves(available, x, y, board_size, offsets)
    return available


def check_players_free_moves(available, board_size, offsets):
    for y in range(board_size):
        for x in range(board_size):
            if Board.board[y][x] == FigureType.white_pawn:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy < board_size and 0 <= x + ix < board_size:
                        if Board.board[y + iy][x + ix] == 0:
                            available.append(((x, y), (x + ix, y + iy)))
                        if Board.board[y + iy][x + ix] == FigureType.black_pawn or \
                                Board.board[y + iy][x + ix] == FigureType.black_king:
                            if 0 <= y + iy * 2 < board_size and 0 <= x + ix * 2 < board_size:
                                if Board.board[y + iy * 2][x + ix * 2] == 0:
                                    available.append(((x, y), (x + ix * 2, y + iy * 2)))
            if Board.board[y][x] == FigureType.white_king:
                available = check_kings_moves(available, x, y, board_size, offsets)
    return available


def run_game():
    game = True
    max_recursion_depth = 3
    offsets =[(-1, -1), (-1, 1), (1, -1), (1, 1)]
    board_size = 8
    square_size = 100
    Board.board = Board.create_initial_board()
    draw_surface(Board.board, board_size, square_size)
    unselected_square = -1


    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos[0] // square_size, event.pos[1] // square_size
                curr_square = (x, y)
                curr_figure = Board.board[curr_square[1]][curr_square[0]]
                if curr_figure == 1 or curr_figure == 2:
                    Move.from_x, Move.from_y = x, y
                else:
                    if Move.from_x != unselected_square:
                        Move.to_x, Move.to_y = x, y
                        if Player.is_players_move:
                            players_move(board_size, square_size, offsets)
                            if not Player.is_players_move:
                                time.sleep(0.5)
                                computers_move(board_size, square_size, offsets, max_recursion_depth)
                        Move.from_x = unselected_square
        draw_surface(Board.board, board_size, square_size)
        pygame.display.update()
        time.sleep(0.5)


def draw_surface(board, board_size, square_size):
    display.fill((255, 255, 255))
    for i in range(board_size):
        for j in range(board_size):
            if (i + j) % 2 == 1:
                pygame.draw.rect(display, (0, 0, 0), (i * square_size, j * square_size, square_size, square_size))
            if board[j][i] == FigureType.white_pawn:
                display.blit(Image.white_pawn_image, (i * square_size, j * square_size))
            elif board[j][i] == FigureType.white_king:
                display.blit(Image.white_king_image, (i * square_size, j * square_size))
            elif board[j][i] == FigureType.black_pawn:
                display.blit(Image.black_pawn_image, (i * square_size, j * square_size))
            elif board[j][i] == FigureType.black_king:
                display.blit(Image.black_king_image, (i * square_size, j * square_size))
    pygame.display.update()


run_game()


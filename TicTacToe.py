import copy
import sys
import pygame
import random
import numpy as np

width = 800
height = 800
rows = 3
cols = 3
sq_size = width // cols
line_width = 15
circ_width = 15
cross_width = 20
rad = sq_size // 3
offset = 50
bg_color = (222, 71, 89)  
line_COLOR = (255,255,255) 
circ_COLOR = (255, 255, 255) 
cross_COLOR = (255, 255, 255) 

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(bg_color)

class TicTacToe:
    def __init__(self):
        self.cells = np.zeros((rows, cols))
        self.empty_cells = self.cells
        self.marked_cells = 0

    def game_result(self, show=False):
        for col in range(cols):
            if self.cells[0][col] == self.cells[1][col] == self.cells[2][col] != 0:
                if show:
                    color = circ_COLOR if self.cells[0][col] == 2 else cross_COLOR
                    start_pos = (col * sq_size + sq_size // 2, 20)
                    end_pos = (col * sq_size + sq_size // 2, height - 20)
                    pygame.draw.line(screen, color, start_pos, end_pos, line_width)
                return self.cells[0][col]
        for row in range(rows):
            if self.cells[row][0] == self.cells[row][1] == self.cells[row][2] != 0:
                if show:
                    color = circ_COLOR if self.cells[row][0] == 2 else cross_COLOR
                    start_pos = (20, row * sq_size + sq_size // 2)
                    end_pos = (width - 20, row * sq_size + sq_size // 2)
                    pygame.draw.line(screen, color, start_pos, end_pos, line_width)
                return self.cells[row][0]
        if self.cells[0][0] == self.cells[1][1] == self.cells[2][2] != 0:
            if show:
                color = circ_COLOR if self.cells[1][1] == 2 else cross_COLOR
                start_pos = (20, 20)
                end_pos = (width - 20, height - 20)
                pygame.draw.line(screen, color, start_pos, end_pos, cross_width)
            return self.cells[1][1]
        if self.cells[2][0] == self.cells[1][1] == self.cells[0][2] != 0:
            if show:
                color = circ_COLOR if self.cells[1][1] == 2 else cross_COLOR
                start_pos = (20, height - 20)
                end_pos = (width - 20, 20)
                pygame.draw.line(screen, color, start_pos, end_pos, cross_width)
            return self.cells[1][1]
        return 0

    def mark_cell(self, row, col, player):
        self.cells[row][col] = player
        self.marked_cells += 1

    def empty_cell(self, row, col):
        return self.cells[row][col] == 0

    def get_empty_cells(self):
        empty_cells = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_cell(row, col):
                    empty_cells.append((row, col))
        return empty_cells

    def is_full(self):
        return self.marked_cells == 9

    def is_empty(self):
        return self.marked_cells == 0


class ComputerPlayer:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def random_move(self, game_board):
        empty_cells = game_board.get_empty_cells()
        idx = random.randrange(0, len(empty_cells))
        return empty_cells[idx]

    def minimax(self, game_board, maximizing):
        result = game_board.game_result()
        if result == 1:
            return 1, None
        if result == 2:
            return -1, None
        elif game_board.is_full():
            return 0, None
        if maximizing:
            max_eval = -100
            best_move = None
            empty_cells = game_board.get_empty_cells()
            for (row, col) in empty_cells:
                temp_board = copy.deepcopy(game_board)
                temp_board.mark_cell(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_cells = game_board.get_empty_cells()
            for (row, col) in empty_cells:
                temp_board = copy.deepcopy(game_board)
                temp_board.mark_cell(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move
        
    def evaluate(self, main_board):
        if self.level == 0:
            return self.random_move(main_board)
        else:
            _, move = self.minimax(main_board, False)
            return move



class TicTacToeGame:
    def __init__(self):
        self.board = TicTacToe()
        self.computer = ComputerPlayer()
        self.current_player = 1
        self.game_mode = 'computer'
        self.running = True
        self.display_lines()

    def display_lines(self):
        screen.fill(bg_color)
        pygame.draw.line(screen, line_COLOR, (sq_size, 0), (sq_size, height), line_width)
        pygame.draw.line(screen, line_COLOR, (width - sq_size, 0), (width - sq_size, height), line_width)
        pygame.draw.line(screen, line_COLOR, (0, sq_size), (width, sq_size), line_width)
        pygame.draw.line(screen, line_COLOR, (0, height - sq_size), (width, height - sq_size), line_width)

    def draw_figure(self, row, col):
        if self.current_player == 1:
            start_pos = (col * sq_size + offset, row * sq_size + offset)
            end_pos = (col * sq_size + sq_size - offset, row * sq_size + sq_size - offset)
            pygame.draw.line(screen, cross_COLOR, start_pos, end_pos, cross_width)
            start_pos = (col * sq_size + offset, row * sq_size + sq_size - offset)
            end_pos = (col * sq_size + sq_size - offset, row * sq_size + offset)
            pygame.draw.line(screen, cross_COLOR, start_pos, end_pos, cross_width)
        elif self.current_player == 2:
            center = (col * sq_size + sq_size // 2, row * sq_size + sq_size // 2)
            pygame.draw.circle(screen, circ_COLOR, center, rad, circ_width)

    def make_move(self, row, col):
        self.board.mark_cell(row, col, self.current_player)
        self.draw_figure(row, col)
        self.switch_turn()

    def switch_turn(self):
        self.current_player = self.current_player % 2 + 1

    def change_game_mode(self):
        self.game_mode = 'computer' if self.game_mode == 'player' else 'player'

    def is_game_over(self):
        return self.board.game_result(show=True) != 0 or self.board.is_full()

    def reset_game(self):
        self.__init__()

def main():
    tic_tac_toe = TicTacToeGame()
    game_board = tic_tac_toe.board
    computer_player = tic_tac_toe.computer

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    tic_tac_toe.change_game_mode()
                if event.key == pygame.K_r:
                    tic_tac_toe.reset_game()
                    game_board = tic_tac_toe.board
                    computer_player = tic_tac_toe.computer
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // sq_size
                col = pos[0] // sq_size
                if game_board.empty_cell(row, col) and tic_tac_toe.running:
                    tic_tac_toe.make_move(row, col)
                    if tic_tac_toe.is_game_over():
                        tic_tac_toe.running = False
        if tic_tac_toe.game_mode == 'computer' and tic_tac_toe.current_player == computer_player.player and tic_tac_toe.running:
            pygame.display.update()
            row, col = computer_player.evaluate(game_board)
            tic_tac_toe.make_move(row, col)
            if tic_tac_toe.is_game_over():
                tic_tac_toe.running = False
        pygame.display.update()

if __name__ == "__main__":
    main()

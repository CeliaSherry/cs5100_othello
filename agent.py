import random

NONE = '.'
BLACK = 'B'
WHITE = 'W'
MOST_CELLS = 'M'
LEAST_CELLS = 'L'
DEFAULT_ROWS = 8
DEFAULT_COLS = 8
BOARD_DEPTH = 2

class RandomAgent:

    def __init__(self):
        self.possible_moves = []

    def get_next_action(self, board_state):
        possible_moves = board_state.get_possible_moves()
        next_move = random.choice(possible_moves)
        return next_move

class AlphaBetaAgent:
    def __init__(self):
        self.possible_moves = []

    def get_next_action(self, board_state):
        board = self.copy_state(board_state)
        return self.max_value(board_state, board, 0, float("-inf"), float("inf"))

    def max_value(self, board_state, board, depth, alpha, beta):
        if self.is_game_over(board_state, board):
            return self.get_total_cells(board_state.turn, board_state, board)
        max_score = float("-inf")

        legalMoves = self.get_possible_moves(board_state, board)

        for move in legalMoves:
            newBoard = self.copy_board(board_state, board)
            row = move[0]
            col = move[1]
            self.move(row, col, board_state, newBoard)
            score = self.min_value(newBoard, depth, board_state, 1, alpha, beta)
            if score > max_score:
                max_score = score
                action = move
            alpha = max(alpha, max_score)
            if max_score > beta:
                return max_score

        if depth == 0:
            #print(legalMoves)
            return action
        else:
            return max_score


    def min_value(self, board, depth, board_state, agent, alpha, beta):
        if self.is_game_over(board_state, board):
            return self.get_total_cells(board_state.turn, board_state, board)

        next = 0
        legalMoves = self.get_opponent_moves(board_state, board)
        min_score = float("inf")

        for move in legalMoves:
            if agent > 0:
                newBoard = self.copy_board(board_state, board)
                row = move[0]
                col = move[1]
                self.move_opponent(row, col, board_state, newBoard)
                score = self.min_value(newBoard, depth, board_state, next, alpha, beta)
            else:
                newBoard = self.copy_board(board_state, board)
                row = move[0]
                col = move[1]
                self.move_opponent(row, col, board_state, newBoard)
                if (depth+1) == BOARD_DEPTH:
                    score = self.evaluationFunction(newBoard, board_state, move)
                else:
                    score = self.max_value(board_state, newBoard, depth+1, alpha, beta)

            if score < min_score:
                min_score = score
            beta = min(beta, min_score)
            if min_score < alpha:
                return min_score

        return min_score

    def evaluationFunction(self, board, board_state, move):
        return self.get_total_cells(board_state.turn, board_state, board)
        # Corner
        #if (move[0] == 0 or move[0] == 1) and (move[1] == 0 or move[1] == 1):
        #    return 100

    def betterEvaluationFunction(self, board, board_state, move):
        blackPieces = self.get_total_cells(board_state.turn, board_state, board)
        whitePices = self.get_total_cells(board_state._opposite_turn(board_state.turn), board_state, board)
        blackMoves = len(self.get_possible_moves(board_state,board))
        whiteMoves = len(self.get_opponent_moves(board_state, board))

        # Number of pieces on board
        p = 0
        if blackPieces > whitePices:
            p = 100*(float(blackPieces)/float(blackPieces+whitePices))
        if whitePices > blackPieces:
            p = -100*(float(whitePices)/float(blackPieces+whitePices))

        # Number of moves
        m = 0
        if blackMoves > whiteMoves:
            m = 100*(float(blackMoves)/float(blackMoves+whiteMoves))
        if whiteMoves > blackMoves:
            m = -100 * (float(whiteMoves) / float(blackMoves + whiteMoves))


        # Corner occupancy
        blackCorner = 0
        whiteCorner = 0
        if board[0][0] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[0][0] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        if board[0][DEFAULT_COLS-1] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[0][DEFAULT_COLS-1] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        if board[DEFAULT_ROWS-1][0] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[DEFAULT_ROWS-1][0] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        if board[DEFAULT_ROWS-1][DEFAULT_COLS-1] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[DEFAULT_ROWS-1][DEFAULT_COLS-1] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        c = (25*blackCorner) - (25*whiteCorner)

        return p + m + c




    def get_total_cells(self, turn: str, board_state, board) -> int:
        total = 0
        for row in range(board_state.rows):
            for col in range(board_state.cols):
                if board[row][col] == turn:
                    total += 1
        return total

    def is_game_over(self, board_state, board) -> bool:
        return self.can_move(BLACK, board_state, board) == False and self.can_move(WHITE, board_state, board) == False

    def copy_state(self, board_state):
        board = []
        for row in range(board_state.rows):
            new_row = []
            for col in range(board_state.cols):
                new_row.append(board_state.current_board[row][col])
            board.append(new_row)
        return board

    def copy_board(self, board_state, oldBoard):
        board = []
        for row in range(board_state.rows):
            new_row = []
            for col in range(board_state.cols):
                new_row.append(oldBoard[row][col])
            board.append(new_row)
        return board

    def get_possible_moves(self, board_state, board):
        self.can_move(board_state.turn, board_state, board)
        return self.possible_moves

    def get_opponent_moves(self, board_state, board):
        self.can_move(board_state._opposite_turn(board_state.turn), board_state, board)
        return self.possible_moves

    def move(self, row: int, col: int, board_state, board) -> None:
        self._require_valid_empty_space_to_move(row, col, board_state, board)
        possible_directions = self._adjacent_opposite_color_directions(row, col, board_state.turn, board_state, board)

        next_turn = board_state.turn
        for direction in possible_directions:
            if self._is_valid_directional_move(row, col, direction[0], direction[1], board_state.turn, board_state, board):
                next_turn = board_state._opposite_turn(board_state.turn)
            self._convert_adjacent_cells_in_direction(row, col, direction[0], direction[1], board_state.turn, board_state, board)

        if next_turn != board_state.turn:
            board[row][col] = board_state.turn
          #  if self.can_move(next_turn, board_state, board):
          #      board_state.switch_turn()
        else:
            raise InvalidMoveException()

    def move_opponent(self, row: int, col: int, board_state, board) -> None:
        self._require_valid_empty_space_to_move(row, col, board_state, board)
        possible_directions = self._adjacent_opposite_color_directions(row, col, board_state._opposite_turn(board_state.turn), board_state, board)

        next_turn = board_state.turn
        for direction in possible_directions:
            if self._is_valid_directional_move(row, col, direction[0], direction[1], board_state._opposite_turn(board_state.turn), board_state,
                                               board):
                next_turn = board_state.turn
            self._convert_adjacent_cells_in_direction(row, col, direction[0], direction[1], board_state._opposite_turn(board_state.turn),
                                                      board_state, board)

        if next_turn != board_state._opposite_turn(board_state.turn):
            board[row][col] = board_state._opposite_turn(board_state.turn)
        #  if self.can_move(next_turn, board_state, board):
        #      board_state.switch_turn()
        else:
            raise InvalidMoveException()

    def can_move(self, turn: str, board_state, board) -> bool:
        can_move = False
        new_possible_moves = []
        for row in range(board_state.rows):
            for col in range(board_state.cols):
                if board[row][col] == NONE:
                    for direction in self._adjacent_opposite_color_directions(row, col, turn, board_state, board):
                        if self._is_valid_directional_move(row, col, direction[0], direction[1], turn, board_state, board):
                            new_possible_moves.append([row, col])
                            can_move = True
        self.possible_moves = new_possible_moves
        return can_move

    def _require_valid_empty_space_to_move(self, row: int, col: int, board_state, board) -> bool:
        ''' In order to move, the specified cell space must be within board boundaries
            AND the cell has to be empty '''

        if self._is_valid_cell(row, col, board_state) and self._cell_color(row, col, board_state, board) != NONE:
            raise InvalidMoveException()

    def _is_valid_cell(self, row: int, col: int, board_state) -> bool:
        ''' Returns True if the given cell move position is invalid due to
            position (out of bounds) '''
        return self._is_valid_row_number(row, board_state) and self._is_valid_col_number(col, board_state)

    def _is_valid_row_number(self, row: int, board_state) -> bool:
        ''' Returns True if the given row number is valid; False otherwise '''
        return 0 <= row < board_state.rows

    def _is_valid_col_number(self, col: int, board_state) -> bool:
        ''' Returns True if the given col number is valid; False otherwise '''
        return 0 <= col < board_state.cols


    def _cell_color(self, row: int, col: int, board_state, board) -> str:
        ''' Determines the color/player of the specified cell '''
        return board[row][col]

    def _adjacent_opposite_color_directions(self, row: int, col: int, turn: str, board_state, board) -> [tuple]:
        dir_list = []
        for rowdelta in range(-1, 2):
            for coldelta in range(-1, 2):
                if self._is_valid_cell(row+rowdelta, col + coldelta, board_state):
                    if board[row + rowdelta][col + coldelta] == board_state._opposite_turn(turn):
                        dir_list.append((rowdelta, coldelta))
        return dir_list

    def _is_valid_directional_move(self, row: int, col: int, rowdelta: int, coldelta: int, turn: str, board_state, board) -> bool:
        current_row = row + rowdelta
        current_col = col + coldelta

        last_cell_color = board_state._opposite_turn(turn)

        while True:
            # Immediately return false if the board reaches the end (b/c there's no blank
            # space for the cell to sandwich the other colored cell(s)
            if not self._is_valid_cell(current_row, current_col, board_state):
                break
            if self._cell_color(current_row, current_col, board_state, board) == NONE:
                break
            if self._cell_color(current_row, current_col, board_state, board) == turn:
                last_cell_color = turn
                break

            current_row += rowdelta
            current_col += coldelta

        return last_cell_color == turn

    def _convert_adjacent_cells_in_direction(self, row: int, col: int,
                                             rowdelta: int, coldelta: int, turn: str, board_state, board) -> None:
        if self._is_valid_directional_move(row, col, rowdelta, coldelta, turn, board_state, board):
            current_row = row + rowdelta
            current_col = col + coldelta

            while self._cell_color(current_row, current_col, board_state, board) == board_state._opposite_turn(turn):
                self._flip_cell(current_row, current_col, board_state, board)
                current_row += rowdelta
                current_col += coldelta

    def _flip_cell(self, row: int, col: int, board_state, board) -> None:
        ''' Flips the specified cell over to the other color '''
        board[row][col] = board_state._opposite_turn(board[row][col])


class ExpectimaxAgent:

    def __init__(self):
        self.possible_moves = []

    def get_next_action(self, board_state):
        board = self.copy_state(board_state)
        return self.max_value(board_state, 0, board)

    def max_value(self, board_state, depth, board):
        if self.is_game_over(board_state, board):
            return self.get_total_cells(board_state.turn, board_state, board)
        max_score = float("-inf")

        legalMoves = self.get_possible_moves(board_state,board)

        for move in legalMoves:
            newBoard = self.copy_board(board_state, board)
            row = move[0]
            col = move[1]
            self.move(row, col, board_state, newBoard)
            score = self.exp_value(newBoard, depth, board_state, 1)
            if score > max_score:
                max_score = score
                action = move

        if depth == 0:
            return action
        else:
            return max_score



    def exp_value(self, board, depth, board_state, agent):
        if self.is_game_over(board_state, board):
            return self.get_total_cells(board_state.turn, board_state, board)

        next = 0
        legalMoves = self.get_opponent_moves(board_state, board)
        v = 0

        for move in legalMoves:
            if agent > 0:
                newBoard = self.copy_board(board_state, board)
                row = move[0]
                col = move[1]
                self.move_opponent(row, col, board_state, newBoard)
                score = self.exp_value(newBoard, depth, board_state, next)
            else:
                newBoard = self.copy_board(board_state, board)
                row = move[0]
                col = move[1]
                self.move_opponent(row, col, board_state, newBoard)
                if (depth+1) == BOARD_DEPTH:
                    score = self.evaluationFunction(newBoard, board_state, move)
                else:
                    score = self.max_value(board_state, depth+1, newBoard)

            v = v + score

        if len(legalMoves) == 0:
            return 1
        else:
            return float(v) / float(len(legalMoves))
        #return 1

    def evaluationFunction(self, board, board_state, move):
        return self.get_total_cells(board_state.turn, board_state, board)
        # Corner
        #if (move[0] == 0 or move[0] == 1) and (move[1] == 0 or move[1] == 1):
        #    return 100

    def betterEvaluationFunction(self, board, board_state, move):
        blackPieces = self.get_total_cells(board_state.turn, board_state, board)
        whitePices = self.get_total_cells(board_state._opposite_turn(board_state.turn), board_state, board)
        blackMoves = len(self.get_possible_moves(board_state,board))
        whiteMoves = len(self.get_opponent_moves(board_state, board))

        # Number of pieces on board
        p = 0
        if blackPieces > whitePices:
            p = 100*(float(blackPieces)/float(blackPieces+whitePices))
        if whitePices > blackPieces:
            p = -100*(float(whitePices)/float(blackPieces+whitePices))

        # Number of moves
        m = 0
        if blackMoves > whiteMoves:
            m = 100*(float(blackMoves)/float(blackMoves+whiteMoves))
        if whiteMoves > blackMoves:
            m = -100 * (float(whiteMoves) / float(blackMoves + whiteMoves))


        # Corner occupancy
        blackCorner = 0
        whiteCorner = 0
        if board[0][0] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[0][0] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        if board[0][DEFAULT_COLS-1] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[0][DEFAULT_COLS-1] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        if board[DEFAULT_ROWS-1][0] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[DEFAULT_ROWS-1][0] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        if board[DEFAULT_ROWS-1][DEFAULT_COLS-1] == board_state.turn:
            blackCorner = blackCorner + 1
        if board[DEFAULT_ROWS-1][DEFAULT_COLS-1] == board_state._opposite_turn(board_state.turn):
            whiteCorner = whiteCorner + 1

        c = (25*blackCorner) - (25*whiteCorner)

        return p + m + c




    def get_total_cells(self, turn: str, board_state, board) -> int:
        total = 0
        for row in range(board_state.rows):
            for col in range(board_state.cols):
                if board[row][col] == turn:
                    total += 1
        return total

    def is_game_over(self, board_state, board) -> bool:
        return self.can_move(BLACK, board_state, board) == False and self.can_move(WHITE, board_state, board) == False

    def copy_state(self, board_state):
        board = []
        for row in range(board_state.rows):
            new_row = []
            for col in range(board_state.cols):
                new_row.append(board_state.current_board[row][col])
            board.append(new_row)
        return board

    def copy_board(self, board_state, oldBoard):
        board = []
        for row in range(board_state.rows):
            new_row = []
            for col in range(board_state.cols):
                new_row.append(oldBoard[row][col])
            board.append(new_row)
        return board

    def get_possible_moves(self, board_state, board):
        self.can_move(board_state.turn, board_state, board)
        return self.possible_moves

    def get_opponent_moves(self, board_state, board):
        self.can_move(board_state._opposite_turn(board_state.turn), board_state, board)
        return self.possible_moves

    def move(self, row: int, col: int, board_state, board) -> None:
        self._require_valid_empty_space_to_move(row, col, board_state, board)
        possible_directions = self._adjacent_opposite_color_directions(row, col, board_state.turn, board_state, board)

        next_turn = board_state.turn
        for direction in possible_directions:
            if self._is_valid_directional_move(row, col, direction[0], direction[1], board_state.turn, board_state, board):
                next_turn = board_state._opposite_turn(board_state.turn)
            self._convert_adjacent_cells_in_direction(row, col, direction[0], direction[1], board_state.turn, board_state, board)

        if next_turn != board_state.turn:
            board[row][col] = board_state.turn
          #  if self.can_move(next_turn, board_state, board):
          #      board_state.switch_turn()
        else:
            raise InvalidMoveException()

    def move_opponent(self, row: int, col: int, board_state, board) -> None:
        self._require_valid_empty_space_to_move(row, col, board_state, board)
        possible_directions = self._adjacent_opposite_color_directions(row, col, board_state._opposite_turn(board_state.turn), board_state, board)

        next_turn = board_state.turn
        for direction in possible_directions:
            if self._is_valid_directional_move(row, col, direction[0], direction[1], board_state._opposite_turn(board_state.turn), board_state,
                                               board):
                next_turn = board_state.turn
            self._convert_adjacent_cells_in_direction(row, col, direction[0], direction[1], board_state._opposite_turn(board_state.turn),
                                                      board_state, board)

        if next_turn != board_state._opposite_turn(board_state.turn):
            board[row][col] = board_state._opposite_turn(board_state.turn)
        #  if self.can_move(next_turn, board_state, board):
        #      board_state.switch_turn()
        else:
            raise InvalidMoveException()

    def can_move(self, turn: str, board_state, board) -> bool:
        can_move = False
        new_possible_moves = []
        for row in range(board_state.rows):
            for col in range(board_state.cols):
                if board[row][col] == NONE:
                    for direction in self._adjacent_opposite_color_directions(row, col, turn, board_state, board):
                        if self._is_valid_directional_move(row, col, direction[0], direction[1], turn, board_state, board):
                            new_possible_moves.append([row, col])
                            can_move = True
        self.possible_moves = new_possible_moves
        return can_move

    def _require_valid_empty_space_to_move(self, row: int, col: int, board_state, board) -> bool:
        ''' In order to move, the specified cell space must be within board boundaries
            AND the cell has to be empty '''

        if self._is_valid_cell(row, col, board_state) and self._cell_color(row, col, board_state, board) != NONE:
            raise InvalidMoveException()

    def _is_valid_cell(self, row: int, col: int, board_state) -> bool:
        ''' Returns True if the given cell move position is invalid due to
            position (out of bounds) '''
        return self._is_valid_row_number(row, board_state) and self._is_valid_col_number(col, board_state)

    def _is_valid_row_number(self, row: int, board_state) -> bool:
        ''' Returns True if the given row number is valid; False otherwise '''
        return 0 <= row < board_state.rows

    def _is_valid_col_number(self, col: int, board_state) -> bool:
        ''' Returns True if the given col number is valid; False otherwise '''
        return 0 <= col < board_state.cols


    def _cell_color(self, row: int, col: int, board_state, board) -> str:
        ''' Determines the color/player of the specified cell '''
        return board[row][col]

    def _adjacent_opposite_color_directions(self, row: int, col: int, turn: str, board_state, board) -> [tuple]:
        dir_list = []
        for rowdelta in range(-1, 2):
            for coldelta in range(-1, 2):
                if self._is_valid_cell(row+rowdelta, col + coldelta, board_state):
                    if board[row + rowdelta][col + coldelta] == board_state._opposite_turn(turn):
                        dir_list.append((rowdelta, coldelta))
        return dir_list

    def _is_valid_directional_move(self, row: int, col: int, rowdelta: int, coldelta: int, turn: str, board_state, board) -> bool:
        current_row = row + rowdelta
        current_col = col + coldelta

        last_cell_color = board_state._opposite_turn(turn)

        while True:
            # Immediately return false if the board reaches the end (b/c there's no blank
            # space for the cell to sandwich the other colored cell(s)
            if not self._is_valid_cell(current_row, current_col, board_state):
                break
            if self._cell_color(current_row, current_col, board_state, board) == NONE:
                break
            if self._cell_color(current_row, current_col, board_state, board) == turn:
                last_cell_color = turn
                break

            current_row += rowdelta
            current_col += coldelta

        return last_cell_color == turn

    def _convert_adjacent_cells_in_direction(self, row: int, col: int,
                                             rowdelta: int, coldelta: int, turn: str, board_state, board) -> None:
        if self._is_valid_directional_move(row, col, rowdelta, coldelta, turn, board_state, board):
            current_row = row + rowdelta
            current_col = col + coldelta

            while self._cell_color(current_row, current_col, board_state, board) == board_state._opposite_turn(turn):
                self._flip_cell(current_row, current_col, board_state, board)
                current_row += rowdelta
                current_col += coldelta

    def _flip_cell(self, row: int, col: int, board_state, board) -> None:
        ''' Flips the specified cell over to the other color '''
        board[row][col] = board_state._opposite_turn(board[row][col])






import random

NONE = '.'
BLACK = 'B'
WHITE = 'W'
MOST_CELLS = 'M'
LEAST_CELLS = 'L'
DEFAULT_ROWS = 8
DEFAULT_COLS = 8
DEPTH = 1

class RandomAgent:

    def __init__(self):
        self.possible_moves = []

    def get_next_action(self, board_state):
        possible_moves = board_state.get_possible_moves()
        next_move = random.choice(possible_moves)

        board = self.copy_state(board_state)
        newBoard = self.copy_board(board_state, board)
        row = next_move[0]
        col = next_move[1]
        self.move(row, col, board_state, board)

        whiteCells = self.get_total_cells(board_state._opposite_turn(board_state.turn), board_state, board)
        blackCells = self.get_total_cells(board_state.turn, board_state, board)
        #print(board_state.turn)
        #print(board)

        print(newBoard)
        #print(whiteCells)
        #print(blackCells)



        #turns = self.get_possible_moves(board_state)
        #opponentTurns = self.get_opponent_moves(board_state)
        #print(board_state.turn)
        #print(turns)
        #print(board_state._opposite_turn(board_state.turn))
        #print(opponentTurns)
        #print(board_state._opposite_turn(board_state.turn))
        return next_move

    def copy_board(self, board_state, oldBoard):
        board = []
        for row in range(board_state.rows):
            new_row = []
            for col in range(board_state.cols):
                new_row.append(oldBoard[row][col])
            board.append(new_row)
        return board

    def get_total_cells(self, turn: str, board_state, board) -> int:
        ''' Returns the total cell count of the specified colored player '''
        total = 0
        for row in range(board_state.rows):
            for col in range(board_state.cols):
                if board[row][col] == turn:
                    total += 1
        return total

    def copy_state(self, board_state):
        board = []
        for row in range(board_state.rows):
            new_row = []
            for col in range(board_state.cols):
                new_row.append(board_state.current_board[row][col])
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
           # if self.can_move(next_turn, board_state, board):
              #  board_state.switch_turn()
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

# to get opposite turn: board_state._opposite_turn(board_state.turn)


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
            score = self.exp_value(newBoard, depth, board_state)
            if score > max_score:
                max_score = score
                action = move

        if depth == 0:
            return action
        else:
            return max_score

    def exp_value(self, board, depth, board_state):
        if self.is_game_over(board_state, board):
            return self.get_total_cells(board_state.turn, board_state, board)

        next = 0

        legalMoves = self.get_opponent_moves(board_state, board)
        v = 0
        successors = 0

        for move in legalMoves:
            newBoard = self.copy_board(board_state, board)
            row = move[0]
            col = move[1]
            self.move_opponent(row, col, board_state, newBoard)
            score = self.evaluationFunction(newBoard, board_state, move)


            # score = self.exp_value(newBoard, depth, board_state, next)
            # else:
            #     # make new board to try out moves
            #     newBoard = self.copy_board(board_state, board)
            #     row = move[0]
            #     col = move[1]
            #     self.move(row, col, board_state, newBoard)
            #     if (depth + 1) == DEPTH:
            #         score = self.evaluationFunction(newBoard, board_state, move)
            #     else:
            #         score = self.max_value(board_state, depth + 1, newBoard)
            v = v + score


        return float(v) / float(len(legalMoves))
        #return 1

    def evaluationFunction(self, board, board_state, move):
        return self.get_total_cells(board_state.turn, board_state, board)
        # Corner
        #if (move[0] == 0 or move[0] == 1) and (move[1] == 0 or move[1] == 1):
        #    return 100


    def get_total_cells(self, turn: str, board_state, board) -> int:
        ''' Returns the total cell count of the specified colored player '''
        total = 0
        for row in range(board_state.rows):
            for col in range(board_state.cols):
                if board[row][col] == turn:
                    total += 1
        return total

    def is_game_over(self, board_state, board) -> bool:
        ''' Looks through every empty cell and determines if there are
            any valid moves left. If not, returns True; otherwise returns False '''
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












    # def getAction(self, board_state):
    #     """
    #     Returns the expectimax action using self.depth and self.evaluationFunction
    #
    #     """
    #     return self.max_value(board_state, 0)
    #
    # def max_value(self, board_state, depth):
    #     if board_state.is_game_over():
    #         return board_state.get_total_cells(BLACK)
    #     max_score = float("-inf")
    #     legalMoves = board_state.get_possible_moves()
    #     return legalMoves[0]

    #     for move in legalMoves:
    #         score = self.exp_value(board_state.move(move), depth, 1)
    #         if score > max_score:
    #             max_score = score
    #             action = move
    #         if depth == 0:
    #             return action
    #         else:
    #             return max_score
    #
    # def exp_value(self, gameState, depth, agent):
    #     if board_state.is_game_over():
    #         return board_state.get_total_cells(BLACK)
    #
    #     if agent == 1:
    #         next = 0
    #     else:
    #         next = agent + 1
    #
    #     self.switch_turn()
    #     legalMoves = board_state._agent_w.get_possible_moves()
    #     v = 0
    #     successors = 0
    #
    #     for move in legalMoves:
    #         if next > 0:
    #             score = self.exp_value(board_state.move(move), depth, next)
    #         else:
    #             if(depth+1) == self.depth:
    #                 score = self.get_total_cells(self.color)
    #             else:
    #                 score = self.max_value(board_state.move(move), depth+1)
    #
    #         v = v + score
    #         successors = successors + 1
    #
    #     return float(v)/float(successors)


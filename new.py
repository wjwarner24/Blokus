import random


# Dimensions of the board
board_dimensions = 8

# 0 = empty square
# 1 = square occupied by the piece
# 2 = valid corner-touching position
# 3 = invalid block-touching position
pieces = {
    "plus": {
        "shape": [
        [0, 2, 3, 2, 0],
        [2, 3, 1, 3, 2],
        [3, 1, 1, 1, 3],
        [2, 3, 1, 3, 2],
        [0, 2, 3, 2, 0]
        ],
        "value": 5
    },
    "L": {
        "shape": [
        [2, 3, 2, 0],
        [3, 1, 3, 0],
        [3, 1, 3, 2],
        [3, 1, 1, 3],
        [2, 3, 3, 2]
        ],
        "value": 4
    },
    "T": {
        "shape": [
        [2, 3, 2, 0],
        [3, 1, 3, 2],
        [3, 1, 1, 3],
        [3, 1, 3, 2],
        [2, 3, 2, 0]
        ],
        "value": 4
    },
    "square": {
        "shape": [
        [2, 3, 3, 2],
        [3, 1, 1, 3],
        [3, 1, 1, 3],
        [2, 3, 3, 2]
        ],
        "value": 4
    },
    "corner": {
        "shape": [
        [2, 3, 2, 0],
        [3, 1, 3, 2],
        [3, 1, 1, 3],
        [2, 3, 3, 2]
        ],
        "value": 3
    },
    "line3": {
        "shape": [
        [2, 3, 2],
        [3, 1, 3],
        [3, 1, 3],
        [3, 1, 3],
        [2, 3, 2]
        ],
        "value": 3
    },
    "line2": {
        "shape": [
        [2, 3, 2],
        [3, 1, 3],
        [3, 1, 3],
        [2, 3, 2]
        ],
        "value": 2
    },
    "dot": {
        "shape": [
        [2, 3, 2],
        [3, 1, 3],
        [2, 3, 2]
        ],
        "value": 1
    }
}

class Board:
    def __init__(self, board_dim):
        self.dim = board_dim
        self.squares = [[0 for _ in range(board_dim)] for _ in range(board_dim)]
    
    # gets the number of blocks for a player
    def get_num_blocks(self, player):
        count = 0
        for row in self.squares:
            for cell in row:
                if cell == player:
                    count += 1
        return count
    
    # gets the block diff between the two players
    def get_block_diff(self):
        count = 0
        for row in self.squares:
            for cell in row:
                if cell == 1:
                    count += 1
                elif cell == 2:
                    count -= 1
        return count
    
    # determines whether a cell is a corner for a given player
    def is_corner(self, x, y, player):
        if self.get_square(x, y) != 0:
            return False
        corner_squares = [
            [x - 1, y - 1],
            [x - 1, y + 1],
            [x + 1, y - 1],
            [x + 1, y + 1]
        ]
        for corner in corner_squares:
            if self.get_square(corner[0], corner[1]) == player:
                return True
        return False
        
    # gets the number of corners for a player    
    def num_corners(self, player):
        count = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.is_corner(i, j, player):
                    count += 1
        return count
    
    # Gets the corner diff between the two players
    def get_corner_diff(self):
        count = 0
        for i in range(self.dim):
            for j in range(self.dim):
                if self.is_corner(i, j, 1):
                    count += 1
                if self.is_corner(i, j, 2):
                    count -= 1
        return count
    
    # gets the value of a square
    def get_square(self, x, y):
        if 0 <= x < self.dim and 0 <= y < self.dim:
            return self.squares[x][y]
        return -1
    
    # determines if a piece can be placed at a given position
    def is_move_valid(self, piece, x, y, ori, current_player, is_first_move):
        
        touching_corner = False
        
        # rotate the piece if needed
        if ori == "right":
            piece = [[piece[j][i] for j in range(len(piece) - 1, -1, -1)] for i in range(len(piece[0]))]
        elif ori == "left":
            piece = [[piece[j][i] for j in range(len(piece))] for i in range(len(piece[0]) - 1, -1, -1)]
        elif ori == "down":
            piece = [row[::-1] for row in piece[::-1]]
        
        # starting corner for each player
        corner_x, corner_y = (0, 0) if current_player == 1 else (self.dim - 1, self.dim - 1)
    
        # iterate over the piece
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                
                # ensure the piece is within the board bounds and the position is empty
                if piece[i][j] == 1 and self.get_square(x + i, y + j) != 0:
                    return False
                
            
                # ensure the piece has a corner touching another piece of the same player
                if piece[i][j] == 2 and self.get_square(x + i, y + j) == current_player:
                    touching_corner = True
            
                # ensure the piece does not have a block touching another piece of the same player
                if piece[i][j] == 3 and self.get_square(x + i, y + j) == current_player:
                    return False
                
                # If its the first, move the piece must touch the starting corner
                if (piece[i][j] == 1 and 
                    is_first_move and
                    (corner_x, corner_y) == (x + i, y + j)
                ):
                    touching_corner = True

        # Return true as long as there was at least one corner
        return touching_corner
    
    # places a piece on the board
    def place_piece(self, piece, x, y, ori, current_player):
        
        if ori == "right":
            piece = [[piece[j][i] for j in range(len(piece) - 1, -1, -1)] for i in range(len(piece[0]))]
        elif ori == "left":
            piece = [[piece[j][i] for j in range(len(piece))] for i in range(len(piece[0]) - 1, -1, -1)]
        elif ori == "down":
            piece = [row[::-1] for row in piece[::-1]]
            
        for i in range(len(piece)):
            for j in range(len(piece[0])):
                if piece[i][j] == 1:
                    self.squares[x + i][y + j] = current_player
    
    # undo a move            
    def undo_move(self, piece, x, y, ori):
            
            if ori == "right":
                piece = [[piece[j][i] for j in range(len(piece) - 1, -1, -1)] for i in range(len(piece[0]))]
            elif ori == "left":
                piece = [[piece[j][i] for j in range(len(piece))] for i in range(len(piece[0]) - 1, -1, -1)]
            elif ori == "down":
                piece = [row[::-1] for row in piece[::-1]]
                
            for i in range(len(piece)):
                for j in range(len(piece[0])):
                    if piece[i][j] == 1:
                        self.squares[x + i][y + j] = 0
                
    
    # Gets the corner diff of a move
    def corner_diff_for_move(self, piece, x, y, ori, current_player):
        
        starting_corner_diff = self.get_corner_diff()
        self.place_piece(piece, x, y, ori, current_player)
        ending_corner_diff = self.get_corner_diff()
        self.undo_move(piece, x, y, ori)
        value = ending_corner_diff - starting_corner_diff
        if current_player == 2:
            value *= -1
        return value
                    
                    
    # prints the board
    def print_board(self):
        for _ in range(self.dim * 2 + 2):
            print("─", end="")
        print()
        for i, row in enumerate(self.squares):
            print("|", end="")
            for cell in row:
                if cell == 0:
                    print(" ", end=" ")
                elif cell == 1:
                    print("X", end=" ")
                elif cell == 2:
                    print("O", end=" ")
                else:
                    print("#", end=" ")
            if i < len(self.squares) - 1:
                print("|")  # End the line
            else:
                print("|", end="") 
        print()
        for _ in range(self.dim * 2 + 2):
            print("─", end="")
        print()
                


class Blokus:
    def __init__(self, board_dim, pieces, p1_strategy, p2_strategy):
        self.board = Board(board_dim)
        self.pieces = pieces
        self.players = {
            1: list(pieces.keys()),
            2: list(pieces.keys())
        }
        self.current_player = 1
        self.first_move = {1: True, 2: True}
        self.strategies = {1: p1_strategy, 2: p2_strategy}
        self.cannot_move = {1: False, 2: False}
        print(f"Player 1 strategy: {p1_strategy} Player 2 strategy: {p2_strategy}")
    
        
    # get all valid moves
    def get_valid_moves(self):
        
        valid_moves = []
        # iterate over the pieces of the current player
        for piece_name in self.players[self.current_player]:
            piece = self.pieces[piece_name]["shape"]
            
            # iterate over the board with extra padding
            for x in range(-5, self.board.dim + 5):
                for y in range(-5, self.board.dim + 5):
                    
                    #add the move if it is valid in all orientations
                    if self.board.is_move_valid(piece, x, y, "up", self.current_player, self.first_move[self.current_player]):
                        valid_moves.append((piece_name, piece, x, y, "up"))
                    if self.board.is_move_valid(piece, x, y, "right", self.current_player, self.first_move[self.current_player]):
                        valid_moves.append((piece_name, piece, x, y, "right"))
                    if self.board.is_move_valid(piece, x, y, "left", self.current_player, self.first_move[self.current_player]):
                        valid_moves.append((piece_name, piece, x, y, "left"))
                    if self.board.is_move_valid(piece, x, y, "down", self.current_player, self.first_move[self.current_player]):
                        valid_moves.append((piece_name, piece, x, y, "down"))
                    
        return valid_moves
    
    # # picks a random move from the valid moves
    def select_random_move(self):
        
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None, None, None, None, None
        random_index = random.randint(0, len(valid_moves) - 1)
        return valid_moves[random_index]
    
    # picks a random move from the valid moves with the largest piece size
    def select_large_move(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None, None, None, None, None

        # Pair sizes with their indices, adding a small random value for randomness
        sizes = [(pieces[move[0]]["value"] + random.random(), i) for i, move in enumerate(valid_moves)]
    
        # Sort by size (now includes random tiebreaker)
        sizes.sort(key=lambda x: x[0], reverse=True)
    
        # Select the index of the smallest size
        index = sizes[0][1]
        return valid_moves[index]
    
    def get_corner_move(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None, None, None, None, None
        corner_moves = []
        for piece_name, piece, x, y, ori in valid_moves:
            corner_diff = self.board.corner_diff_for_move(piece, x, y, ori, self.current_player)
            #print(corner_diff + random.random(), (piece_name, piece, x, y, ori))
            corner_moves.append((corner_diff + random.random(), (piece_name, piece, x, y, ori)))
            
        corner_moves.sort(key=lambda x: x[0], reverse=True)
        return corner_moves[0][1]
    
    def get_combo_move(self):
        valid_moves = self.get_valid_moves()
        if not valid_moves:
            return None, None, None, None, None
        corner_moves = []
        for piece_name, piece, x, y, ori in valid_moves:
            corner_diff = self.board.corner_diff_for_move(piece, x, y, ori, self.current_player)
            #print(corner_diff + random.random(), (piece_name, piece, x, y, ori))
            corner_moves.append((pieces[piece_name]["value"] + corner_diff + random.random(), (piece_name, piece, x, y, ori)))
            
        corner_moves.sort(key=lambda x: x[0], reverse=True)
        return corner_moves[0][1]
                    
    # makes a move for the current player
    def make_move(self):
        
        # select a move
        piece_name, piece, x, y, ori = None, None, None, None, None
        
        if self.strategies[self.current_player] == "random":
            piece_name, piece, x, y, ori = self.select_random_move()
        elif self.strategies[self.current_player] == "large":
            piece_name, piece, x, y, ori = self.select_large_move()
        elif self.strategies[self.current_player] == "corner":
            piece_name, piece, x, y, ori = self.get_corner_move()
        elif self.strategies[self.current_player] == "combo":
            piece_name, piece, x, y, ori = self.get_combo_move()
        elif self.strategies[self.current_player] == "minimax-large":
            piece_name, piece, x, y, ori = self.get_minimax_move("large", depth=3)
        elif self.strategies[self.current_player] == "minimax-corner":
            piece_name, piece, x, y, ori = self.get_minimax_move("corner", depth=3)
        elif self.strategies[self.current_player] == "minimax-combo":
            piece_name, piece, x, y, ori = self.get_minimax_move("combo", depth=3)
        
        else:
            raise ValueError("Invalid strategy")
        
        # if no valid moves
        if piece_name is None:
            
            self.cannot_move[self.current_player] = True
            print(f"Player {self.current_player} has no valid moves")
            self.first_move[self.current_player] = False
            self.current_player = 3 - self.current_player
            
            if self.cannot_move[1] == True and self.cannot_move[2] == True:
                return -1
            
            return 0
            
        
        # place the piece on the board
        self.board.place_piece(piece, x, y, ori, self.current_player)
        print(f"Player {self.current_player} placed {piece_name} {ori} at ({x}, {y}).")
        self.board.print_board()
        
        # remove the piece from the player's list of pieces
        self.players[self.current_player].remove(piece_name)
        
        # It is no longer this player's first move
        self.first_move[self.current_player] = False
        
        # update the current player
        self.current_player = 3 - self.current_player
    
        return 0
    
    # play the game
    def play_game(self):
        
        # print the initial board
        print(f"Starting Blokus! {self.board.dim}x{self.board.dim} board")
        self.board.print_board()
        
        # initialize the value to 0
        value = 0
        
        # play the game while the current player has a move
        while value == 0:
            
            # set the value to the result of the move
            value = self.make_move()
            
        p1_pieces = sum((self.pieces[piece]["value"]) for piece in self.players[1])
        p2_pieces = sum((self.pieces[piece]["value"]) for piece in self.players[2])
        
        # if the current player has no moves, the other player wins
        if p1_pieces > p2_pieces:
            value = 2
        elif p2_pieces > p1_pieces:
            value = 1
        else:
            print(f"Game over! Its a tie!")
            print(f"Both players have no pieces left!")
            return 0
            
        print(f"Game over! Player {value} wins!")
        print(f"Player 1 has {p1_pieces} blocks left, Player 2 has {p2_pieces} blocks left")
        return value

    
    
    def minimax_large(self, board, depth, alpha, beta, maximizing_player):
      
        # Check if we've reached the depth limit or if there are no valid moves
        valid_moves = self.get_valid_moves()
        
        player_making_move = 1 if maximizing_player else 2
        
        if depth == 0 or not valid_moves:
            # Evaluate the board using the heuristic
            return board.get_block_diff(), (None, None, None, None, None)
        
        sizes = [(pieces[move[0]]["value"], move) for move in valid_moves]
        sizes.sort(key=lambda x: x[0], reverse=True)
        max_size = sizes[0][0]
        valid_moves = [move for size, move in sizes if size == max_size or size == max_size - 1 or size == max_size - 2]

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for move in valid_moves:
                piece_name, piece, x, y, ori = move
                # Apply the move
                board.place_piece(piece, x, y, ori, player_making_move)
                # Recurse
                eval, _ = self.minimax_large(board, depth - 1, alpha, beta, False)
                # Undo the move
                board.undo_move(piece, x, y, ori)
                # Update the best evaluation
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                # Alpha-beta pruning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_move = None

            for move in valid_moves:
                piece_name, piece, x, y, ori = move
                # Apply the move
                board.place_piece(piece, x, y, ori, player_making_move)
                # Recurse
                eval, _ = self.minimax_large(board, depth - 1, alpha, beta, True)
                # Undo the move
                board.undo_move(piece, x, y, ori)
                # Update the best evaluation
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                # Alpha-beta pruning
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move
        
    def minimax_corner(self, board, depth, alpha, beta, maximizing_player):
      
        # Check if we've reached the depth limit or if there are no valid moves
        valid_moves = self.get_valid_moves()
        
        player_making_move = 1 if maximizing_player else 2
        
        if depth == 0 or not valid_moves:
            # Evaluate the board using the heuristic
            return board.get_corner_diff(), (None, None, None, None, None)
        
        corner_moves = []
        for move in valid_moves:
            piece_name, piece, x, y, ori = move
            corner_diff = self.board.corner_diff_for_move(piece, x, y, ori, self.current_player)
            corner_moves.append((corner_diff, move))
            
        corner_moves.sort(key=lambda x: x[0], reverse=True)
        max_corners = corner_moves[0][0]
        valid_moves = [move for corner_diff, move in corner_moves if corner_diff == max_corners or corner_diff == max_corners - 1 or corner_diff == max_corners - 2]
        

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for move in valid_moves:
                piece_name, piece, x, y, ori = move
                # Apply the move
                board.place_piece(piece, x, y, ori, player_making_move)
                # Recurse
                eval, _ = self.minimax_corner(board, depth - 1, alpha, beta, False)
                # Undo the move
                board.undo_move(piece, x, y, ori)
                # Update the best evaluation
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                # Alpha-beta pruning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_move = None

            for move in valid_moves:
                piece_name, piece, x, y, ori = move
                # Apply the move
                board.place_piece(piece, x, y, ori, player_making_move)
                # Recurse
                eval, _ = self.minimax_corner(board, depth - 1, alpha, beta, True)
                # Undo the move
                board.undo_move(piece, x, y, ori)
                # Update the best evaluation
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                # Alpha-beta pruning
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move
        
    
    def minimax_combo(self, board, depth, alpha, beta, maximizing_player):
      
        # Check if we've reached the depth limit or if there are no valid moves
        valid_moves = self.get_valid_moves()
        
        player_making_move = 1 if maximizing_player else 2
        
        if depth == 0 or not valid_moves:
            # Evaluate the board using the heuristic
            return board.get_block_diff() + board.get_corner_diff(), (None, None, None, None, None)
        
        corner_moves = []
        for move in valid_moves:
            piece_name, piece, x, y, ori = move
            corner_diff = board.corner_diff_for_move(piece, x, y, ori, player_making_move)
            size = pieces[piece_name]["value"]
            corner_moves.append((corner_diff + size, move))
            
        corner_moves.sort(key=lambda x: x[0], reverse=True)
        max_corners = corner_moves[0][0]
        valid_moves = [move for corner_diff, move in corner_moves if 
                       corner_diff == max_corners or 
                       corner_diff == max_corners - 1 or 
                       corner_diff == max_corners - 2 or 
                       corner_diff == max_corners - 3 or 
                       corner_diff == max_corners - 4]
        

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for move in valid_moves:
                piece_name, piece, x, y, ori = move
                # Apply the move
                board.place_piece(piece, x, y, ori, player_making_move)
                # Recurse
                eval, _ = self.minimax_combo(board, depth - 1, alpha, beta, False)
                # Undo the move
                board.undo_move(piece, x, y, ori)
                # Update the best evaluation
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                # Alpha-beta pruning
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = float('inf')
            best_move = None

            for move in valid_moves:
                piece_name, piece, x, y, ori = move
                # Apply the move
                board.place_piece(piece, x, y, ori, player_making_move)
                # Recurse
                eval, _ = self.minimax_combo(board, depth - 1, alpha, beta, True)
                # Undo the move
                board.undo_move(piece, x, y, ori)
                # Update the best evaluation
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                # Alpha-beta pruning
                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move


    def get_minimax_move(self, strategy, depth=3):
        if strategy == "large":
            maximizing_player = (self.current_player == 1)
            _, best_move = self.minimax_large(self.board, depth, float('-inf'), float('inf'), maximizing_player)
            return best_move
        elif strategy == "corner":
            maximizing_player = (self.current_player == 1)
            _, best_move = self.minimax_corner(self.board, depth, float('-inf'), float('inf'), maximizing_player)
            return best_move
        elif strategy == "combo":
            maximizing_player = (self.current_player == 1)
            _, best_move = self.minimax_combo(self.board, depth, float('-inf'), float('inf'), maximizing_player)
            return best_move




def play_games(n, p1_strategy, p2_strategy):
    p1_wins = 0
    p2_wins = 0
    ties = 0
    for _ in range(n):
        game = Blokus(board_dimensions, pieces, p1_strategy, p2_strategy)
        value = game.play_game()
        if value == 1:
            p1_wins += 1
        elif value == 2:
            p2_wins += 1
        else:
            ties += 1
    for _ in range(n):
        game = Blokus(board_dimensions, pieces, p2_strategy, p1_strategy)
        value = game.play_game()
        if value == 1:
            p2_wins += 1
        elif value == 2:
            p1_wins += 1
        else:
            ties += 1
    return p1_wins, p2_wins, ties

# Simulate games between strategies
def play_all_strategies(scores):
    strategies = list(scores.keys())

    # Play each pair of strategies
    for i in range(len(strategies)):
        for j in range(i + 1, len(strategies)):
            strat1 = strategies[i]
            strat2 = strategies[j]

            # Simulate games between the two strategies
            p1_wins, p2_wins, ties = play_games(5, strat1, strat2)

            # Update scores for strat1 (player 1)
            scores[strat1][0] += p1_wins  # Wins
            scores[strat1][1] += p2_wins  # Losses
            scores[strat1][2] += ties     # Ties

            # Update scores for strat2 (player 2)
            scores[strat2][0] += p2_wins  # Wins
            scores[strat2][1] += p1_wins  # Losses
            scores[strat2][2] += ties     # Ties
    


# if __name__ == "__main__":
#     scores = {
#         "random": [0, 0, 0],
#         "large": [0, 0, 0],
#         "corner": [0, 0, 0],
#         "combo": [0, 0, 0],
#         "minimax-large": [0, 0, 0],
#         "minimax-corner": [0, 0, 0],
#         "minimax-combo": [0, 0, 0]
#     }
    
#     play_all_strategies(scores)
    
#     # Display final scores
#     for strat, results in scores.items():
#         print(f"{strat}: Wins={results[0]}, Losses={results[1]}, Ties={results[2]}")
    
    

if __name__ == "__main__":
    game = Blokus(board_dimensions, pieces, "large", "combo")
    game.play_game()
    
    



    
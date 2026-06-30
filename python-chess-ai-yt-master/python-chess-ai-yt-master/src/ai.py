import copy

class MinimaxAI:

    PAWN_TABLE = [
    [0,   0,   0,   0,   0,   0,   0,   0],
    [5,   5,   5,   5,   5,   5,   5,   5],
    [10, 10, 10, 15, 15, 10, 10, 10],
    [15, 15, 20, 25, 25, 20, 15, 15],
    [20, 20, 25, 30, 30, 25, 20, 20],
    [30, 30, 35, 40, 40, 35, 30, 30],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [0,   0,   0,   0,   0,   0,   0,   0]
]
    KNIGHT_TABLE = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

    PIECE_VALUES = {
        "pawn": 100,
        "knight": 320,
        "bishop": 330,
        "rook": 500,
        "queen": 900,
        "king": 20000   

        
    }

    def __init__(self, depth=2):
        self.depth = depth

    # ADD THIS FUNCTION HERE
    def capture_score(self, move, attacker):

        if move.final.piece is None:
            return 0

        victim = move.final.piece

        return (
            self.PIECE_VALUES[victim.name] * 10
            - self.PIECE_VALUES[attacker.name]
        )


    def evaluate(self, board):
     score = 0

     for r in range(8):
            for c in range(8):

                square = board.squares[r][c]

                if square.has_piece():

                    piece = square.piece
                    value = self.PIECE_VALUES[piece.name]

                    # Knight bonus
                    if piece.name == "knight":
                        if piece.color == "white":
                            value += self.KNIGHT_TABLE[r][c]
                        else:
                            value += self.KNIGHT_TABLE[7-r][c]

                    # Pawn bonus
                    if piece.name == "pawn":
                        if piece.color == "white":
                            value += self.PAWN_TABLE[r][c]
                        else:
                            value += self.PAWN_TABLE[7-r][c]

                    if piece.color == "white":
                        score += value
                    else:
                        score -= value

            return score

    def get_all_moves(self, board, color):
        captures = []
        quiet_moves = []

        for r in range(8):
            for c in range(8):

                square = board.squares[r][c]

                if square.has_piece():
                    piece = square.piece

                    if piece.color == color:

                        piece.clear_moves()
                        board.calc_moves(piece, r, c, False)

                        for move in piece.moves:
                            if move.final.piece is not None:
                                score = self.capture_score(move, piece)
                                captures.append((score, piece, move))
                            else:
                                quiet_moves.append((piece, move))

        captures.sort(reverse=True, key=lambda x: x[0])

        ordered_moves = []

        for _, piece, move in captures:
            ordered_moves.append((piece, move))

        ordered_moves.extend(quiet_moves)

        return ordered_moves

    def minimax(self, board, depth, alpha, beta, maximizing):

        if depth == 0:
            return self.evaluate(board), None

        color = "white" if maximizing else "black"

        moves = self.get_all_moves(board, color)

        if len(moves) == 0:
            return self.evaluate(board), None

        if maximizing:

            maxEval = -999999
            bestMove = None

            for piece, move in moves:

                captured_piece, piece_moved_before, last_move_before = board.move(
                    piece,
                    move,
                    testing=True
                )

                evaluation, _ = self.minimax(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    False
                )

                board.undo_move(
                    piece,
                    move,
                    captured_piece,
                    piece_moved_before,
                    last_move_before
                )

                if evaluation > maxEval:
                    maxEval = evaluation
                    bestMove = (piece, move)

                alpha = max(alpha, evaluation)

                if beta <= alpha:
                    break

            return maxEval, bestMove

        else:

            minEval = 999999
            bestMove = None

            for piece, move in moves:

                captured_piece, piece_moved_before, last_move_before = board.move(
                    piece,
                    move,
                    testing=True
                )

                evaluation, _ = self.minimax(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    True
                )

                board.undo_move(
                    piece,
                    move,
                    captured_piece,
                    piece_moved_before,
                    last_move_before
                )

                if evaluation < minEval:
                    minEval = evaluation
                    bestMove = (piece, move)

                beta = min(beta, evaluation)

                if beta <= alpha:
                    break

            return minEval, bestMove

    def best_move(self, board):

        _, move = self.minimax(
            board,
            self.depth,
            -999999,
            999999,
            False      # Black AI
        )

        return move 
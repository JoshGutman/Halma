import math
import time
from board import Board

# 5:04 PM
class Minimax:

    def __init__(self, board, time_limit, alpha_beta):
        self.board = board
        self.time_limit = time_limit
        self.alpha_beta = alpha_beta
        self.depth_limit = 0
        self.max_team = None
        self.min_team = None
        self.minimum = 10000000000
        self.maximum = 0

    def score(self, board, team):
        score = 0

        def _distance(node1, node2):
            #return abs(node2.coords[0]-node1.coords[0]) + abs(node2.coords[1]-node1.coords[1])
            return math.sqrt((node1.coords[0]-node2.coords[0])**2 + (node1.coords[1]-node2.coords[1])**2)
        
        def _least_distance(node):
            if node.val == Board.GREEN:
                target = board.red_starts
            else:
                target = board.green_starts

            minimum = _distance(node, target[0])
            n = target[0]
            for t in target:
                pmin = _distance(node, t)
                if pmin < minimum:
                    minimum = pmin
                    n = t
            return (n, minimum)
            
            

        pieces = []

        for lst in board.board:
            for node in lst:
                if node.val == team:
                    pieces.append(node)

        for p in pieces:
            score += _least_distance(p)[1]

        return score




    def search(self, team):

        self.max_team = team
        if team == Board.RED:
            self.min_team = Board.GREEN
        else:
            self.min_team = Board.RED
            
        self.start_time = time.time()
        initial_moves = self.board.generate_moves(team)

        def id_search(board, team, start, end, depth):


            new_board = board.move_piece(start, end)
            score = self.score(new_board, team)

            if time.time() - self.start_time < self.time_limit and depth < self.depth_limit and new_board.check_win() == Board.EMPTY:
                new_board = board.move_piece(start, end)

                '''
                if team == self.max_team:
                    self.maximum = max(self.score(new_board, team), self.maximum)

                else:
                    self.minimum = min(self.score(new_board, team), self.minimum)
                '''

                
                
                if team == self.max_team:
                    new_moves = new_board.generate_moves(Board.GREEN)
                    for key in new_moves:
                        for value in new_moves[key]:
                            return (max(score, id_search(new_board, Board.GREEN, key.coords, value.coords, depth+1)), start, end)
                else:
                    new_moves = new_board.generate_moves(Board.RED)
                    for key in new_moves:
                        for value in new_moves[key]:
                            return (min(score, id_search(new_board, Board.RED, key.coords, value.coords, depth+1)), start, end)

            return (score, start, end)

            

        while time.time()-self.start_time < self.time_limit:
            for key in initial_moves:
                for value in initial_moves[key]:
                    return id_search(self.board, team, key.coords, value.coords, 0)
            self.depth_limit += 1
                
            
        
            

            


if __name__ == "__main__":
    b = Board(8)
    print("TEsting:")
    print(b)
    print("\n\n\n")
    m = Minimax(b, 6, None)
    score = m.search(Board.RED)
    print(score)
    start = score[1]
    end = score[2]
    new_board = b.move_piece(start, end)
    print(new_board)
    
    

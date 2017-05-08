import math
import time
from board import Board

# 5:04 PM
class Minimax:

    def __init__(self, time_limit, alpha_beta):
        self.time_limit = time_limit
        self.alpha_beta = alpha_beta
        self.depth_limit = 1
        self.max_team = None
        self.min_team = None
        self.minimum = 10000000000
        self.maximum = (0,0,0)

        self.move = None

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



    def test(self, board, team):
        self.start_time = time.time()
        x = self.search(board, team)
        return board.move_piece(x[0], x[1])


    def search(self, board, team):

        # Less points = better
        self.min_team = team
        if team == Board.RED:
            self.max_team = Board.GREEN
        else:
            self.max_team = Board.RED
            
        initial_moves = board.generate_moves(team)

        def id_search(board, team, start, end, depth):

            new_board = board.move_piece(start, end)
            score = self.score(new_board, team)

            if time.time() - self.start_time < self.time_limit and depth < self.depth_limit and new_board.check_win() == Board.EMPTY:
                
                if team == self.min_team:
                    new_moves = new_board.generate_moves(self.min_team)
                    for key in new_moves:
                        for value in new_moves[key]:
                            return (max(score, id_search(new_board, self.max_team, key.coords, value.coords, depth+1)[0]), start, end)
                else:
                    new_moves = new_board.generate_moves(self.max_team)
                    for key in new_moves:
                        for value in new_moves[key]:
                            return (min(score, id_search(new_board, self.min_team, key.coords, value.coords, depth+1)[0]), start, end)

            return (score, start, end)

            
        minimum = (1000000000,0,0)
        k = None
        v = None
        while time.time()-self.start_time < self.time_limit:
            for key in initial_moves:
                for value in initial_moves[key]:
                    score = id_search(board, team, key.coords, value.coords, 0)
                    if score[0] < minimum[0]:
                        minimum = score
                        k = key
                        v = value
            self.depth_limit += 1
                
        return k.coords,v.coords       
        
            

            


if __name__ == "__main__":
    b = Board(8)
    m = Minimax(.25, None)
    i = 0
    while b.check_win() == Board.EMPTY:
        if i % 2 == 0:
            team = Board.RED
        else:
            team = Board.GREEN
        b = m.test(b, team)
        i += 1
        print(b)
        print("\n")
    print(b)
    

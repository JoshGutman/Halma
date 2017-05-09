import math
import time
from board import Board

class Minimax:

    def __init__(self, time_limit, alpha_beta):
        self.time_limit = time_limit
        self.alpha_beta = alpha_beta
        self.depth_limit = 1
        self.max_team = None
        self.min_team = None
        self.count = 0


    # Judge points based off of distance away from opposite corner.
    # If the piece makes it to the other zone, that piece doesn not
    # add any points to the score
    def score(self, board, team):
        score = 0

        def _distance(node1, node2):
            #return abs(node2.coords[0]-node1.coords[0]) + abs(node2.coords[1]-node1.coords[1])
            return math.sqrt((node1.coords[0]-node2.coords[0])**2 + (node1.coords[1]-node2.coords[1])**2)

        '''
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
        ''' 
            

        pieces = []

        for lst in board.board:
            for node in lst:
                if node.val == team:
                    pieces.append(node)

        for p in pieces:
            '''
            if p.val == Board.RED and p.starting_position == Board.GREEN:
                pass
            elif p.val == Board.GREEN and p.starting_position == Board.RED:
                pass
            else:
                score += _least_distance(p)[1]
            '''

            if p.val == Board.RED and p.starting_position == Board.GREEN:
                pass
            elif p.val == Board.GREEN and p.starting_position == Board.RED:
                pass
            else:
                if team == Board.RED:
                    score += _distance(p, board.board[board.size-1][board.size-1])
                else:
                    score += _distance(p, board.board[0][0])
            

        return score



    def search(self, board, team):
        self.start_time = time.time()
        
        # Less points = better
        self.min_team = team
        if team == Board.RED:
            self.max_team = Board.GREEN
        else:
            self.max_team = Board.RED
            
        initial_moves = board.generate_moves(team)

        def id_search(board, team, start, end, depth):

            new_board = board.move_piece(start, end)
            self.count += 1
            score = self.score(new_board, self.min_team)

            if self.alpha_beta:
                if score > self.alpha and team == self.max_team:
                    return (score, start, end) 

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


        self.depth_limit = 1
        self.alpha = 100000000
        minimum = (1000000000,0,0)
        k = None
        v = None
        while time.time()-self.start_time < self.time_limit:
            for key in initial_moves:
                for value in initial_moves[key]:
                    score = id_search(board, team, key.coords, value.coords, 0)
                    if score[0] < minimum[0]:
                        minimum = score
                        self.alpha = minimum[0]
                        k = key
                        v = value
            self.depth_limit += 1

        return board.move_piece(k.coords, v.coords), k, v  
        
            

            


if __name__ == "__main__":
    b = Board(8)
    m = Minimax(.25, None)
    i = 0
    while b.check_win() == Board.EMPTY:
        if i % 2 == 0:
            team = Board.RED
        else:
            team = Board.GREEN
        b = m.search(b, team)[0]
        i += 1
        print(b)
        print("\n")
    print(b)
    

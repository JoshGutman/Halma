import math
import time
from board import Board

class Minimax:

    def __init__(self, board, time_limit, alpha_beta):
        self.board = board
        self.time_limit = time_limit
        self.alpha_beta = alpha_beta

    def score(self):
        red_score = 0
        green_score = 0

        def _distance(node1, node2):
            #return abs(node2.coords[0]-node1.coords[0]) + abs(node2.coords[1]-node1.coords[1])
            return math.sqrt((node1.coords[0]-node2.coords[0])**2 + (node1.coords[1]-node2.coords[1])**2)
        
        def _least_distance(node):
            if node.val == Board.GREEN:
                target = self.board.red_starts
            else:
                target = self.board.green_starts

            minimum = _distance(node, target[0])
            n = target[0]
            for t in target:
                pmin = _distance(node, t)
                if pmin < minimum:
                    minimum = pmin
                    n = t
            return (n, minimum)
            
            

        reds = []
        greens = []

        for lst in self.board.board:
            for node in lst:
                if node.val == Board.RED:
                    reds.append(node)
                elif node.val == Board.GREEN:
                    greens.append(node)

        for r in reds:
            red_score += _least_distance(r)[1]

        for g in greens:
            green_score += _least_distance(g)[1]

        return (red_score, green_score)


    def search(self):
        if self.start_time = time.time()

        def id_search(depth):
            if time.time() - start_time >= self.time_limit:
                return

            


if __name__ == "__main__":
    b = Board(8)
    m = Minimax(b, None, None)
    print(m.score())

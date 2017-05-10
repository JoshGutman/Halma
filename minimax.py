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


    def get_score(self, board):
        red_score = 0
        green_score = 0

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
            
            

        reds = []
        greens = []

        for lst in board.board:
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


    # Judge points based off of distance away from opposite corner.
    # If the piece makes it to the other zone, that piece does not
    # add any points to the score
    def score(self, board, team):
        score = 0

        def _distance(node1, node2):
            # the equation to determine the distance to corner
            return math.sqrt((node1.coords[0]-node2.coords[0])**2 + (node1.coords[1]-node2.coords[1])**2)

       
            

        pieces = []
        enemy_pieces = []

        # add the pieces relating to your team
        for lst in board.board:
            for node in lst:
                if node.val == team:
                    pieces.append(node)
                elif node.val != board.EMPTY:
                    enemy_pieces.append(node)


        for e in enemy_pieces:
            score += len(self._get_node_jumps(board, e))

        
        for p in pieces:

            # pieces in the goal do not have to be scored
            if p.val == Board.RED and p.starting_position == Board.GREEN:
                pass
            elif p.val == Board.GREEN and p.starting_position == Board.RED:
                pass

            # find the distance to the goal based on team color
            else:
                if team == Board.RED:
                    score += _distance(p, board.board[board.size-1][board.size-1])
                else:
                    score += _distance(p, board.board[0][0])
            

        return score



    # Call on enemy team
    def _get_node_jumps(self, board, node):

        def __get_jump_coords(start, end):
            val = (start[0]-end[0], start[1]-end[1])
            
            if val[0] < 0:
                x = val[0]-1
            elif val[0] == 0:
                x = 0
            else:
                x = val[0]+1

            if val[1] < 0:
                y = val[1]-1
            elif val[1] == 0:
                y = 0
            else:
                y = val[1]+1

            out = (start[0]-x,start[1]-y)

            if out[0] >= 0 and out[0] < board.size:
                if out[1] >= 0 and out[1] < board.size:
                    return out

            return None



        def _distance(node1, node2):
            # the equation to determine the distance to corner
            return math.sqrt((node1.coords[0]-node2.coords[0])**2 + (node1.coords[1]-node2.coords[1])**2)

        team = node.val
        jumps = []
        
        for n in node.neighbors:
            if n.val != Board.EMPTY and n.val != team:
                jump = __get_jump_coords(node.coords, n.coords)
                if jump is None:
                    continue
                else:
                    jump_node = board.board[jump[0]][jump[1]]
                    if team == Board.GREEN:
                        if _distance(jump_node, board.board[0][0]) < _distance(node, board.board[0][0]):
                            jumps.append(jump)
                    else:
                        if _distance(jump_node, board.board[board.size-1][board.size-1]) < _distance(node, board.board[board.size-1][board.size-1]):
                            jumps.append(jump)

        return jumps        
                    

        

    def search(self, board, team):
        self.start_time = time.time()
        
        # Less points = better

        # because better scores have less points the
        # player is the min team and the opponent
        # is the max team
        self.min_team = team
        if team == Board.RED:
            self.max_team = Board.GREEN
        else:
            self.max_team = Board.RED

        # generate the moves for your team 
        initial_moves = board.generate_moves(team)


        # an iterative depth first search
        def id_search(board, team, start, end, depth):

            # create a new board with the given move and score it
            new_board = board.move_piece(start, end)
            self.count += 1
            score = self.score(new_board, self.min_team)

            # alpha beta pruning
            if self.alpha_beta:
                if score > self.alpha and team == self.max_team:
                    return (score, start, end) 

            # as long as there is no winner and time limit is not reached find the min or max score based on team
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

        # for all possible moves find their score
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

        # return the board that was generated with the start and end coordinates
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
    

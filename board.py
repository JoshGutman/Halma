import sys

class Board:

    GREEN = "G"
    RED = "R"
    EMPTY = "X"

    def __init__(self, size):
        self.size = size
        self.new_game()

        


    # Initializes self.board, which is a 2D array of Node objects
    def new_game(self):
        self.board = []
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                self.board[i].append(Node(Board.EMPTY, (i,j)))

        for i in range(4):
            for j in range(4-i):
                self.board[i][self.size-j-1].val = Board.RED
                self.board[self.size-j-1][i].val = Board.GREEN

        # Find neighbors for each node
        for lst in self.board:
            for node in lst:
                coords = self._get_neighbors(node.coords, self.size)
                for c in coords:
                    node.neighbors.append(self.board[c[0]][c[1]])



    def checkWin(self):
        x = self.size//2
        green_count = 0
        red_count = 0
        for i in range(0, self.size//2):
            for j in range(x, self.size):
                if self.board[i][j].val == "G":
                    green_count += 1
            x += 1

        x = self.size//2
        for i in range(self.size-1, self.size//2-1, -1):
            for j in range(0, x):
                if self.board[i][j].val == "R":
                    red_count += 1
            x -= 1
        
        if green_count == 10:
            return "G"
        elif red_count == 10:
            return "R"
        else:
            return "F"

        for lst in self.board:
            for node in lst:
                coords = self._get_neighbors(node.coords, size)
                for c in coords:
                    node.neighbors.append(self.board[c[0]][c[1]])



    # Returns a dictionary where all 10 nodes of the specified color are keys,
    # and a list of every valid move for the key as values
    def generate_moves(self, color):
        moves = {}

        # Assign all pieces of team color as keys in moves dict
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].val == color:
                    moves[self.board[i][j]] = []


        def _check_jumps(node):
            for n in node.neighbors:
                if n.val != Board.EMPTY:
                    
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

                        if out[0] >= 0 and out[0] < self.size:
                            if out[1] >= 0 and out[1] < self.size:
                                return out

                        return None


                    possible = __get_jump_coords(node.coords, n.coords)
                    if possible is None:
                        continue

                    new_node = self.board[possible[0]][possible[1]]
                    if new_node.val == Board.EMPTY and new_node not in moves[move]:
                        moves[move].append(new_node)
                        _check_jumps(new_node)


        for move in moves:

            # Check for normal moves
            for n in move.neighbors:
                if n.val == Board.EMPTY:
                    moves[move].append(n)

            # Check for jumps
            _check_jumps(move)

        return moves
                        


    # Moves Node at coord1 to Node at coord2
    # Assertion error if node1 is equal to Board.EMPTY or if node2 is not equal to Board.EMPTY
    def move_piece(self, coord1, coord2):

        # Find the Nodes of coord1 and coord2
        for lst in self.board:
            for node in lst:
                if node.coords == coord1:
                    node1 = node
                elif node.coords == coord2:
                    node2 = node
                
        
        assert node1.val != Board.EMPTY
        assert node2.val == Board.EMPTY

        node2.val = node1.val
        node1.val = Board.EMPTY




    # Finds neighboring nodes
    def _get_neighbors(self, coords, size):

        # Returns list of all neighboring coordinates, regardless if they are valid
        def __potential_neighbors(coords):
            out = []
            out.append((coords[0], coords[1]-1))    # N
            out.append((coords[0]+1, coords[1]-1))  # NE
            out.append((coords[0]+1, coords[1]))    # E
            out.append((coords[0]+1, coords[1]+1))  # SE
            out.append((coords[0], coords[1]+1))    # S
            out.append((coords[0]-1, coords[1]+1))  # SW
            out.append((coords[0]-1, coords[1]))    # W
            out.append((coords[0]-1, coords[1]-1))  # NW

            return out
            
        out = []
        potentials = __potential_neighbors(coords)

        # Check the validity of each coord
        for coord in potentials:
            if coord[0] >= 0 and coord[0] < size and coord[1] >= 0 and coord[1] < size:
                out.append(coord)

        return out






class Node:

    def __init__(self, val, coords):
        self.val = val
        self.coords = coords
        self.neighbors = []

    def __str__(self):
        return self.val

    
    def __eq__(self, x):
        if x == self.coords:
            return True
        if type(x) is Node:
            if x.coords == self.coords:
                return True
        return False


    def __hash__(self):
        return hash(self.coords)

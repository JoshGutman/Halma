import sys

class Board:

    GREEN = "G"
    RED = "R"
    EMPTY = "X"

    def __init__(self, size, board_array=None):
        self.size = size
        self.green_starts = []
        self.red_starts = []

        if board_array == None:
            self.new_game()

        else:
            self.board = board_array
            for i in range(4):
                for j in range(4-i):

                    self.board[i][j].starting_position = Board.RED
                    self.red_starts.append(self.board[i][j])
                    
                    self.board[self.size-i-1][self.size-j-1].starting_position = Board.GREEN
                    self.green_starts.append(self.board[self.size-i-1][self.size-j-1])

            # Find neighbors for each node
            for lst in self.board:
                for node in lst:
                    coords = self._get_neighbors(node.coords, self.size)
                    for c in coords:
                        node.neighbors.append(self.board[c[0]][c[1]])
            
        


    # Initializes self.board, which is a 2D array of Node objects
    def new_game(self):
        self.board = []
        for i in range(self.size):
            self.board.append([])
            for j in range(self.size):
                self.board[i].append(Node(Board.EMPTY, (i,j)))


        for i in range(4):
            for j in range(4-i):
                self.board[i][j].val = Board.RED
                self.board[i][j].starting_position = Board.RED
                self.red_starts.append(self.board[i][j])
                
                self.board[self.size-i-1][self.size-j-1].val = Board.GREEN
                self.board[self.size-i-1][self.size-j-1].starting_position = Board.GREEN
                self.green_starts.append(self.board[self.size-i-1][self.size-j-1])


        # Find neighbors for each node
        for lst in self.board:
            for node in lst:
                coords = self._get_neighbors(node.coords, self.size)
                for c in coords:
                    node.neighbors.append(self.board[c[0]][c[1]])



    # Returns "G" for green win, "R" for red win, "X" for no win
    def check_win(self):
        greens = []
        reds = []
        
        for lst in self.board:
            for node in lst:
                if node.val == Board.GREEN:
                    greens.append(node)
                elif node.val == Board.RED:
                    reds.append(node)

        green_win = True
        red_win = True

        for g in greens:
            if g.starting_position != Board.RED:
                green_win = False
                break

        for r in reds:
            if r.starting_position != Board.GREEN:
                red_win = False
                break

        if green_win:
            return Board.GREEN

        if red_win:
            return Board.RED

        return Board.EMPTY


    # Returns a dictionary where all 10 nodes of the specified color are keys,
    # and a list of every valid move for the key as values
    def generate_moves(self, color):

        # Return True if move is valid -- checks to make sure piece isn't
        # going back into the its own starting position
        def _check_starting_position(node, new_node):
            if node.starting_position == node.val:
                return True
            elif new_node.starting_position == node.val:
                return False
            else:
                return True

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
                        if _check_starting_position(node, new_node) == True:
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

        #node2.val = node1.val
        #node1.val = Board.EMPTY

        copy = []
        for i in range(self.size):
            copy.append([])
            for j in range(self.size):
                copy[i].append(Node(self.board[i][j].val, self.board[i][j].coords))


        out = Board(self.size, copy)
        target = out.board[coord1[0]][coord1[1]].val
        out.board[coord1[0]][coord1[1]].val = Board.EMPTY
        out.board[coord2[0]][coord2[1]].val = target


        return out




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


    def __str__(self):
        out = ""
        for i in range(self.size):
            for j in range(self.size):
                out += str(self.board[i][j]) + " "
            out += "\n"
        return out






class Node:

    def __init__(self, val, coords):
        self.val = val
        self.coords = coords
        self.starting_position = Board.EMPTY
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


if __name__ == "__main__":
    b1 = Board(8)
    print(b1)
    

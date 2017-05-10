import tkinter as tk
#import threading
#import multiprocessing
import time
from board import *
from minimax import Minimax

class GUI:

    def __init__(self, size, time_limit=30):
        root = tk.Tk()
        root.wm_title("Halma")
        window = Window(size, time_limit, master=root)
        window.mainloop()
        self.size = size
        

class Window(tk.Frame):

    # If an 8x8 board is desired, size should be 8 (as opposed to 64)
    def __init__(self, size, time=30, master=None):

        assert size > 4
        super().__init__(master)
        self.master = master

        # Images for buttons
        self.image_size = "normal"
        self.red = tk.PhotoImage(file="images/red_{}.gif".format(self.image_size))
        self.green = tk.PhotoImage(file="images/green_{}.gif".format(self.image_size))
        self.background = tk.PhotoImage(file="images/background_{}.gif".format(self.image_size))
        self.highlight = tk.PhotoImage(file="images/highlight_{}.gif".format(self.image_size))
        self.hlred = tk.PhotoImage(file="images/hlred_{}.gif".format(self.image_size))
        self.hlgreen = tk.PhotoImage(file="images/hlgreen_{}.gif".format(self.image_size))

        # Used for moving a piece from one space to another
        self.move = False
        self.to_remove = []
        self.color = None

        self.size = size
        self.move_count = 0

        self.board = Board(size)
        self.only_allow_valid_moves = False

        self.time_limit = time
        self.current_time = time
        
        self.create_widgets()



    def create_widgets(self):

        # Status bar
        self.status = tk.Label(height=2, text="Welcome to Halma")
        self.status.pack()

        # Container that holds the buttons -> uses grid layout
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        # Create numbering and lettering for the board
        letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
                   'n','o','p','q','r','s','t','u','v','w','x','y','z']
        for i in range(self.size):
            temp_label = tk.Label(button_frame, text=str(self.size-i))
            temp_label.grid(row=i,column=0)

            temp_label = tk.Label(button_frame, text=letters[i])
            temp_label.grid(row=self.size, column=i+1)
        

        # Create and store all buttons in self.buttons
        self.buttons = []
        for i in range(self.size):
            to_append = []    
            for j in range(self.size):
                temp_button = tk.Button(button_frame, image=self.background, command=lambda x=i, y=j: self.action(x,y))
                temp_button.image = self.background
                temp_button.config(height=64,width=64)
                temp_button.grid(row=i,column=j+1)
                to_append.append(temp_button) 
            self.buttons.append(to_append)


        # Add a menubar
        self.menubar = tk.Menu(self.master, tearoff=False)
        self.gamemenu = tk.Menu(self.menubar, tearoff=False)
        
        # Add New Game button to the menubar
        self.gamemenu.add_command(label="New game", command=self.new_game)

        # Valid moves only button
        self.gamemenu.add_radiobutton(label="Valid moves only", command=self.toggle_valid_moves)

        # Add Size submenu to menubar
        self.sizemenu = tk.Menu(self.gamemenu, tearoff=False)
        self.sizemenu.add_radiobutton(label="Normal", command=lambda: self.change_size("normal"))
        self.sizemenu.add_radiobutton(label="Small", command=lambda: self.change_size("small"))
        
        # Attach sizemenu to gamemenu and gamemenu to menubar
        self.gamemenu.add_cascade(label="Size", menu=self.sizemenu)
        self.menubar.add_cascade(label="Menu", menu=self.gamemenu)

        self.gamemenu.add_separator()

        # Add Quit button to the menubar
        self.gamemenu.add_command(label="Quit", command=self.master.destroy)
        
        self.master.config(menu=self.menubar)


        self.aimenu = tk.Menu(self.menubar, tearoff=False)
        self.aimenu.add_command(label="AI vs. AI", command=self.ai_vs_ai)
        #self.aimenu.add_command(label="AI vs. Human", command=lambda:print(test))
        self.ai_select = tk.Menu(self.aimenu, tearoff=False)
        self.ai_select.add_command(label="AI is team RED", command=lambda:self.ai_vs_human(Board.RED))
        self.ai_select.add_command(label="AI is team GREEN", command=lambda:self.ai_vs_human(Board.GREEN))
        self.aimenu.add_cascade(label="AI vs. Human", menu=self.ai_select)
        self.menubar.add_cascade(label="AI", menu=self.aimenu)
        self.aimenu.add_command(label="Get AI move count", command=self.get_move_count)
        self.aimenu.add_command(label="Get score", command=self.get_score)

        self.new_game()


    # This method is run when a button is clicked
    def action(self, i, j):

        
        # Takes in (i,j) and returns "letter-number"
        def _notation(coords):
            return chr(coords[1]+97) + str(-1*coords[0]+self.size)

        
        # Second click in move operation
        if self.move == True:

            x = self.to_remove[0]
            y = self.to_remove[1]

            if self.only_allow_valid_moves:
                moves = self.board.generate_moves(self.board.board[x][y].val)
                if (i,j) not in moves[self.board.board[x][y]]:
                    self.status.config(text="Invalid move.")
                    self.buttons[x][y].config(relief=tk.RAISED)
                    self.move = False
                    return
        
            if (i,j) != (x,y):

                # Remove any old highlighting from the board
                for lst in self.buttons:
                    for button in lst:
                        if button.image == self.hlred:
                            button.config(image=self.red)
                            button.image = self.red
                        elif button.image == self.hlgreen:
                            button.config(image=self.green)
                            button.image = self.green
                        elif button.image == self.highlight:
                            button.config(image=self.background)
                            button.image = self.background
                
                # Add piece to destination
                if self.color == self.red or self.color == self.hlred:
                    self.buttons[i][j].config(image=self.hlred)
                    self.buttons[i][j].image = self.hlred
                elif self.color == self.green or self.color == self.hlgreen:
                    self.buttons[i][j].config(image=self.hlgreen)
                    self.buttons[i][j].image = self.hlgreen

                # Remove piece from source
                self.buttons[x][y].config(image=self.highlight)
                self.buttons[x][y].image = self.highlight

                # Update status
                self.status.config(text="Moved piece from  {}  to  {}".format(_notation((x,y)),_notation((i,j))))
                
                self.move_count += 1
                self.board = self.board.move_piece((x,y), (i,j))

                # check to see if the game is won
                win = self.board.check_win()
                if win == "R":
                    self.status.config(text="Red Player Has Won!!!!!!!!!!!!!!!!!")
                elif win == "G":
                    self.status.config(text="Green Player Has Won!!!!!!!!!!!!!!!!!")

            else:
                self.status.config(text="Move cancelled")


            self.buttons[x][y].config(relief=tk.RAISED)
            self.move = False
            

        # First click in move operation
        elif self.board.board[i][j].val != Board.EMPTY:

            # Save necessary information for second click
            self.move = True
            self.to_remove = [i,j]
            self.color = self.buttons[i][j].image

            # Update status and give clicked button a sunken effect
            self.status.config(text="Moving piece at  {} ...".format(_notation((i,j))))
            self.buttons[i][j].config(relief=tk.SUNKEN) 

        
        # Click on empty space
        elif self.board.board[i][j].val == Board.EMPTY:
            pass


    # Creates red and green circles in the top right and bottom left corners respectively
    # Run when the "New game" menubar button is pressed
    def new_game(self):

        
        # Get rid of any other circles on the board
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(image=self.background)
                self.buttons[i][j].image = self.background
                

        # Place red and green circles
        for i in range(4):
            for j in range(4-i):
                self.buttons[i][j].config(image=self.red)
                self.buttons[i][j].image = self.red

                self.buttons[self.size-i-1][self.size-j-1].config(image=self.green)
                self.buttons[self.size-i-1][self.size-j-1].image = self.green
        

        # Update status bar
        self.status.config(text="New game started")

        self.move_count = 0
        self.board.new_game()



    # Changes the size of the board -> 2 sizes: small (48x48 tiles)
    # and normal (64x64 tiles). Called by the sizemenu commands
    def change_size(self, size):
        self.image_size = size
        
        for lst in self.buttons:
            for button in lst:
                if size == "small":
                    button.config(height=48)
                    button.config(width=48)
                elif size == "normal":
                    button.config(height=64)
                    button.config(width=64)

        
        self.master.update()


    def toggle_valid_moves(self):
        self.only_allow_valid_moves = not self.only_allow_valid_moves



    def ai_vs_ai(self):
        m = Minimax(self.time_limit, True)
        i = 0
        while self.board.check_win() == Board.EMPTY:
            if i % 2 == 0:
                team = Board.GREEN
            else:
                team = Board.RED
            self.board = m.search(self.board, team)[0]
            i += 1
            self.display_board(self.board)
            self.master.update()

    def display_board(self, board):
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j].val == Board.RED:
                    color = self.red
                elif board.board[i][j].val == Board.GREEN:
                    color = self.green
                else:
                    color = self.background
                self.buttons[i][j].config(image=color)
                self.buttons[i][j].image = color


    def ai_vs_human(self, team):
        self.menubar.add_command(label="AI Go", command=self.ai_move)
        self.ai_team = team
        self.only_allow_valid_moves = True
        # AI time limit defined here
        self.m = Minimax(self.time_limit, True)
        self.master.update()


    def ai_move(self):
        self.current_time = self.time_limit
        self.status.config(text="AI is thinking...")
        self.master.update()
        #p = multiprocessing.Pool(1)
        #p.apply_async(self.timer)
        #threading.Thread(target=self.timer())
        #self.timer()
        #self.timer(True)
        result = self.m.search(self.board, self.ai_team)
        self.board = self.board.move_piece(result[1].coords, result[2].coords)

        self.display_board(self.board)


        # Takes in (i,j) and returns "letter-number"
        def _notation(coords):
            return chr(coords[1]+97) + str(-1*coords[0]+self.size)

        # Sorry...
        self.buttons[result[1].coords[0]][result[1].coords[1]].config(image=self.highlight)
        self.buttons[result[1].coords[0]][result[1].coords[1]].image = self.highlight
        if self.ai_team == Board.RED:
            self.buttons[result[2].coords[0]][result[2].coords[1]].config(image=self.hlred)
            self.buttons[result[2].coords[0]][result[2].coords[1]].image = self.hlred
        else:
            self.buttons[result[2].coords[0]][result[2].coords[1]].config(image=self.hlgreen)
            self.buttons[result[2].coords[0]][result[2].coords[1]].image = self.hlgreen

        self.status.config(text="Moved piece at {} to {}".format(_notation(result[1].coords), _notation(result[2].coords)))
        


    def get_move_count(self):
        try:
            print(self.m.count)
        except:
            pass

    def get_score(self):
        try:
            print("Red Score: {}".format(self.m.get_score(self.board)[0]))
            print("Green Score: {}".format(self.m.get_score(self.board)[1]))
        except:
            pass


    '''
    def timer(self):
        if self.current_time > 0:
            self.status.config(text="AI is thinking... Time: {}".format(self.current_time))
            self.master.update()
            self.current_time -= 1
            self.master.after(1000, self.timer)
        else:
            self.status.config(text="Time up!")
    '''

    '''
    def timer(self, start):
        if start:
            self.new_window = tk.Toplevel(self.master)
            self.time_label = tk.Label(self.new_window, text="{}".format(self.current_time))
            self.time_label.pack()
            self.current_time -= 1

        else:
            self.time_label.config(text="{}".format(self.current_time))
            self.current_time -= 1
            if self.current_time > 0:
                self.new_window.after(1000, self.timer, False)
            else:
                self.new_window.destroy()
    '''

    '''
    def timer(self):
        while self.current_time > 0:
            self.status.config(text="AI is thinking... Time: {}".format(self.current_time))
            self.master.update()
            self.current_time -= 1
            time.sleep(1)

        self.status.config(text="Time up!")
    '''
    


if __name__ == "__main__":
    if len(sys.argv) == 3:
        time_limit = int(sys.argv[2])
    else:
        time_limit = 30
    if len(sys.argv) == 2:           
        size = int(sys.argv[1])
        if size == 8 or size == 10 or size == 16:
            GUI(size, time_limit)
        else:
            GUI(8, time_limit)
    else:
        GUI(8, time_limit)



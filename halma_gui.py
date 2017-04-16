import tkinter as tk
import sys


class Board(tk.Frame):

    # If an 8x8 board is desired, size should be 8 (as opposed to 64)
    def __init__(self, size, master=None):

        if size < 4:
            print("Size too small. Program exiting...")
            sys.exit()
        
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

        # Add Size submenu to menubar
        self.sizemenu = tk.Menu(self.gamemenu, tearoff=False)
        self.sizemenu.add_radiobutton(label="Normal", command=lambda: self.change_size("normal"))
        self.sizemenu.add_radiobutton(label="Small", command=lambda: self.change_size("small"))
        
        # Attach sizemenu to gamemenu and gamemenu to menubar
        self.gamemenu.add_cascade(label="Size", menu=self.sizemenu)
        self.menubar.add_cascade(label="Game", menu=self.gamemenu)

        self.gamemenu.add_separator()

        # Add Quit button to the menubar
        self.gamemenu.add_command(label="Quit", command=root.destroy)
        
        self.master.config(menu=self.menubar)


    # This method is run when a button is clicked
    def action(self, i, j):

        # Takes in (i,j) and returns "letter-number"
        def _notation(coords):
            return chr(coords[1]+97) + "-" + str(-1*coords[0]+self.size)
        
        # Second click in move operation
        if self.move == True:

            x = self.to_remove[0]
            y = self.to_remove[1]
        
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

            else:
                self.status.config(text="Move cancelled")


            self.buttons[x][y].config(relief=tk.RAISED)
            self.move = False
            

        # First click in move operation
        elif self.buttons[i][j].image != self.background:        

            # Save necessary information for second click
            self.move = True
            self.to_remove = [i,j]
            self.color = self.buttons[i][j].image

            # Update status and give clicked button a sunken effect
            self.status.config(text="Moving piece at  {} ...".format(_notation((i,j))))
            self.buttons[i][j].config(relief=tk.SUNKEN) 

        
        # Click on empty space
        elif self.buttons[i][j].image == self.background:
            if self.move_count % 2 == 0:
                self.buttons[i][j].config(image=self.green)
                self.buttons[i][j].image = self.green
            else:
                self.buttons[i][j].config(image=self.red)
                self.buttons[i][j].image = self.red
            self.move_count += 1


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
                self.buttons[i][self.size-j-1].config(image=self.red)
                self.buttons[i][self.size-j-1].image = self.red

                self.buttons[self.size-j-1][i].config(image=self.green)
                self.buttons[self.size-j-1][i].image = self.green

        # Update status bar
        self.status.config(text="New game started")

        self.move_count = 0



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
        


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Halma")
    board = Board(8, master=root)
    board.mainloop()

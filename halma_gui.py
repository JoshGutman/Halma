import tkinter as tk
import sys

class Board(tk.Frame):

    # If an 8x8 board is desired, size should equal 8 (as opposed to 64)
    def __init__(self, size, master=None):

        if size < 4:
            print("Size too small. Program exiting...")
            sys.exit()
        
        super().__init__(master)
        self.size = size
        self.master = master

        # Images for buttons
        self.red = tk.PhotoImage(file="images/red.gif")
        self.green = tk.PhotoImage(file="images/green.gif")
        self.background = tk.PhotoImage(file="images/background.gif")

        # Used for moving a piece from one space to another
        self.move = False
        self.to_remove = []
        self.color = None
        
        self.create_widgets()



    def create_widgets(self):

        # Status bar
        self.status = tk.Label(height=2, text="New game created...", )
        self.status.pack()

        # Container that holds the buttons -> uses grid layout
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        # Create and store all buttons in self.buttons
        self.buttons = []
        for i in range(self.size):
            to_append = []
            
            for j in range(self.size):
                temp_button = tk.Button(button_frame, image=self.background, command=lambda x=i, y=j: self.action(x,y))
                temp_button.image = self.background
                temp_button.config(height=64,width=64)
                temp_button.grid(row=i,column=j)
                to_append.append(temp_button)
                
            self.buttons.append(to_append)


        # Add a menubar
        self.menubar = tk.Menu(self.master)
        # Add New Game and Quit buttons to the menubar
        self.menubar.add_command(label="New game", command=self.new_game)
        self.menubar.add_command(label="Quit", command=root.destroy)
        self.master.config(menu=self.menubar)


    # This method is run when a button is clicked
    def action(self, i, j):
        
        # Second click in move operation
        if self.move == True:
            
            # Add piece to destination
            self.buttons[i][j].config(image=self.color)
            self.buttons[i][j].image = self.color

            # Remove piece from source
            x = self.to_remove[0]
            y = self.to_remove[1]
            self.buttons[x][y].config(image=self.background)
            self.buttons[x][y].image = self.background

            # Update status and remove sunken effect on source button
            self.status.config(text="Moved piece from {},{} to {},{}".format(x,y,i,j))
            self.buttons[x][y].config(relief=tk.RAISED)

            self.move = False


        # First click in move operation
        elif self.buttons[i][j].image != self.background:

            # Save necessary information for second click
            self.move = True
            self.to_remove = [i,j]
            self.color = self.buttons[i][j].image

            # Update status and give clicked button a sunken effect
            self.status.config(text="Moving piece at {},{}...".format(i,j))
            self.buttons[i][j].config(relief=tk.SUNKEN)
     
        
        # Click on empty space
        elif self.buttons[i][j].image == self.background:
            self.buttons[i][j].config(image=self.green)
            self.buttons[i][j].image = self.green



    # Creates red and green circles in the top right and bottom left corners respectively
    # Run when the "New game" menubar button is pressed
    def new_game(self):

        tiles_to_keep = []

        # Place red and green circles
        for i in range(4):
            for j in range(4-i):
                self.buttons[i][self.size-j-1].config(image=self.red)
                self.buttons[i][self.size-j-1].image = self.red
                tiles_to_keep.append((i,self.size-j-1))

                self.buttons[self.size-j-1][i].config(image=self.green)
                self.buttons[self.size-j-1][i].image = self.green
                tiles_to_keep.append((self.size-j-1,i))

        # Get rid of any other circles on the board
        for i in range(self.size):
            for j in range(self.size):
                if (i,j) not in tiles_to_keep:
                    self.buttons[i][j].config(image=self.background)
                    self.buttons[i][j].image = self.background


if __name__ == "__main__":
    root = tk.Tk()
    board = Board(8, master=root)
    board.mainloop()

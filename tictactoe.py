from tkinter import *
from ai import *
import threading
import time
import random
'''
class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("hi there, everyone!")

root = Tk()

app = App(root)

def callback(event):
    print("clicked at", event.x, event.y)

frame = Frame(root, width=100, height=100)
frame.bind("<Button-1>", callback)
frame.pack()

root.mainloop()
root.destroy() # optional; see description below
'''
player = 1
gamestate = [[None]*3 for _ in range(3)]
gameon = 1

def checkend(gamestate, id,p, c):
    gamestate[int((id-1)/3)][(id%3)-1].destroy()
    gamestate[int((id-1)/3)][(id%3)-1] = p
    w_player = -1
    w_state = None
    if gamestate[0][0]==gamestate[0][1] and gamestate[0][1] == gamestate[0][2]:
        w_player = gamestate[0][0]
        w_state = [(0,0),(0,1),(0,2)]
    elif gamestate[1][0]==gamestate[1][1] and gamestate[1][1] == gamestate[1][2]:
        w_player = gamestate[1][0]
        w_state = [(1,0),(1,1),(1,2)]
    elif gamestate[2][0]==gamestate[2][1] and gamestate[2][1] == gamestate[2][2]:
        w_player = gamestate[2][0]
        w_state = [(2,0),(2,1),(2,2)]
    elif gamestate[0][0]==gamestate[1][0] and gamestate[1][0] == gamestate[2][0]:
        w_player = gamestate[0][0]
        w_state = [(0,0),(1,0),(2,0)]
    elif gamestate[0][1]==gamestate[1][1] and gamestate[1][1] == gamestate[2][1]:
        w_player = gamestate[0][1]
        w_state = [(0,1),(1,1),(2,1)]
    elif gamestate[0][2]==gamestate[1][2] and gamestate[1][2] == gamestate[2][2]:
        w_player = gamestate[0][2]
        w_state = [(0,2),(1,2),(2,2)]
    elif gamestate[0][0]==gamestate[1][1] and gamestate[1][1] == gamestate[2][2]:
        w_player = gamestate[0][0]
        w_state = [(0,0),(1,1),(2,2)]
    elif gamestate[0][2]==gamestate[1][1] and gamestate[1][1] == gamestate[2][0]:
        w_player = gamestate[0][2]
        w_state = [(0,2),(1,1),(2,0)]
    done = 1
    for i in range(len(gamestate)):
        for j in range(len(gamestate[0])):
            if type(gamestate[i][j]) == B:
                done = 0
    if w_player != -1 or done == 1:
        endgame(gamestate, c, w_player, w_state)


def endgame(gamestate,c,w_player,w_state):
    global gameon
    if w_player == -1:
        print("Tie!")
    else:
        for i in range(len(gamestate)):
            for j in range(len(gamestate[0])):
                if type(gamestate[i][j]) == B:
                    gamestate[i][j].config(state=DISABLED,background = "#D3D3D3", relief = SUNKEN)
        c.create_line(w_state[0][1]*100+50,w_state[0][0]*100+50,w_state[2][1]*100+50,w_state[2][0]*100+50, width=5, fill="#228B22")
        print("Player {0} Won!".format(w_player))
    gameon = 0



class B(Button):

    def __init__(self,master,state,id,text=None,position=None):
        super().__init__(master=master,command=self.switch_state,text=text)
        self.state = state
        self.id = id
        self.position = position

    def switch_state(self):
        global player, gamestate
        self.state = "X" if player == 1 else "O"
        self.master.create_text(self.position[0],self.position[1],text=self.state, font=("Arial", 44), fill="#B22222" if player==1 else "black")
        print("Player {0}: placed an {1} at grid {2}".format(player, self.state, self.id))
        currp = player
        player = 2 if player == 1 else 1
        checkend(gamestate,int(self.id),currp, self.master)

def makeButton(c,position,state,id,width,height,gameindex):
    #global gamestate
    gamestate[gameindex[0]][gameindex[1]] = B(master=c,state=state,id=id,text=state,position = position)
    c.create_window(position,window=gamestate[gameindex[0]][gameindex[1]],width=width,height=height)

class App(threading.Thread):
    def __init__(self):
        super().__init__()
        self.start()

    def end(self):
        global gameon
        gameon = 0
        self.root.quit()

    def run(self):
        self.root = Tk()

        self.root.protocol("WM_DELETE_WINDOW", self.end)

        self.w = Canvas(self.root, width=300, height=300)
        self.w.pack()

        self.w.create_line(100, 0, 100, 300,fill="blue")
        self.w.create_line(200, 0, 200, 300,fill="blue")
        self.w.create_line(0, 100, 300, 100,fill="blue")
        self.w.create_line(0, 200, 300, 200,fill="blue")

        for j in range(3):  #j is vertical
            for i in range(3):  #i is horizontal
                makeButton(self.w,(100*i + 50, 100*j + 50), None, str(i + 3*j + 1), 60, 60,(j,i))

        #makeButton(w,(50,50),"X","1",60,60)

        '''Label(master, text="First").grid(row=0)
        Label(master, text="Second").grid(row=1)
        Label(master, text="Third").grid(row=1)


        def c():
            print("hi")
        b1 = Button(w,command=c)
        b2 = Button(w,command=c)
        b3 = Button(w,command=c)

        b1.grid(row=0, column=0,sticky="E")
        b2.grid(row=0, column=1)
        b3.grid(row=0, column=2)
        print(w.grid_size())
        #e2.grid(row=1, column=1)
        #e3.grid(row=1,column=2)
        '''
        self.root.mainloop()

app = App()

opponent = Ai()
player = random.randint(1,2)
if player == 1:
    print("Player {0}'s turn".format(1))
while gameon:
    if player == 2:
        print("Player {0}'s turn".format(2))
        opponent.test+=1
        time.sleep(0.15)
        opponent.makeMove(gamestate, gameon)
        opponent.test+=1
        if gameon:
            print("Player {0}'s turn".format(1))

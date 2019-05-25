class Ai():
    def __init__(self):
        self.win = 30
        self.loss = -100
        self.draw = 10
        self.test = 1
    def makeMove(self, gamestate, gameon):
        if not gameon:
            return
        cp = [[None]*3 for _ in range(3)]
        for i in range(0,len(cp)):
            for j in range(0,len(cp[0])):
                if type(gamestate[i][j]) != int:
                    cp[i][j] = None
                else:
                    cp[i][j] = gamestate[i][j]
        bs, bp = self.bestMove(cp, 0, True)
        #print(bp)
        if cp[1][1] == None:
            gamestate[1][1].switch_state()
        else:
            gamestate[bp[0]][bp[1]].switch_state()


    def bestMove(self, state, depth, player):
        if (state[0][0]==state[0][1] and state[0][1] == state[0][2] and state[0][2]!=None) or \
            (state[1][0]==state[1][1] and state[1][1] == state[1][2] and state[1][2]!=None) or \
            (state[2][0]==state[2][1] and state[2][1] == state[2][2] and state[2][2]!=None) or \
            (state[0][0]==state[1][0] and state[1][0] == state[2][0] and state[2][0]!=None) or \
            (state[0][1]==state[1][1] and state[1][1] == state[2][1] and state[2][1]!=None) or \
            (state[0][2]==state[1][2] and state[1][2] == state[2][2] and state[2][2]!=None) or \
            (state[0][0]==state[1][1] and state[1][1] == state[2][2] and state[2][2]!=None) or \
            (state[0][2]==state[1][1] and state[1][1] == state[2][0] and state[2][0]!=None):
            if not player:
                return self.win - depth, None
            else:
                return self.loss + depth, None
        over = 1
        for i in range(0,len(state)):
            for j in range(0,len(state[0])):
                if state[i][j] == None:
                    over = 0
        if over == 1:
            return self.draw-depth, None
        bestpos = (None, None)
        bestscore = -float("inf") if player else float("inf")
        for i in range(0,len(state)):
            for j in range(0,len(state[0])):
                if state[i][j] == None:
                    state[i][j] = 2 if player else 1
                    s, p = self.bestMove(state, depth+1, not player)
                    temp = max(s, bestscore) if player else min(s, bestscore)
                    #if depth == 0:
                    #    print("\n")
                    #if self.test==6:
                    #    print(self.bestMove(state, depth+1, not player),i,j,depth, player)
                    if temp != bestscore:
                        bestpos = (i,j)
                        bestscore = temp
                    state[i][j] = None
        return bestscore, bestpos

"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    if terminal(board=board):
        return None
    
    emptycount = 0
    for r in board:
        emptycount += r.count(EMPTY)
    
    if emptycount % 2 == 0:
        return O
    else:
        return X


def actions(board):
    a = []

    for i,r in enumerate(board):
        for j,c in enumerate(r):
            if c is not EMPTY:
                a.append((i,j))

    return a

def result(board, action):
    board[action[0]][action[1]] = player(board=board)
    return board

def winner(board):

    inrow = 0

    #Horizontal rows for X
    for i in range(3):
        inrow = 0
        for j in range(3):
            if board[i][j] == X:
                inrow += 1
        if inrow == 3:
            return X

    #Horizontal rows for O
    for i in range(3):
        inrow = 0
        for j in range(3):
            if board[i][j] == O:
                inrow += 1
        if inrow == 3:
            return O

    #Vertical Columns for X
    for i in range(3):
        inrow = 0
        for j in range(3):
            if board[j][i] == X:
                inrow += 1
        if inrow == 3:
            return X

    #Vertical Columns for O
    for i in range(3):
        inrow = 0
        for j in range(3):
            if board[j][i] == O:
                inrow += 1
        if inrow == 3:
            return O
    
    #Right diagonal for X
    inrow = 0
    for i in range(3):
        if board[i][i] == X:
            inrow += 1
        if inrow == 3:
            return X
    
    #Right diagonal for O
    inrow = 0
    for i in range(3):
        if board[i][i] == O:
            inrow += 1
        if inrow == 3:
            return O
    
    #Left diagonal for X
    inrow = 0
    for i in range(3):
        if board[i][2-i] == X:
            inrow += 1
        if inrow == 3:
            return X
        
    #Left diagonal for O
    inrow = 0
    for i in range(3):
        if board[i][2-i] == O:
            inrow += 1
        if inrow == 3:
            return O
        
    return None
    

def terminal(board):
    if actions(board=board) is None or winner(board=board) is not None:
        return True
    else:
        return False


def utility(board):
    if winner(board=board) == X:
        return 1
    elif winner(board=board) == O:
        return -1
    else:
        return 0

def mm(board):
    if terminal(board=board):
        return utility(board=board)
    
    ac = actions(board=board)
    if player(board=board) == X:
        return max(mm(result(board=board,action=a)) for a in ac) 

    

    if player(board=board) == O:
        return min(mm(result(board=board,action=a)) for a in ac) 
        


def minimax(board):
    if terminal(board=board):
        return None
    

    ac = actions(board=board)
    if player(board=board) == X:
        u = 0
        i=0
        j=0
        for a in ac:
            if u >= mm(result(board=board,action=a)):
                u =  mm(result(board=board,action=a))
                i = a[0]
                j = a[1]
        return (i,j)
    
    if player(board=board) == O:
        u = 0
        i=0
        j=0
        for a in ac:
            if u <= mm(result(board=board,action=a)):
                u =  mm(result(board=board,action=a))
                i = a[0]
                j = a[1]
        return (i,j)



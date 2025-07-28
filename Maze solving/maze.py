from PIL import Image,ImageDraw
        
import sys

class Node():
    def __init__(self,state,parent,action):
        self.state = state
        self.parent = parent
        self.action = action

class Frontier():
    def __init__(self,algorithm):
        self.frontier = []
        self.alg = algorithm

    def add(self,node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0
    
    def remove(self):
        if self.empty():
            raise Exception("Empty Frontier")
        else:
            if self.alg == 'DFS':
                node = self.frontier[-1]
                self.frontier = self.frontier[:-1]
                return node
            elif self.alg == 'BFS':
                node = self.frontier[0]
                self.frontier = self.frontier[1:]
                return node

class Maze():
    def __init__(self,filename,algorithm):
        with open(filename) as f:
            contents = f.read()

        self.alg = algorithm
        self.num_explored = 0
        self.distance = 0

        if contents.count('A') != 1:
            raise Exception('Only one start point shd be present')
        if contents.count('B') != 1:
            raise Exception('Only one end point shd be present')
        
        contents = contents.splitlines()
        self.length = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []

        for i in range(self.length):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == 'A':
                        self.start = (i,j)
                        row.append(False)
                    elif contents[i][j] == 'B':
                        self.goal = (i,j)
                        row.append(False)
                    elif contents[i][j] == ' ':
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)

            self.walls.append(row)
        
        self.solution = None

    def print(self):
        
        print()
        print('number of explored states : ',self.num_explored)
        
        sol = self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print('#',end='')
                elif (i,j) == self.start:
                    print('A',end='')
                elif (i,j) == self.goal:
                    print('B',end='')
                elif sol is not None and (i,j) in sol:
                    ind = sol.index((i,j))
                    act = self.solution[0]
                    if act[ind] == 'up':
                        print('^',end='')
                    elif act[ind] == 'down':
                        print('v',end='')
                    elif act[ind] == 'left':
                        print('<',end='')
                    else:
                        print('>',end='')

                else:
                    print(' ',end='')
            print()
        print()

    def neighbours(self,state):
        row,col = state

        candidates = [
            ('up',(row-1,col)),
            ('down',(row+1,col)),
            ('left',(row,col-1)),
            ('right',(row,col+1))
        ]

        result = []

        for action,(r,c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action,(r,c)))
            except IndexError:
                continue
        return result
    
    def solve(self):
        
        start = Node(state = self.start, parent = None, action= None)
        frontier = Frontier(algorithm= self.alg)
        frontier.add(node=start)

        self.explored = set()

        while True:

            if frontier.empty():
                raise Exception('no solutions found')
            
            node = frontier.remove()
            self.num_explored += 1

            if  node.state == self.goal:
                actions = []
                cells = []

                while node.parent is not None:
                    actions.append(node.parent.action)
                    cells.append(node.parent.state)
                    node = node.parent
                    self.distance += 1
                actions.reverse()
                cells.reverse()

                self.solution = (actions,cells)
                return
            
            self.explored.add(node.state)

            for action, state in self.neighbours(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state= state, parent= node, action= action)
                    frontier.add(child)


    def output_image(self,filename,show_solution = True,show_explored = False):
        cell_size = 50
        cell_border = 2

        img = Image.new("RGBA",(self.width * cell_size, self.length * cell_size),"black")
        draw = ImageDraw.Draw(img)

        sol = self.solution[1] if self.solution is not None else None
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    fill = (40,40,40)
                elif (i,j) == self.start:
                    fill = (255,0,0)
                elif (i,j) == self.goal:
                    fill = (0,171,28)
                elif sol is not None and show_solution and (i,j) in sol:
                    fill = (220,235,113)
                elif sol is not None and show_explored and (i,j) in sol:
                    fill = (212,97,85)
                else:
                    fill = (235,240,252)

                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_border + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                      fill = fill
                )
        img.save(filename)

if len(sys.argv) != 3:
    sys.exit("Usage : python maze.py 'maze file name' algorithm")

m = Maze(sys.argv[1],sys.argv[2])
m.print()
m.solve()
m.print()
m.output_image("maze.png", show_explored=True)

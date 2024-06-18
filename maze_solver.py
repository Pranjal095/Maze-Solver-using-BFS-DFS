class Node:
    def __init__(self,row,col,parent,action):
        self.row = row
        self.col = col
        self.parent = parent
        self.action = action

class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add_node(self,node):
        self.frontier.append(node)

    def is_contained(self,row,col):
        return any(node.row == row and node.col == col for node in self.frontier)
    
    def is_empty(self):
        return len(self.frontier) == 0
    
    def remove_node(self):
        if(self.is_empty()):
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
class QueueFrontier(StackFrontier):
    def remove_node(self):
        if(self.is_empty()):
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
class Maze:
    def __init__(self,filename):
        with open(filename) as input_file:
            contents=input_file.read()

        if(contents.count('A')!=1):
            raise Exception("Number of initial states should be one")
        
        if(contents.count('B')!=1):
            raise Exception("Number of goal states should be one") 
        
        self.row_num = len(contents.splitlines())
        self.col_num = len(contents.splitlines()[0])
        self.goal = 'B'
        self.walls = []
        self.grid = contents.splitlines()
        self.actions = { "up": "r-", "down": "r+", "left": "c-", "right": "c+"}

        for i in range(self.row_num):
            for j in range(self.col_num):
                if(self.grid[i][j] == '#'):
                    self.walls.append((i,j))
                elif(self.grid[i][j] == 'A'):
                    self.initial = (i,j)
                elif(self.grid[i][j] == 'B'):
                    self.end = (i,j)
    
    def solve_maze(self):
        self.states_num = 0
        self.nodes_explored = set()
        frontier = StackFrontier()

        initial_node = Node(row=self.initial[0],col=self.initial[1],parent=None,action=None)
        frontier.add_node(initial_node)
        
        while True:
            if(frontier.is_empty()):
                self.solution = "No solution found"
                break
            
            node = frontier.remove_node()
            if((node.row,node.col) in self.nodes_explored or frontier.is_contained(node.row,node.col)):
                continue
            self.nodes_explored.add((node.row,node.col))
            self.states_num += 1

            if(self.grid[node.row][node.col] == self.goal):
                node=node.parent
                while(node.parent is not None):
                    #replacing the ' ' character with '*' to indicate path
                    self.grid[node.row] = self.grid[node.row][:node.col] + 'o' + self.grid[node.row][node.col+1:]
                    node = node.parent
                self.solution = self.grid
                break
            
            for key in self.actions:
                if(key=="up"):
                    if(node.row > 0):
                        if(self.grid[node.row-1][node.col]!='#'):
                            frontier.add_node(Node(row=node.row-1,col=node.col,parent=node,action="up"))

                elif(key=="down"):
                    if(node.row < self.row_num-1):
                        if(self.grid[node.row+1][node.col]!='#'):   
                            frontier.add_node(Node(row=node.row+1,col=node.col,parent=node,action="down"))
        
                elif(key=="left"):
                    if(node.col > 0):
                        if(self.grid[node.row][node.col-1]!='#'):
                            frontier.add_node(Node(row=node.row,col=node.col-1,parent=node,action="left"))

                elif(key=="right"):
                    if(node.col < self.col_num-1):
                        if(self.grid[node.row][node.col+1]!='#'):
                            frontier.add_node(Node(row=node.row,col=node.col+1,parent=node,action="right"))
                        
                
maze = Maze("maze.txt")
maze.solve_maze()
with open("solved_maze_DFS.txt","w") as output_file:
    for i in maze.solution:
        output_file.write(i)
        output_file.write('\n')
    output_file.write('\n')
    output_file.write(f"Number of states explored (DFS): {maze.states_num}")

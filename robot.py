from cell import Cell
from maze import Maze

class Robot:
    ''' Robot class properties:
    
        start    : starting cell with coordinates (0,0)
        currrent : the cell robot is currently in
        
        grid  : array that stores all maze cells visited by the robot
                to get cell at position x, y use grid [(x,y)]
                where x and y are coordinates of the cell relative to starting cell
        
        grids : boundary coordinates of the grid in the tuple (x0,y0,x1,y1)
                x0 and y0 are the minimum coordinates from all cells in the grid
                x1 and y1 are the maximum
       
        steps   : number of steps to reach the exit
        visisted: number of cells visited by robot during the run
        repeated: number of visits to previously visited cells
       
    '''

    def __init__(self, maze = None):
        self.start = Cell(0,0)
        self.grid = {}
        self.grid[(0,0)] = self.start
        self.grids = (0,0,0,0)
        self.current = self.start
        self.current.visits = 1
        if maze:
            self.maze = maze
        else:
            self.maze = Maze()

    def cell(self, x, y):
        ''' add the new cell to the robot internal map '''
    
        cell = Cell(x, y)
        self.grid[(x,y)] = cell
        (x0, y0, x1, y1) = self.grids
        if x < x0: x0 = x
        if y < y0: y0 = y
        if x > x1: x1 = x
        if y > y1: y1 = y
        self.grids = (x0, y0, x1, y1)
        return cell

    def select(self, step, previous):
        ''' select the best next move, step is the step number '''

        cell = self.current
        
        neighbours = {(-1,0): cell.up,
                      (0,1):  cell.right,
                      (1,0):  cell.down,
                      (0,-1): cell.left}
        
        moves = list(neighbours.keys())
#        random.shuffle(moves)
    
        def distance(cell):
            ''' auixilary method to calculate distance to the nearest non-visited cell '''
        
            for xy in self.grid:
                i = self.grid[xy]
                i.distance = None
                i.moveto = None

            cell.distance = 0
            cells = [cell]
            
            while len(cells) > 0:
                ci = cells.pop(0)
                if ci.visits == 0:
                    path = []
                    cii = ci
                    while cii.moveto != None:
                        (xi, yi, cii) = cii.moveto
                        path.append((yi, xi))
                    return (ci.distance, path)
                ns = ci.neighbours()
                for ni in ns:
                    if ni.distance is None:
                        ni.distance = ci.distance + 1
                        xi = yi = 0
                        if ci.x > ni.x: xi = -1
                        elif ci.x < ni.x: xi = 1
                        elif ci.y > ni.y: yi = -1
                        elif ci.y < ni.y: yi = 1
                        ni.moveto = (xi, yi, ci)
                        cells.append(ni)
            
            return False


        # to store good moves
        good = []
        
        for mi in moves:
            ci = neighbours[mi]
            if not ci.wall:
                # if a move to the non-visited cell possible, do it
                if ci.visits == 0:
                    return mi
                if ci == previous:
                    previous = mi
                else:
                    good.append(mi)
            
        # if no move is possible from the current position, return back
        if len(good) == 0:
            return previous
        
        # if one move is possible from the current position, make it
        if len(good) == 1:
            return good[0]
        
        # otherwise, select the visited cell closest to any non-visited cell

        mins = 65535
        move = None
        minp = []
        
        for mi in good:
            (di, pi) = distance(neighbours[mi])
            if di < mins:
                mins = di
                move = mi
                minp = pi
        
        self.path = minp
        
        return move
        


    def build(self):
        ''' create neighbouring cells for the current cell
            and place them to the grid to visit later
        '''
    
        cell = self.current
        area = [(-1,0), (1,0), (0,-1), (0,1)]
        
        for yx in area:
            (y, x) = yx
            x = cell.x + x
            y = cell.y + y
            if (x, y) in self.grid:
                neighbour = self.grid[(x, y)]
            else:
                neighbour = self.cell(x, y)
                self.grid[(x, y)] = neighbour
            cell.connect(neighbour)
        
        (x0, y0, x1, y1) = self.grids
        
        add = []
        for i in range(x0, x1 + 1):
            for j in range(y0, y1 + 1):
                if not (i,j) in self.grid:
                    cell = Cell(i, j)
                    self.grid[(i,j)] = cell
                    add.append(cell)

        for cell in add:
            for yx in area:
                (y, x) = yx
                x = cell.x + x
                y = cell.y + y
                if (x, y) in self.grid:
                    cell.connect(self.grid[(x, y)])


    def mindmap(self):
        ''' auixilary method used for animation
            non neccessary for navigation
        '''
    
        mindmap = []
        maxx = maxy = -65535
        minx = miny = 65535
            
        for xy in self.grid:
            (x, y) = xy
            if x > maxx: maxx = x
            if y > maxy: maxy = y
            if x < minx: minx = x
            if y < miny: miny = y
             
              
        for i in range(miny, maxy + 1):
            row = ''
            for j in range(minx, maxx + 1):
                if (j, i) in self.grid:
                    cell = self.grid[(j, i)]
                    if cell.wall:
                        row += '.'
                    elif cell.visits == 0:
                        row += '?'
                    else:
                        if i == self.current.y and j == self.current.x:
                            row += '*'
                        else:
                            row += ' '
                else:
                    row += '-'
            mindmap.append(row)
        
        return mindmap


    def navigate(self, animation = True):
    
        mapping = {(-1,0): "UP",
                   (1,0):  "DOWN",
                   (0,-1): "LEFT",
                   (0,1):  "RIGHT"}
        
        result = ""
        step = 0
        previous = None
        self.path = []
        
        self.visited = self.repeated = 0
        
        while result != "win":
            step = step + 1
            
            # initialize neighbouring cells that we can move to
            self.build()
            
            if len(self.path) > 0:
                (y, x) = self.path.pop()
            
            else:
            # select the next move
                (y, x) = self.select(step, previous)

            # convert the move from coordinates to word: up, down, left, right
            move = mapping[(y, x)]

            # select the cell that we are moving to and mark it as visited
            x += self.current.x
            y += self.current.y
            cell = self.grid[(x, y)]
            
            vs = cell.visit(step)
            if vs > 1:
                self.repeated += 1
            self.visited += 1
            
            if animation:
                print(move)
            
            # print("\npress any key to do the selected move...")
            # input('')
            
            # do the move
            result = self.maze.go(move, animation)

            if result == "true":
                previous = self.current
                self.current = cell
            
            elif result == "false":
                cell.wall = True
                
                if animation:
                    print('WALL')

            # display the animation or output stats to the console
            if animation:
                self.maze.viewer.robot(self.mindmap())
            else:
                print('steps: ' + str(self.maze.steps) + ', visited: ' + str(self.visited) + ', repeated: ' + str(self.repeated), end = "\r")

            # pause and wait for keypress vefore next move
            #if result == "true":
            
        
        if not animation: print ('')
        
        self.steps = self.maze.steps
        
        return self.steps

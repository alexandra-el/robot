from random import randint

class Cell:
    ''' class to store information about every cell in the maze
        x and y   : coordinates of the cell realtive to the robot starting point
        lastvisit : the last step when the cell was visited
        visits    : number of times the cell was visited
        up        : the cell that is upper neighbour of this cell in the maze
        down      : lower neighbour
        left      : left neighbour
        right     : right neighbour
        wall      : True if the cell is wall
        id        : the unique identifier of the cell 
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lastvisit = 0
        self.visits = 0
        self.up =    \
        self.down =  \
        self.left =  \
        self.right = None
        self.wall = False
        self.id = '[' + str(x) + ',' + str(y) + '] ' + str(randint(0,65535))

    def connect(self, cell):
        ''' attach the cell to the neighbour '''
    
        # if the neighbour is in the same row, attach left or right
        if self.x == cell.x:
            if self.y < cell.y:
                cell.up = self
                self.down = cell
            else:
                self.up = cell
                cell.down = self
        
        # otherwise, attach up or down
        elif self.x < cell.x:
            self.right = cell
            cell.left = self
        else:
            self.left = cell 
            cell.right = self


    def visit(self, step):
        ''' increase the number of visits and save the last time the cell was visited '''
        self.visits += 1
        self.lastvisit = step
        return self.visits

    def neighbours(self):
        ''' return all cells that are neighbouring this cell '''
    
        result = []
        full = [self.up, self.down, self.right, self.left]
        for i in full:
            if i:
                if not i.wall: result.append(i)
        
        return result


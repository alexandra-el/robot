import numpy

from random import randint
from animation import Animation


class Maze:
    ''' Maze class properties:
    
        robotRow and robotCol : current coordinates of the robot inside the maze
        prevRow  and prevCol  : coordinates of the robot inside the maze at previous step
        
        exitij   : coordinated of the exit gate
        startij  : starting coordinates of the robot
        steps    : number of steps that robot has made
        minsteps : minimum number of steps required to reach the exit gate
        
        map : map of the maze in ASCII format
        Z   : map of the maze in numerical format, used for animation
    
    '''

    def __init__(self, rows = 64, cols = 64, density = 30, infile = None):
      self.viewer = Animation(self)
      
      # if the input txt file is given, load maze from file  
      if infile:
          self.loadfile(infile)
     
      # otherwise, generate a random maze
      else:
          self.generate(rows, cols, density)
      
      self.reset()
      

    def savefile(self, outfile):
        ''' save the maze to file '''
        
        # replace the smile with 'r' symbol
        m, y = self.map, self.startij[0]
        m[y] = m[y].replace('☻', 'r')
        
        with open(outfile, 'w') as f:
            f.write("\n".join(m) + "\n")
        

    def loadfile(self, infile):
        ''' loads the pre-generated maze from file '''
        
        self.map = []
        with open(infile) as f:
            for line in f:
                self.map.append(line.strip())
                
        h = len(self.map)
        w = len(self.map[0])
        
        # create the numerical representation of the maze
        self.Z = numpy.zeros((w, h), dtype = int)
        mapping = {' ':0, '.':1, 'X':2, 'r':3, '☻':3}
        y = 0
        for row in self.map:
            x = 0
            for cell in row:
                self.Z[x, y] = mapping[cell]
                x += 1
            y += 1
        
        # set the starting coordinates of the robot and exit gate position
        self.startij = self.exitij = None
        for i in range(w):
            for j in range(h):
                if self.Z[i, j] == 3:
                    self.startij = (j, i)
                elif self.Z[i, j] == 2:
                    self.exitij = (j, i)
                if self.startij and self.exitij:
                    break
                    
        # calculate the number of steps from start to exit
        self.minsteps = self.stepsto()
       

    def reset(self):
        ''' set the position of the robot in the maze to initial state '''
        (self.robotRow, self.robotCol) = self.startij
        self.prevRow = self.robotRow
        self.prevCol = self.robotCol
        self.steps = 0

    def go(self, direction, animation):
    
      if (direction != "UP" and \
          direction != "DOWN" and \
          direction != "LEFT" and \
          direction != "RIGHT"):
        
        self.steps += 1
        return "false"

      currentRow = self.robotRow
      currentCol = self.robotCol
      
      if (direction == "UP"):
          currentRow -= 1
      elif (direction == "DOWN"):
          currentRow += 1
      elif (direction == "LEFT"):
          currentCol -= 1
      else:
          currentCol += 1

      if (self.map[currentRow][currentCol] == 'X'):
          self.steps += 1
          return "win"
          
      elif (self.map[currentRow][currentCol] == '.'):
          self.steps += 1
          return "false"
      
      else:
          self.steps += 1
          self.robotRow = currentRow
          self.robotCol = currentCol
          
          if animation:
              self.viewer.animate()
          
          self.prevRow = self.robotRow
          self.prevCol = self.robotCol
        
          return "true"


    def view(self):
        for row in self.map:
            print(row)


    def stepsto(self, a = None, b = None):
        ''' calculate the minimum number of steps to go from A to B '''
        
        # by default, count the number of steps from startig point to exit gate
        
        if not a: a = self.startij
        if not b: b = self.exitij
        
        (ay, ax) = a
        (by, bx) = b
        
        w = len(self.map[0])
        h = len(self.map)
        
        steps = numpy.ones((w, h), dtype = int) * -1
        steps[ay, ax] = 0
            
        stack = [(ay,ax)]
        while len(stack) > 0:
            (i, j) = stack.pop(0)
            s = steps[i, j]
            neighbours = [(i+1,j), (i,j+1), (i-1,j), (i,j-1)]
            for ni in neighbours:
                (i, j) = ni
                if i > 0 and j > 0 and i < h - 1 and j < w - 1:
                    if (by,bx) == (i,j):
                        return s
                    elif self.map[i][j] == ' ' and steps[i,j] < 0:
                        steps[i,j] = s + 1
                        stack.append(ni)
         
        # return False if point B is unreachable from point A
        return False


    def generate(self, rows = 64, cols = 64, density = 30):
    
        w = rows
        h = cols

        # initialize the maze cells and draw the border around it
        Z = numpy.zeros((w, h), dtype = int)
        Z[0, :] = Z[:, 0] = Z[h - 1, :] = Z[:, w - 1] = 1
        
        # add some walls to the maze
        # density is the percentage of wall cells
        walls = (w - 2) * (h - 2) * density // 100
        while walls > 0:
            (i, j) = (randint(1, h - 2), randint(1, w - 2))
            if Z[i ,j] == 0:
                Z[i, j] = 1
                walls -= 1
    
        # create ASCII representation of the maze
        self.map = []
        mapping = [' ', '.']
        for i in range(w):
            row = ''
            for j in range(h):
                row += mapping[Z[i, j]]
            self.map.append(row)
    
        # now generate a random starting point for the robot and exit gate
        # making sure that exit gate is reachable
        while True:
            (ry, rx) = (randint(1, h - 2), randint(1, w - 2))
            (ey, ex) = (randint(1, h - 2), randint(1, w - 2))
            steps = self.stepsto((ry, rx), (ey, ex))
            if steps:
                self.minsteps = steps
                break
        
        Z[ey, ex] = 2
        Z[ry, rx] = 3
        
        self.map[ry] = self.map[ry][:rx] + '☻' + self.map[ry][rx+1:]
        self.map[ey] = self.map[ey][:ex] + 'X' + self.map[ey][ex+1:]
        
        self.startij = (ry, rx)
        
        self.Z = Z
        
    


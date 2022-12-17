import numpy
import matplotlib.pyplot as pyplot

class Animation:
    ''' auxiliary class used for displaying animation of the robot navigating the maze
    
        maze: the maze to display, should be passed in constructor
        
        animate() display the maze and the current position of the robot inside it
        robot()   display the map of the maze, that was built by the robot
    '''

    def __init__(self, maze):
        self.maze = maze
        self.image = None
        self.imageRo = None

    def robot(self, mindmap):
        ''' display map as it is remembered by robot '''
    
        self.plot()
    
        y = 0
        for row in mindmap:
            x = 0
            for i in row:
                if i == '*':
                    rx = x
                    ry = y
                    break
                x += 1
            y += 1
        
        dy = self.maze.robotRow - ry
        dx = self.maze.robotCol - rx
        
        palette = {'*': [0.8, 0.0, 0.2],
                   '-': [0.95, 0.95, 0.95],
                   '?': [0.9, 0.9, 1.0],
                   ' ': [1.0, 1.0, 1.0],
                   '.': [0.0, 0.0, 0.0]} 
        
        y = 0
        for row in mindmap:
            x = 0
            for cell in row:
                self.imagero[y + dy, x + dx] = palette[cell]
                x += 1
            y += 1
        
        self.mind.set_data(self.imagero)
        
        pyplot.draw()


    def plot(self):
        ''' initialize the animation canvas '''
    
        if self.image is None or self.imagero is None:
        
            palette = numpy.array( [ [1.0, 1.0, 1.0],
                                     [0.0, 0.0, 0.0],
                                     [0.0, 1.0, 0.0],
                                     [0.0, 0.0, 1.0],
                                     [0.95, 0.95, 0.95]] )
                                     
            self.image = palette[self.maze.Z.astype(int)]
            self.imagero = palette[numpy.ones((len(self.maze.Z), len(self.maze.Z[0])), dtype = int) * 4]
            
            figure, axes = pyplot.subplots(1, 2, figsize = (10, 10))
            figure.tight_layout()
            
            pyplot.xticks([]), pyplot.yticks([])
            
            if isinstance(axes, numpy.ndarray):
                self.axes = list(axes.flat)
            else:
                self.axes = [axes]
            
            self.canvas = self.axes[0].imshow(self.image)
            self.mind   = self.axes[1].imshow(self.imagero)

        
    def animate(self):
        ''' display the maze and the current position of the robot inside it '''
        
        self.plot()
        self.image[self.maze.prevRow, self.maze.prevCol] = [0.8, 0.8, 0.8]
        self.image[self.maze.robotRow, self.maze.robotCol] = [0.8, 0.0, 0.2]
        self.canvas.set_data(self.image)
        pyplot.draw()
        pyplot.pause(0.0001)

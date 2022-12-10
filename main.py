import os

from maze import Maze
from robot import Robot
from rrobot import RandomRobot


def mazes(start = 8, stop = 256):
    ''' generate many mazes and save them to file '''
    
    # path to folder to save maze files
    path = os.path.dirname(os.path.realpath(__file__)) + '/mazes'
    
    for i in range(start, stop + 1):
        size = str(i) + 'x' + str(i)
        m = Maze(i, i)
        m.savefile(path + '/' + size + '.txt')
        print ('generating mazes: ' + size, end = '\r')
    
    print("\ndone.")


def test(size = '99x99'):
    ''' load the maze of the specified size from file and test it with normal and random traversal '''

    # path to folder where maze files are stored
    path = os.path.dirname(os.path.realpath(__file__)) + '/mazes'
    
    maze = Maze(infile = path + '/' + size + '.txt')
    
    print ('loaded maze ' + size)
    print ('minimum steps to reach exit gate: ' + str(maze.minsteps))
    
    print ('testing normal Robot')
    robot = Robot(maze)
    robot.navigate(animation = False)
    
    maze.reset()
    
    print ('testing random Robot')
    robot = RandomRobot(maze)
    robot.navigate(animation = False)
    

# mazes()

for i in range(8, 192):
    test(str(i) + 'x' + str(i))
    print('')



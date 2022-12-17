import os
import time
from memory_profiler import memory_usage

from maze import Maze
from robot import Robot
from rrobot import RandomRobot


def mazes(start = 8, stop = 256):
    ''' generate many mazes and save them to file '''
    
    # path to folder to save maze files
    path = os.path.dirname(os.path.realpath(__file__)) + '/mazes'
    
    for i in range(start, stop + 1):
        for j in range(start, stop + 1):
            size = str(i) + 'x' + str(j)
            m = Maze(i, j)
            m.savefile(path + '/' + size + '.txt')
            print ('generating mazes: ' + size, end = '\r')
    
    print("\ndone.")


def test(size = '99x99'):
    ''' load the maze of the specified size from file and test it with normal and random traversal '''

    def nav():
        robot.navigate(animation = False)

    # path to folder where maze files are stored
    path = os.path.dirname(os.path.realpath(__file__)) + '/mazes'
    
    mazetxt = path + '/' + size + '.txt'
    
    if not os.path.exists(mazetxt):
        m = Maze(i, j)
        m.savefile(mazetxt)
    
    maze = Maze(infile = mazetxt)
    
    print ('loaded maze ' + size)
    print ('minimum steps to reach exit gate: ' + str(maze.minsteps))
    
    print ('testing normal Robot')
    robot = Robot(maze)
    ts = time.time()
#    mem = memory_usage(nav)
    nav()
    tt = time.time() - ts
#    mem = max(mem)
    mem = 0
    
    with open('test.txt', 'a') as f:
        data = [size, robot.steps, robot.visited, robot.repeated, tt, mem]
        f.write("\t".join(map(str, data)) + "\n")
    
#    maze.reset()
    
#    print ('testing random Robot')
#    robot = RandomRobot(maze)
#    robot.navigate(animation = False)
    

# mazes()

#for i in range(8, 192):
#    for j in range(8, 192):
#        test(str(i) + 'x' + str(j))
#        print('')


Robot(Maze(16,32)).navigate()

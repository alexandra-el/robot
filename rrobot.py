import random

from robot import Robot


class RandomRobot(Robot):

    def select(self, step, previous = None):

        cell = self.current
        
        neighbours = {(-1,0): cell.up,
                      (0,1):  cell.right,
                      (1,0):  cell.down,
                      (0,-1): cell.left}
        
        moves = list(neighbours.keys())
        random.shuffle(moves)
        
        return moves[0]


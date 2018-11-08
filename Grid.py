import numpy as np
import pygame
from Cell import Cell


class Grid:

    def __init__(self, width, height):
        #fill the grid with cells
        self.grid = [[Cell() for j in range(height)] for i in range(width)]

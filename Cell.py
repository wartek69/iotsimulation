import numpy as np


class Cell:
    def __init__(self):
        r = [np.random.uniform(0, 1) for i in range(0,3)]
        s = sum(r)
        self.rock = r[0]/s
        self.pop = r[1]/s
        self.techno = r[2]/s
        print("")

    #Return the color to use, the style you like the most and the value for that style
    def getPreferences(self):
        temp = max(self.rock, self.pop, self.techno)
        if self.rock == temp:
            return (255 * temp, 0, 0), "rock", self.rock
        elif self.pop == temp:
            return (0, 0, 255 * temp), "pop", self.pop
        else:
            return (0, 255 * temp, 0), "techno", self.techno

    #returns your influence factor to your neighbour
    def getInfluenceFactor(self):
        ifa = 0.25 * self.getPreferences()[2] + 0.25 * np.random.uniform(0, 1)
        return ifa, self.getPreferences()[1]



import random
from math import sqrt
class Point:
    distance = int()
    def __init__(self,x,y):
        self.f1 = x
        self.f2 = y
    
    def distance_to(self,point):
        return sqrt((self.f1 - point.f1)**2 + (self.f2 - point.f2)**2)


class Points:
    def __init__(self):
        self.points = []
    def generate(self,n):
        while len(self.points) < n:
            x = random.uniform(0,100)
            y = random.uniform(0,100)
            if ((x**2)/2304 + (y-24)**2/576 <= 1) & (-x+y <= 24) & (x+y >= 48):
                self.points.append(Point(x,y))
from math import sqrt
class Point:
    def __init__(self, f1,f2,number):
        self.f1 = f1
        self.f2 = f2
        self.number = number
        self.unoptimal = False
        self.efficiency = 0
        self.n = 0
        self.omega = False


class Points:
    def __init__(self, arr, clusters=[1,0.85,0.75]):
        self.array = arr
        self.clusters = clusters
        self.optimal = []
        self.centroids = [None]*len(self.clusters)

    def exclude_unoptimal(self):
        for i in self.array:
            if i.unoptimal == True:
                continue
            print("Точка номер ",i.number, '( f1= ',i.f1,', f2 = ',i.f2,'):', sep='')
            for j in self.array:
                if j.unoptimal == True or j == i:
                    continue
                if j.f1 >= i.f1 and j.f2 >= i.f2:
                    j.unoptimal = True
                    print(j.number)
        self.optimal = [i for i in self.array if i.unoptimal==False]
        print('Парето-оптимальные точки:',','.join([str(i.number) for i in self.optimal]))
    

    def find_omega(self):
        for i in self.optimal:
            if i.f2 <= i.f1 and 0.6*i.f2 >= 0.4*i.f1:
                i.omega = True
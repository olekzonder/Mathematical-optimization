from math import sqrt
class Point:
    def __init__(self, f1,f2,number):
        self.f1 = f1
        self.f2 = f2
        self.number = number
        self.unoptimal = False
        self.efficiency = 0
        self.cluster_id = -1
        self.iterations_list = []
        self.points_list = []
        self.n = 0


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
            print("Точка номер ",i.number, '( f1= ',i.f1,', f2 = ',i.f2,')', sep='')
            for j in self.array:
                if j.unoptimal == True:
                    j.iterations_list.append('-')
                    continue
                if j == i:
                    i.iterations_list.append('!')
                    continue
                if j.f1 <= i.f1 and j.f2 <= i.f2:
                    j.unoptimal = True
                    print("Точка номер ",j.number, '( f1= ',i.f1,', f2 = ',i.f2,') в обратном конусе доминирования точки ', i.number, sep='')
                    j.iterations_list.append('X')
                else:
                    j.iterations_list.append('')
        self.optimal = [i for i in self.array if i.unoptimal==False]
        print('Парето-оптимальные точки:',','.join([str(i.number) for i in self.optimal]))
    
    def efficiency_index(self):
        for i in self.array:
            print("Точка номер ",i.number, '( f1= ',i.f1,', f2 = ',i.f2,')', sep='')
            n = 0
            for j in self.array:
                if i != j and (j.f1 >= i.f1 and j.f2 >= i.f2):
                    n += 1
                    print("Точка номер ",j.number, '( f1= ',i.f1,', f2 = ',i.f2,') в конусе доминирования точки ', i.number, sep='')
                    i.points_list.append(j)
            i.n = n
            i.efficiency=1/(1+(n/(len(self.array)-1)))
            clust_diff = []
            for j in self.clusters:
                clust_diff.append(sqrt((i.efficiency-j)**2))
            i.cluster_id = clust_diff.index(min(clust_diff))

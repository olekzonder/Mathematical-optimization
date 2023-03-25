import itertools
from math import sqrt
import numpy
class Point:
    def __init__(self, j1,j2,number):
        self.j1 = j1
        self.j2 = j2
        self.number = number
        self.unoptimal = False
        self.n = number
        self.omega = None

def gray_code_product(*args, repeat=1):
    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x+[y] for i, x in enumerate(result) for y in (
            reversed(pool) if i % 2 else pool)]
    for prod in result:
        yield tuple(prod)

class Points:
    def __init__(self, arr, clusters=[1,0.85,0.75]):
        self.array = arr
        self.clusters = clusters
        self.optimal = []

    def exclude_unoptimal(self):
        for i in self.array:
            if i.unoptimal == True:
                continue
            print("Точка номер ",i.number, '( j1= ',i.j1,', j2 = ',i.j2,'):', sep='')
            for j in self.array:
                if j.unoptimal == True or j == i:
                    continue
                if j.j1 >= i.j1 and j.j2 >= i.j2:
                    j.unoptimal = True
                    print(j.number)
        self.optimal = [i for i in self.array if i.unoptimal==False]
        print('Парето-оптимальные точки:',','.join([str(i.number) for i in self.optimal]))
    
    def find_omega(self,mu_arr=[[0.2,0.6],[0.2,0.5]]):
        B = [list(i) for i in list(gray_code_product(mu_arr[0],mu_arr[1]))]
        L = [round(sum(i)-1,1) for i in B]
        b = []
        for i in range(len(B)):
            T = []
            A = []
            C = []
            for j in range(i, len(B)):
                if i == j or (B[i][0] != B[j][0] and B[i][1] != B[j][1]) or L[i] * L[j] >= 0:
                    continue
                T = [B[i],B[j]]
            if T:
                A = [[1 for i in range(len(mu_arr))]]
                C = [[1]]
                if T[0][0] == T[1][0]:
                    A.append([1,0])
                    C.append([T[0][0]])
                if T[0][1] == T[1][1]:
                    A.append([0,1])
                    C.append([T[0][1]])
                solution = [float(i) for i in numpy.linalg.solve(numpy.array(A),numpy.array(C))]
                if solution not in b:
                    b.append(solution)
        b = numpy.matrix(b)
        for i in self.optimal:
            if i.omega == False:
                continue
            for j in self.optimal:
                if i == j or j.omega == False:
                    continue
                opt_arr = numpy.matrix([[i.j1-j.j1],[i.j2-j.j2]])
                omega_arr = b*opt_arr
                if omega_arr[0] <= 0 and omega_arr[1] <= 0 and omega_arr[0] != omega_arr[1]:
                    j.omega = False
            if i.omega == None:
                    i.omega = True
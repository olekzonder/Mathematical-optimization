import numpy as np
from scipy.optimize import linprog

qf2=1
qf3=3

D = np.array([[1, 2], [-2, -1],[-1, 0],[1, 0], [0, -1],[0, 1]])
b = np.array([96, -24, 0, 48, 0, 36])
c = np.array([-1, 3])
res3 = linprog(c, A_ub=D, b_ub=b)
print('Оптимизация по f3: f*3=', round(-1*res3.fun, ndigits=2))

#2
f2 = -1*res3.fun-qf3
D1 = np.array([[1, 2], [-2, -1], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, 3]])
b = np.array([96, -24, 0, 48, 0, 36,-f2])
c = np.array([3, -1])
res2 = linprog(c, A_ub=D1, b_ub=b)
print('Оптимизация по f2: f*2=', round(-1*res2.fun, ndigits=2))

#3
f1 = round(res2.fun*-1-qf2, ndigits=2)
D2 = np.array([[1, 2], [-2, -1], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, 3], [3, -1]])
b = np.array([96, -24, 0, 48, 0, 36,-f2,-f1])
c = np.array([-1, -1])
res1 = linprog(c, A_ub=D2, b_ub=b)
print('Оптимизация по f3: f*3=', round(res1.fun*-1, ndigits=2))
print('Точка оптимального решения:',res1.x[0],res1.x[1])
print('Оптимальное решение:')
print('f1=',round(res1.fun*-1, ndigits=2))
print('f2=', round(res2.fun*-1, ndigits=2))
print('f3=', round(res3.fun*-1, ndigits=2))

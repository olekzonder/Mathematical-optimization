import numpy as np
from scipy.optimize import linprog
from sympy import symbols, diff, poly, solve

#постановка задачи
funcs = [[-1,-1],[3,-1],[-1,3]] # функции
d =  [[-1,-1],[1,-2],[-3,2],[-1,0],[1,0],[0,-1],[0,1]] # ограничения D
d_rhs =  [-48,24,48,0,96,0,72] #ограничения D, <= - отрицательный знак, >= - положительный
X = np.matrix([72,48]).transpose() # начальное приближение


x1,x2,l = symbols('x1 x2 l')
ideal_points = []

#Создание идеальных точек
for f in funcs:
    res = linprog(c=f,A_ub=d,b_ub=d_rhs)
    ideal_points.append(round(res.fun*-1,2))
print("F*",ideal_points,sep=': ')

#Создание вспомогательной функции
f1 = -1*funcs[0][0]*x1- 1*funcs[0][1]*x2
f2 = -1*funcs[1][0]*x1 -1*funcs[1][1]*x2
f3 = -1*funcs[2][0]*x1 -1*funcs[2][1]*x2
fi  = (f1-ideal_points[0])**2 + (f2 - ideal_points[1])**2 + (f3 - ideal_points[2])**2
fi1 = diff(fi,x1)
fi2 = diff(fi,x2)
k = 0
prev_solution = 1
prev = fi.subs({x1:X[0,0],x2:X[1,0]})
print("ф({}):".format(k),prev)

while True:
    print('------------------------','Приближение ',k,'------------------',sep = '')
    x = X[0,0]
    y = X[1,0]
    aux = poly(fi1.subs({x1:x,x2:y})*x1+ fi2.subs({x1:x,x2:y})*x2)
    res = linprog(c=[aux.coeffs()[0],aux.coeffs()[1]],A_ub=d,b_ub=d_rhs)
    Xn = np.matrix([res.x[0],res.x[1]]).transpose()
    Xn = X + l*(Xn-X)
    print(Xn)
    fi_Xn = fi.subs({x1:Xn[0,0],x2:Xn[1,0]})
    print(fi_Xn)
    solution = solve(diff(fi_Xn,l))[0]
    Xn = np.matrix([i[0,0].subs({l:solution}) for i in Xn]).transpose()
    cur = fi.subs({x1:Xn[0,0],x2:Xn[1,0]})
    if round(prev,3) > round(cur,3):
        print("X{}".format(k),[X[0,0],X[1,0]],sep=":")
        print("Вспомогательная функция",aux.as_expr(),sep=': ')
        print("Оптимальная точка".format(k),[round(res.x[0],2),round(res.x[1],2)],sep=': ')
        print("Решение задачи λ:",solution)
        print("X{}".format(k+1),[Xn[0,0],Xn[1,0]],sep=':')
        print("ф({}):".format(k),prev)
        print("ф({}):".format(k+1),cur)
        X = Xn
        prev = cur
        k+=1
    else:
        break
print()
print("Ответ:")
print("f1", f1.subs({x1:X[0,0],x2:X[1,0]}),sep=":")
print("f2", f2.subs({x1:X[0,0],x2:X[1,0]}),sep=":")
print("f3", f3.subs({x1:X[0,0],x2:X[1,0]}),sep=":")


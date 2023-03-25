#Смирнов А.И. 2022
#https://github.com/olekzonder
import sympy as sy
class Fibonacci:
    def __init__(self, function):
        self.function = sy.sympify(function)
        self.fibArr = []
    def calculate(self, **kwargs):
        return self.function.subs(kwargs)

    def fibonacci(self,n):
        if n in {0,1}:
            return n
        return self.fibonacci(n-1)+self.fibonacci(n-2)
    
    def optimizeMin(self, a,b, **kwargs):
        if 'e' in kwargs.keys():
                e = kwargs['e']
                _n = (b-a)/e
                k = 0
                i = self.fibonacci(k)
                while _n > i:
                    self.fibArr.append(i)
                    k+=1
                    i = self.fibonacci(k)
                _n = k-2
                print("N = ",_n)
                self.optimizeMin(a,b,n=_n+1)
                return
        else:
            n = kwargs['n']
        xl = a
        xr = b
        x1 = xl + self.fibArr[n-2]/self.fibArr[n]*(xr-xl)
        x2 = xl + self.fibArr[n-1]/self.fibArr[n]*(xr-xl)
        if x1==x2:
            res = x1
            print('x = ',res)
            print('f(x) = ', self.calculate(x=res))
            return
        y1 = self.calculate(x=x1)
        y2 = self.calculate(x=x2)
        if y1>y2:
            xl = x1
        if y2>y1:
            xr = x2
        _n = n-1
        self.optimizeMin(xl,xr,n=_n)

    def optimizeMax(self, a,b, **kwargs):
        if 'e' in kwargs.keys():
                e = kwargs['e']
                _n = (b-a)/e
                k = 0
                i = self.fibonacci(k)
                while _n > i:
                    self.fibArr.append(i)
                    k+=1
                    i = self.fibonacci(k)
                _n = k-2
                print("N = ",_n)
                self.optimizeMax(a,b,n=_n+1)
                return
        else:
            n = kwargs['n']
        xl = a
        xr = b
        x1 = xl + self.fibArr[n-2]/self.fibArr[n]*(xr-xl)
        x2 = xl + self.fibArr[n-1]/self.fibArr[n]*(xr-xl)
        if x1==x2:
            res = x1
            print('x = ',res)
            print('f(x) = ', self.calculate(x=res))
            return
        y1 = self.calculate(x=x1)
        y2 = self.calculate(x=x2)
        if y1<y2:
            xl = x1
        if y2<y1:
            xr = x2
        _n = n-1
        self.optimizeMax(xl,xr,n=_n)


if __name__ == "__main__":
    import os
    while True:
        function = input("Введите функцию: ")
        fibonacci = Fibonacci(function)
        break
    flag = True
    while flag:
        print('[1] Максимизировать функцию')
        print('[2] Минимизировать функцию')
        print('[0] Выйти')
        try:
            choice = int(input('> '))
        except ValueError:
            continue
        if choice == 0:
            flag = False
        if choice == 1:
            # try:
                l = float(input("Нижняя граница: "))
                r = float(input("Верхняя граница: "))
                e = float(input("Погрешность: "))
                fibonacci.optimizeMax(l,r,e=e)

        if choice == 2:
            try:
                l = float(input("Нижняя граница: "))
                r = float(input("Верхняя граница: "))
                e = float(input("Погрешность: "))
                fibonacci.optimizeMin(l,r,e=e)
            except ValueError:
                print("Ошибка при вводе значений...")
        input("Нажмите ENTER, чтобы продолжить...")
        if(os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')
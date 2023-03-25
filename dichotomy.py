#Смирнов А.И. 2022
#https://github.com/olekzonder
import sympy as sy
class Dichotomy:
    def __init__(self, function):
        self.function = sy.sympify(function)

    def calculate(self, **kwargs):
        return self.function.subs(kwargs)

    def optimizeMax(self,l,r,e):
        roundTo = len(str(e).replace('.','')) - len(str(int(e)))
        if round(abs(l-r),roundTo) <= e:
            res = round((l+r)/2,roundTo)
            print('x = ', res)
            print('f(x) = ', self.calculate(x=res))
            return
        xl = l
        xr = r
        x1 = (xl+xr)/2-(e/2)
        x2 = (xl+xr)/2+(e/2)
        y1 = self.calculate(x=x1)
        y2 = self.calculate(x=x2)
        if y1<y2:
            xl = x1
        if y2<y1:
            xr = x2
        self.optimizeMax(xl,xr,e)

    def optimizeMin(self,l,r,e):
        roundTo = len(str(e).replace('.','')) - len(str(int(e)))
        if round(abs(l-r),roundTo) <= e:
            res = round((l+r)/2,roundTo)
            print('x = ', res)
            print('f(x) = ', self.calculate(x=res))
            return
        xl = l
        xr = r
        x1 = (xl+xr)/2-(e/2)
        x2 = (xl+xr)/2+(e/2)
        y1 = self.calculate(x=x1)
        y2 = self.calculate(x=x2)
        if y1>y2:
            xl = x1
        if y2>y1:
            xr = x2
        self.optimizeMin(xl,xr,e)

if __name__ == "__main__":
    import os
    while True:
        function = input("Введите функцию: ")
        dichotomy = Dichotomy(function)
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
                dichotomy.optimizeMax(l,r,e)

        if choice == 2:
            try:
                l = float(input("Нижняя граница: "))
                r = float(input("Верхняя граница: "))
                e = float(input("Погрешность: "))
                dichotomy.optimizeMin(l,r,e)
            except ValueError:
                print("Ошибка при вводе значений...")
        input("Нажмите ENTER, чтобы продолжить...")
        if(os.name == 'posix'):
            os.system('clear')
        else:
            os.system('cls')
#Смирнов А.И. 2022
#https://github.com/olekzonder
import numpy as np
import copy
class Interpolation:
    def __init__(self, _x,_y):
        self.xtable = _x
        self.ytable = _y
        self.varlist = []
        self.result = 0

    def createMatrix(self,x):
        closest = sorted(sorted(self.xtable, key = lambda val: abs(val-x)))[:3]
        matrix = []
        for i in range(3):
            row = []
            for j in range(2,-1,-1):
                row.append(closest[i]**j)
            matrix.append(row)
        matrix.append([self.ytable[self.xtable.index(i)] for i in closest ])
        return matrix
    
    def getDet(self, arr):
        matrix = np.asarray(arr)
        return np.linalg.det(matrix)

    def interpolate(self, arr):
        det = self.getDet(arr[:3])
        backupArr = copy.deepcopy(arr[:3])
        for i in range(3):
            tempArr = copy.deepcopy(backupArr)
            for j in range(3):
                tempArr[j][i] = arr[3][j]
            self.varlist.append(self.getDet(tempArr)/det)

    def calculate(self,x):
        self.result=0
        matrix = self.createMatrix(x)
        self.interpolate(matrix)
        pwr = 0
        for i in reversed(self.varlist):
            self.result += i*pow(x,pwr)
            pwr+=1
        self.getOutput()
        return self.result

    def getOutput(self):
        pw = 2
        output = ""
        for i in range(len(self.varlist)):
            if pw > 1:
                if self.varlist[i] != 0:
                    output += str(self.varlist[i] if abs(self.varlist[i]) != 1 else "" if self.varlist[i] > 0  else "-") + "x^" + str(pw)
            elif pw == 1:
                if self.varlist[i] != 0:
                    output += str(self.varlist[i] if abs(self.varlist[i]) != 1 else "" if self.varlist[i] > 0  else "-") + "x"
            else:
                if self.varlist[i] != 0:
                    output += str(self.varlist[i])
            if i != len(self.varlist)-1:
                if self.varlist[i+1] > 0:
                    output += "+"
            pw -= 1
        print("Многочлен:",output)


if __name__ == "__main__":
    import os
    x = []
    y = []
    print("Для окончания ввода нажмите ENTER...")
    while True:
        try:
            a = [float(i) for i in input("Введите известное значение x и f(x) через пробел > ").split()]
            x.append(a[0])
            y.append(a[1])
        except IndexError:
            break
        except ValueError:
            break
    interpolation = Interpolation(x,y)
    print('f(x) = ', interpolation.calculate(float(input("Введите значение x >"))))
import subprocess
from point import Point, Points
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import csv
import tkinter as tk
from tkinter import filedialog
import os
x = np.linspace(0,50,1000)
y = np.linspace(0,50,1000)
a,b = np.meshgrid(x,y)

def in_constraints(point):
    if ((point.f1-25)**2+(point.f2-25)**2 - 25**2 <= 0) and ((-point.f1 + point.f2) - 25 <= 0) and ((point.f1+point.f2)-50 >= 0):
        return True
    else:
        return False

def plot(points,type=None):
    C1 = (a-25)**2+(b-25)**2-625
    figure, axes = plt.subplots()
    axes.contour(a,b,C1, [0], colors=['#000000'])
    y1 = (x+25)
    y2 = (50-x)
    plt.plot(x,y1,label='Ограничение 2: -f₁ + f₂ ≤ 25')
    plt.plot(x,y2,label='Ограничение 3: f₁ + f₂ ≥ 50')
    
    plt.xlabel('f₁')
    plt.ylabel('f₂')
    plt.axis("equal")
    plt.grid()
    match(type):
        case None:
            for i in points.array:
                plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                plt.text(i.f1,i.f2,str(i.number))
        case 1:
            k1 = False
            k2 = False
            plt.title('Паретто-эффективные точки')
            for i in points.array:
                if i.unoptimal:
                    if not k1:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r',label="Неэффективная точка")
                        k1 = True
                    else:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                else:
                    if not k2:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g',label="Паретто-эффективная точка")
                        k2 = True
                    else:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g')
                plt.text(i.f1,i.f2,str(i.number))
                      
        case 2:
            k1 = False
            k2 = False
            k3 = False
            plt.title('Кластеризация точек')
            for i in points.array:
                match i.cluster_id:
                    case 0:
                        if not k1:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g',label="K1=1")
                            k1 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g')
                        plt.text(i.f1,i.f2,str(i.number))
                    case 1:
                        if not k2:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='y',label="K2=0.85")
                            k2 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                    case 2:
                        if not k3:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r',label="K3=0.75")
                            k3 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                plt.text(i.f1,i.f2,str(i.number))
    plt.legend(loc="best")
    plt.savefig('График '+str(type)+'.png')
    plt.show()
def random_gen(n):
    arr = []
    for i in range(n):
        while True:
            f1 = random.uniform(0,60)
            f2 = random.uniform(0,60)
            if in_constraints(Point(f1,f2,i+1)):
                break
        arr.append(Point(f1,f2,i+1))
    return Points(arr)    

def file_gen(file):
    arr = [i.split(',') for i in file.read().split('\n')][:-1]
    points = []
    n = 1
    for i in arr:
        f1 = float(i[0])
        f2 = float(i[1])
        if not in_constraints(Point(f1,f2,n)):
            print("Ошибка в точке",n)
            raise ValueError
        points.append(Point(f1,f2,n))
        n += 1
    return Points(points)

def to_csv(points,type=None):
    file = filedialog.asksaveasfilename(defaultextension='.csv')
    if file == ():
        return
    with open(file,'w',newline='') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        if type == 1:
            writer.writerow(['Номер точки','f1','f2']+[i for i in range(1,max(len(x) for x in [i.iterations_list for i in points.array])+1)])
            for i in points.array:
                lst = [i.number,i.f1,i.f2]+i.iterations_list
                writer.writerow(lst)
        if type == 2:
            writer.writerow(['Номер точки','f1','f2','B','Ф','Кластер'])
            for i in points.array:
                if len(i.points_list) > 0:
                    lst = [i.number,i.f1,i.f2,str(i.n)+'('+','.join([str(k.number) for k in i.points_list])+')',round(i.efficiency,2),"K"+str(i.cluster_id+1)]
                else:
                    lst = [i.number,i.f1,i.f2,str(i.n),round(i.efficiency,2),"K"+str(i.cluster_id+1)]
                writer.writerow(lst)
    subprocess.call(('xdg-open', file))
def clear():
    if(os.name == 'posix'):
        os.system('clear')
    else:
        os.system('cls')
clear()
print("[1] Открыть файл")
print("[2] Сгенерировать точки")
print("[0] Выход")
while True:
    try:
        choice = int(input("> "))
        if choice == 1 or choice == 2 or choice == 0:
            break
        else:
            print("Неверный пункт меню...")
    except:
            continue

if choice == 1:
    print("Выберите файл в открывшемся диалоговом окне...")
    file = filedialog.askopenfile(initialdir =os.getcwd(), title = "Выберите файл", filetypes=(("Text Files", "*.txt"),))
    if file == None:
        quit()
    else:
        try:
            points = file_gen(file)
        except:
            quit()
if choice == 2:
    while True:
        try:
            n = int(input("Количество точек > "))
            break
        except:
            continue
    points = random_gen(n)
if choice == 0:
        quit()

while True:
    clear()
    print("[1] Алгоритм исключения заведомо неэффективных решений")
    print("[2] Кластеризация множества проектов")
    print("[0] Выход")
    while True:
        try:
            choice = int(input("> "))
            if choice == 1 or choice == 2 or choice == 0:
                break
            else:
                print("Неверный пункт меню...")
        except:
            continue
    match choice:
        case 1:
            points.exclude_unoptimal()
            plot(points,type=1)
            to_csv(points,type=1)
            print()
        case 2:
            points.efficiency_index()
            plot(points,type=2)
            to_csv(points,type=2)
            print()
        case 0:
            quit()
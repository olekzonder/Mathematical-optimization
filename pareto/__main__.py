import subprocess
import time

from matplotlib.ticker import AutoMinorLocator, MultipleLocator
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
name = str(int(time.time()))
u_points = []
def in_constraints(point):
    if ((point.f1-24)**2+(point.f2-24)**2 - 24**2 <= 0) and ((-point.f1 + point.f2) - 24 <= 0) and ((point.f1+point.f2)-48 >= 0):
        return True
    else:
        return False

def plot(points,type=None):
    # C1 = (a-24)**2+(b-24)**2-576
    figure, axes = plt.subplots()
    # axes.contour(a,b,C1, [0], colors=['#000000'])
    # y1 = (x+24)
    # y2 = (48-x)
    # plt.plot(x,y1,label='Ограничение 2: -f₁ + f₂ ≤ 24')
    # plt.plot(x,y2,label='Ограничение 3: f₁ + f₂ ≥ 48')
    
    plt.xlabel('f₁')
    plt.ylabel('f₂')
    plt.xlim(0,50)
    plt.ylim(0,50)
    axes.set_xlim(xmin=0,xmax=50)
    axes.set_ylim(ymin=0,ymax=50)
    axes.spines[["left", "bottom"]].set_position(("data", 0))
    axes.spines["top"].set_visible(False)
    axes.spines["right"].set_visible(False)
    axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
    axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)
    axes.xaxis.set_major_locator(MultipleLocator(5))
    axes.yaxis.set_major_locator(MultipleLocator(5))
    axes.xaxis.set_minor_locator(AutoMinorLocator(5))
    axes.yaxis.set_minor_locator(AutoMinorLocator(5))
    axes.grid(which='major', color='#CCCCCC', linestyle='--')
    axes.grid(which='minor', color='#CCCCCC', linestyle=':')
    match(type):
        case None:
            for i in points.array:
                plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                plt.text(i.f1,i.f2,str(i.number))
        case 1:
            k1 = False
            k2 = False
            for i in points.array:
                if i.unoptimal:
                    if not k1:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                        k1 = True
                    else:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                else:
                    if not k2:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g')
                        k2 = True
                    else:
                        plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g')
                plt.text(i.f1,i.f2,str(i.number))
                      
        case 2:
            k1 = False
            k2 = False
            k3 = False
            for i in points.array:
                match i.cluster_id:
                    case 0:
                        if not k1:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g',label="K1")
                            k1 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='g')
                    case 1:
                        if not k2:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='y',label="K2")
                            k2 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='y')
                    case 2:
                        if not k3:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r',label="K3")
                            k3 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='5',color='r')
                if len(points.array) < 100:
                    plt.text(i.f1,i.f2,str(i.number))
    plt.legend(loc="best")
    plt.savefig(name+'.png')
    print("График сохранён как:",name+'.png')
    plt.show()
def random_gen(n):
    arr = []
    for i in range(n):
        while True:
            f1 = int(random.uniform(0,50))
            f2 = int(random.uniform(0,50))
            # if in_constraints(Point(f1,f2,i+1)):
            break
        arr.append(Point(f1,f2,i+1))
    return Points(arr)    

def file_gen(file):
    arr = [i.split(',') for i in file.read().split('\n')]
    points = []
    n = 1
    for i in arr:
        f1 = float(i[0])
        f2 = float(i[1])
        # if not in_constraints(Point(f1,f2,n)):
        #     print("Ошибка в точке",n)
        #     raise ValueError
        points.append(Point(f1,f2,n))
        n += 1
    return Points(points)

def to_csv(points,type=None):
    file = name+'.csv'
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
    print('Таблица сохранена как:',name+'.csv')
    # subprocess.call(('xdg-open', file))
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
plot(points)
while True:
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
            name = str(int(time.time()))
            points.exclude_unoptimal()
            plot(points,type=1)
            to_csv(points,type=1)
            print()
        case 2:
            name = str(int(time.time()))
            points.efficiency_index()
            plot(points,type=2)
            to_csv(points,type=2)
            print()
        case 0:
            quit()
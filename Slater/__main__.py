import subprocess
import sys
import time
from point import Point, Points
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import random
import csv
import tkinter as tk
from tkinter import filedialog
import os
x = np.linspace(0,6000)
y = np.linspace(0,6000)
a,b = np.meshgrid(x,y)
name = str(int(time.time()))
points_arr = []

def get_csv(points):
    file = name + '.csv'
    k = 0
    with open(file,'w',newline='') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        writer.writerow(['Номер точки','u1','u2','J1','J2','P'])
        for i in points.array:
            writer.writerow([i.n,points_arr[k][0],points_arr[k][1],i.j1,i.j2,'+' if not i.unoptimal else ''])
            k += 1
    print('CSV-таблица сохранена как', file)
def plot(points,type=0):
    k1 = False
    k2 = False
    k3 = False
    for i in points.array:
                if not i.unoptimal and type != 0:
                    if not i.omega:
                        if not k1:
                            plt.plot(i.j1,i.j2,marker='o',markersize='4',color='y',label="Множеcтво Парето")
                            k1 = True
                        else:
                            plt.plot(i.j1,i.j2,marker='o',markersize='4',color='y')
                    else:
                        if not k2:
                            plt.plot(i.j1,i.j2,marker='o',markersize='4',color='g',label='Ω-оптимальные решения')
                            k2 = True
                        else:
                            plt.plot(i.j1,i.j2,marker='o',markersize='4',color='g')
                else:
                    if i.unoptimal and type == 2:
                         continue
                    if not k3:
                        if type == 0:
                             label = 'Точки таблицы испытаний'
                        else:
                             label = 'Заведомо не эффективные точки'
                        plt.plot(i.j1,i.j2,marker='o',markersize='4',color='r',label=label)
                        k3 = True
                    else:
                            plt.plot(i.j1,i.j2,marker='o',markersize='4',color='r') 
    plt.ylabel('J2') 
    plt.xlabel('J1')
    plt.legend(loc="best")
    plt.savefig(name+'.png')
    print("График сохранён как:",name+'.png')
    plt.show()

def random_gen(n):
    arr = []
    for i in range(n):
        u1 = np.random.uniform(0,79)
        u2 = np.random.uniform(0,79)
        j1 = 0.2*(u1-70)**2+0.8*(u2-20)**2
        j2 = 0.2*(u1-10)**2+0.8*(u2-70)**2
        if sys.argv[1] == 'i':
                u1 = int(u1)
                u2 = int(u2)
                points_arr.append([u1,u2])
                j1 = round(j1,2)
                j2 = round(j2,2)
        arr.append(Point(j1,j2,i+1))
    return Points(arr)



if __name__ == '__main__':
    name = str(int(time.time()))
    if len(sys.argv) > 1 :
        if 'i' in sys.argv:
            n = sys.argv[2]
        else:
            n = sys.argv[1]
    else:
        print("ERROR: incorrect args")
        quit()
    points = random_gen(int(n))
    plot(points)
    name = str(int(time.time()))
    points.exclude_unoptimal()
    plot(points,type=1)
    if sys.argv[1] == 'i':
         get_csv(points)
    points.find_omega()
    name = str(int(time.time()))
    plot(points,type=2)
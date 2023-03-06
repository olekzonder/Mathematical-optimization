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

def plot(points,type=None):
    k1 = False
    k2 = False
    k3 = False
    for i in points.array:
                if not i.unoptimal:
                    if not i.omega:
                        if not k1:
                            plt.plot(i.f1,i.f2,marker='o',markersize='4',color='y',label="Множеcтво Парето")
                            k1 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='4',color='y')
                    else:
                        if not k2:
                            plt.plot(i.f1,i.f2,marker='o',markersize='4',color='g',label='Ω-оптимальные решения')
                            k2 = True
                        else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='4',color='g')
                else:
                    if not k3:
                        plt.plot(i.f1,i.f2,marker='o',markersize='4',color='r',label='Заведомо не эффективные точки')
                        k3 = True
                    else:
                            plt.plot(i.f1,i.f2,marker='o',markersize='4',color='r') 
    plt.ylabel('J2')
    plt.xlabel('J1')
    plt.legend(loc="best")
    plt.savefig(name+'.png')
    print("График сохранён как:",name+'.png')
    plt.show()

def random_gen(n):
    arr = []
    for i in range(n):
        u1 = random.uniform(0,79)
        u2 = random.uniform(0,79)
        f1 = 0.2*(u1-70)**2+0.8*(u2-20)**2
        f2 = 0.2*(u1-10)**2+0.8*(u2-70)**2
        arr.append(Point(f1,f2,i+1))
    return Points(arr)



if __name__ == '__main__':
    name = str(int(time.time()))
    if len(sys.argv) == 2:
        n = sys.argv[1]
    else:
        print("ERROR: incorrect args")
        quit()
    points = random_gen(int(n))
    points.exclude_unoptimal()
    points.find_omega()
    plot(points)
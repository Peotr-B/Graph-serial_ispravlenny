#!/usr/local/bin/python
# -*- coding: utf-8 -*-
#
# переработанный http://purepython.narod.ru/tkinter.html
#
#N.B! https://mail.python.org/pipermail/tkinter-discuss/2011-August/002916.html
# tkMessageBox has been renamed to messagebox in Python 3.x. Also this
# module is not available in tkinter. Therefore:
# [code]
# >>> from tkinter import messagebox
# >>> messagebox.showwarning("hello", "world")
# [/code]

import sys
import os

from math import *
from tkinter import *
from tkinter import messagebox  #Нужно ли? Ведь уже from tkinter import *

#
# для работы с COM-портом нужна библиотека pySerial,
# кроме того, под винду понадобится еще pyWin32
#
import serial
ser = 0

#ser.close() #Для работы при повторном включении!
# либо делать "перезапуск ядра", либо использовать Visual Code,
# либо перезапускать Arduino

SERIAL_PORT = 'COM6'
#SERIAL_SPEED = 38400
SERIAL_SPEED = 9600

codepage = 'utf-8'
debug = 0	# Уровень отладки 0 значит, что никаких сообщений не будет выводиться 
			# см. http://www.cnc-club.ru/wiki/index.php/LinuxCNC_Integrators_Manual_%D0%93%D0%BB%D0%B0%D0%B2%D0%B0_IV_-_%D0%A4%D0%B0%D0%B9%D0%BB_INI
#data_file = 't.txt'
#data_file = 't.txt'
#data_file = 'D:/PyFile/USO/Cito!/Ardu-Pyton_graf/TablSIN__.txt'
data_file = 'D:\WinPython\FilePy\Graph-serial_ispravlenny\TablSIN__.txt'
#data_file = 'D:\WinPython\FilePy\Graph-serial_ispravlenny\data_sin.txt'
data_sin = 'D:\WinPython\FilePy\Graph-serial_ispravlenny\data_sin.txt'	#Расположение введенного мной контрольного файла


class App:
    age=0
    data0=0
    data1=0
    itable=[]

    def __init__(self):
        self.window = Tk()
        self.window.title("Oscilloscope")
        self.window.resizable(0, 0)     #Запрещает разворот окна на весь экран

        self.workspace = Frame(self.window, relief=FLAT)
        self.workspace.grid(row=0, column=0)

        self.G = Canvas(self.window, borderwidth=2, relief=GROOVE)
        self.G.grid(row=1, column=0)
        self.G.config(width=500, height=500, background="black")

        self.gbtn = Button(self.workspace, text=u"Start")
        self.gbtn["command"] = self.draw
        self.gbtn.grid(row=3, column=10)

        self.gbtn = Button(self.workspace, text=u"Serial")
        self.gbtn["command"] = self.get_data_from_com
        self.gbtn.grid(row=3, column=11)

        self.gbtn = Button(self.workspace, text=u"File")
        self.gbtn["command"] = self.draw_file
        self.gbtn.grid(row=3, column=12)

        self.gbtn = Button(self.workspace, text=u"Quit")
        self.gbtn["command"] = self.quit
        self.gbtn.grid(row=3, column=13)

        self.draw_axis()
        #self.get_data(data_file)
        #self.draw()
        self.window.mainloop()

    def quit(self):
        if (ser):
            ser.close()
        self.window.destroy()

    def draw(self):				#============ Start ===============
        fml = str("sin(x)")
        x1 = float("-10")   #регулировка длины развёртки (частоты)
        x2 = float("10")
        #x1 = float("-100")
        #x2 = float("100")
        
        #y1 = float("-10")
        #y2 = float("10")
        y1 = float("-1.1")  #регулировка усиления (амплитуды)
        y2 = float("1.1")
        
#        if x1>=x2:
#            showerror("Error", u"StartX должно быть меньше, чем FinishX")
#            return

        dx = (x2-x1)/500
        dy = (y2-y1)/500    #не используется?
        coords = []

        file_ = open(data_sin, 'w')	#Я ввёл для создания контрольного файла

        try:
            x = x1
            y = eval(fml)   #функция eval(), которая выполняет строку с кодом 
                            #и возвращает результат выполнения
                            #ВНИМАНИЕ! ф-ю  eval() нужно использовать с 
                            #осторожностью, поскольку имеется риск нанести 
                            #непоправимый вред ПК: 
                            #https://habr.com/ru/post/221937/
            
        except SyntaxError:
            showerror("Error", u"Ошибка в формуле!")
            return
        except:
            pass

        for i in range(500):
            x = x1 + dx*i
            #print (x)
            try:
                y = eval(fml)
                print(y)
                file_.write(str(y) + '\n')	#Я ввёл для создания контрольного файла
            except:
                j = None
            else:
                j=500-500*(y-y1)/(y2-y1)
            coords.append(j)
        file_.close()		#Я ввёл для создания контрольного файла

        self.G.delete("all")

        ax = 500*(-x1)/(x2-x1)
        self.G.create_line(ax, 0, ax, 500, fill='brown')
        ay = 500 - 500*(-y1)/(y2-y1)
        self.G.create_line(0, ay, 500, ay, fill='brown')

        for i in range(499):
            a = coords[i]
            b = coords[i+1]
            if a!=None and b!=None:
                self.G.create_line(i,a,i+1,b,fill="green")

    def draw_file(self):		#============= File ===================
        self.get_data(data_file)
        return

    def draw_axis(self):
        x1 = float("-10")
        x2 = float("10")
        #y1 = float("-10")
        #y2 = float("10")
        
        #y1 = float("-1.1")
        #y2 = float("1.1")
        
        y1 = float("-1100")
        y2 = float("1100")
        
        
        ax = 500*(-x1)/(x2-x1)
        
        #ax = 1000*(-x1)/(x2-x1)
        
        self.G.create_line(ax, 0, ax, 500, fill='brown')
        #ay = 500 - 500*(-y1)/(y2-y1)
        
        #ay = 500 - 500*(-y1)/(y2-y1)
        
        ay = 500 - 500*(-y1)/(y2-y1)
        
        self.G.create_line(0, ay, 500, ay, fill='brown')
        
        #self.G.create_line(0, ay, 500, ay, fill='brown')
        return

    def drawdata(self,data):		#============= Serial & File=============
        #print (data)
        #lid = self.G.create_line(0,0,500,500,fill="white")
        
        #x1 = float("-10")
        #x2 = float("10")
        #(не используется!)
                        
        y1 = float("-1100")
        y2 = float("1100")
        
        center=0     #смещение по оси X
        #j=data-150
               
        #j=data+500     #смещение по оси Y
        
        j=500-500*(data-y1)/(y2-y1) #масштаб и смещение по оси Y

        self.itable.append(j)

        i = self.age
        a = self.itable[i-1]
        b = self.itable[i]

        #print i-1,a
#        print i,b
        #if a!=None and b!=None:
        #lid=self.G.create_line(i-1+center,a,i+center,b,fill="green")
        
        lid=self.G.create_line(i-1+center,a,i+center,b,fill="blue")
        
        #self.G.create_line(0,0,i,b,fill="white")
        #print lid
        self.age=self.age+1
        print (data)
        return None

    def get_data(self,file_name_):	#================= File ==============
        #
        # read data from file
        #
        self.G.delete("all")
        self.draw_axis()

        i=0
        j=0
        
        self.age=0
        self.itable=[]
        
        try:
            f=open(file_name_,'r')
            print ("[i] open "+file_name_,)
        except IOError:
            print ("[!] Cant open file "+file_name_)
            return -1
        print ("..ok")
        lines=len(f.readlines())
        #lines=len(f.read())
        f.seek(0)
        print (lines)
        data=0
        for l in range(0,lines):
            data=float(f.readline())
            #data=float(f.readline()) / 1

            self.drawdata(data)
        f.close()

        #self.age=0
        #self.itable=[]

        return None

    def get_data_from_com(self):	#================= Serial ===============
        self.G.delete("all")
        self.draw_axis()
        self.age=0
        self.itable=[]

        ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)

        #while 1:
        for i in range(0,500):
            #s = ser.read()
            s = ser.readline().strip()
            #self.drawdata(float(s) / 1)
            self.drawdata(float(s))

        return None
"""    
    def quit(self):
        if (ser):
            ser.close()
        self.window.destroy()
"""
#App()

#-----------------------------------------
#
# begin here :)
#

def main():
    print ("[i] Start testing...")
    app = App()

    print ("[i] done.")
    return None
if __name__ == "__main__":
    main()

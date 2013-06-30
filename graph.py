from math import *
from random import random

class Ploter:
    def __init__(self, equacao, inicio, fim, passos, passosy = None, sensibilidade_derivada = 0.2):
        self.eq_str = equacao
        self.equacao = lambda x: eval(equacao)
        self.extremos = (inicio, fim)
        self.passos = passos
        self.dP = (fim - inicio) / float(passos)
        if passosy == None:
            self.passosy = passos
        else:
            self.passosy = passosy
        self.sensibilidade_derivada = sensibilidade_derivada

    def gerar_imagens(self):
        self.ims = []
        for i in range(self.passos):
            x = i * self.dP + self.extremos[0]
            try:
                y = self.equacao(x)
            except:
                y = None
            self.ims.append(y)
        mini = max(self.ims)
        for img in self.ims[1:]:
            if img == None:
                continue
            if img < mini:
                mini = img
        self.extremosy = (mini, max(self.ims))
        delta = self.extremosy[1] - self.extremosy[0]
        if delta == 0:
            delta = 0.0001
        self.ims_normalizadas = [int(round((i - self.extremosy[0]) / float(delta) * self.passosy)) for i in self.ims if i != None]
        self.ims_normalizadas.reverse()
        self.dPy = (self.extremosy[1] - self.extremosy[0]) / float(self.passosy)

    def gerar_matriz(self):
        self.x_cord_lines = len(str(self.passos))
        self.matriz = [[" " for i in range(self.passos)] for j in range(self.passosy + 2 + self.x_cord_lines)]
        for i, j in enumerate(self.ims_normalizadas):
            if j == None: continue
            x = self.extremos[1] - (i + 1) * self.dP
            d = self.derivada(x)
            if d > self.sensibilidade_derivada:
                self.matriz[j + self.x_cord_lines + 1][i] = "/"
            elif d < -self.sensibilidade_derivada:
                self.matriz[j + self.x_cord_lines + 1][i] = "\\"
            else:
                self.matriz[j + self.x_cord_lines + 1][i] = "-"
        for i in range(self.passos):
            self.matriz[self.x_cord_lines][i] = "-"
        for i in range(self.x_cord_lines):
            for j in range(self.passos):
                value = ((j / (10 ** (i))) % (10 ** (i + 1)))
                if value == 0 and j != 0 and i != 0:
                    continue
                self.matriz[i][self.passos - j - 1] = value
        

    def printa(self):
        print "y =", self.eq_str
        for i, linha in enumerate(self.matriz[::-1]):
            if i > self.passosy - self.x_cord_lines + 3:
                y_cord = " " * 10
            elif i == self.passosy - self.x_cord_lines + 3:
                y_cord = "-" * 10
            else:
                y_cord = "%.2e" % (self.extremosy[1] - self.dPy * i)
                y_cord = y_cord + " " * (10 - len(y_cord))
            print y_cord , "|",
            for char in linha[::-1]:
                print char,
            if i != self.passosy + 3:
                print
        print "(* %.2f + %.2f)" % (self.dP, self.extremos[0])

    def derivada(self, x):
        deltax = self.dP / 1e10
        deltay =self.equacao(x + deltax) - self.equacao(x)
        m = deltay / deltax
        return m

    def achar_raiz(self, init):
        x_atual = init
        dx = 0
        for i in range(1000):
            d = self.derivada(x_atual)
            y = self.equacao(x_atual)
            if d == 0:
                return
            if abs(y) < 1e-5 and dx < 1e-10:
                return x_atual
                break
            nx = x_atual - y / d
            dx = abs(x_atual - nx)
            x_atual = nx
        return

    def pegar_raiz_qualquer(self):
        for i in range(200):
            init = random() * (self.extremos[1] - self.extremos[0]) + self.extremos[0]
            try:
                d = self.achar_raiz(init)
            except:
                d = None
            if d != None:
                return d
        return d

    def plot(self):
        self.gerar_imagens()
        self.gerar_matriz()
        self.printa()

p = Ploter("sin(x + 1)", -10,10, 80, 30, 0.8)
p.plot()
print "Uma raiz ->", p.pegar_raiz_qualquer()
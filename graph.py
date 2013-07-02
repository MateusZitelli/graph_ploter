# coding:utf-8
from math import *
from random import random

class Ploter:
    def __init__(self, equacao, inicio, fim, passos, passosy = None, sensibilidade_derivada = 0.2):
        self.eq_str = equacao
        self.equacao = lambda x: eval(equacao) #Transforma a string da equação em uma função
        self.extremos = (inicio, fim)
        self.passos = passos
        self.dP = (fim - inicio) / float(passos) #Define o passo em X
        if passosy == None: #Se não for passado valor de passos em y é definido como o número de passos X
            self.passosy = passos
        else:
            self.passosy = passosy
        self.sensibilidade_derivada = sensibilidade_derivada

    def gerar_imagens(self):
        self.ims = [] #Lista das imagens da funçao
        for i in range(self.passos):
            x = i * self.dP + self.extremos[0]
            try: #Tenta rodar a função
                y = self.equacao(x)
            except: #Se der erro define que não existe imagem nesse ponto
                y = None
            self.ims.append(y)
        mini = max(self.ims)
        for img in self.ims: #Acha, a menor imagem, pois o min do python não funciona, selecionando um valor None
            if img == None:
                continue
            if img < mini:
                mini = img
        self.extremosy = (mini, max(self.ims))
        delta = self.extremosy[1] - self.extremosy[0]
        if delta == 0:
            delta = 0.0001
        #Normaliza os valores da imagem entre 0~passosy e arredonda para o inteiro mais próximo para ser usada como índice
        self.ims_normalizadas = [int(round((i - self.extremosy[0]) / float(delta) * self.passosy)) for i in self.ims if i != None]
        self.ims_normalizadas.reverse()
        self.dPy = (self.extremosy[1] - self.extremosy[0]) / float(self.passosy)

    def gerar_matriz(self):
        self.x_cord_lines = len(str(self.passos))
        self.matriz = [[" " for i in range(self.passos)] for j in range(self.passosy + 2 + self.x_cord_lines)]
        for i, j in enumerate(self.ims_normalizadas):
            if j == None:
                continue
            x = self.extremos[1] - (i + 1) * self.dP #Acha o valor de X para encontrar a derivada nesse ponto
            try:
                d = self.derivada(x)
            except:
                d = 0
            if d > self.sensibilidade_derivada: #Escolhe o caracter para representar o ponto dependendo da devivada
                self.matriz[j + self.x_cord_lines + 1][i] = "/"
            elif d < -self.sensibilidade_derivada:
                self.matriz[j + self.x_cord_lines + 1][i] = "\\"
            else:
                self.matriz[j + self.x_cord_lines + 1][i] = "-"
        for i in range(self.passos): #Linha inferior
            self.matriz[self.x_cord_lines][i] = "-"
        for i in range(self.x_cord_lines): #Valores de X
            for j in range(self.passos):
                value = "0" * (self.x_cord_lines - len(str(j))) + str(j)
                value = value[self.x_cord_lines - 1 - i]
                self.matriz[i][self.passos - j - 1] = value
        

    def printa(self):
        print "y =", self.eq_str
        for i, linha in enumerate(self.matriz[::-1]):
            if i > self.passosy - self.x_cord_lines + self.x_cord_lines + 1: #Espaço no canto inferior esquerdo
                y_cord = " " * 10
            elif i == self.passosy - self.x_cord_lines + self.x_cord_lines + 1: #Traços encima do espaço
                y_cord = "-" * 10
            else: #Coordenadas de Y
                y_cord = "%.2e" % (self.extremosy[1] - self.dPy * i)
                y_cord = y_cord + " " * (10 - len(y_cord))
            print y_cord , "|",
            for char in linha[::-1]: #Printa o gráfico
                print char,
            if i != self.passosy + 4: #Pula a linha
                print
        print "(* %.2f + %.2f)" % (self.dP, self.extremos[0])

    def derivada(self, x):
        deltax = self.dP / 1e10
        deltay =self.equacao(x + deltax) - self.equacao(x)
        m = deltay / deltax
        return m

    def achar_raiz(self, init):
        #Método de Newton
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

p = Ploter("sin(x) / x", -10,10, 130,50, 0.2)
p.plot()
print "Uma raiz ->", p.pegar_raiz_qualquer()

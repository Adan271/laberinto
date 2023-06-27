import turtle as trl
import numpy as np
import fractions
import re
from math import acos, pi
import sys, ctypes, os
from datetime import datetime

if not os.path.exists('logs'):
    # if here current thread is stopped and the same dir is created in other thread
    # the next line will raise an exception
    os.makedirs('logs') 
logfile = open('logs/'+str(np.random.randint(999999))+'.log','w')
now = datetime.now().time() # time object

datetime_object = datetime.now()
logfile.write('Nuevo juego: '+str(datetime_object))



# coordinate system size
# si se cambia la relación 1x1 se debería cambiar la pantalla de turtle
WIDTH, HEIGHT = 40, 40 
LAB1 = np.array([
        [[-WIDTH//2,-HEIGHT//2],[-WIDTH//2, HEIGHT//2]],
        [[-WIDTH//2, HEIGHT//2],[ WIDTH//2, HEIGHT//2]],
        [[ WIDTH//2, HEIGHT//2],[ WIDTH//2,-HEIGHT//2]],
        [[ WIDTH//2,-HEIGHT//2],[-WIDTH//2,-HEIGHT//2]],
        [[-15, 20],[-14,-15]],
        # [[  0, 20],[-10,  5]],
        [[  3,-20],[-12,  4]],
        # [[- 3,-11],[- 1,  3]],
        [[  0,-10],[ 20, 10]]
        ])
LAB2 = np.array([
        [[-WIDTH//2,-HEIGHT//2],[-WIDTH//2, HEIGHT//2]],
        [[-WIDTH//2, HEIGHT//2],[ WIDTH//2, HEIGHT//2]],
        [[ WIDTH//2, HEIGHT//2],[ WIDTH//2,-HEIGHT//2]],
        [[ WIDTH//2,-HEIGHT//2],[-WIDTH//2,-HEIGHT//2]],
        [[-15, 20],[-15,-15]],
        [[ -3,-20],[ -3,  7]],
        [[  2, -3],[  2, 20]],
        [[ 17,-20],[ 17, 18]]
        # [[  0,-10],[ 20, 10]]
        ])
END = np.array([
    [[ 18.0,-18.5],[ 18.5,-19.0]],
    [[ 18.5,-19.0],[ 18.0,-19.5]],
    [[ 18.0,-19.5],[ 17.5,-19.0]],
    [[ 17.5,-19.0],[ 18,-18.5]]
    ])

easy = input('Modo facil? (s/n) ')
if easy in ['si','sí','Si','Sí','SI','SÍ','S','s','Yes','Y','YES','yes','y']:
    easy = True
else:
    easy = False
logfile.write('\neasy = '+str(easy))
level = 4
print('Determina el nivel (4,5,6,7):')
while True:
    level = input('nivel = ')
    try:
        level = int(level)
        if level > 7:
            print('El nivel máximo es 7')
        elif level<4:
            print('Debes proporcionar un número entero mayor a 4')
        else:
            break
    except:
        print('Debes proporcionar un número entero')
logfile.write('\nlevel = '+str(level))
while True:
    p = np.sort(np.random.randint(-15,18,level))
    aux = [p[i+1]-p[i] for i in range(level-1)]
    if min(aux)>3:
        break
alturas = np.random.randint(20+level,38,level)
orientacion = np.random.randint(0,2,level,dtype=bool)
orientacion = np.array(([1,0]*level)[:level],dtype=bool)
orientacion[-1] = False
LAB = [
        [[-WIDTH//2,-HEIGHT//2],[-WIDTH//2, HEIGHT//2]],
        [[-WIDTH//2, HEIGHT//2],[ WIDTH//2, HEIGHT//2]],
        [[ WIDTH//2, HEIGHT//2],[ WIDTH//2,-HEIGHT//2]],
        [[ WIDTH//2,-HEIGHT//2],[-WIDTH//2,-HEIGHT//2]]
    ]
for i in range(level):
    if orientacion[i]:
        LAB.append([[p[i],20],[p[i],20-alturas[i]]])
    else:
        LAB.append([[p[i],-20+alturas[i]],[p[i],-20]])
LAB = np.array(LAB)
logfile.write('\nLAB = \n')
logfile.write(str(LAB))
# LAB = np.concatenate((LAB1,END),axis=0)
# LAB = np.concatenate((LAB2,END),axis=0)
LAB = np.concatenate((LAB,END),axis=0)
logfile.write('\nEND = \n')
logfile.write(str(END))
EPS = 0.00001

def rational(v):
    if abs(int(v)-v) < EPS:
        return str(int(v))
    else:
        f = fractions.Fraction(abs(v)).limit_denominator()
        sol = ''
        if v<-EPS:
            sol+='-'
        if f.denominator == 1:
            sol+=str(f.numerator)
        elif f.denominator<1000:
            sol+=str(f.numerator) + '/' + str(f.denominator)
        else:
            sol+=str(np.round(abs(v), decimals=3))
        return sol


def plot_lab(t,LAB,END):
    t.pensize(width=5)
    for p1,p2 in LAB:
        t.goto(p1)
        t.pendown()
        t.goto(p2)
        t.penup()
    t.pencolor('purple')
    for p1,p2 in END:
        t.goto(p1)
        t.pendown()
        t.goto(p2)
        t.penup()

def axis(t, distance,distance2, tick):
    t.pensize(width=0.5)
    position = t.position()
    t.pendown()
    i=1
    for _ in range(0, distance // 2, tick):
        t.forward(tick)
        t.dot()
        t.write(str(i))
        t.pensize(width=0.15)
        p = t.position()
        t.left(90)
        t.forward(distance2/2)
        t.setposition(p)
        t.backward(distance2/2)
        t.right(90)
        t.setposition(p)
        t.pensize(width=0.5)
        i+=1
    t.setposition(position)
    i = -1
    for _ in range(0, distance // 2, tick):
        t.backward(tick)
        t.pensize(width=0.15)
        p = t.position()
        t.left(90)
        t.forward(distance2/2)
        t.setposition(p)
        t.backward(distance2/2)
        t.setposition(p)
        t.pensize(width=0.5)
        t.dot()
        t.right(90)
        t.write(str(i))
        i-=1

class Player:
    def __init__(self,name,position,right_side,segment,turtle):
        self.name = name
        self.position = np.array(position)
        self.segment = segment
        self.right_side = right_side
        self.turtle = turtle
        self.angle = 270
    def __str__(self):
        if self.right_side:
            side = 'dr'
        else:
            side = 'iz'
        return(self.name+': '+'['+
            rational(self.position[0])+','+
            rational(self.position[1])+']')
    def is_valid_move(self,m,n,LAB):
        return self.position[1] < (m*self.position[0]+n+EPS) and self.position[1] > (m*self.position[0]+n-EPS)
    def move(self,m,n,LAB):
        # y = mx+n
        INTbool = np.zeros(LAB.shape[0],dtype=bool)
        INT = np.zeros((LAB.shape[0],LAB.shape[1]))
        for i,(p1,p2) in enumerate(LAB):

            if i == self.segment:
                INT[i] == self.position
                continue
            x1,y1 = p1
            x2,y2 = p2
            if abs(x2-x1)<EPS:
                x0,y0 = x1,m*x1+n
                if y1<=y2:
                    INTbool[i] = y1<=y0 and y0<=y2
                else:
                    INTbool[i] = y2<=y0 and y0<=y1
                lamb = (y0-y1)/(y2-y1)
                INT[i] = [x0,y0]
            else:
                aux = (y2-y1)/(x2-x1)
                #si las rectas son paralelas pasamos
                if abs(aux-m)<EPS: continue
                x0 = (-n-x1*aux+y1)/(m-aux)
                y0 = m*x0+n
                lamb = (x0-x1)/(x2-x1)
                INTbool[i] = lamb<(1+EPS) and lamb>-EPS
                INT[i] = [x0,y0]
            if INTbool[i]:
                INTbool[i] = False
                p1,p2 = LAB[self.segment]
                x1,y1 = p1
                x2,y2 = p2
                if abs(x2-x1)<EPS:
                    if (self.right_side and (y2-y1)*x1<x0*(y2-y1) or (not(self.right_side) and (y2-y1)*x1>x0*(y2-y1))):
                        INTbool[i] = True
                else:
                    aux = (y2-y1)/(x2-x1)
                    if (self.right_side and y0<(aux*(x0-x1)+y1)) or (not(self.right_side) and y0>(aux*(x0-x1)+y1)):
                        INTbool[i] = True
        if sum(INTbool)==0:
            #la recta nos deja en el mismo punto
            return
        try:
            i0 = np.arange(INT.shape[0])[INTbool][np.sum((INT-self.position)**2,axis=1)[INTbool].argmin()]
        except:
            print(INT)
            print(INTbool)
            print(np.arange(INT.shape[0])[INTbool])
            print(np.sum((INT-self.position)**2,axis=1))
            print(np.sum((INT-self.position)**2,axis=1)[INTbool].argmin())
            raise

        x0,y0 = self.position #posicion anterior
        v = INT[i0]-self.position
        angle = acos(v[0]/np.sqrt(np.sum(v**2)))
        angle = 180*angle/pi
        p1,p2 = LAB[i0]
        x1,y1 = p1
        x2,y2 = p2
        if abs(x2-x1)<EPS:
            self.right_side = (y2-y1)*x0>(y2-y1)*x1
        else:
            aux = (y2-y1)/(x2-x1)
            self.right_side = y0<(aux*(x0-x1)+y1)
        #actualizamos posicion y demas
        self.position = INT[i0]
        self.segment = i0
        self.angle = angle

    def ask_for_move(self,logfile,easy,intento=1,max_inentos=3):
        while True:
            m = input('m = ')
            if re.findall(r'-?[0-9]+/[0-9]+',m) != []:
                m = int(re.findall(r'-?[0-9]+(?=/)',m)[0])/int(re.findall(r'(?<=/)[0-9]+',m)[0])
                break
            elif m=='exit':
                logfile.write('\nSalimos del juego')
                sys.exit("Salimos del juego")
            else:
                try:
                    m = float(m)
                    break
                except:
                    print('m tiene que ser un numero')
                    logfile.write('\nerror: m tiene que ser un numero')
                    continue
        while True:
            n = input('b = ')
            if re.findall(r'-?[0-9]+/[0-9]+',n) != []:
                n = int(re.findall(r'-?[0-9]+(?=/)',n)[0])/int(re.findall(r'(?<=/)[0-9]+',n)[0])
                logfile.write('\nb = '+rational(n))
                break
            elif n=='exit':
                logfile.write('\nSalimos del juego')
                sys.exit("Salimos del juego")
            elif n=='' and easy:
                n = self.position[1]-m*self.position[0]
                print('(b = '+rational(n)+')')
                logfile.write('\ngeneramos b = '+rational(n))
                break
            else:
                try:
                    n = float(n)
                    logfile.write('\nb = '+rational(n))
                    break
                except:
                    print('b tiene que ser un numero')
                    logfile.write('\nerror: b tiene que ser un numero')
                    continue
        if self.is_valid_move(m,n,LAB):
            return m,n
        else:
            if intento+1>max_inentos:
                print('Maximo de intentos, perdistes el turno...')
                logfile.write('\nMaximo de intentos, perdistes el turno...')
                return 
            else:
                print('La recta debe pasar por la tortuga (te quedan '+str(max_inentos-intento)+')')
                logfile.write('\nLa recta debe pasar por la tortuga (te quedan '+str(max_inentos-intento)+')')
                return self.ask_for_move(logfile,easy,intento=intento+1)

    def draw_move(self):
        # self.turtle.getscreen().getcanvas().postscript(file='borrar.eps')
        self.turtle.setheading(self.angle)
        self.turtle.goto(self.position)
        self.turtle.dot()
        self.turtle.setheading(-self.angle)


class Game:
    def __init__(self,n_players,positions_init,end_point,segment,right_side,logfile,turn=0,easy=True):
        self.n_players = n_players
        players = []
        colors = ['blue','red','green','cyan','magenta','yellow','black','white']
        positions_init = np.array(positions_init)
        segment = segment
        for i in range(n_players):
            turtle = trl.Turtle(visible=True)
            turtle.shape("turtle")
            turtle.pensize(width=5)
            turtle.penup()
            turtle.goto(positions_init[i])
            turtle.pendown()
            turtle.pencolor(colors[i])
            turtle.dot(10)
            players.append(Player(name='Jugador '+str(i+1) +' ('+colors[i]+')',
                                  position = positions_init[i],
                                  right_side = right_side,
                                  segment = segment,
                                  turtle=turtle))

        self.players = players
        self.end_point = np.array(end_point)
        self.logfile = logfile
        self.turn = turn
        self.easy = easy
    def play(self):
        print('Turno de '+str(self.players[self.turn]))
        print('Introduce la recta y=mx+b')
        self.logfile.write('\nTurno de '+str(self.players[self.turn]))

        sol = self.players[self.turn].ask_for_move(logfile = self.logfile,easy=self.easy)
        if sol == None:
            if self.turn == self.n_players-1:
                self.turn = 0
            else:
                self.turn += 1
            self.play()
        else:
            m,n = sol
            self.players[self.turn].move(m,n,LAB)
            self.players[self.turn].draw_move()
            print('('+str(self.players[self.turn]))
            if self.players[self.turn].segment>=(LAB.shape[0]-4):
                print('Ha ganado el '+self.players[self.turn].name)
                self.logfile.write('\nHa ganado el '+self.players[self.turn].name)
                print('Enhorabuena!')
                input()
            else:
                if self.turn == self.n_players-1:
                    self.turn = 0
                else:
                    self.turn += 1
                self.play()

screen = trl.Screen()
try:
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen.setup(int(0.9*min(screensize)), 
                 int(0.9*min(screensize))) 
except:
    screen.setup(1080, 
                 1080)
screen.setworldcoordinates(-WIDTH/2, -HEIGHT/2, WIDTH//2, HEIGHT/2)

ivy = trl.Turtle(visible=False)
ivy.speed('fastest')
ivy.penup()
axis(ivy, WIDTH,HEIGHT, 1)

ivy.penup()
ivy.home()
ivy.setheading(90)
axis(ivy, WIDTH,HEIGHT, 1)

plot_lab(ivy,LAB,END)

print('Determina el número de jugadores:')
while True:
    n_players = input('n = ')
    try:
        n_players = int(n_players)
        if n_players > 5:
            print('El máximo número de jugadores permitido es 5')
        elif n_players<1:

            print('Debes proporcionar un número entero mayor a 0')
        else:
            break
    except:
        print('Debes proporcionar un número entero')

logfile.write('\nn_players = '+str(n_players))

d = 5/(n_players+1)
positions_init = []
for i in range(n_players):
    positions_init.append([int(-20+d*(i+1)),20])
logfile.write('\npositions_init = \n')
logfile.write(str(positions_init)+'\n')
logfile.write('\n Empieza el juego:')
g = Game(n_players=n_players,
    positions_init=positions_init,
    end_point=[18,-19],
    segment=1,
    right_side=True,
    logfile = logfile,
    easy=easy)
g.play()
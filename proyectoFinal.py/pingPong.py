import pygame
from pygame.locals import *
import pygame_menu as pm
import random
import os

ruta_base = os.path.dirname(__file__) 

#Colores de la pelota
rutaImagenPongNaranja = os.path.join(ruta_base, "pongNaranja.png")
rutaImagenPongAzul = os.path.join(ruta_base, "pongAzul.png")
rutaImagenPongVerde = os.path.join(ruta_base, "pongVerde.png")
rutaImagenPongRojo = os.path.join(ruta_base, "pongRojo.png")
rutaImagenPongNegro = os.path.join(ruta_base, "pongNegro.png")
rutaImagenPongAmarillo = os.path.join(ruta_base, "pongAmarillo.png")
rutaImagenPongMorado = os.path.join(ruta_base, "pongMorado.png")
pong=rutaImagenPongNaranja


rutaImagenRaquetaNegra = os.path.join(ruta_base, "raquetaNegra.png")
rutaImagenRaquetaAzul = os.path.join(ruta_base, "raquetaAzul.png")
rutaImagenRaquetaNaranja = os.path.join(ruta_base, "raquetaNaranja.png")
rutaImagenRaquetaVerde = os.path.join(ruta_base, "raquetaVerde.png")
rutaImagenRaquetaRojo = os.path.join(ruta_base, "raquetaRojo.png")
rutaImagenRaquetaMorado = os.path.join(ruta_base, "raquetaMorado.png")
rutaImagenRaquetaAmarillo = os.path.join(ruta_base, "raquetaAmarillo.png")
raquetaB = rutaImagenRaquetaNegra



winHori = 800
winVert = 600
fps = 75
white = (255, 255, 255)
black = (0, 0, 0)

class pelotaP:
    def __init__(self, ficheroImagen):
        self.imagen = pygame.image.load(pong).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = winHori / 2 - self.ancho / 2
        self.y = winVert / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.puntuacion = 0
        self.puntuacion_maquina = 0

    def cambiar_color(self, color):
        global pong
        if color == "Naranja":
            pong = rutaImagenPongNaranja
        elif color == "Azul":
            pong = rutaImagenPongAzul
        elif color == "Verde":
            pong = rutaImagenPongVerde
        elif color == "Negro":
            pong = rutaImagenPongNegro
        elif color == "Rojo":
            pong = rutaImagenPongRojo
        elif color == "Amarillo":
            pong = rutaImagenPongAmarillo
        elif color == "Morado":
            pong = rutaImagenPongMorado
        self.imagen = pygame.image.load(pong).convert_alpha()

    def movimiento(self):
        self.x += self.dir_x
        self.y += self.dir_y

    def reiniciar(self):
        self.x = winHori / 2 - self.ancho / 2
        self.y = winVert / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])

    def rebotar(self):
        if self.x <= -self.ancho:
            self.reiniciar()
            self.puntuacion_maquina += 1
        if self.x >= winHori:
            self.reiniciar()
            self.puntuacion += 1
        if self.y <= 0 or self.y + self.alto >= winVert:
            self.dir_y = -self.dir_y


class raqueta:
    def __init__(self):
        self.imagen = pygame.image.load(raquetaB).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = 0
        self.y = winVert / 2 - self.alto / 2
        self.dir_y = 0

    def movimiento(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= winVert:
            self.y = winVert - self.alto

    def movimiento_maquina(self, pelota,dificultad_actual):
        
        if self.y > pelota.y:
            self.dir_y = -dificultad_actual["velocidad"]
        elif self.y < pelota.y:
            self.dir_y = dificultad_actual["velocidad"]
        else:
            self.dir_y = 0
        self.y += self.dir_y

    def golpear(self, pelota):
        if (
            pelota.dir_x < 0 and  # La pelota se está moviendo hacia la raqueta
            pelota.x + pelota.dir_x < self.x + self.ancho and  # Cruza el lado derecho de la raqueta
            pelota.x + pelota.ancho > self.x and  # Está dentro del rango horizontal de la raqueta
            pelota.y + pelota.alto > self.y and  # Está dentro del rango vertical de la raqueta
            pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho
            pelota.dir_y*=1.1
            pelota.dir_x*=1.1

    def golpear_maquina(self, pelota):
        if (
            pelota.dir_x > 0 and  # La pelota se está moviendo hacia la raqueta
            pelota.x + pelota.dir_x + pelota.ancho > self.x and  # Cruza el lado izquierdo de la raqueta
            pelota.x < self.x + self.ancho and  # Está dentro del rango horizontal de la raqueta
            pelota.y + pelota.alto > self.y and  # Está dentro del rango vertical de la raqueta
            pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - pelota.ancho
            pelota.dir_y*=1.1
            pelota.dir_x*=1.1

    def cambiar_color_raqueta(self, colorR):
        global raquetaB
        if colorR == "Naranja":
            raquetaB = rutaImagenRaquetaNaranja
        elif colorR == "Azul":
            raquetaB = rutaImagenRaquetaAzul
        elif colorR == "Verde":
            raquetaB = rutaImagenRaquetaVerde
        elif colorR == "Negro":
            raquetaB = rutaImagenRaquetaNegra
        elif colorR == "Rojo":
            raquetaB = rutaImagenRaquetaRojo
        elif colorR == "Amarillo":
            raquetaB = rutaImagenRaquetaAmarillo
        elif colorR == "Morado":
            raquetaB = rutaImagenRaquetaMorado
        self.imagen = pygame.image.load(raquetaB).convert_alpha()
            


def main():
    #Inicio y posición de raquetas
    pygame.init()
    win = pygame.display.set_mode((winHori, winVert))
    pygame.display.set_caption("Ping Pong")
    pelota = pelotaP("pong.png")
    fuente = pygame.font.Font(None, 60)
    raqueta_1 = raqueta()
    raqueta_1.x = 60
    raqueta_2 = raqueta()
    raqueta_2.x = winHori - 60 - raqueta_2.ancho

    dificultad_actual = {"velocidad": 5}

    def set_difficulty(value, difficulty):
        if difficulty == "Fácil":
            dificultad_actual["velocidad"] = 5
        elif difficulty == "Medio":
            dificultad_actual["velocidad"] = 8
        elif difficulty == "Difícil":
            dificultad_actual["velocidad"] = 15
        elif difficulty == "Muy difícil":
            dificultad_actual["velocidad"] = 18

    def set_color(value, color):
        pelota.cambiar_color(color)

    def set_colorRaqueta(value, colorR):
        raqueta_1.cambiar_color_raqueta(colorR)
        raqueta_2.cambiar_color_raqueta(colorR)

    # Menú de configuración
    settings = pm.Menu(title="Configuración", width=winHori, height=winVert)
    settings.add.selector("Dificultad: ", [("Fácil", "Fácil"), ("Medio", "Medio"), ("Difícil", "Difícil"), ("Muy difícil", "Muy difícil")],
                          onchange=set_difficulty)
    settings.add.selector("Color pelota: ", [("Naranja", "Naranja"), ("Azul", "Azul"),("Verde","Verde"),("Negro","Negro"),("Rojo","Rojo"),("Amarillo","Amarillo"), ("Morado","Morado")],
                          onchange=set_color)
    settings.add.selector("Color raqueta: ", [("Negro","Negro"),("Naranja", "Naranja"), ("Azul", "Azul"),("Verde","Verde"),("Rojo","Rojo"),("Amarillo","Amarillo"), ("Morado","Morado")],
                          onchange=set_colorRaqueta)
    
  
    # Menú principal
    main_menu = pm.Menu(title="Menú principal", width=winHori, height=winVert,)
    main_menu.add.button("Jugar", lambda: start_game(win, pelota, raqueta_1, raqueta_2, fuente, dificultad_actual))
    main_menu.add.button("Configuración", settings)
    main_menu.add.button("Salir", pm.events.EXIT)


    # Mostrar el menú principal
    main_menu.mainloop(win)

#Función de inicio de juego
def start_game(win, pelota, raqueta_1, raqueta_2, fuente, dificultad_actual):
    jugando = True
    while jugando:
        pelota.movimiento()
        pelota.rebotar()
        raqueta_1.movimiento()
        raqueta_2.movimiento_maquina(pelota, dificultad_actual)
        raqueta_1.golpear(pelota)
        raqueta_2.golpear_maquina(pelota)

        win.fill(white)
        win.blit(pelota.imagen, (pelota.x, pelota.y))
        win.blit(raqueta_1.imagen, (raqueta_1.x, raqueta_1.y))
        win.blit(raqueta_2.imagen, (raqueta_2.x, raqueta_2.y))
        text = f"{pelota.puntuacion} : {pelota.puntuacion_maquina}"
        letrero = fuente.render(text, False, black)
        win.blit(letrero, (winHori / 2 - fuente.size(text)[0] / 2, 50))

        for event in pygame.event.get():
            if event.type == QUIT:
                jugando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = -8
                if event.key == pygame.K_s:
                    raqueta_1.dir_y = 8
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    raqueta_1.dir_y = 0

        pygame.display.flip()
        pygame.time.Clock().tick(fps)
    pygame.quit()


if __name__ == "__main__":
    main()

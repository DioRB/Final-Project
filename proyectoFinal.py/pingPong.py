import pygame
from pygame.locals import *
import random
import os

ruta_base = os.path.dirname(__file__)  # Directorio del script actual
ruta_imagen = os.path.join(ruta_base, "pong.png")  # Construye la ruta completa
ruta_imagen_raqueta = os.path.join(ruta_base, "raqueta.png")  # Construye la ruta completa

winHori = 800 #Tamaño de la ventana en horizontal
winVert = 600 #Tamaño de la ventana en vertical
fps = 75
white = (255, 255, 255)
black = (0, 0, 0)

class pelotaP:
    def __init__(self, ficheroImagen):
        self.imagen = pygame.image.load(ruta_imagen).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = winHori / 2 - self.ancho / 2
        self.y = winVert / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.puntuacion = 0
        self.puntuacion_maquina = 0

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
        self.imagen = pygame.image.load(ruta_imagen_raqueta).convert_alpha()
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

    def movimiento_maquina(self, pelota):
        if self.y > pelota.y:
            self.dir_y = -8
        elif self.y < pelota.y:
            self.dir_y = 8
        else:
            self.dir_y = 0
        self.y += self.dir_y

    def golpear(self, pelota):
        if (
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho
            pelota.dir_y*=1.1
            pelota.dir_x*=1.1

    def golpear_maquina(self, pelota):
        if (
            pelota.x + pelota.ancho > self.x
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - pelota.ancho
            pelota.dir_y*=1.1
            pelota.dir_x*=1.1
            


def main():
    pygame.init()
    win = pygame.display.set_mode((winHori, winVert))
    pygame.display.set_caption("Ping Pong")
    pelota = pelotaP("pong.png")
    fuente = pygame.font.Font(None, 60)
    raqueta_1 = raqueta()
    raqueta_1.x = 60
    raqueta_2 = raqueta()
    raqueta_2.x = winHori - 60 - raqueta_2.ancho

    jugando = True
    while jugando:
        pelota.movimiento()
        pelota.rebotar()
        raqueta_1.movimiento()
        raqueta_2.movimiento_maquina(pelota)
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

#Librerias
import pygame
from pygame.locals import *
import pygame_menu as pm
import random
import os


ruta_base = os.path.dirname(__file__)  #Encontrar las imagenes

iconRute = os.path.join(ruta_base, "icon.jpg")

#Colores de la pelota
rutaImagenPongNaranja = os.path.join(ruta_base, "pongNaranja.png")
rutaImagenPongAzul = os.path.join(ruta_base, "pongAzul.png")
rutaImagenPongVerde = os.path.join(ruta_base, "pongVerde.png")
rutaImagenPongRojo = os.path.join(ruta_base, "pongRojo.png")
rutaImagenPongNegro = os.path.join(ruta_base, "pongNegro.png")
rutaImagenPongAmarillo = os.path.join(ruta_base, "pongAmarillo.png")
rutaImagenPongMorado = os.path.join(ruta_base, "pongMorado.png")
pong=rutaImagenPongNaranja

#Colores de las raquetas
rutaImagenRaquetaNegra = os.path.join(ruta_base, "raquetaNegra.png")
rutaImagenRaquetaAzul = os.path.join(ruta_base, "raquetaAzul.png")
rutaImagenRaquetaNaranja = os.path.join(ruta_base, "raquetaNaranja.png")
rutaImagenRaquetaVerde = os.path.join(ruta_base, "raquetaVerde.png")
rutaImagenRaquetaRojo = os.path.join(ruta_base, "raquetaRojo.png")
rutaImagenRaquetaMorado = os.path.join(ruta_base, "raquetaMorado.png")
rutaImagenRaquetaAmarillo = os.path.join(ruta_base, "raquetaAmarillo.png")
raquetaB = rutaImagenRaquetaNegra

#Musica y sonidos
pygame.mixer.init()
sonido_golpe = pygame.mixer.Sound(os.path.join(ruta_base, "golpe.mp3"))
sonido_punto = pygame.mixer.Sound(os.path.join(ruta_base, "punto.mp3"))
sonido_fondo = pygame.mixer.Sound(os.path.join(ruta_base, "musica_fondo.mp3"))
sonido_fondo.play(-1)


winHori = 800
winVert = 600
fps = 75
white = (255, 255, 255)
black = (0, 0, 0)

#Clase para las funciones de la pelota 
class pelotaP:
    def __init__(self, ficheroImagen): #Función de inicio de juego
        self.imagen = pygame.image.load(pong).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = winHori / 2 - self.ancho / 2
        self.y = winVert / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])
        self.puntuacion = 0
        self.puntuacion_maquina = 0

    #Función para el cambio de color de la pelota
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

    #Movimiento de la pelota
    def movimiento(self):
        self.x += self.dir_x
        self.y += self.dir_y

    #Reposición de la pelota al anotar
    def reiniciar(self):
        self.x = winHori / 2 - self.ancho / 2
        self.y = winVert / 2 - self.alto / 2
        self.dir_x = random.choice([-5, 5])
        self.dir_y = random.choice([-5, 5])

    #Rebote de la pelota
    def rebotar(self):
        if self.x <= -self.ancho:
            self.reiniciar()
            self.puntuacion_maquina += 1
            sonido_punto.play()
        if self.x >= winHori:
            self.reiniciar()
            self.puntuacion += 1
            sonido_punto.play()
        if self.y <= 0 or self.y + self.alto >= winVert:
            self.dir_y = -self.dir_y
        

#Clase para las funciones de la raqueta
class raqueta:
    def __init__(self):
        self.imagen = pygame.image.load(raquetaB).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = 0
        self.y = winVert / 2 - self.alto / 2
        self.dir_y = 0

    #Movimientos y limitaciones para la raqueta
    def movimiento(self):
        self.y += self.dir_y
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= winVert:
            self.y = winVert - self.alto

    #Movimiento automatico de la raqueta de la maquina según dificultad
    def movimiento_maquina(self, pelota,dificultad_actual):        
        velocidad = dificultad_actual["velocidad"]
        nueva_y = pelota.y - self.alto / 2
        
        if self.y < nueva_y:
            self.y += min(velocidad, nueva_y - self.y)
        elif self.y > nueva_y:
            self.y -= min(velocidad, self.y - nueva_y) 

    #Modificación de la dirección y posición de la pelota al golpe con la raqueta
    def golpear(self, pelota):
        if (
            pelota.dir_x < 0 and 
            pelota.x + pelota.dir_x < self.x + self.ancho and  
            pelota.x + pelota.ancho > self.x and  
            pelota.y + pelota.alto > self.y and  
            pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x + self.ancho
            pelota.dir_y*=1.1
            pelota.dir_x*=1.1
            sonido_golpe.play()

    #Modificación de la dirección y posición de la pelota al golpe con la raqueta de la maquina
    def golpear_maquina(self, pelota):
        if (
            pelota.dir_x > 0 and 
            pelota.x + pelota.dir_x + pelota.ancho > self.x and
            pelota.x < self.x + self.ancho and  
            pelota.y + pelota.alto > self.y and  
            pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -pelota.dir_x
            pelota.x = self.x - pelota.ancho
            pelota.dir_y*=1.1
            pelota.dir_x*=1.1
            sonido_golpe.play()

    #Cambio de color de la raquetas
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
            

#Inicio de juego
def main():
    #Inicio y posición de raquetas
    pygame.init()
    win = pygame.display.set_mode((winHori, winVert))
    pygame.display.set_caption("Ping Pong")
    pelota = pelotaP("pong.png")
    icono = pygame.image.load(iconRute)
    pygame.display.set_icon(icono)
    fuente = pygame.font.Font(None, 60)
    raqueta_1 = raqueta()
    raqueta_1.x = 60
    raqueta_2 = raqueta()
    raqueta_2.x = winHori - 60 - raqueta_2.ancho    
    dificultad_actual = {"velocidad": 5}

    #Seleccionar la dificultad
    def set_difficulty(value,difficulty):
        if difficulty == "Fácil":
            dificultad_actual["velocidad"] = 5
        elif difficulty == "Medio":
            dificultad_actual["velocidad"] = 8
        elif difficulty == "Difícil":
            dificultad_actual["velocidad"] = 15
        elif difficulty == "Muy difícil":
            dificultad_actual["velocidad"] = 18

    #Cambio de color de la pelota desde el menú
    def set_color(value,color):
        pelota.cambiar_color(color)

    #Cambio de color de la raqueta desde el menú
    def set_colorRaqueta(value,colorR):
        raqueta_1.cambiar_color_raqueta(colorR)
        raqueta_2.cambiar_color_raqueta(colorR)



    # Menú de configuración
    custom_theme = pm.Theme(
    background_color=(242, 243, 244), 
    title_background_color=(214, 234, 248), 
    title_font_color=(0,0,0), 
    widget_font_color=(0,0,0), 
    selection_color=(118, 150, 229),)
    
    settings = pm.Menu(title="Configuración", width=winHori, height=winVert, theme=custom_theme)
    settings.add.selector("Dificultad: ", [("Fácil", "Fácil"), ("Medio", "Medio"), ("Difícil", "Difícil"), ("Muy difícil", "Muy difícil")],
                          onchange=set_difficulty)
    settings.add.selector("Color pelota: ", [("Naranja", "Naranja"), ("Azul", "Azul"),("Verde","Verde"),("Negro","Negro"),("Rojo","Rojo"),("Amarillo","Amarillo"), ("Morado","Morado")],
                          onchange=set_color)
    settings.add.selector("Color raqueta: ", [("Negro","Negro"),("Naranja", "Naranja"), ("Azul", "Azul"),("Verde","Verde"),("Rojo","Rojo"),("Amarillo","Amarillo"), ("Morado","Morado")],
                          onchange=set_colorRaqueta)

    # Cómo jugar menu
    about = pm.Menu(title="Controles", width=winHori, height=winVert, theme=custom_theme)
    about.add.label("W - Mover raqueta arriba", font_size=23)
    about.add.label("S - Mover raqueta abajo", font_size=23)
    about.add.label("ESC - Volver al menú", font_size=23)
  
    # Menú principal
    main_menu = pm.Menu(title="Menú principal", width=winHori, height=winVert, theme=custom_theme)
    main_menu.add.button("Jugar", lambda: start_game(win, pelota, raqueta_1, raqueta_2, fuente, dificultad_actual))
    main_menu.add.button("Cómo jugar", about)
    main_menu.add.button("Configuración", settings)
    main_menu.add.button("Salir", pm.events.EXIT)


    # Mostrar el menú principal
    main_menu.mainloop(win)

#Función de inicio de juego
def start_game(win, pelota, raqueta_1, raqueta_2, fuente, dificultad_actual):
    pelota = pelotaP("pong.png")
    raqueta_1 = raqueta()
    raqueta_1.x = 60
    raqueta_2 = raqueta()
    raqueta_2.x = winHori - 60 - raqueta_2.ancho
    jugando = True

    pygame.draw.circle(win, (255, 165, 0, 100), (int(pelota.x), int(pelota.y)), 10)
    while jugando:
        pelota.movimiento()
        pelota.rebotar()
        raqueta_1.movimiento()
        raqueta_2.movimiento_maquina(pelota, dificultad_actual)
        raqueta_1.golpear(pelota)
        raqueta_2.golpear_maquina(pelota)
        win.fill((242, 243, 244))
        win.blit(pelota.imagen, (pelota.x, pelota.y))
        win.blit(raqueta_1.imagen, (raqueta_1.x, raqueta_1.y))
        win.blit(raqueta_2.imagen, (raqueta_2.x, raqueta_2.y))
        text = f"{pelota.puntuacion} : {pelota.puntuacion_maquina}"
        letrero = fuente.render(text, False, black)
        win.blit(letrero, (winHori / 2 - fuente.size(text)[0] / 2, 50))

        #Control y movimiento de raqueta
        for event in pygame.event.get():
            if event.type == QUIT:
                jugando = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    raqueta_1.dir_y = -8
                if event.key == pygame.K_s: 
                    raqueta_1.dir_y = 8
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    raqueta_1.dir_y = 0

        pygame.display.flip()
        pygame.time.Clock().tick(fps)
    pygame.quit()


if __name__ == "__main__":
    main()

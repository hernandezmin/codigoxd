import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("La Aventura en la Isla Misteriosa")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fuente
font = pygame.font.Font(None, 36)

class DecisionNode:
    def __init__(self, message, options=None, end_message=None):
        self.message = message
        self.options = options if options else {}
        self.end_message = end_message

    def add_option(self, option_text, next_node):
        self.options[option_text] = next_node

    def display(self):
        screen.fill(WHITE)
        render_text(self.message, 50, 50)
        if self.end_message:
            render_text(self.end_message, 50, 100)
            pygame.display.flip()
            wait_for_key()
            return None
        y = 150
        option_rects = []
        for option in self.options.keys():
            option_rects.append(render_text(option, 50, y))
            y += 50
        pygame.display.flip()
        return get_choice(option_rects)

def render_text(text, x, y):
    lines = text.split('\n')
    y_offset = 0
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (x, y + y_offset))
        y_offset += text_surface.get_height()
    return pygame.Rect(x, y, text_surface.get_width(), y_offset)

def get_choice(option_rects):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        return list(nodo_actual.options.values())[i]

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

# Crear nodos de la historia
final_1 = DecisionNode("Final 1: Alex construye un refugio seguro y sobrevive hasta ser rescatado.", end_message="Fin del juego.")
final_2 = DecisionNode("Final 2: Alex encuentra una tribu amistosa que lo ayuda y lo integra a su comunidad.", end_message="Fin del juego.")
final_3 = DecisionNode("Final 3: Alex encuentra una cueva con suministros y un mapa que lo lleva a un puerto escondido para escapar.", end_message="Fin del juego.")
final_4 = DecisionNode("Final 4: Alex es rescatado por un barco tras hacer una señal de socorro exitosa.", end_message="Fin del juego.")
final_5 = DecisionNode("Final 5: Alex no logra encontrar recursos suficientes y, lamentablemente, no sobrevive.", end_message="Fin del juego.")

# Nivel 4
seguir_rio = DecisionNode("Nivel 4: Seguir el sonido de un río")
seguir_rio.add_option("Beber del río", final_1)
seguir_rio.add_option("Seguir el río para encontrar ayuda", final_2)

buscar_plantas = DecisionNode("Nivel 4: Buscar agua en las plantas")
buscar_plantas.add_option("Exprimir las plantas", final_5)
buscar_plantas.add_option("Recoger el rocío de la mañana", final_2)

dirigirse_cueva = DecisionNode("Nivel 4: Dirigirse hacia una cueva")
dirigirse_cueva.add_option("Explorar la cueva", final_3)
dirigirse_cueva.add_option("Hacer una señal de socorro", final_4)

seguir_huellas = DecisionNode("Nivel 4: Seguir huellas de animales")
seguir_huellas.add_option("Cazar un animal", final_5)
seguir_huellas.add_option("Seguir las huellas hasta una fuente de agua", seguir_rio)

construir_piedras = DecisionNode("Nivel 4: Construir con piedras")
construir_piedras.add_option("Hacer un muro de protección", final_1)
construir_piedras.add_option("Construir una pequeña cabaña", final_1)

usar_hojas_ramas = DecisionNode("Nivel 4: Utilizar hojas y ramas")
usar_hojas_ramas.add_option("Construir una choza", final_1)
usar_hojas_ramas.add_option("Hacer una cama improvisada", final_5)

pescar_mar = DecisionNode("Nivel 4: Pescar en el mar")
pescar_mar.add_option("Usar una lanza improvisada", final_5)
pescar_mar.add_option("Hacer una trampa para peces", final_1)

recoger_frutas = DecisionNode("Nivel 4: Recoger frutas")
recoger_frutas.add_option("Comer las frutas directamente", final_5)
recoger_frutas.add_option("Guardar las frutas para más tarde", final_1)

# Nivel 3
buscar_agua = DecisionNode("Nivel 3: Buscar una fuente de agua")
buscar_agua.add_option("Seguir el sonido de un río", seguir_rio)
buscar_agua.add_option("Buscar agua en las plantas", buscar_plantas)

seguir_sendero = DecisionNode("Nivel 3: Seguir un sendero")
seguir_sendero.add_option("Seguir huellas de animales", seguir_huellas)
seguir_sendero.add_option("Dirigirse hacia una cueva", dirigirse_cueva)

construir_refugio = DecisionNode("Nivel 3: Construir un refugio")
construir_refugio.add_option("Utilizar hojas y ramas", usar_hojas_ramas)
construir_refugio.add_option("Construir con piedras", construir_piedras)

buscar_comida = DecisionNode("Nivel 3: Buscar comida")
buscar_comida.add_option("Recoger frutas", recoger_frutas)
buscar_comida.add_option("Pescar en el mar", pescar_mar)

# Nivel 2
adentrarse_jungla = DecisionNode("Nivel 2: Adentrarse en la jungla")
adentrarse_jungla.add_option("Seguir un sendero", seguir_sendero)
adentrarse_jungla.add_option("Buscar una fuente de agua", buscar_agua)

explorar_playa = DecisionNode("Nivel 2: Explorar la playa")
explorar_playa.add_option("Buscar comida", buscar_comida)
explorar_playa.add_option("Construir un refugio", construir_refugio)

# Nivel 1
llegada_isla = DecisionNode("Nivel 1: Llegada a la Isla")
llegada_isla.add_option("Explorar la playa", explorar_playa)
llegada_isla.add_option("Adentrarse en la jungla", adentrarse_jungla)

# Iniciar la historia
def iniciar_historia():
    global nodo_actual
    nodo_actual = llegada_isla
    while nodo_actual:
        nodo_actual = nodo_actual.display()

# Comenzar la aventura
iniciar_historia()
pygame.quit()

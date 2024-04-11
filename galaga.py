import pygame
import random

# Definición de colores

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Clase para la nave del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])  # Tamaño de la nave
        self.image.fill(WHITE)  # Color de la nave
        self.rect = self.image.get_rect()
        self.rect.x = 400  # Posición inicial x
        self.rect.y = 550  # Posición inicial y
         # Dibujar un cuadrado rojo en la nave
        pygame.draw.rect(self.image, RED, [0, 50, 20, 20])

        # Dibujar un círculo verde en la nave
        pygame.draw.circle(self.image, GREEN, (25, 40), 10)

        # Dibujar un triángulo azul en la nave
        pygame.draw.polygon(self.image, BLUE, [(5, 30), (25, 5), (45, 30)])

        # Asegúrate de cambiar también los valores de rect para que se ajusten a las nuevas dimensiones
        self.rect = self.image.get_rect()

    def update(self):
        # Control de movimiento horizontal de la nave con las teclas de flecha
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])  # Tamaño del enemigo
        self.image.fill(WHITE)  # Color del enemigo
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 750)  # Posición inicial x aleatoria
        self.rect.y = random.randrange(-100, -40)  # Posición inicial y aleatoria
        self.speedy = random.randrange(1, 3)  # Velocidad de movimiento aleatoria
       

    def update(self):
        self.rect.y += self.speedy
        # Reiniciar posición si el enemigo se sale de la pantalla
        if self.rect.top > 600:
            self.rect.x = random.randrange(0, 750)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)

# Inicialización de Pygame y creación de la ventana
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Galaxian")

# Lista de todos los sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Crear el jugador
player = Player()
all_sprites.add(player)

# Crear enemigos y agregarlos a la lista de sprites
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar todos los sprites
    all_sprites.update()

    # Comprobación de colisiones entre el jugador y los enemigos
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False  # Si hay colisión, el juego termina

    # Dibujar todos los sprites
    screen.fill(BLACK)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

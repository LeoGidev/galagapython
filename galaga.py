import pygame
import random
import os

# Definición de colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Inicialización de Pygame y creación de la ventana
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Galaxian")

# Clase para la nave del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar imagen de la nave y ajustar su tamaño
        original_image = pygame.image.load(os.path.join('img', 'nave.png')).convert()
        self.image = pygame.transform.scale(original_image, (100, 100))  # Tamaño de la nave (100x100 píxeles)
        self.image.set_colorkey(BLACK)  # Establecer color transparente
        self.rect = self.image.get_rect()
        self.rect.centerx = 400  # Posición inicial x centrada
        self.rect.bottom = 600  # Posición inicial y en la parte inferior de la pantalla
        self.speed = 5
        self.lives = 3  # Inicializar contador de vidas del jugador

    def update(self):
        # Control de movimiento horizontal de la nave con las teclas de flecha
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Limitar el movimiento dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800

# Clase para los enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar imágenes de asteroides y seleccionar una al azar
        asteroid_images = ['asteroide1.png', 'asteroide2.png']
        asteroid_image = random.choice(asteroid_images)
        self.image = pygame.image.load(os.path.join('img', asteroid_image)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))  # Redimensionar imagen a 50x50 píxeles
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

# Clase para los disparos
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])  # Tamaño del disparo
        self.image.fill(RED)  # Color del disparo (se usará solo para la detección de colisiones)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10  # Velocidad de movimiento hacia arriba

    def update(self):
        self.rect.y += self.speed
        # Eliminar el disparo si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()

# Lista de todos los sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Crear el jugador
player = Player()
all_sprites.add(player)

# Crear enemigos y agregarlos a la lista de sprites
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Cargar imagen de fondo
background = pygame.image.load(os.path.join('img', 'universo.jpg')).convert()

# Puntuación del jugador
score = 0

# Fuente para mostrar la puntuación
font = pygame.font.Font(None, 36)

# Mensaje de Game Over
game_over_font = pygame.font.Font(None, 72)

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Crear un nuevo disparo y agregarlo a la lista de sprites
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Actualizar todos los sprites
    all_sprites.update()

    # Comprobación de colisiones entre los disparos y los enemigos
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        # Crear nuevos enemigos para reemplazar los eliminados
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        # Incrementar la puntuación
        score += 10

    # Comprobación de colisiones entre el jugador y los enemigos
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        player.lives -= 1  # Restar una vida al jugador
        if player.lives == 0:
            print('hola')
            #running = False  # Si el jugador se queda sin vidas, terminar el juego
        else:
            # Reiniciar la posición del jugador
            player.rect.centerx = 400
            player.rect.bottom = 600

    # Dibujar el fondo
    screen.blit(background, (0, 0))

    # Dibujar todos los sprites
    all_sprites.draw(screen)

    # Mostrar puntuación en pantalla
    score_text = font.render("Score: {}".format(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Mostrar vidas del jugador en pantalla
    lives_text = font.render("Lives: {}".format(player.lives), True, WHITE)
    screen.blit(lives_text, (10, 50))

    # Si el jugador se queda sin vidas, mostrar mensaje de Game Over
    if player.lives == 0:
        game_over_text = game_over_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (250, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()




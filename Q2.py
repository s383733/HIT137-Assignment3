import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Game variables
GRAVITY = 1
PLAYER_SPEED = 5
JUMP_STRENGTH = 15
PROJECTILE_SPEED = 10
ENEMY_SPEED = 3
LEVEL_COUNT = 3

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_y = 0
        self.health = 100
        self.lives = 3
        self.score = 0

    def move(self, left, right, jumping):
        # Horizontal movement
        if left:
            self.rect.x -= PLAYER_SPEED
        if right:
            self.rect.x += PLAYER_SPEED

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        # Jumping
        if jumping:
            self.vel_y = -JUMP_STRENGTH

        # Update vertical position
        self.rect.y += self.vel_y

        # Prevent player from falling off the screen
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = 0

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x += PROJECTILE_SPEED
        # Remove the projectile if it moves off screen
        if self.rect.left > WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.x -= ENEMY_SPEED
        # Remove the enemy if it moves off screen
        if self.rect.right < 0:
            self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        if type == "health":
            self.image.fill(GREEN)
        elif type == "life":
            self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.type = type

# Game Over function
def game_over():
    font = pygame.font.SysFont("Arial", 72)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH//4, HEIGHT//3))
    pygame.display.flip()
    pygame.time.wait(2000)

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Create player
player = Player(100, HEIGHT-100)
all_sprites.add(player)

# Main game loop
level = 1
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    left, right, jumping = False, False, False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left = True
            if event.key == pygame.K_RIGHT:
                right = True
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_UP:
                jumping = True

    # Spawn enemies and collectibles
    if random.randint(0, 100) < 2:
        enemy = Enemy(WIDTH, HEIGHT-100)
        all_sprites.add(enemy)
        enemies.add(enemy)

    if random.randint(0, 100) < 1:
        collectible = Collectible(random.randint(WIDTH, WIDTH+200), HEIGHT-100, random.choice(["health", "life"]))
        all_sprites.add(collectible)
        collectibles.add(collectible)

    # Update sprites
    player.move(left, right, jumping)
    all_sprites.update()

    # Check for collisions
    enemy_hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
    for hit in enemy_hits:
        player.score += 100

    player_hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in player_hits:
        player.health -= 20
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            if player.lives == 0:
                game_over()
                running = False

    collectible_hits = pygame.sprite.spritecollide(player, collectibles, True)
    for hit in collectible_hits:
        if hit.type == "health":
            player.health += 20
        elif hit.type == "life":
            player.lives += 1

    # Draw everything
    all_sprites.draw(screen)
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
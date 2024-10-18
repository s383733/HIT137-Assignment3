import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
ENEMY_SPAWN_RATE = 30  # Frames between enemy spawns

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 70
        self.speed_x = 0
        self.speed_y = 0
        self.jumps = 0

    def update(self):
        self.speed_y += GRAVITY
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Ground collision
        if self.rect.y >= SCREEN_HEIGHT - 70:
            self.rect.y = SCREEN_HEIGHT - 70
            self.speed_y = 0
            self.jumps = 0

    def jump(self):
        if self.jumps < 2:
            self.speed_y = -15
            self.jumps += 1

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.top)
        all_sprites.add(projectile)
        projectiles.add(projectile)

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed_x = 10

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.x > SCREEN_WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - 70

    def update(self):
        self.rect.x -= 5
        if self.rect.x < -50:
            self.kill()  # Remove enemy when it goes off-screen

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 70)

# Level class
class Level:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.spawn_collectibles(3)  # Initial collectibles

    def spawn_enemies(self):
        if len(self.enemies) < 5:  # Keep a max number of enemies on screen
            enemy = Enemy()
            self.enemies.add(enemy)
            all_sprites.add(enemy)

    def spawn_collectibles(self, count):
        for _ in range(count):
            collectible = Collectible()
            self.collectibles.add(collectible)
            all_sprites.add(collectible)

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Side Scrolling Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.score = 0
        self.frames = 0  # Track frames for enemy spawning
        self.reset_game()

    def reset_game(self):
        global all_sprites, projectiles
        all_sprites = pygame.sprite.Group()
        projectiles = pygame.sprite.Group()

        self.level = Level()
        self.player = Player()
        all_sprites.add(self.player)

        self.score = 0
        self.game_over = False  # Reset game over status

    def run(self):
        while self.running:
            self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_r:  # Restart the game
                        self.reset_game()
                else:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_z:
                        self.player.shoot()
                    elif event.key == pygame.K_RIGHT:
                        self.player.speed_x = 5
                    elif event.key == pygame.K_LEFT:
                        self.player.speed_x = -5
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    self.player.speed_x = 0

    def update(self):
        all_sprites.update()

        # Enemy spawning logic
        self.frames += 1
        if self.frames % ENEMY_SPAWN_RATE == 0:
            self.level.spawn_enemies()

        # Collision detection for projectiles and enemies
        for projectile in projectiles:
            hits = pygame.sprite.spritecollide(projectile, self.level.enemies, True)
            for hit in hits:
                projectile.kill()
                self.score += 1

        # Check if the player has collided with any enemies (game over condition)
        if pygame.sprite.spritecollideany(self.player, self.level.enemies):
            self.game_over = True

        # Check for collectible collisions
        collectible_hits = pygame.sprite.spritecollide(self.player, self.level.collectibles, True)
        for hit in collectible_hits:
            self.score += 5

    def draw(self):
        self.screen.fill(BLACK)
        all_sprites.draw(self.screen)
        
        score_text = pygame.font.Font(None, 36).render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = pygame.font.Font(None, 72).render('Game Over', True, WHITE)
            restart_text = pygame.font.Font(None, 36).render('Press R to Restart', True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 36))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
        
        pygame.display.flip()

# Main loop
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()

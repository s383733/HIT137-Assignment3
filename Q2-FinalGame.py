# HIT137 Assignment3
# Answer to Q2
# Available at Git repo: https://github.com/s383733/HIT137-Assignment3


import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1024, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side Scroller 2D Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game clock
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.SysFont(None, 48)

# Confetti colors for victory screen
CONFETTI_COLORS = [RED, GREEN, BLUE, YELLOW, WHITE]

# Enemies for different levels
ENEMIES_BY_LEVEL = {
    1: 'Enemy1',
    2: 'Enemy2',
    3: 'Enemy3',
    4: 'Enemy4',
    5: 'Enemy5'
}

# Welcome Screen
def welcome_screen():
    screen.fill(BLACK)
    title_text = font.render("Welcome to Side Scroller 2D Game by Group100", True, YELLOW)
    instruction_text = font.render("Press any key to start", True, WHITE)
    additional_text = font.render("Use Arrow keys to move/jump, Space to shoot", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2))
    screen.blit(additional_text, (WIDTH // 2 - additional_text.get_width() // 2, HEIGHT // 2 + 80))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Game Over Screen
def game_over_screen(final_score):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, RED)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    score_text = font.render(f"Final Score: {final_score}", True, GREEN)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 40))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Victory Screen with Confetti
def victory_screen(final_score):
    screen.fill(BLACK)
    victory_text = font.render("Congrats! You won!!", True, GREEN)
    score_text = font.render(f"Final Score: {final_score}", True, YELLOW)
    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 50))
    pygame.display.flip()

    # Simulating confetti animation
    confetti = []
    for i in range(100):
        confetti.append([random.randint(0, WIDTH), random.randint(-1000, 0), random.choice(CONFETTI_COLORS)])

    while True:
        screen.fill(BLACK)
        screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 50))

        # Drawing confetti
        for c in confetti:
            pygame.draw.circle(screen, c[2], (c[0], c[1]), 5)
            c[1] += random.randint(2, 5)  # Simulate falling
            if c[1] > HEIGHT:
                c[1] = random.randint(-100, 0)
                c[0] = random.randint(0, WIDTH)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Stickman player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(50, HEIGHT - 150, 40, 60)  # Placeholder rect for player
        self.speed = 5
        self.jump_power = -15
        self.high_jump_power = -25  # Higher jump power
        self.gravity = 1
        self.velocity_y = 0
        self.jump = False
        self.health = 100
        self.lives = 3
        self.score = 0

    def update(self, keys):
        # Movement: left, right, jumping
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Regular jump (Shift or Up Arrow)
        if not self.jump and (keys[pygame.K_UP] or keys[pygame.K_LSHIFT]):
            self.jump = True
            if keys[pygame.K_UP] and keys[pygame.K_LSHIFT]:  # Higher jump with both keys
                self.velocity_y = self.high_jump_power
            else:
                self.velocity_y = self.jump_power

        if self.jump:
            self.rect.y += self.velocity_y
            self.velocity_y += self.gravity
            if self.rect.y >= HEIGHT - 150:  # Ground level
                self.rect.y = HEIGHT - 150
                self.jump = False

        # Ensure player stays in bounds
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width

    def shoot(self):
        # Create a new projectile and add it to the sprite groups
        projectile = Projectile(self.rect.centerx, self.rect.centery)
        projectiles.add(projectile)

    def draw(self, screen):
        # Drawing a more detailed stickman figure
        pygame.draw.circle(screen, YELLOW, (self.rect.centerx, self.rect.top + 15), 10)  # Head
        pygame.draw.line(screen, YELLOW, (self.rect.centerx, self.rect.top + 25), (self.rect.centerx, self.rect.bottom), 4)  # Body
        pygame.draw.line(screen, YELLOW, (self.rect.centerx, self.rect.top + 35), (self.rect.centerx - 20, self.rect.top + 50), 3)  # Left arm
        pygame.draw.line(screen, YELLOW, (self.rect.centerx, self.rect.top + 35), (self.rect.centerx + 20, self.rect.top + 50), 3)  # Right arm
        pygame.draw.line(screen, YELLOW, (self.rect.centerx, self.rect.bottom), (self.rect.centerx - 15, self.rect.bottom + 20), 4)  # Left leg
        pygame.draw.line(screen, YELLOW, (self.rect.centerx, self.rect.bottom), (self.rect.centerx + 15, self.rect.bottom + 20), 4)  # Right leg

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 7

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.kill()  # Remove the projectile when it goes off screen

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type, level):
        super().__init__()
        self.enemy_type = enemy_type
        self.image = pygame.Surface((50 + (level * 10), 50 + (level * 10)))  # size increment
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = self.calculate_speed(level)  # Speed scales with level
        self.set_color_by_level(level)  # Set color based on the level

    def calculate_speed(self, level):
        # Calculate speed based on the level
        base_speed = -2  # Base speed at level 1
        return base_speed - (level - 1)  # increment with each level

    def set_color_by_level(self, level):
        # Set enemy color based on the level
        if level == 1:
            self.image.fill(WHITE)
        elif level == 2:
            self.image.fill(YELLOW)
        elif level == 3:
            self.image.fill(GREEN)
        elif level == 4:
            self.image.fill(BLUE)
        elif level == 5:
            self.image.fill(RED)

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.rect.left = WIDTH

# Moving Collectible class (Diamond Shape)
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, BLUE if type == 'life' else GREEN, [(10, 0), (20, 10), (10, 20), (0, 10)])  # Diamond shape
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type  # "health" or "life"
        self.speed_y = random.choice([-2, -1, 1, 2])  # Moving up and down

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top < 50 or self.rect.bottom > HEIGHT - 100:
            self.speed_y *= -1  # Change direction

# Set up player, enemies, projectiles, collectibles
player = Player()
player_group = pygame.sprite.Group(player)

projectiles = pygame.sprite.Group()
enemies = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

# Add some collectibles
for i in range(5):  # Increase the number of collectibles
    collectible = Collectible(random.randint(200, WIDTH), random.randint(50, 300), random.choice(["health", "life"]))  # Positioned higher
    collectibles.add(collectible)

# Function to spawn enemies based on level
def spawn_enemies(level):
    enemies.empty()  # Clear old enemies
    enemy_type = ENEMIES_BY_LEVEL[level]
    for i in range(5 + level):  # enemies, increasing by level
        enemy = Enemy(random.randint(400, WIDTH), HEIGHT - 150, enemy_type, level)
        enemies.add(enemy)

# Function to draw health bar
def draw_health_bar(screen, player):
    pygame.draw.rect(screen, RED, (10, 10, player.health * 2, 20))
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 20), 2)  # Border

# Main game loop
def game_loop():
    level = 1
    spawn_enemies(level)
    running = True
    while running:
        clock.tick(60)  # 60 frames per second

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Get the current key states for movement
        keys = pygame.key.get_pressed()

        # Update player, projectiles, enemies, and collectibles
        player.update(keys)
        projectiles.update()
        enemies.update()
        collectibles.update()

        # Handle collisions between projectiles and enemies
        for projectile in projectiles:
            hit_enemy = pygame.sprite.spritecollideany(projectile, enemies)
            if hit_enemy:
                hit_enemy.kill()
                projectile.kill()  # Remove the projectile when it hits an enemy
                player.score += 10  # Increase score for defeating an enemy

        # Handle player collisions with enemies (lose health)
        if pygame.sprite.spritecollideany(player, enemies):
            player.health -= 1  # Lose health for each collision
            if player.health <= 0:
                if game_over_screen(player.score) == "restart":
                    return "restart"

        # Handle player collisions with collectibles
        for collectible in pygame.sprite.spritecollide(player, collectibles, True):
            if collectible.type == "health":
                player.health = min(100, player.health + 20)  # Restore health
            elif collectible.type == "life":
                player.lives += 1  # Gain an extra life
                player.score += 5  # Add to score

        # Check if all enemies are defeated and move to the next level
        if not enemies:
            level += 1
            if level > 5:
                victory_screen(player.score)
                return "won"
            else:
                spawn_enemies(level)

        # Clear the screen
        screen.fill(BLACK)

        # Draw player and all objects
        player.draw(screen)
        projectiles.draw(screen)
        enemies.draw(screen)
        collectibles.draw(screen)

        # Draw health bar and score
        draw_health_bar(screen, player)
        score_text = font.render(f"Score: {player.score} | Level: {level}", True, WHITE)
        screen.blit(score_text, (10, 40))

        # Update the display
        pygame.display.flip()

# Start the game with the welcome screen and then the main game loop
welcome_screen()

while True:
    result = game_loop()
    if result == "won":
        break
    elif result == "restart":
        continue

# Quit the game
pygame.quit()

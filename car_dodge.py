import pygame
import sys
import random

pygame.init()

# Configurar para tela cheia (modo janela)
info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h
FPS = 60

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

CAR_WIDTH = int(WINDOW_WIDTH * 0.07)
CAR_HEIGHT = int(WINDOW_HEIGHT * 0.15)
CAR_SPEED = 300

OBSTACLE_WIDTH = int(WINDOW_WIDTH * 0.07)
OBSTACLE_HEIGHT = int(WINDOW_HEIGHT * 0.15)
OBSTACLE_SPEED = 200

ROAD_WIDTH = int(WINDOW_WIDTH * 0.67)
ROAD_X = (WINDOW_WIDTH - ROAD_WIDTH) // 2

class Car:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2 - CAR_WIDTH // 2
        self.y = WINDOW_HEIGHT - CAR_HEIGHT - 50
        self.speed = CAR_SPEED
        self.rect = pygame.Rect(self.x, self.y, CAR_WIDTH, CAR_HEIGHT)
        
    def update(self, dt, keys):
        # Movement with arrow keys
        if keys[pygame.K_LEFT] and self.x > ROAD_X:
            self.x -= self.speed * dt
        if keys[pygame.K_RIGHT] and self.x < ROAD_X + ROAD_WIDTH - CAR_WIDTH:
            self.x += self.speed * dt
        if keys[pygame.K_UP] and self.y < WINDOW_HEIGHT - CAR_HEIGHT:
            self.y += self.speed * dt
        if keys[pygame.K_DOWN] and self.y > 0:
            self.y -= self.speed * dt
            
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def draw(self, screen):
        # Draw car as blue rectangle with details
        pygame.draw.rect(screen, BLUE, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        
        # Car details
        # Windows
        window_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 30, 15)
        pygame.draw.rect(screen, WHITE, window_rect)
        
        # Wheels
        wheel1 = pygame.Rect(self.rect.x + 2, self.rect.y + 45, 8, 12)
        wheel2 = pygame.Rect(self.rect.x + 30, self.rect.y + 45, 8, 12)
        pygame.draw.rect(screen, BLACK, wheel1)
        pygame.draw.rect(screen, BLACK, wheel2)

class Obstacle:
    def __init__(self):
        self.x = random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - OBSTACLE_WIDTH)
        self.y = -OBSTACLE_HEIGHT
        self.speed = OBSTACLE_SPEED
        self.rect = pygame.Rect(self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        self.color = random.choice([RED, YELLOW, GREEN, GRAY])
        
    def update(self, dt):
        self.y += self.speed * dt
        self.rect.y = int(self.y)
        
    def draw(self, screen):
        # Draw obstacle car
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        # Car details
        # Windows
        window_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 40, 30, 15)
        pygame.draw.rect(screen, WHITE, window_rect)
        
        # Wheels
        wheel1 = pygame.Rect(self.rect.x + 2, self.rect.y + 3, 8, 12)
        wheel2 = pygame.Rect(self.rect.x + 30, self.rect.y + 3, 8, 12)
        pygame.draw.rect(screen, BLACK, wheel1)
        pygame.draw.rect(screen, BLACK, wheel2)
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT

class CarDodgeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Desviar de Carros - Arcade Clássico")
        self.clock = pygame.time.Clock()
        
        self.car = Car()
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_interval = 1.5
        self.score = 0
        self.game_over = False
        self.speed_multiplier = 1.0
        
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        # Road lines animation
        self.road_line_offset = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()

        return True
    
    def update(self, dt):
        if self.game_over:
            return
            
        keys = pygame.key.get_pressed()
        self.car.update(dt, keys)
        
        # Spawn obstacles
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.obstacles.append(Obstacle())
            self.spawn_timer = 0
            # Gradually increase difficulty
            if self.spawn_interval > 0.8:
                self.spawn_interval -= 0.01
            
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.speed = OBSTACLE_SPEED * self.speed_multiplier
            obstacle.update(dt)
            
            # Remove off-screen obstacles and add score
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 10
                
                # Increase speed every 100 points
                if self.score > 0 and self.score % 100 == 0:
                    self.speed_multiplier += 0.1
            
            # Check collision
            if obstacle.rect.colliderect(self.car.rect):
                self.game_over = True
        
        # Animate road lines
        self.road_line_offset += 400 * dt * self.speed_multiplier
        if self.road_line_offset >= 40:
            self.road_line_offset = 0
    
    def draw_road(self):
        # Road background
        road_rect = pygame.Rect(ROAD_X, 0, ROAD_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, DARK_GRAY, road_rect)
        
        # Road borders
        pygame.draw.line(self.screen, WHITE, (ROAD_X, 0), (ROAD_X, WINDOW_HEIGHT), 4)
        pygame.draw.line(self.screen, WHITE, (ROAD_X + ROAD_WIDTH, 0), (ROAD_X + ROAD_WIDTH, WINDOW_HEIGHT), 4)
        
        # Center line (animated)
        center_x = ROAD_X + ROAD_WIDTH // 2
        line_length = 30
        line_gap = 40
        
        y = -line_length + self.road_line_offset
        while y < WINDOW_HEIGHT:
            if y + line_length > 0:
                start_y = max(0, y)
                end_y = min(WINDOW_HEIGHT, y + line_length)
                pygame.draw.line(self.screen, YELLOW, (center_x, start_y), (center_x, end_y), 3)
            y += line_gap
    
    def draw_controls(self):
        # Control scheme (standardized): ↑ Amarelo, ← Vermelho, ↓ Azul, → Verde
        controls = [
            ("← Vermelho - Esquerda", RED, 20, 20),
            ("→ Verde - Direita", GREEN, 20, 50),
            ("↑ Amarelo - Frente", YELLOW, 20, 80),
            ("↓ Azul - Trás", BLUE, 20, 110)
        ]
        
        for text, color, x, y in controls:
            control_text = pygame.font.Font(None, 20).render(text, True, color)
            self.screen.blit(control_text, (x, y))
    
    def draw_ui(self):
        # Score
        score_text = self.font.render(f"Pontos: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, WINDOW_HEIGHT - 60))
        
        # Speed indicator
        speed_text = self.small_font.render(f"Velocidade: {self.speed_multiplier:.1f}x", True, WHITE)
        self.screen.blit(speed_text, (20, WINDOW_HEIGHT - 30))
        
        # Title
        title = self.small_font.render("Desvie dos Carros!", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        if self.game_over:
            # Game over screen
            game_over_text = self.font.render("FIM DE JOGO", True, RED)
            restart_text = self.small_font.render("Pressione ESPAÇO para reiniciar", True, WHITE)
            final_score = self.small_font.render(f"Pontuação Final: {self.score}", True, WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            score_rect = final_score.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            
            # Semi-transparent overlay
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(restart_text, restart_rect)
            self.screen.blit(final_score, score_rect)
    
    def draw(self):
        self.screen.fill(GREEN)  # Grass on sides
        self.draw_road()
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)
        
        # Draw player car
        self.car.draw(self.screen)
        
        self.draw_controls()
        self.draw_ui()
        
        pygame.display.flip()
    
    def reset_game(self):
        self.car = Car()
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_interval = 1.5
        self.score = 0
        self.game_over = False
        self.speed_multiplier = 1.0
        self.road_line_offset = 0
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = CarDodgeGame()
    game.run()

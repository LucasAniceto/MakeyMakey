import pygame
import sys
import random
import math

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)

BUTTON_SIZE = 60
BUTTON_SPACING = 30

class Particle:
    def __init__(self, x, y, color, effect_type):
        self.x = x
        self.y = y
        self.color = color
        self.effect_type = effect_type
        self.life = 1.0
        self.max_life = 1.0
        
        if effect_type == "firework":
            angle = random.uniform(-math.pi/3, -2*math.pi/3)  # Upward angles only
            speed = random.uniform(200, 400)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.size = random.randint(8, 20)
            
        elif effect_type == "star":
            angle = random.uniform(-math.pi/4, -3*math.pi/4)  # Upward angles
            speed = random.uniform(150, 350)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.size = random.randint(15, 30)
            self.rotation = 0
            self.rotation_speed = random.uniform(-5, 5)
            
        elif effect_type == "flower":
            angle = random.uniform(-math.pi/6, -5*math.pi/6)  # Wide upward spread
            speed = random.uniform(120, 280)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.size = random.randint(20, 35)
            self.angle = random.uniform(0, 2 * math.pi)
            
        elif effect_type == "heart":
            angle = random.uniform(-math.pi/5, -4*math.pi/5)  # Upward heart burst
            speed = random.uniform(180, 320)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.size = random.randint(18, 35)
            self.bounce = 0
    
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt
        
        if self.effect_type == "firework":
            self.vy += 200 * dt  # gravity
        elif self.effect_type == "star":
            self.vy += 150 * dt  # gravity
            self.rotation += self.rotation_speed * dt
        elif self.effect_type == "flower":
            self.vy += 100 * dt  # gravity
            self.angle += dt * 3
        elif self.effect_type == "heart":
            self.vy += 180 * dt  # gravity
            self.bounce += dt * 10
    
    def draw(self, screen):
        if self.life <= 0:
            return
            
        alpha = self.life / self.max_life
        size = int(self.size * alpha)
        
        if size < 1:
            return
            
        if self.effect_type == "firework":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)
            
        elif self.effect_type == "star":
            self.draw_star(screen, int(self.x), int(self.y), size)
            
        elif self.effect_type == "flower":
            self.draw_flower(screen, int(self.x), int(self.y), size)
            
        elif self.effect_type == "heart":
            self.draw_heart(screen, int(self.x), int(self.y), size)
    
    def draw_star(self, screen, x, y, size):
        points = []
        for i in range(10):
            angle = (i * math.pi / 5) + self.rotation
            if i % 2 == 0:
                radius = size
            else:
                radius = size // 2
            px = x + math.cos(angle) * radius
            py = y + math.sin(angle) * radius
            points.append((px, py))
        
        if len(points) > 2:
            pygame.draw.polygon(screen, self.color, points)
    
    def draw_flower(self, screen, x, y, size):
        for i in range(6):
            angle = (i * math.pi / 3) + self.angle
            px = x + math.cos(angle) * size
            py = y + math.sin(angle) * size
            pygame.draw.circle(screen, self.color, (int(px), int(py)), size // 3)
        pygame.draw.circle(screen, WHITE, (x, y), size // 4)
    
    def draw_heart(self, screen, x, y, size):
        heart_points = [
            (x, y + size // 2),
            (x - size // 2, y),
            (x - size // 4, y - size // 3),
            (x, y - size // 6),
            (x + size // 4, y - size // 3),
            (x + size // 2, y)
        ]
        pygame.draw.polygon(screen, self.color, heart_points)

class MagicButton:
    def __init__(self, x, y, color, effect_type, name):
        self.rect = pygame.Rect(x, y, BUTTON_SIZE, BUTTON_SIZE)
        self.color = color
        self.effect_type = effect_type
        self.name = name
        self.pressed = False
        self.press_time = 0
        self.glow = 0
        self.glow_direction = 1
        
    def update(self, dt):
        if self.pressed:
            self.press_time -= dt
            if self.press_time <= 0:
                self.pressed = False
        
        self.glow += self.glow_direction * dt * 100
        if self.glow > 50:
            self.glow_direction = -1
        elif self.glow < 0:
            self.glow_direction = 1
    
    def press(self):
        self.pressed = True
        self.press_time = 0.3
    
    def draw(self, screen):
        # Draw glow effect
        glow_color = (
            max(0, min(255, self.color[0] + int(self.glow))),
            max(0, min(255, self.color[1] + int(self.glow))),
            max(0, min(255, self.color[2] + int(self.glow)))
        )
        
        if self.pressed:
            pygame.draw.circle(screen, WHITE, self.rect.center, BUTTON_SIZE // 2 + 15)
            pygame.draw.circle(screen, glow_color, self.rect.center, BUTTON_SIZE // 2 + 10)
        else:
            pygame.draw.circle(screen, glow_color, self.rect.center, BUTTON_SIZE // 2 + 8)
        
        pygame.draw.circle(screen, self.color, self.rect.center, BUTTON_SIZE // 2)
        pygame.draw.circle(screen, BLACK, self.rect.center, BUTTON_SIZE // 2, 3)
        
        # Draw icon
        self.draw_icon(screen)
    
    def draw_icon(self, screen):
        center_x, center_y = self.rect.center
        
        if self.effect_type == "firework":
            # Explosion icon
            for i in range(8):
                angle = i * math.pi / 4
                start_x = center_x + math.cos(angle) * 8
                start_y = center_y + math.sin(angle) * 8
                end_x = center_x + math.cos(angle) * 20
                end_y = center_y + math.sin(angle) * 20
                pygame.draw.line(screen, BLACK, (start_x, start_y), (end_x, end_y), 2)
                
        elif self.effect_type == "star":
            # Star icon
            points = []
            for i in range(10):
                angle = i * math.pi / 5
                if i % 2 == 0:
                    radius = 15
                else:
                    radius = 8
                px = center_x + math.cos(angle) * radius
                py = center_y + math.sin(angle) * radius
                points.append((px, py))
            pygame.draw.polygon(screen, BLACK, points)
            
        elif self.effect_type == "flower":
            # Flower icon
            for i in range(6):
                angle = i * math.pi / 3
                px = center_x + math.cos(angle) * 12
                py = center_y + math.sin(angle) * 12
                pygame.draw.circle(screen, BLACK, (int(px), int(py)), 4, 2)
            pygame.draw.circle(screen, BLACK, (center_x, center_y), 3, 2)
            
        elif self.effect_type == "heart":
            # Heart icon
            pygame.draw.circle(screen, BLACK, (center_x - 5, center_y - 3), 6, 2)
            pygame.draw.circle(screen, BLACK, (center_x + 5, center_y - 3), 6, 2)
            pygame.draw.polygon(screen, BLACK, [
                (center_x, center_y + 10),
                (center_x - 10, center_y),
                (center_x + 10, center_y)
            ], 2)

class MagicButtons:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Magic Buttons")
        self.clock = pygame.time.Clock()
        
        button_start_x = (WINDOW_WIDTH - (4 * BUTTON_SIZE + 3 * BUTTON_SPACING)) // 2
        button_y = WINDOW_HEIGHT - 100
        
        self.buttons = [
            MagicButton(button_start_x, button_y, YELLOW, "firework", "Fireworks"),
            MagicButton(button_start_x + BUTTON_SIZE + BUTTON_SPACING, button_y, GREEN, "star", "Stars"),
            MagicButton(button_start_x + 2 * (BUTTON_SIZE + BUTTON_SPACING), button_y, BLUE, "flower", "Flowers"),
            MagicButton(button_start_x + 3 * (BUTTON_SIZE + BUTTON_SPACING), button_y, RED, "heart", "Hearts")
        ]
        
        self.particles = []
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
        self.background_particles = []
        self.bg_particle_timer = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.activate_magic(0)
                elif event.key == pygame.K_DOWN:
                    self.activate_magic(1)
                elif event.key == pygame.K_UP:
                    self.activate_magic(2)
                elif event.key == pygame.K_RIGHT:
                    self.activate_magic(3)
                elif event.key == pygame.K_SPACE:
                    self.clear_all()
        
        return True
    
    def activate_magic(self, button_index):
        button = self.buttons[button_index]
        button.press()
        
        # Create magic particles
        center_x, center_y = button.rect.center
        
        if button.effect_type == "firework":
            # Explosive burst
            for _ in range(50):
                particle = Particle(center_x, center_y, YELLOW, "firework")
                self.particles.append(particle)
                
        elif button.effect_type == "star":
            # Floating stars
            for _ in range(25):
                x = center_x + random.randint(-100, 100)
                y = center_y + random.randint(-100, 100)
                particle = Particle(x, y, GREEN, "star")
                self.particles.append(particle)
                
        elif button.effect_type == "flower":
            # Growing flowers
            for _ in range(20):
                x = center_x + random.randint(-150, 150)
                y = center_y + random.randint(-150, 150)
                particle = Particle(x, y, BLUE, "flower")
                self.particles.append(particle)
                
        elif button.effect_type == "heart":
            # Floating hearts
            for _ in range(30):
                x = center_x + random.randint(-120, 120)
                y = center_y + random.randint(-120, 120)
                particle = Particle(x, y, RED, "heart")
                self.particles.append(particle)
    
    def update(self, dt):
        for button in self.buttons:
            button.update(dt)
            
        # Update particles
        self.particles = [p for p in self.particles if p.life > 0]
        for particle in self.particles:
            particle.update(dt)
            
        # Add random background sparkles
        self.bg_particle_timer += dt
        if self.bg_particle_timer > 0.5:
            self.bg_particle_timer = 0
            x = random.randint(50, WINDOW_WIDTH - 50)
            y = random.randint(50, WINDOW_HEIGHT - 50)
            color = random.choice([YELLOW, GREEN, BLUE, RED, PURPLE, ORANGE])
            effect = random.choice(["star", "heart", "flower"])
            
            bg_particle = Particle(x, y, color, effect)
            bg_particle.life = 0.5
            bg_particle.max_life = 0.5
            bg_particle.vx = 0
            bg_particle.vy = 0
            self.background_particles.append(bg_particle)
            
        # Update background particles
        self.background_particles = [p for p in self.background_particles if p.life > 0]
        for particle in self.background_particles:
            particle.update(dt)
    
    def clear_all(self):
        self.particles.clear()
        self.background_particles.clear()
    
    def draw(self):
        # Create gradient background
        for y in range(WINDOW_HEIGHT):
            color_ratio = y / WINDOW_HEIGHT
            r = int(20 + (40 - 20) * color_ratio)
            g = int(20 + (60 - 20) * color_ratio)
            b = int(60 + (100 - 60) * color_ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))
        
        # Draw background sparkles
        for particle in self.background_particles:
            particle.draw(self.screen)
        
        # Draw title
        title = self.font.render("Magic Buttons", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)
        
        # Draw instruction
        instruction = self.small_font.render("Press arrow keys to create magic!", True, WHITE)
        inst_rect = instruction.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(instruction, inst_rect)
        
        # Draw controls
        controls = ["← Fireworks", "↓ Stars", "↑ Flowers", "→ Hearts"]
        for i, control in enumerate(controls):
            color = [YELLOW, GREEN, BLUE, RED][i]
            text = self.small_font.render(control, True, color)
            self.screen.blit(text, (20, 20 + i * 30))
        
        clear_text = self.small_font.render("SPACE - Clear", True, WHITE)
        self.screen.blit(clear_text, (20, 140))
        
        # Draw magic particles
        for particle in self.particles:
            particle.draw(self.screen)
            
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)
            
        pygame.display.flip()
    
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
    game = MagicButtons()
    game.run()
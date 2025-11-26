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

BUTTON_WIDTH = int(WINDOW_WIDTH * 0.09)
BUTTON_HEIGHT = int(WINDOW_HEIGHT * 0.11)
BUTTON_Y = int(WINDOW_HEIGHT * 0.62)

NOTE_WIDTH = int(WINDOW_WIDTH * 0.08)
NOTE_HEIGHT = int(WINDOW_HEIGHT * 0.05)
NOTE_SPEED = 300
HIT_ZONE_TOLERANCE = 30

class GuitarButton:
    def __init__(self, x, y, color, key):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.color = color
        self.key = key
        self.pressed = False
        
    def draw(self, screen):
        if self.pressed:
            pygame.draw.rect(screen, WHITE, self.rect)
            pygame.draw.rect(screen, self.color, self.rect, 5)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        pygame.draw.rect(screen, BLACK, self.rect, 3)

class Note:
    def __init__(self, lane, color):
        self.lane = lane
        self.color = color
        self.rect = pygame.Rect(0, -NOTE_HEIGHT, NOTE_WIDTH, NOTE_HEIGHT)
        self.hit = False
        self.missed = False
        
    def update(self, dt, button_x):
        self.rect.x = button_x + (BUTTON_WIDTH - NOTE_WIDTH) // 2
        self.rect.y += NOTE_SPEED * dt
        
        if self.rect.y > WINDOW_HEIGHT and not self.hit:
            self.missed = True
    
    def draw(self, screen):
        if not self.hit:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, WHITE, self.rect, 2)
    
    def is_in_hit_zone(self, button_y):
        return abs(self.rect.bottom - button_y) <= HIT_ZONE_TOLERANCE

class GuitarHero:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Herói da Guitarra - Protótipo")
        self.clock = pygame.time.Clock()
        
        button_spacing = (WINDOW_WIDTH - (4 * BUTTON_WIDTH)) // 5
        start_x = button_spacing
        
        self.buttons = [
            GuitarButton(start_x, BUTTON_Y, YELLOW, pygame.K_LEFT),
            GuitarButton(start_x + BUTTON_WIDTH + button_spacing, BUTTON_Y, GREEN, pygame.K_DOWN),
            GuitarButton(start_x + 2 * (BUTTON_WIDTH + button_spacing), BUTTON_Y, BLUE, pygame.K_UP),
            GuitarButton(start_x + 3 * (BUTTON_WIDTH + button_spacing), BUTTON_Y, RED, pygame.K_RIGHT)
        ]
        
        self.font = pygame.font.Font(None, 36)
        
        self.notes = []
        self.note_spawn_timer = 0
        self.note_spawn_interval = 1.0
        self.score = 0
        self.hits = 0
        self.misses = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                for i, button in enumerate(self.buttons):
                    if event.key == button.key:
                        button.pressed = True
                        self.check_hit(i)

            if event.type == pygame.KEYUP:
                for button in self.buttons:
                    if event.key == button.key:
                        button.pressed = False

        return True
    
    def spawn_note(self):
        lane = random.randint(0, 3)
        color = [YELLOW, GREEN, BLUE, RED][lane]
        note = Note(lane, color)
        self.notes.append(note)
    
    def check_hit(self, lane):
        for note in self.notes:
            if note.lane == lane and not note.hit and not note.missed:
                if note.is_in_hit_zone(BUTTON_Y):
                    note.hit = True
                    self.score += 100
                    self.hits += 1
                    return True
        return False
    
    def update_notes(self, dt):
        for note in self.notes[:]:
            if not note.hit:
                button_x = self.buttons[note.lane].rect.x
                note.update(dt, button_x)
                
                if note.missed:
                    self.misses += 1
                    self.notes.remove(note)
            else:
                self.notes.remove(note)
    
    def update(self, dt):
        self.note_spawn_timer += dt
        if self.note_spawn_timer >= self.note_spawn_interval:
            self.spawn_note()
            self.note_spawn_timer = 0
            self.note_spawn_interval = random.uniform(0.8, 2.0)
        
        self.update_notes(dt)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        title = self.font.render("Herói da Guitarra - Protótipo", True, WHITE)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)

        score_text = pygame.font.Font(None, 24).render(f"Pontuação: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))

        stats_text = pygame.font.Font(None, 24).render(f"Acertos: {self.hits} | Erros: {self.misses}", True, WHITE)
        self.screen.blit(stats_text, (20, 50))

        instructions = [
            "← Amarelo  ↓ Verde  ↑ Azul  → Vermelho",
            "Acerte as notas quando chegarem aos botões!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 20).render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 80 + i * 25))
            self.screen.blit(text, text_rect)
        
        for note in self.notes:
            note.draw(self.screen)
        
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
    game = GuitarHero()
    game.run()

import pygame
import random
import time
import sys
import math

pygame.init()

FPS = 60

# Configurar para tela cheia
info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
YELLOW = (255, 255, 100)
DARK_RED = (150, 50, 50)
DARK_GREEN = (50, 150, 50)
DARK_BLUE = (50, 50, 150)
DARK_YELLOW = (150, 150, 50)

CIRCLE_CENTER = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
CIRCLE_RADIUS = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 4  # Ajusta ao tamanho da tela
INNER_RADIUS = CIRCLE_RADIUS // 6

class GeniusGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("JOGO DA MEMORIA GENIUS")
        self.clock = pygame.time.Clock()
        
        self.sequence = []
        self.player_sequence = []
        self.current_level = 1
        self.game_state = "esperando"  # esperando, mostrando, entrada, completo, fim_jogo
        self.active_button = None
        self.button_flash_time = 0
        self.sequence_index = 0
        self.last_flash_time = 0
        self.flash_duration = 500  # Duração consistente do flash em ms
        self.completion_time = 0  # Tempo quando sequência foi completada
        
        self.sectors = {
            'red': {'start_angle': 0, 'end_angle': 90},
            'yellow': {'start_angle': 90, 'end_angle': 180},
            'green': {'start_angle': 180, 'end_angle': 270},
            'blue': {'start_angle': 270, 'end_angle': 360}
        }
        
        self.colors = {
            'red': (RED, DARK_RED),
            'green': (GREEN, DARK_GREEN),
            'blue': (BLUE, DARK_BLUE),
            'yellow': (YELLOW, DARK_YELLOW)
        }
        
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        
    def generate_sequence(self):
        self.sequence.append(random.choice(['red', 'green', 'blue', 'yellow']))
        
    def start_new_game(self):
        self.sequence = []
        self.player_sequence = []
        self.current_level = 1
        self.generate_sequence()
        self.show_sequence()
        
    def show_sequence(self):
        self.game_state = "mostrando"
        self.sequence_index = 0
        self.active_button = None
        self.last_flash_time = pygame.time.get_ticks()
        
    def update_sequence_display(self):
        current_time = pygame.time.get_ticks()
        
        if self.sequence_index < len(self.sequence):
            if current_time - self.last_flash_time > 500:
                if self.active_button is None:
                    self.active_button = self.sequence[self.sequence_index]
                    self.button_flash_time = current_time
                elif current_time - self.button_flash_time > self.flash_duration:
                    self.active_button = None
                    self.sequence_index += 1
                    self.last_flash_time = current_time
        else:
            if current_time - self.last_flash_time > 500:
                self.game_state = "entrada"
                self.player_sequence = []
                
    def get_clicked_sector(self, pos):
        x, y = pos
        cx, cy = CIRCLE_CENTER
        
        distance = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
        if distance < INNER_RADIUS or distance > CIRCLE_RADIUS:
            return None
            
        angle = math.degrees(math.atan2(y - cy, x - cx))
        if angle < 0:
            angle += 360
            
        for sector_name, sector_data in self.sectors.items():
            if sector_data['start_angle'] <= angle < sector_data['end_angle']:
                return sector_name
        return None
    
    def handle_keyboard_input(self, color):
        if self.game_state != "entrada":
            return
            
        self.player_sequence.append(color)
        self.active_button = color
        self.button_flash_time = pygame.time.get_ticks()
        
        if self.player_sequence[-1] != self.sequence[len(self.player_sequence) - 1]:
            self.game_state = "fim_jogo"
        elif len(self.player_sequence) == len(self.sequence):
            self.game_state = "completo"
            self.completion_time = pygame.time.get_ticks()
                
    def draw_sector(self, sector_name, is_active):
        start_angle = math.radians(self.sectors[sector_name]['start_angle'])
        end_angle = math.radians(self.sectors[sector_name]['end_angle'])
        
        color = self.colors[sector_name][0] if is_active else self.colors[sector_name][1]
        
        points = [CIRCLE_CENTER]
        for angle in [start_angle + i * (end_angle - start_angle) / 50 for i in range(51)]:
            x = CIRCLE_CENTER[0] + CIRCLE_RADIUS * math.cos(angle)
            y = CIRCLE_CENTER[1] + CIRCLE_RADIUS * math.sin(angle)
            points.append((x, y))
        points.append(CIRCLE_CENTER)
        
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, WHITE, points, 3)
        
        inner_points = [CIRCLE_CENTER]
        for angle in [start_angle + i * (end_angle - start_angle) / 20 for i in range(21)]:
            x = CIRCLE_CENTER[0] + INNER_RADIUS * math.cos(angle)
            y = CIRCLE_CENTER[1] + INNER_RADIUS * math.sin(angle)
            inner_points.append((x, y))
        inner_points.append(CIRCLE_CENTER)
        
        pygame.draw.polygon(self.screen, BLACK, inner_points)

    def draw(self):
        self.screen.fill(BLACK)
        
        current_time = pygame.time.get_ticks()
        
        for sector_name in self.sectors.keys():
            is_active = (self.active_button == sector_name and 
                        current_time - self.button_flash_time < self.flash_duration)
            self.draw_sector(sector_name, is_active)
            
        pygame.draw.circle(self.screen, BLACK, CIRCLE_CENTER, INNER_RADIUS)
        pygame.draw.circle(self.screen, WHITE, CIRCLE_CENTER, INNER_RADIUS, 3)
        
        if self.game_state == "entrada" and current_time - self.button_flash_time > self.flash_duration:
            self.active_button = None
            
        if self.game_state != "esperando":
            level_text = self.font.render(f"Nivel: {self.current_level}", True, WHITE)
            self.screen.blit(level_text, (WINDOW_WIDTH // 2 - level_text.get_width() // 2, WINDOW_HEIGHT - 150))
        
        if self.game_state == "esperando":
            # Posicionar textos abaixo do círculo do Genius
            text_start_y = CIRCLE_CENTER[1] + CIRCLE_RADIUS + 80
            
            start_text = self.font.render("Pressione ESPACO para iniciar", True, WHITE)
            self.screen.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, text_start_y))
            
            controls_title = self.font.render("Controles:", True, WHITE)
            self.screen.blit(controls_title, (WINDOW_WIDTH // 2 - controls_title.get_width() // 2, text_start_y + 80))
            
            # Organizar controles nas laterais da tela
            left_margin = 50
            right_margin = WINDOW_WIDTH - 250
            
            control_up = self.small_font.render("CIMA = Azul", True, BLUE)
            self.screen.blit(control_up, (left_margin, text_start_y + 130))
            
            control_left = self.small_font.render("ESQUERDA = Verde", True, GREEN)
            self.screen.blit(control_left, (left_margin, text_start_y + 170))
            
            control_down = self.small_font.render("BAIXO = Amarelo", True, YELLOW)
            self.screen.blit(control_down, (right_margin, text_start_y + 130))
            
            control_right = self.small_font.render("DIREITA = Vermelho", True, RED)
            self.screen.blit(control_right, (right_margin, text_start_y + 170))
            
            exit_text = self.small_font.render("Pressione ESC para sair", True, WHITE)
            self.screen.blit(exit_text, (WINDOW_WIDTH // 2 - exit_text.get_width() // 2, text_start_y + 230))
        elif self.game_state == "mostrando":
            watch_text = self.font.render("Observe a sequencia...", True, WHITE)
            self.screen.blit(watch_text, (WINDOW_WIDTH // 2 - watch_text.get_width() // 2, WINDOW_HEIGHT - 100))
        elif self.game_state == "entrada":
            input_text = self.font.render("Use as setas para repetir a sequencia", True, WHITE)
            self.screen.blit(input_text, (WINDOW_WIDTH // 2 - input_text.get_width() // 2, WINDOW_HEIGHT - 100))
        elif self.game_state == "completo":
            success_text = self.font.render("Correto! Avancando para o proximo nivel...", True, WHITE)
            self.screen.blit(success_text, (WINDOW_WIDTH // 2 - success_text.get_width() // 2, WINDOW_HEIGHT - 100))
        elif self.game_state == "fim_jogo":
            game_over_text = self.font.render("Fim de Jogo!", True, WHITE)
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT - 150))
            restart_text = self.font.render("Pressione ESPACO para reiniciar", True, WHITE)
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT - 100))
            
        pygame.display.flip()
        
    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        if self.game_state in ["esperando", "fim_jogo"]:
                            self.start_new_game()
                    elif event.key == pygame.K_UP:
                        self.handle_keyboard_input('blue')
                    elif event.key == pygame.K_LEFT:
                        self.handle_keyboard_input('green')
                    elif event.key == pygame.K_DOWN:
                        self.handle_keyboard_input('yellow')
                    elif event.key == pygame.K_RIGHT:
                        self.handle_keyboard_input('red')
                        
            if self.game_state == "mostrando":
                self.update_sequence_display()
            elif self.game_state == "completo":
                current_time = pygame.time.get_ticks()
                if current_time - self.completion_time > self.flash_duration + 500:
                    self.current_level += 1
                    self.generate_sequence()
                    self.show_sequence()
                
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GeniusGame()
    game.run()
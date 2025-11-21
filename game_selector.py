import pygame
import sys
import subprocess

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)

class GameSelector:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Protótipo seletor PEC1")
        self.clock = pygame.time.Clock()
        
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 36)
        
        self.games = [
            {"name": "Jogo TESTE", "file": "magic_buttons.py"},
            {"name": "Jogo Da Cobrinha", "file": "snake_game.py"},
            {"name": "Jogo Dos Blocos", "file": "tetris_game.py"},
            {"name": "Jogo Dos Carros", "file": "car_dodge.py"},
            {"name": "Jogo Da Musica", "file": "guitar_hero.py"},
	    {"name": "Jogo De Memoria", "file": "genius_game.py"}
        ]
        
        self.button_height = 60
        self.button_width = 400
        self.button_spacing = 20
        self.start_y = 140
        
        self.selected_index = 0
       	
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.games)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.games)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.launch_game(self.selected_index)
                elif event.key == pygame.K_ESCAPE:
                    return False
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(len(self.games)):
                    button_y = self.start_y + i * (self.button_height + self.button_spacing)
                    button_x = (WINDOW_WIDTH - self.button_width) // 2
                    
                    if (button_x <= mouse_x <= button_x + self.button_width and
                        button_y <= mouse_y <= button_y + self.button_height):
                        self.selected_index = i
                        self.launch_game(i)
                        
        return True
    
    def launch_game(self, index):
        game_file = self.games[index]["file"]
        try:
            subprocess.run([sys.executable, game_file], cwd=".")
        except Exception as e:
            print(f"Error launching {game_file}: {e}")
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Title
        title_text = self.font_title.render("Selecione seu jogo", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        for i, game in enumerate(self.games):
            button_y = self.start_y + i * (self.button_height + self.button_spacing)
            button_x = (WINDOW_WIDTH - self.button_width) // 2
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            
            mouse_hover = button_rect.collidepoint(mouse_x, mouse_y)
            
            if i == self.selected_index:
                button_color = BLUE
                text_color = WHITE
            elif mouse_hover:
                button_color = LIGHT_GRAY
                text_color = BLACK
            else:
                button_color = GRAY
                text_color = WHITE

            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, BLACK, button_rect, 3)
            
            # Draw text
            text = self.font_button.render(game["name"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    selector = GameSelector()
    selector.run()

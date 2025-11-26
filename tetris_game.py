import pygame
import sys
import random

pygame.init()

# Configurar para tela cheia (modo janela)
info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h
FPS = 60

GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = int(min(WINDOW_WIDTH, WINDOW_HEIGHT) / 25)  # Responsivo

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

GAME_AREA_X = int(WINDOW_WIDTH * 0.05)
GAME_AREA_Y = int(WINDOW_HEIGHT * 0.05)

class TetrisPiece:
    def __init__(self, shape_type, color):
        self.shape_type = shape_type
        self.color = color
        self.rotation = 0
        self.x = GRID_WIDTH // 2 - 1
        self.y = 0
        
        # Define shapes (4 simple pieces)
        self.shapes = {
            'I': [  # Line piece (Blue)
                [
                    [1, 1, 1, 1]
                ],
                [
                    [1],
                    [1],
                    [1],
                    [1]
                ]
            ],
            'O': [  # Square piece (Yellow)
                [
                    [1, 1],
                    [1, 1]
                ]
            ],
            'L': [  # L piece (Green)
                [
                    [1, 0],
                    [1, 0],
                    [1, 1]
                ],
                [
                    [1, 1, 1],
                    [1, 0, 0]
                ],
                [
                    [1, 1],
                    [0, 1],
                    [0, 1]
                ],
                [
                    [0, 0, 1],
                    [1, 1, 1]
                ]
            ],
            'T': [  # T piece (Red)
                [
                    [0, 1, 0],
                    [1, 1, 1]
                ],
                [
                    [1, 0],
                    [1, 1],
                    [1, 0]
                ],
                [
                    [1, 1, 1],
                    [0, 1, 0]
                ],
                [
                    [0, 1],
                    [1, 1],
                    [0, 1]
                ]
            ]
        }
    
    def get_shape(self):
        return self.shapes[self.shape_type][self.rotation % len(self.shapes[self.shape_type])]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes[self.shape_type])

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Tétris Simples")
        self.clock = pygame.time.Clock()
        
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.grid_colors = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        self.piece_types = [
            ('I', BLUE),
            ('O', YELLOW),
            ('L', GREEN),
            ('T', RED)
        ]
        
        self.current_piece = self.spawn_piece()
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def spawn_piece(self):
        piece_type, color = random.choice(self.piece_types)
        return TetrisPiece(piece_type, color)
    
    def is_valid_position(self, piece, dx=0, dy=0, rotation=None):
        if rotation is None:
            shape = piece.get_shape()
        else:
            old_rotation = piece.rotation
            piece.rotation = rotation % len(piece.shapes[piece.shape_type])
            shape = piece.get_shape()
            piece.rotation = old_rotation
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + dx
                    new_y = piece.y + y + dy
                    
                    if (new_x < 0 or new_x >= GRID_WIDTH or 
                        new_y >= GRID_HEIGHT or
                        (new_y >= 0 and self.grid[new_y][new_x])):
                        return False
        return True
    
    def place_piece(self, piece):
        shape = piece.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = piece.x + x
                    grid_y = piece.y + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = 1
                        self.grid_colors[grid_y][grid_x] = piece.color
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(GRID_HEIGHT):
            if all(self.grid[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.grid[y]
            del self.grid_colors[y]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            self.grid_colors.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += len(lines_to_clear) * 100 * (len(lines_to_clear))  # Bonus for multiple lines
            
            # Speed up game as lines are cleared
            if self.lines_cleared > 0 and self.lines_cleared % 5 == 0:
                self.fall_speed = max(100, self.fall_speed - 50)
    
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
                else:
                    if event.key == pygame.K_LEFT:
                        if self.is_valid_position(self.current_piece, dx=-1):
                            self.current_piece.x -= 1

                    elif event.key == pygame.K_RIGHT:
                        if self.is_valid_position(self.current_piece, dx=1):
                            self.current_piece.x += 1

                    elif event.key == pygame.K_DOWN:
                        new_rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shapes[self.current_piece.shape_type])
                        if self.is_valid_position(self.current_piece, rotation=new_rotation):
                            self.current_piece.rotate()

                    elif event.key == pygame.K_UP:
                        if self.is_valid_position(self.current_piece, dy=1):
                            self.current_piece.y += 1
                            self.score += 1
        
        return True
    
    def update(self, dt):
        if self.game_over:
            return
            
        self.fall_time += dt
        
        if self.fall_time >= self.fall_speed:
            if self.is_valid_position(self.current_piece, dy=1):
                self.current_piece.y += 1
            else:
                self.place_piece(self.current_piece)
                self.clear_lines()
                self.current_piece = self.spawn_piece()
                
                if not self.is_valid_position(self.current_piece):
                    self.game_over = True
            
            self.fall_time = 0
    
    def draw_grid(self):
        # Draw game area background
        game_rect = pygame.Rect(GAME_AREA_X, GAME_AREA_Y, GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE)
        pygame.draw.rect(self.screen, BLACK, game_rect)
        pygame.draw.rect(self.screen, WHITE, game_rect, 2)
        
        # Draw placed blocks
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    rect = pygame.Rect(
                        GAME_AREA_X + x * BLOCK_SIZE,
                        GAME_AREA_Y + y * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    )
                    pygame.draw.rect(self.screen, self.grid_colors[y][x], rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
        
        # Draw grid lines
        for x in range(GRID_WIDTH + 1):
            start_x = GAME_AREA_X + x * BLOCK_SIZE
            pygame.draw.line(self.screen, GRAY, 
                           (start_x, GAME_AREA_Y), 
                           (start_x, GAME_AREA_Y + GRID_HEIGHT * BLOCK_SIZE))
        
        for y in range(GRID_HEIGHT + 1):
            start_y = GAME_AREA_Y + y * BLOCK_SIZE
            pygame.draw.line(self.screen, GRAY,
                           (GAME_AREA_X, start_y),
                           (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE, start_y))
    
    def draw_piece(self, piece):
        shape = piece.get_shape()
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        GAME_AREA_X + (piece.x + x) * BLOCK_SIZE,
                        GAME_AREA_Y + (piece.y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    )
                    pygame.draw.rect(self.screen, piece.color, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
    
    def draw_ui(self):
        # Title
        title = self.font.render("Tétris Simples", True, WHITE)
        self.screen.blit(title, (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE + 20, 50))

        # Score
        score_text = self.small_font.render(f"Pontuação: {self.score}", True, WHITE)
        self.screen.blit(score_text, (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE + 20, 100))

        # Lines
        lines_text = self.small_font.render(f"Linhas: {self.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE + 20, 130))
        
        # Controls (standardized: ↑ Amarelo, ← Vermelho, ↓ Azul, → Verde)
        controls = [
            "← (Vermelho) Esquerda",
            "→ (Verde) Direita",
            "↓ (Azul) Baixo",
            "↑ (Amarelo) Girar"
        ]
        
        for i, control in enumerate(controls):
            text = pygame.font.Font(None, 18).render(control, True, WHITE)
            self.screen.blit(text, (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE + 20, 200 + i * 25))
        
        # Piece colors
        color_info = [
            ("Linha Azul", BLUE),
            ("Quadrado Amarelo", YELLOW),
            ("L Verde", GREEN),
            ("T Vermelho", RED)
        ]
        
        for i, (name, color) in enumerate(color_info):
            text = pygame.font.Font(None, 18).render(name, True, color)
            self.screen.blit(text, (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE + 20, 350 + i * 25))
        
        if self.game_over:
            game_over_text = self.font.render("FIM DE JOGO", True, RED)
            restart_text = self.small_font.render("Pressione ESPAÇO para reiniciar", True, WHITE)
            
            self.screen.blit(game_over_text, (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE + 20, 500))
            self.screen.blit(restart_text, (GAME_AREA_X + GRID_WIDTH * BLOCK_SIZE + 20, 540))
    
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.grid_colors = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.spawn_piece()
        self.fall_time = 0
        self.fall_speed = 500
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
    
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        
        if not self.game_over:
            self.draw_piece(self.current_piece)
        
        self.draw_ui()
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS)
            running = self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()
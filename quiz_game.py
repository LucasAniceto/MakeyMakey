import pygame
import sys

pygame.init()

# Configurar para tela cheia (modo janela)
info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

class QuizGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption("Quiz de Privacidade e Proteção de Dados")
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.Font(None, 48)
        self.font_question = pygame.font.Font(None, 40)
        self.font_button = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Perguntas do quiz com a estrutura correta
        # Verde (CIMA) = OK, pode compartilhar
        # Amarelo (ESQUERDA) = Cuidado, problema médio
        # Vermelho (DIREITA) = NÃO, crítico
        # Azul (BAIXO) = Dica
        self.questions = [
            {
                "question": "Compartilhar seu NOME é seguro?",
                "answers": {
                    "green": {"text": "Sim, é público", "correct": True, "explanation": "Correto! Nome é informação pública."},
                    "yellow": {"text": "Cuidado", "correct": False, "explanation": "Errado! Nome é informação pública e segura."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Errado! Nome é informação pública."}
                },
                "tip": "Nome é informação pública e não compromete segurança"
            },
            {
                "question": "Compartilhar seu CPF é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! CPF é documento sensível e pode ser usado para fraudes."},
                    "yellow": {"text": "Cuidado, risco", "correct": True, "explanation": "Correto! CPF exige cuidado pois pode ser usado para roubo de identidade."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Parcialmente certo, mas 'Cuidado' é mais apropriado que 'Nunca'."}
                },
                "tip": "CPF pode ser usado para fraudes e roubo de identidade"
            },
            {
                "question": "Compartilhar sua SENHA é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Senha deve ser confidencial."},
                    "yellow": {"text": "Cuidado", "correct": False, "explanation": "Errado! Senhas NUNCA devem ser compartilhadas, nem com cuidado."},
                    "red": {"text": "NUNCA!", "correct": True, "explanation": "Correto! Senhas são confidenciais e pessoais. Nunca compartilhe!"}
                },
                "tip": "Senhas são confidenciais e pessoais, NUNCA compartilhe!"
            },
            {
                "question": "Compartilhar seu DIAGNÓSTICO DE SAÚDE é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Diagnóstico é informação muito sensível e privada."},
                    "yellow": {"text": "Cuidado", "correct": False, "explanation": "Errado! Diagnósticos não devem ser compartilhados, mesmo com cuidado."},
                    "red": {"text": "Não!", "correct": True, "explanation": "Correto! Dados de saúde são altamente sensíveis e privados."}
                },
                "tip": "Diagnósticos revelam informações muito pessoais sobre você"
            },
            {
                "question": "Compartilhar seu NÚMERO DE CELULAR é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Celular pode ser usado para golpes e rastreamento."},
                    "yellow": {"text": "Cuidado", "correct": True, "explanation": "Correto! Celular exige cuidado pois permite contato direto e fraudes."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Nem sempre. Às vezes é necessário compartilhar com confiança."}
                },
                "tip": "Número de celular pode ser usado para fraudes e rastreamento"
            },
            {
                "question": "Compartilhar sua DATA DE NASCIMENTO é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Data de nascimento é chave para roubo de identidade."},
                    "yellow": {"text": "Cuidado", "correct": True, "explanation": "Correto! Data de nascimento é parte importante de sua identidade."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Às vezes é necessário compartilhar, então 'Cuidado' é mais apropriado."}
                },
                "tip": "Data de nascimento + CPF = informação para roubo de identidade"
            },
            {
                "question": "Compartilhar sua FOTO é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Fotos podem ser usadas para deepfakes e fraudes."},
                    "yellow": {"text": "Cuidado", "correct": True, "explanation": "Correto! Fotos precisam de cuidado pois podem ser manipuladas."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Nem sempre. Fotos em redes sociais públicas são aceitáveis."}
                },
                "tip": "Fotos podem ser usadas em deepfakes ou para fraudes"
            },
            {
                "question": "Compartilhar sua RELIGIÃO/ORIENTAÇÃO POLÍTICA é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Isso pode gerar discriminação e assédio online."},
                    "yellow": {"text": "Cuidado", "correct": False, "explanation": "Errado! Essas informações não devem ser compartilhadas."},
                    "red": {"text": "Não!", "correct": True, "explanation": "Correto! Informações sensíveis que podem gerar discriminação."}
                },
                "tip": "Intolerância existe. Proteja sua identidade política e religiosa"
            },
            {
                "question": "Compartilhar seu ENDEREÇO RESIDENCIAL é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Endereço permite roubo, invasão e assédio."},
                    "yellow": {"text": "Cuidado", "correct": True, "explanation": "Correto! Endereço exige cuidado. Só compartilhe com confiança."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Às vezes é necessário, então 'Cuidado' é mais apropriado."}
                },
                "tip": "Seu endereço permite roubo, invasão de privacidade e assédio"
            },
            {
                "question": "Compartilhar seu EMAIL é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": True, "explanation": "Correto! Email é informação pública geralmente segura."},
                    "yellow": {"text": "Cuidado", "correct": False, "explanation": "Errado! Email é informação pública e necessária."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Errado! Email precisa ser compartilhado para se comunicar."}
                },
                "tip": "Email é necessário para comunicação e recuperação de conta"
            },
            {
                "question": "Compartilhar seus CARTÕES DE CRÉDITO é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": False, "explanation": "Errado! Dados de cartão permitem fraudes e roubo."},
                    "yellow": {"text": "Cuidado", "correct": False, "explanation": "Errado! Cartão NUNCA deve ser compartilhado, nem com cuidado."},
                    "red": {"text": "Não!", "correct": True, "explanation": "Correto! Dados de cartão nunca devem ser compartilhados."}
                },
                "tip": "Seu cartão é como dinheiro. Nunca compartilhe esses dados!"
            },
            {
                "question": "Compartilhar seu NOME DE USUÁRIO é seguro?",
                "answers": {
                    "green": {"text": "Sim", "correct": True, "explanation": "Correto! Nome de usuário é informação pública."},
                    "yellow": {"text": "Cuidado", "correct": False, "explanation": "Errado! Nome de usuário é informação pública."},
                    "red": {"text": "Não!", "correct": False, "explanation": "Errado! Nome de usuário é necessário para comunicação."}
                },
                "tip": "Nome de usuário é informação pública em plataformas"
            }
        ]

        self.current_question = 0
        self.score = 0
        self.answered = False
        self.show_tip = False
        self.game_over = False
        self.feedback_timer = 0
        self.feedback_text = ""
        self.feedback_explanation = ""
        self.is_correct = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if not self.game_over:
                    # Seta CIMA = Verde (resposta)
                    if event.key == pygame.K_UP:
                        if not self.answered:
                            self.submit_answer("green")
                    # Seta ESQUERDA = Amarelo (resposta)
                    elif event.key == pygame.K_LEFT:
                        if not self.answered:
                            self.submit_answer("yellow")
                    # Seta DIREITA = Vermelho (resposta)
                    elif event.key == pygame.K_RIGHT:
                        if not self.answered:
                            self.submit_answer("red")
                    # Seta BAIXO = Azul (Dica)
                    elif event.key == pygame.K_DOWN:
                        self.show_tip = not self.show_tip
                else:
                    # Qualquer tecla na tela de game over avança
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE, pygame.K_RETURN]:
                        return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_over and not self.answered:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.check_click(mouse_x, mouse_y)

        return True

    def check_click(self, mouse_x, mouse_y):
        # Verificar clique nos 4 botões D-Pad
        center_x = WINDOW_WIDTH // 2
        center_y = 450

        button_size = 100

        # Botão CIMA (Verde)
        green_rect = pygame.Rect(center_x - button_size // 2, center_y - 150, button_size, button_size)
        if green_rect.collidepoint(mouse_x, mouse_y):
            self.submit_answer("green")
            return

        # Botão ESQUERDA (Amarelo)
        yellow_rect = pygame.Rect(center_x - 250, center_y, button_size, button_size)
        if yellow_rect.collidepoint(mouse_x, mouse_y):
            self.submit_answer("yellow")
            return

        # Botão DIREITA (Vermelho)
        red_rect = pygame.Rect(center_x + 150, center_y, button_size, button_size)
        if red_rect.collidepoint(mouse_x, mouse_y):
            self.submit_answer("red")
            return

        # Botão BAIXO (Azul - Dica)
        blue_rect = pygame.Rect(center_x - button_size // 2, center_y + 150, button_size, button_size)
        if blue_rect.collidepoint(mouse_x, mouse_y):
            self.show_tip = not self.show_tip
            return

    def submit_answer(self, answer_key):
        if self.answered:
            return

        self.answered = True
        question = self.questions[self.current_question]
        correct = question["answers"][answer_key]["correct"]

        if correct:
            self.score += 1
            self.feedback_text = "✓ CORRETO!"
            self.is_correct = True
        else:
            self.feedback_text = "✗ ERRADO!"
            self.is_correct = False

        # Armazenar explicação da resposta
        self.feedback_explanation = question["answers"][answer_key]["explanation"]
        self.feedback_timer = 240  # 4 segundos a 60 FPS para ler a explicação

    def next_question(self):
        self.current_question += 1

        if self.current_question >= len(self.questions):
            self.game_over = True
        else:
            self.answered = False
            self.show_tip = False
            self.feedback_timer = 0
            self.feedback_text = ""
            self.feedback_explanation = ""

    def draw(self):
        self.screen.fill(DARK_GRAY)

        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_question()

        pygame.display.flip()

    def draw_game_over(self):
        # Título
        title_text = self.font_title.render("Quiz Concluído!", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Pontuação
        score_text = self.font_question.render(
            f"Sua pontuação: {self.score}/{len(self.questions)}",
            True, WHITE
        )
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(score_text, score_rect)

        # Mensagem de acordo com pontuação
        percentage = (self.score / len(self.questions)) * 100
        if percentage == 100:
            msg = "Perfeito! Você conhece bem sobre privacidade!"
            color = GREEN
        elif percentage >= 75:
            msg = "Bom! Você sabe bastante sobre proteção de dados!"
            color = YELLOW
        elif percentage >= 50:
            msg = "Você está no caminho certo. Continue aprendendo!"
            color = YELLOW
        else:
            msg = "Continue aprendendo sobre privacidade e segurança!"
            color = RED

        msg_text = self.font_button.render(msg, True, color)
        msg_rect = msg_text.get_rect(center=(WINDOW_WIDTH // 2, 400))
        self.screen.blit(msg_text, msg_rect)

        # Instruções
        inst_text = self.font_small.render("Pressione qualquer seta para sair", True, LIGHT_GRAY)
        inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, 550))
        self.screen.blit(inst_text, inst_rect)

    def draw_question(self):
        question = self.questions[self.current_question]

        # Número da pergunta
        q_num_text = self.font_small.render(
            f"Pergunta {self.current_question + 1}/{len(self.questions)}",
            True, LIGHT_GRAY
        )
        q_num_rect = q_num_text.get_rect(topleft=(20, 20))
        self.screen.blit(q_num_text, q_num_rect)

        # Pontuação
        score_text = self.font_small.render(
            f"Acertos: {self.score}",
            True, GREEN
        )
        score_rect = score_text.get_rect(topright=(WINDOW_WIDTH - 20, 20))
        self.screen.blit(score_text, score_rect)

        # Pergunta (no topo)
        question_text = self.font_question.render(question["question"], True, WHITE)
        question_rect = question_text.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(question_text, question_rect)

        # Dica (se ativada)
        if self.show_tip:
            tip_bg = pygame.Rect(50, 160, WINDOW_WIDTH - 100, 100)
            pygame.draw.rect(self.screen, BLUE, tip_bg)
            pygame.draw.rect(self.screen, WHITE, tip_bg, 3)

            tip_text = self.font_small.render(question["tip"], True, WHITE)
            tip_rect = tip_text.get_rect(center=tip_bg.center)
            self.screen.blit(tip_text, tip_rect)

        # D-Pad com 4 botões
        center_x = WINDOW_WIDTH // 2
        center_y = 450
        button_size = 100
        spacing = 20

        # Posições dos botões em formato D-Pad
        buttons = {
            "green": {
                "pos": (center_x - button_size // 2, center_y - 150),
                "color": GREEN,
                "label": "OK"
            },
            "yellow": {
                "pos": (center_x - 250, center_y),
                "color": YELLOW,
                "label": "TALVEZ"
            },
            "red": {
                "pos": (center_x + 150, center_y),
                "color": RED,
                "label": "NÃO"
            },
            "blue": {
                "pos": (center_x - button_size // 2, center_y + 150),
                "color": BLUE,
                "label": "DICA"
            }
        }

        # Desenhar os 4 botões
        for key, btn_data in buttons.items():
            button_rect = pygame.Rect(btn_data["pos"][0], btn_data["pos"][1], button_size, button_size)

            # Cor e estilo
            if self.answered and key in ["green", "yellow", "red"]:
                if question["answers"][key]["correct"]:
                    # Resposta correta - borda grossa
                    pygame.draw.rect(self.screen, btn_data["color"], button_rect)
                    pygame.draw.rect(self.screen, WHITE, button_rect, 4)
                else:
                    # Resposta errada - escurece
                    dimmed_color = tuple(int(c * 0.6) for c in btn_data["color"])
                    pygame.draw.rect(self.screen, dimmed_color, button_rect)
                    pygame.draw.rect(self.screen, WHITE, button_rect, 2)
            else:
                pygame.draw.rect(self.screen, btn_data["color"], button_rect)
                pygame.draw.rect(self.screen, WHITE, button_rect, 3)

            # Texto do botão (maior e centrado)
            text = self.font_button.render(btn_data["label"], True, BLACK)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

            # Setas de instrução acima/abaixo/lado do botão
            arrow_font = pygame.font.Font(None, 24)
            if key == "green":
                arrow = arrow_font.render("↑", True, WHITE)
                arrow_rect = arrow.get_rect(center=(button_rect.centerx, button_rect.top - 20))
                self.screen.blit(arrow, arrow_rect)
            elif key == "yellow":
                arrow = arrow_font.render("←", True, WHITE)
                arrow_rect = arrow.get_rect(center=(button_rect.left - 20, button_rect.centery))
                self.screen.blit(arrow, arrow_rect)
            elif key == "red":
                arrow = arrow_font.render("→", True, WHITE)
                arrow_rect = arrow.get_rect(center=(button_rect.right + 20, button_rect.centery))
                self.screen.blit(arrow, arrow_rect)
            elif key == "blue":
                arrow = arrow_font.render("↓", True, WHITE)
                arrow_rect = arrow.get_rect(center=(button_rect.centerx, button_rect.bottom + 20))
                self.screen.blit(arrow, arrow_rect)

        # Feedback
        if self.answered:
            if self.feedback_timer > 0:
                # Fundo semi-transparente para feedback
                feedback_bg = pygame.Rect(50, 250, WINDOW_WIDTH - 100, 150)
                pygame.draw.rect(self.screen, BLACK, feedback_bg)
                pygame.draw.rect(self.screen, WHITE, feedback_bg, 2)

                # Texto de acerto/erro
                feedback_color = GREEN if self.is_correct else RED
                feedback_text = self.font_title.render(
                    self.feedback_text,
                    True,
                    feedback_color
                )
                feedback_rect = feedback_text.get_rect(center=(WINDOW_WIDTH // 2, 270))
                self.screen.blit(feedback_text, feedback_rect)

                # Explicação da resposta
                explanation_text = self.font_small.render(
                    self.feedback_explanation,
                    True,
                    WHITE
                )
                explanation_rect = explanation_text.get_rect(center=(WINDOW_WIDTH // 2, 330))
                self.screen.blit(explanation_text, explanation_rect)

                self.feedback_timer -= 1
            else:
                # Avança para próxima pergunta
                self.next_question()

        # Instruções na parte inferior
        inst_text = self.font_small.render(
            "Aperte as SETAS DIRECIONAIS para responder",
            True, LIGHT_GRAY
        )
        inst_rect = inst_text.get_rect(center=(WINDOW_WIDTH // 2, 650))
        self.screen.blit(inst_text, inst_rect)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = QuizGame()
    game.run()

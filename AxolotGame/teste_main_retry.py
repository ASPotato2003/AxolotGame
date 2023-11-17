import pygame, sys, random
from pygame.math import Vector2

game_active = False
game_over = False


# Classe para o Axolot
class Axolot:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  # Inicializa o corpo do Axolot com três blocos
        self.direction = Vector2(1, 0)  # Inicializa a direção para a direita
        self.new_block = False  # Flag para adicionar um novo bloco ao corpo

        self.head_up = pygame.image.load('Imagens/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Imagens/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Imagens/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Imagens/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Imagens/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Imagens/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Imagens/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Imagens/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Imagens/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Imagens/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Imagens/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Imagens/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Imagens/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Imagens/body_bl.png').convert_alpha()

    def draw(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)
    def update_head_graphics(self):

        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):

        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down
    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True  # Define a flag para adicionar um novo bloco ao corpo

# Classe para o Shrimp (fruta)
class Shrimp:
    def __init__(self):
        self.randomize()  # Inicializa a posição do Shrimp

    def draw(self):
        shrimp_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(shrimp_img, shrimp_rect)  # Desenha o Shrimp usando uma imagem

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)  # Gera uma posição aleatória para o Shrimp
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

# Classe para o jogo Axolot
class AxolotGame:
    def __init__(self):
        self.axolot = Axolot()
        self.shrimp = Shrimp()

    def update(self):
        self.axolot.move()  # Atualiza a posição do Axolot
        self.check_collision()  # Verifica colisão com o Shrimp
        self.check_fail()  # Verifica se o jogo acabou

    def draw_elements(self):
        self.shrimp.draw()  # Desenha o Shrimp
        self.axolot.draw()  # Desenha o Axolot
        #self.draw_score()

    def check_collision(self):
        if self.shrimp.pos == self.axolot.body[0]:
            self.shrimp.randomize()  # Gera uma nova posição para o Shrimp
            self.axolot.add_block()  # Adiciona um novo bloco ao corpo do Axolot

    def check_fail(self):
        if not (0 <= self.axolot.body[0].x < cell_number) or not (0 <= self.axolot.body[0].y < cell_number):
            self.game_over()  # Verifica se o Axolot saiu dos limites do jogo
        for block in self.axolot.body[1:]:
            if block == self.axolot.body[0]:
                self.game_over()  # Verifica colisão do Axolot consigo mesmo

    def game_over(self):
        pygame.quit()
        sys.exit()  # Encerra o jogo

    #def draw_score(self):
        #score_text = str(len(self.axolot.body) - 3)
        #score_surface = game_font.render(score_text,True,(56,74,12))
        #score_x = int(cell_size * cell_number - 60)
        #score_y = int(cell_size * cell_number - 40)
        #score_rect = score_surface.get_rect(center = (score_x,score_y))
        #shrimp_rect = Shrimp.get_rect(midright = (score_rect.left, score_rect.centery))
        #bg_rect = pygame.Rect(shrimp_rect.left,shrimp_rect.top,shrimp_rect.widht + score_rect.width,shrimp_rect.height)

        #pygame.draw.rect(screen,(167,209,61),bg_rect)
        #screen.blit(score_surface,score_rect)
        #screen.blit(Shrimp, shrimp_rect)
        #pygame.draw.rect(screen, (167, 209, 61), bg_rect, 2)

# Configurações iniciais
pygame.init()
cell_size = 48
cell_number = 15
fundo_jogo = pygame.image.load('Imagens/fundo_jogo.jpeg')
fundo_start = pygame.image.load('Imagens/fundo_start.png')
fundo_retry = pygame.image.load('Imagens/fundo_retry.png')
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
shrimp_img = pygame.image.load('Imagens/shrimp.png')
#game_font = pygame.font.Font('Fonte/04B_30__.TTF', 25)

# Instancia o jogo
axolot_game = AxolotGame()

# Timer para atualização da tela
screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 150)

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            axolot_game.update()  # Atualiza o jogo
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not game_active or game_over:
                    # Inicia ou reinicia o jogo
                    game_active = True
                    game_over = False
                    axolot_game = AxolotGame()
            elif game_active:
                if event.key == pygame.K_UP:
                    if axolot_game.axolot.direction.y != 1:
                        axolot_game.axolot.direction = Vector2(0, -1)
                elif event.key == pygame.K_RIGHT:
                    if axolot_game.axolot.direction.x != -1:
                        axolot_game.axolot.direction = Vector2(1, 0)
                elif event.key == pygame.K_DOWN:
                    if axolot_game.axolot.direction.y != -1:
                        axolot_game.axolot.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT:
                    if axolot_game.axolot.direction.x != 1:
                        axolot_game.axolot.direction = Vector2(-1, 0)
            # Restante do código...
            if game_active:
                # Lógica do jogo quando está ativo
                screen.blit(fundo_jogo, (0, 0))
                axolot_game.update()
                axolot_game.draw_elements()
            elif game_over:
                # Lógica do jogo quando está no estado de game over
                screen.blit(fundo_retry, (0, 0))
                # Adicione aqui qualquer outra coisa que você queira exibir no estado de game over
            else:
                # Lógica do jogo quando está no estado de start
                screen.blit(fundo_start, (0, 0))
                # Adicione aqui qualquer outra coisa que você queira exibir no estado de start


    pygame.display.update()
    clock.tick(10)  # Limita a taxa de atualização para 10 quadros por segundo

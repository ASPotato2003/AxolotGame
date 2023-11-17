import pygame,sys,random
from pygame.math import Vector2

class cobra:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_cobra(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(183,111,122),block_rect)

    def move_cobra(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class fruta:
    def __init__(self):
        self.randomize()

    def draw_fruta(self, fruta):
        fruta_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(fruta, fruta_rect)
        #pygame.draw.rect(screen,(126,166,114),fruta_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class main:
    def __init__(self):
        self.cobra = cobra()
        self.fruta = fruta()

    def update(self):
        self.cobra.move_cobra()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruta.draw_fruta()
        self.cobra.draw_cobra()

    def check_collision(self):
        if self.fruta.pos == self.cobra.body[0]:
            self.fruta.randomize()
            self.cobra.add_block()

    def check_fail(self):
        if not 0 <= self.cobra.body[0].x < cell_number or not 0 <= self.cobra.body[0].y < cell_number:
            self.game_over()
        for block in self.cobra.body[1:]:
            if block == self.cobra.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

#Configurações do jogo
pygame.init()
cell_size = 40
cell_number = 20
ceu_img = pygame.image.load('Imagens/ceu.jpg')
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
fruta_img = pygame.image.load('Imagens/apple.png')

#Instanciar o jogo
main_game = main()

#Timer para atualização do game
screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == screen_update:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.cobra.direction.y != 1:
                    main_game.cobra.direction = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                if main_game.cobra.direction.x != -1:
                    main_game.cobra.direction = Vector2(1,0)
            if event.key == pygame.K_DOWN:
                if main_game.cobra.direction.y != -1:
                    main_game.cobra.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.cobra.direction.x != 1:
                    main_game.cobra.direction = Vector2(-1,0)

    screen.blit(ceu_img, (0, 0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
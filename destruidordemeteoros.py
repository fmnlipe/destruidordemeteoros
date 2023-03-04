import pygame as pg, sys, random

class Nave(pg.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pg.image.load("graphics/ship.png").convert_alpha()
        self.rect = self.image.get_rect(center = (comprimento_tela/2, altura_tela/2))
        
        # mask
        self.mask = pg.mask.from_surface(self.image)
        
        # timer
        self.can_shoot = True
        self.shoot_time = None

        #som
        self.sound = pg.mixer.Sound("sounds/laser.ogg")

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pg.time.get_ticks()
            if current_time - self.shoot_time > 500:
                self.can_shoot = True

    def input_position(self):
        pos = pg.mouse.get_pos()
        self.rect.center = pos

    def laser_shoot(self):
        if pg.mouse.get_pressed()[0] and self.can_shoot == True: # indexador indica que apenas usaremos o botão esquerdo do mouse.
            self.can_shoot = False
            self.shoot_time = pg.time.get_ticks()
            self.sound.play()
            Laser(laser_grupo, pos = self.rect.midtop)

    def colisao_meteoro(self):
        if pg.sprite.spritecollide(self, meteoro_grupo, False, pg.sprite.collide_mask):
            self.kill()
            pg.quit()
            sys.exit()

    def update(self):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()
        self.colisao_meteoro()

class Laser(pg.sprite.Sprite):
    def __init__(self, *groups, pos):
        super().__init__(*groups)
        self.image = pg.image.load("graphics/laser.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.mask = pg.mask.from_surface(self.image)
        # float based position
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2(0,-1)
        self.speed = 600
        self.sound = pg.mixer.Sound("sounds/explosion.wav")

    def colisao_meteoro(self):
        if pg.sprite.spritecollide(self, meteoro_grupo, True, pg.sprite.collide_mask):
            self.sound.play()
            self.kill()
            

    def update(self):
        self.pos += self.direction * self.speed * deltatime
        self.rect.topleft = (round(self.pos.x), round(self.pos.y)) # se não arredondassemos aqui, teriamos um número truncado.
        
        if self.rect.bottom < 0:
            self.kill()
        
        self.colisao_meteoro()


class Meteoros(pg.sprite.Sprite):
    def __init__(self, *groups, pos):
        
        # início
        super().__init__(*groups)
        meteoro_surf = pg.image.load("graphics/meteor.png").convert_alpha()
        meteoro_tamanho = pg.math.Vector2(meteoro_surf.get_size()) * random.uniform(0.5, 1.5)
        self.scaled_meteoro = pg.transform.scale(meteoro_surf, meteoro_tamanho)
        self.image = self.scaled_meteoro
        self.rect = self.image.get_rect(center = pos)
        self.mask = pg.mask.from_surface(self.image)
        
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.direction = pg.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 600)

        # rotação
        self.rotation = 0
        self.rotation_speed = random.randint(20,50)
    
    def rotação(self):
        self.rotation += self.rotation_speed * deltatime
        rotate_surf = pg.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotate_surf
        self.rect = self.image.get_rect(center = self.rect.center)
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.pos += self.direction * self.speed * deltatime
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        if self.rect.top > altura_tela:
            self.kill()

class Score:
    def __init__(self):
        self.font = pg.font.Font("graphics/subatomic.ttf", 50)
    
    def display(self):
        score_text = (f"Score: {pg.time.get_ticks()//1000}")
        text_surf = self.font.render( score_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midbottom = (comprimento_tela/2, altura_tela - 80))
        display_surface.blit(text_surf, text_rect)
        pg.draw.rect(display_surface, "crimson", text_rect.inflate(30,30), width = 7)
      
# início
pg.init()
comprimento_tela, altura_tela = 1280, 720
display_surface = pg.display.set_mode((comprimento_tela, altura_tela))
pg.display.set_caption("Destruidor de Meteoros")
clock = pg.time.Clock()

# background
background_surf = pg.image.load("graphics/background.png").convert()

# grupos
nave_grupo = pg.sprite.Group()
laser_grupo = pg.sprite.Group()
meteoro_grupo = pg.sprite.Group()

# criando o objeto
nave = Nave(nave_grupo)
score = Score()
# timer pro meteoro
meteor_timer = pg.event.custom_type()
pg.time.set_timer(meteor_timer, 400)

# música
musica = pg.mixer.Sound("sounds/music.wav")
musica.play(loops = -1)

# game loop
while True:
    # event loop
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == meteor_timer:
            meteoro_y_pos = random.randint(-150, -50)
            meteoro_x_pos = random.randint(-100, comprimento_tela + 100)
            Meteoros(meteoro_grupo, pos = (meteoro_x_pos, meteoro_y_pos))

    deltatime = clock.tick(60)/1000

    # mostrando tela e background
    display_surface.blit(display_surface, (0,0))
    display_surface.fill("black")
    display_surface.blit(background_surf, (0,0))
   
    # updates
    nave_grupo.update()
    laser_grupo.update()
    meteoro_grupo.update()

    # score
    score.display()

    # graphics
    nave_grupo.draw(display_surface)
    laser_grupo.draw(display_surface)
    meteoro_grupo.draw(display_surface)

    # revelando os frames
    pg.display.update()
    

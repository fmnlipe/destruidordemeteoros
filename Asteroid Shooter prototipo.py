import pygame as pg, sys, random

def laser_update(laser_list, speed = 300):
    for laser in laser_list:
        laser.y -= speed * deltatime
        if laser.bottom < 0:
            laser_list.remove(laser)

def display_score():
    score_text = f"Score: {pg.time.get_ticks()//1000}"
    text_surf = font.render(score_text,True ,(255, 255, 255))
    text_rect = text_surf.get_rect(midbottom = (comprimento_tela/2, altura_tela - 80))
    display_surface.blit(text_surf, text_rect)
    pg.draw.rect(display_surface, "crimson", text_rect.inflate(30,30), width = 7)

def timer(can_shoot, duration = 500):
    if not can_shoot:
        current_time = pg.time.get_ticks()
        if current_time - shoot_time > duration:
            can_shoot = True
    return can_shoot

def meteor_update(meteor_list, speed = 300):
    for meteor_tuple in meteor_list:
        direction = meteor_tuple[1]
        meteor_rect = meteor_tuple[0]
        meteor_rect.center += direction * speed * deltatime
        if meteor_rect.top > altura_tela:
            meteor_list.remove(meteor_tuple)

# iniciando o jogo
pg.init()
comprimento_tela, altura_tela = 1280, 720
display_surface = pg.display.set_mode((comprimento_tela, altura_tela)) #medidas da tela
pg.display.set_caption("Asteroid Shooter") # mudar nome depois
clock = pg.time.Clock()

# importando a nave
ship_surf = pg.image.load("graphics/ship.png").convert_alpha()
ship_rect = ship_surf.get_rect(center = (comprimento_tela/2, altura_tela/2))

# importando o laser
laser_surf = pg.image.load("graphics/laser.png").convert_alpha()
laser_list = []

# laser timer
can_shoot = True
shoot_time = None

# fundo
background = pg.image.load("graphics/background.png").convert()

# importando o meteoro
meteor_surf = pg.image.load("graphics/meteor.png").convert_alpha()
meteor_list = []
meteor_rect = meteor_surf.get_rect(midbottom = (comprimento_tela/2, 0))

# meteoro timer
meteor_timer = pg.event.custom_type()
pg.time.set_timer(meteor_timer, 500)

# importando texto
font = pg.font.Font("graphics/subatomic.ttf", 50)

# importando sons
laser_sound = pg.mixer.Sound("sounds/laser.ogg")
explosion_sound = pg.mixer.Sound("sounds/explosion.wav")
music = pg.mixer.Sound("sounds/music.wav")

music.play(loops = -1)

while True: 

    # event loop
    for event in pg.event.get():
        # saindo do jogo
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        
        # controle do laser + sua duração
        if event.type == pg.MOUSEBUTTONDOWN and can_shoot == True:
            # laser logic
            laser_rect = laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)
            # timer
            can_shoot = False
            shoot_time = pg.time.get_ticks()

            # iniciando o som do laser
            laser_sound.play()
        
        # randomizando o meteoro
        if event.type == meteor_timer:

            # posição aleatória
            x_pos = random.randint(-100, comprimento_tela + 100)
            y_pos = random.randint(-100, -50)

            # criando um rect
            meteor_rect = meteor_surf.get_rect(center = (x_pos, y_pos))
            
            # direção aleatória
            direction = pg.math.Vector2(random.uniform(-0.5, 0.5), 1)

            meteor_list.append((meteor_rect, direction)) # coloque em uma tupla

    #framerate limit
    deltatime = clock.tick(120) / 1000 # em segundos

    # mouse input
    ship_rect.center = pg.mouse.get_pos()

    # colisão meteoro-nave
    for meteor_tuple in meteor_list:
        meteor_rect = meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            explosion_sound.play()
            pg.quit()
            sys.exit()
    
    # colisão laser-meteoro
    for laser_rect in laser_list:
        for meteor_tuple in meteor_list:
            if laser_rect.colliderect(meteor_tuple[0]):
                meteor_list.remove(meteor_tuple)
                laser_list.remove(laser_rect)
                explosion_sound.play()

    # updates
    display_surface.fill((0,0,0))
    display_surface.blit(background, (0,0))
    
    display_score()
    
    laser_update(laser_list)
    can_shoot = timer(can_shoot, 500)
    meteor_update(meteor_list)

    display_surface.blit(ship_surf, ship_rect)


    for laser in laser_list:
        display_surface.blit(laser_surf, laser)
    
    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf, meteor_tuple[0])

    # mostrar os frames
    pg.display.update()

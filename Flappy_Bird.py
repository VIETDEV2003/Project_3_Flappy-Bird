import pygame
import sys
import random

def create_pipe():
    pipe_random = random.randint(30, 55) * 10
    top_pipe = pipe.get_rect(midtop = (530, pipe_random))
    bottom_pipe = pipe.get_rect(midtop = (530, pipe_random - 750))
    return top_pipe, bottom_pipe

def draw_pipe(pipe_list):
    for x in pipe_list:
        if x.bottom >= 700:
            screen.blit(pipe, x)
        else: 
            pipe_flip = pygame.transform.flip(pipe, False, True)   
            screen.blit(pipe_flip, x) 

def move_pipe(pipe_list):
    for x in pipe_list:
        x.centerx -= 4 
    return pipe_list

def check_vacham(pipe_list):
    for x in pipe_list:
        if bird_rect.colliderect(x): 
            hit_sound.play()
            return False  
    if bird_rect.centery >= 600:
        die_sound.play()
        return False
    if bird_rect.centery <= -100:
        hit_sound.play()
        return False
    return True       

def score_game(game_state):
    if game_state:
        score_display = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_display.get_rect(center = (225, 50)) 
        screen.blit(score_display, score_rect)     
    if game_state == False:
        score_display = game_font.render(f'Score : {int(score)}', True, (255, 255, 255))
        score_rect = score_display.get_rect(center = (225, 50)) 
        screen.blit(score_display, score_rect) 
        
        high_score_display = game_font.render(f'High Score : {int(high_score)}', True, (255, 0, 0))
        high_score_rect = high_score_display.get_rect(center = (225, 550)) 
        screen.blit(high_score_display, high_score_rect) 

def score_update(score, high_score):
    if score > high_score:
        high_score = score
    return high_score    
 
def bird_animation():
    bird_new = bird_list[bird_index]
    bird_new_rect = bird_new.get_rect(center = (100, bird_rect.centery))
    return bird_new, bird_new_rect
 
def bird_rotozoom(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_move * 3, 1)
    return new_bird

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)            
pygame.init()
pygame.display.set_caption("Flappy Bird")
screen = pygame.display.set_mode((450, 750))
clock = pygame.time.Clock()

x_pos_floor = 0
gravity = 0.25  
bird_move = 0
pipe_list = [] 

bg = pygame.image.load("Python/images/background-night.png").convert()
bg = pygame.transform.scale(bg, (450, 750)) 

floor = pygame.image.load("Python/images/floor.png").convert()
floor = pygame.transform.scale2x(floor)

pipe = pygame.image.load("Python/images/pipe-green.png").convert()
pipe = pygame.transform.scale2x(pipe)


bird_mid = pygame.image.load("Python/images/yellowbird-midflap.png").convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid) 

bird_top = pygame.image.load("Python/images/yellowbird-upflap.png").convert_alpha()
bird_top = pygame.transform.scale2x(bird_top)

bird_bottom = pygame.image.load("Python/images/yellowbird-downflap.png").convert_alpha()
bird_bottom = pygame.transform.scale2x(bird_bottom)

bird_rect = bird_mid.get_rect(center = (100, 150))
bird_list = [bird_mid, bird_top, bird_bottom] 
bird_index = 0
bird = bird_list[bird_index]

game_over = pygame.image.load("Python/images/message.png").convert_alpha()
game_over = pygame.transform.scale2x(game_over)
game_over_rect = game_over.get_rect(center = (225, 300))

event_draw_pipe = pygame.USEREVENT
pygame.time.set_timer(event_draw_pipe, 1200)

event_animation_bird = pygame.USEREVENT + 1
pygame.time.set_timer(event_animation_bird, 300)

game_active = True
game_font = pygame.font.Font('Python/font/04B_19.ttf',35)

score = 0
high_score = 0

die_sound = pygame.mixer.Sound("Python/sounds/sfx_die.wav")
hit_sound = pygame.mixer.Sound("Python/sounds/sfx_hit.wav")
score_sound = pygame.mixer.Sound("Python/sounds/sfx_point.wav")
flap_sound = pygame.mixer.Sound("Python/sounds/sfx_wing.wav")

time_score_sound = 100

while True:   
    screen.blit(bg, (0, 0))    
    x_pos_floor -= 4
    
    if x_pos_floor <= -400:
        x_pos_floor = 0
    
    if game_active: 
        bird_move += gravity
        bird_rect.centery += bird_move
        game_active = check_vacham(pipe_list)   
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_game(game_active)
        bird_rotate = bird_rotozoom(bird)
        screen.blit(bird_rotate, bird_rect)
        time_score_sound -= 1
        if time_score_sound <= 0:
            score_sound.play()
            time_score_sound = 100
    else:   
        screen.blit(game_over, game_over_rect)
        high_score = score_update(score, high_score) 
        score_game(game_active)
                
    screen.blit(floor, (x_pos_floor, 600))
    screen.blit(floor, (x_pos_floor + 450, 600)) 
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_move = 0
                bird_move -= 9 
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()    
                bird_move = 0
                bird_rect.center = (100, 150)
                score = 0
        if event.type == event_draw_pipe:
            pipe_list.extend(create_pipe())
        if event.type == event_animation_bird:
            if bird_index < 2:
                bird_index += 1 
            else: 
                bird_index = 0 
            bird, bird_rect = bird_animation()                               
    pygame.display.update()
    clock.tick(120)              
            
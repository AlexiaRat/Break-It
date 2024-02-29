import pygame
import random
import time
import keyboard
import sys


pygame.init()
# colors
black = (0, 0, 0)
blue = (51, 153, 255)
grey = (160, 160, 160)
brown = (102, 51, 0)
orange = (255, 102, 0)
green = (0, 255, 43)
white = (255, 255, 255)

# display
width = 900
height = 700
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Break-It')
icon = pygame.image.load("images.jpeg")
pygame.display.set_icon(icon)

background_image = pygame.image.load("start.jpg")
background_surface = pygame.Surface((width, height))
background_surface.blit(background_image, (0, 0))

#start/exit
button = []
button_width = 200
button_height = 50
button_color = (100, 100, 100)
hover_color = (150, 150, 150)
button_text_color = (255, 255, 255)
font_3 = pygame.font.Font(None, 24)

def draw_button(screen, button_prop, text, hovered):
    if hovered:
        pygame.draw.rect(screen, hover_color, button_prop)
    else:
        pygame.draw.rect(screen, button_color, button_prop)
    pygame.draw.rect(screen, hover_color, button_prop, 3)
    text = font_3.render(text, True, button_text_color)
    text_rect = text.get_rect(center=button_prop.center)
    screen.blit(text, text_rect)

def is_hovered(button_prop, pos):
    return button_prop.collidepoint(pos)

def menu_buttons():
    start_button_prop = pygame.Rect(300, 250, button_width, button_height)
    exit_button_prop = pygame.Rect(300, 320, button_width, button_height)
    mouse_pos = pygame.mouse.get_pos()
    start_hovered = is_hovered(start_button_prop, mouse_pos)
    exit_hovered = is_hovered(exit_button_prop, mouse_pos)
    draw_button(window, start_button_prop, "Start", start_hovered)
    draw_button(window, exit_button_prop, "Exit", exit_hovered)

    return {
        'Start': start_hovered,
        'Exit': exit_hovered
    }


score_font = pygame.font.SysFont(pygame.font.get_default_font(), 32)
pause_font = pygame.font.SysFont(pygame.font.get_default_font(), 200)
game_over_font = pygame.font.SysFont(pygame.font.get_default_font(), 64)
congratulations_font = pygame.font.SysFont(pygame.font.get_default_font(), 64)

#paddle
paddle_width = 100
paddle_height = 20
paddle_x = (width - paddle_width) // 2
paddle_y = height - paddle_height - 10
paddle_speed = 5

#ball
ball_radius = 10
ball_x = width // 2
ball_y = height // 2 + 30
ball_speed_x = random.choice([-2, 2])
ball_speed_y = 4

n = 9
k = 3
#bricks
bricks_orange = []
bricks_brown = []
bricks_grey = []
bricks_green = []

for i in range(n):
    for j in range(n):
        if i == 0 and j == 0 or i == 0 and j == n - 1 or i == n - 1 and j == 0 or i == n - 1 and j == n - 1:
            brick = pygame.draw.rect(window, grey, [45 + 90 * i, 50 + 30 * j, 90, 30])
            bricks_grey.append(brick)
        elif i >= 1 and i < n - 1 and j == 0 or j > 0 and j < n - 1 and i == 0 or i >= 1 and i < n - 1 and j == n - 1 or j > 0 and j < n - 1 and i == n - 1:
            brick = pygame.draw.rect(window, orange, [45 + 90 * i, 50 + 30 * j, 90, 30])
            bricks_orange.append(brick)
        elif i == j and i > 0 and i < n - 1 or n - 1 == i + j and i > 0 and i < n - 1:
            brick = pygame.draw.rect(window, orange, [45 + 90 * i, 50 + 30 * j, 90, 30])
            bricks_orange.append(brick)
        else:
            brick = pygame.draw.rect(window, brown, [45+ 90 * i, 50 + 30 * j, 90, 30])
            bricks_brown.append(brick)
while k != 0:
    brick = pygame.draw.rect(window, green, [45 + 90 * random.choice(range(n)), 50 + 30 * random.choice(range(n)), 90, 30])
    bricks_green.append(brick)
    k -= 1

clock = pygame.time.Clock()
running = True
paused = False

def pause():
    global paused
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        window.fill(black)
        draw_objects()
        text = pause_font.render("PAUSE", True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        window.blit(text, text_rect)
        pygame.display.update()
        clock.tick(5)

def draw_objects():
    window.fill(black)
    pygame.draw.rect(window, grey, [paddle_x, paddle_y, paddle_width, paddle_height])
    pygame.draw.circle(window, grey, (ball_x, ball_y), ball_radius)
    for brick in bricks_orange:
        pygame.draw.rect(window, orange, brick)
    for brick in bricks_brown:
        pygame.draw.rect(window, brown, brick)
    for brick in bricks_grey:
        pygame.draw.rect(window, grey, brick)
    for brick in bricks_green:
        pygame.draw.rect(window, green, brick)
def show_congratulations():
    congratulations_text = congratulations_font.render("Congratulations!", True, white)
    text_rect = congratulations_text.get_rect(center=(width // 2, height // 2))
    window.blit(congratulations_text, text_rect)

def update_game():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, score

    #stg/dr paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed
        if paddle_x < 0:  
            paddle_x = 0
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed
        if paddle_x > width - paddle_width:  
            paddle_x = width - paddle_width

     #ball speed modif
    if keys[pygame.K_UP]:
        ball_speed_y -= 1
    if keys[pygame.K_DOWN]:
        ball_speed_y += 1

   #b all movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    #collision with walls
    if ball_x <= 0 or ball_x >= width - ball_radius:
        ball_speed_x *= -1
    if ball_y <= 0:
        ball_speed_y *= -1

    #collision with bricks
    for brick in bricks_orange:
        if brick.colliderect(pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)):
            ball_speed_y *= -1
            bricks_orange.remove(brick)
            score += 10
            break

    for brick in bricks_brown:
        if brick.colliderect(pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)):
            ball_speed_y *= -1
            bricks_brown.remove(brick)
            score += 10
            bricks_orange.append(brick) 
            break

    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    ball_rect = pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)
    
    for brick in bricks_grey:
        if brick.colliderect(pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)):
            ball_speed_y *= -1
            break

    for brick in bricks_green:
        if brick.colliderect(pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)):
            ball_speed_y *= -1
            bricks_green.remove(brick)
            break

    #cxollision with paddle
    if pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height).colliderect(pygame.Rect(ball_x, ball_y, ball_radius, ball_radius)):
        ball_speed_y *= -1

    #game over
    if ball_y >= height - ball_radius - paddle_height:
        show_game_over()
        return False
    if len(bricks_orange) ==  0 and len(bricks_brown) == 0 and len(bricks_green) == 0:
            show_congratulations()
        
    return True
def show_game_over():
    global running
    running = False
    while not running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        window.fill(black)
        text = game_over_font.render("GAME OVER", True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        window.blit(text, text_rect)
        pygame.display.update()
        clock.tick(5)

def reset_game():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, score, bricks_orange, bricks_brown, bricks_grey, bricks_green, running

    paddle_x = (width - paddle_width) // 2
    ball_x = width // 2
    ball_y = height // 2 + 30
    ball_speed_x = random.choice([-2, 2])
    ball_speed_y = 4
    score = 0
    k=3
    bricks_orange = []
    bricks_brown = []
    bricks_grey = []
    bricks_green = []

    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0 or i == 0 and j == n - 1 or i == n - 1 and j == 0 or i == n - 1 and j == n - 1:
                brick = pygame.draw.rect(window, grey, [45 + 90 * i, 50 + 30 * j, 90, 30])
                bricks_grey.append(brick)
            elif i >= 1 and i < n - 1 and j == 0 or j > 0 and j < n - 1 and i == 0 or i >= 1 and i < n - 1 and j == n - 1 or j > 0 and j < n - 1 and i == n - 1:
                brick = pygame.draw.rect(window, orange,[ 45 + 90 * i, 50 + 30 * j, 90, 30])
                bricks_orange.append(brick)
            elif i == j and i > 0 and i < n - 1 or n - 1 == i + j and i > 0 and i < n - 1:
                brick = pygame.draw.rect(window, orange, [45 + 90 * i, 50 + 30 * j, 90, 30])
                bricks_orange.append(brick)
            else:
                brick = pygame.draw.rect(window, brown, [45 + 90 * i, 50 + 30 * j, 90, 30])
                bricks_brown.append(brick)

    while k != 0:
        brick = pygame.draw.rect(window, green, [45 + 90 * random.choice(range(n)), 50 + 30 * random.choice(range(n)), 90, 30])
        bricks_green.append(brick)
        k -= 1

    running = True

score = 0

#game Loop
menu_screen = True
game_screen = False
start_time = 0

while menu_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                mouse_pos = pygame.mouse.get_pos()
                clicked = menu_buttons()
                if clicked['Start']:
                    menu_screen = False
                    game_screen = True
                    start_time = time.time()

                if clicked['Exit']:
                    pygame.quit()
                    sys.exit()

    window.blit(background_surface, (0, 0))
    menu_buttons()
    pygame.display.update()

while game_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause()

    if time.time() - start_time >= 1:
        update_game()

    draw_objects()

    score_text = score_font.render("Score: " + str(score), True, white)
    window.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)
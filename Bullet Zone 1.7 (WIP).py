import pygame
import math
import random

from pygame.constants import K_SPACE
def dice(x,y):
    temp = 0
    for i in range(x):
        temp += random.randint(1,y)
    return temp
print("\n\nPlayer1 is Red, WASD to accelerate. Your specials are shift, capslock, tab, and backq\
uote.\nPlayer2 is Green, ARROW keys to accelerate. Your specials are alt, comma, k, and i.\nPress SPACE to unpause")
pygame.time.delay(2000)
WIDTH = 1350
HEIGHT = 700
if True: #colors
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (255,255,0)
    CYAN = (0,255,255)
    MAGENTA = (255,0,255)
    ORANGE = (255,128,0)
    PURPLE = (128,0,255)
    WHITE = (255,255,255)
    GOLD = (218,165,32)
    GREY = (60,60,60)
    BLACK = (0,0,0)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
def HP(x,y):
    pygame.draw.rect(WIN,BLUE,pygame.Rect(200+x,y,30,30))
    pygame.draw.rect(WIN,WHITE,pygame.Rect(212+x,y+5,6,20))
    pygame.draw.rect(WIN,WHITE,pygame.Rect(205+x,y+12,20,6))
def SP1_indicator(x,y,cooldown):
    x += 3
    y += 3
    z = 12
    w = 60
    q = (w/1.4142)-(z*1.4142)
    if cooldown:
        c1 = (255,204,153)
        c2 = (255,255,153)
    else:
        c1 = ORANGE
        c2 = YELLOW
    pygame.draw.rect(WIN,BLACK,pygame.Rect(x-3,y-3,w+6,w+6))
    pygame.draw.rect(WIN,c1,pygame.Rect(x,y,w,w))
    pygame.draw.rect(WIN,c2, pygame.Rect(x+z,y+z,w-2*z,w-2*z))
    corners = [(x+q,y),(x,y+q),(x-q,y),(x,y-q)]
    corners = [(x+w/2+q,y+w/2),(x+w/2,y+w/2+q),(x+w/2-q,y+w/2),(x+w/2,y+w/2-q),]
    pygame.draw.polygon(WIN, c2, corners)
def SP2_indicator(x,y,cooldown):
    if cooldown:
        c1 = (255,204,153)
        c2 = (255,255,153)
    else:
        c1 = ORANGE
        c2 = YELLOW
    a=7
    b=10
    x += 3
    y += 3
    pygame.draw.rect(WIN,BLACK,pygame.Rect(x-3,y-3,66,66))
    pygame.draw.rect(WIN,c1,pygame.Rect(x,y,60,60))
    x += 1
    y += 1
    pygame.draw.rect(WIN,c2,pygame.Rect(x+a,y+a,b,b))
    pygame.draw.rect(WIN,c2,pygame.Rect(x+a,y+3*a+2*b,b,b))
    pygame.draw.rect(WIN,c2,pygame.Rect(x+2*a+b,y+2*a+b,b,b))
    pygame.draw.rect(WIN,c2,pygame.Rect(x+3*a+2*b,y+a,b,b))
    pygame.draw.rect(WIN,c2,pygame.Rect(x+3*a+2*b,y+3*a+2*b,b,b))
def pause_img():
    pygame.draw.circle(WIN,(235,235,255),(WIDTH/2,HEIGHT/2),50)
    pygame.draw.circle(WIN,BLUE,(WIDTH/2,HEIGHT/2),46)
    pygame.draw.rect(WIN,(235,235,255),pygame.Rect(WIDTH/2 - 20,HEIGHT/2 - 20,10,40))
    pygame.draw.rect(WIN,(235,235,255),pygame.Rect(WIDTH/2 + 10 ,HEIGHT/2 - 20,10,40))
def main():
    player_acceleration = .3
    clock = pygame.time.Clock()
    player1 = pygame.Rect((WIDTH / 2) - 85, (HEIGHT / 2)-10, 20, 20)
    player2 = pygame.Rect((WIDTH / 2) + 65, (HEIGHT / 2)-10, 20, 20)
    wall1 = pygame.Rect(195,0,5,HEIGHT)
    wall2 = pygame.Rect(WIDTH-200,0,5,HEIGHT)
    player1_health = 6
    player2_health = 6
    iframe1 = 0
    iframe2 = 0
    player1_Xspeed = 0
    player1_Yspeed = 0
    player2_Xspeed = 0
    player2_Yspeed = 0
    bullets1 = []
    bullets2 = []
    sp2_p1_active = 0
    sp2_p2_active = 0
    SP_P1_active = 0
    sp1_p1 = 200
    sp2_p1 = 300
    sp3_p1 = 200
    SP_P2_active = 0
    sp1_p2 = 200
    sp2_p2 = 300
    sp3_p2 = 200
    timer = 0
    hp_tick = 0
    hp_spot = [-100,-100]
    WAIT = True
    while True:
        WIN.fill((235,235,255))
        pygame.draw.rect(WIN, RED, player1)
        pygame.draw.rect(WIN, GREEN, player2)
        pygame.draw.rect(WIN, BLACK, wall1)
        pygame.draw.rect(WIN, BLACK, wall2)
        iframe1 -= 1
        iframe2 -= 1
        if (sp2_p1_active > 0) or (sp2_p2_active > 0):
            pygame.time.delay(60)
        keys_pressed = pygame.key.get_pressed()
        if player1.colliderect(player2):
                    player1_Xspeed = -player1_Xspeed
                    player1_Yspeed = -player1_Yspeed
                    player2_Xspeed = -player2_Xspeed
                    player2_Yspeed = -player2_Yspeed
        if True: #bullets
            for bullet in bullets1:
                bullet[3] += bullet[1]
                bullet[4] += bullet[2]
                bullet[0].x = bullet[3]
                bullet[0].y = bullet[4]
                pygame.draw.rect(WIN, GREY1, bullet[0])
                if bullet[0].colliderect(player2):
                    bullets1.remove(bullet)
                    if iframe2<0 and bullet[0].width == 10:
                        player2_health-=1
                        iframe2 = 40
                    elif bullet[0].width == 14:
                        player2_health-=1
                        iframe2 = 40
                elif bullet[0].colliderect(wall1) or bullet[0].colliderect(wall2):
                    bullets1.remove(bullet)
                elif bullet[0].y > HEIGHT or bullet[0].y < 0:
                    bullets1.remove(bullet)
            for bullet in bullets2:
                bullet[3] += bullet[1]
                bullet[4] += bullet[2]
                bullet[0].x = bullet[3]
                bullet[0].y = bullet[4]
                pygame.draw.rect(WIN, GREY2, bullet[0])
                if bullet[0].colliderect(player1):
                    bullets2.remove(bullet)
                    if iframe2<0 and bullet[0].width == 10:
                        player2_health-=1
                        iframe2 = 40
                    elif bullet[0].width == 14:
                        player2_health-=1
                        iframe2 = 40
                elif bullet[0].colliderect(wall1) or bullet[0].colliderect(wall2):
                    bullets2.remove(bullet)
                elif bullet[0].y > HEIGHT or bullet[0].y < 0:
                    bullets2.remove(bullet)
            while len(bullets1) > 60:
                del bullets1[0]
            while len(bullets2) > 60:
                del bullets2[0]
            timer += 1
            SP_P1_active += 1
            SP_P2_active += 1
            if timer%7 == 0 and timer > 69:
                if SP_P1_active > 9:
                    bullets1.append([(pygame.Rect(0,0,10,10)), player1_Xspeed*1.2, player1_Yspeed*1.2, player1.x + player1.width/4 , player1.y + player1.width / 4])
                elif sp2_p1_active > 0:
                    vectorx = player2.x-player1.x
                    vectory = player2.y-player1.y
                    mag1 = math.sqrt(vectorx*vectorx + vectory*vectory)
                    bullets1.append([(pygame.Rect(0,0,16,16)), 3*vectorx/mag1, 3*vectory/mag1, player1.x +2, player1.y +2])
                    sp2_p1_active -= 7
                if SP_P2_active > 9:
                    bullets2.append([(pygame.Rect(0,0,10,10)), player2_Xspeed*1.2, player2_Yspeed*1.2, player2.x + player2.width/4, player2.y + player2.width / 4])
                elif sp2_p2_active > 0:
                    vectorx = player1.x-player2.x
                    vectory = player1.y-player2.y
                    mag2 = math.sqrt(vectorx*vectorx + vectory*vectory)
                    bullets2.append([(pygame.Rect(0,0,16,16)), 3*vectorx/mag2, 3*vectory/mag2, player2.x +2, player2.y +2])
                    sp2_p2_active -= 7
            if timer%220 < 5:
                GREY1 = RED
                GREY2 = GREEN
            else:
                GREY1 = GREY2 = GREY
        if True: #health pickup
            hp_tick += 1
            if hp_tick == 600:
                hp_spot[0] = random.randint(1,WIDTH - 430)
                hp_spot[1] = random.randint(0,HEIGHT-30)
            if hp_tick > 1200:
                hp_spot[0] = -100
                hp_spot[1] = -100
                hp_tick = 0
            if pygame.Rect(200+hp_spot[0],hp_spot[1],30,30).colliderect(player1):
                player1_health += 1
                hp_spot[0] = -100
                hp_spot[1] = -100
                hp_tick = 0
            elif pygame.Rect(200+hp_spot[0],hp_spot[1],30,30).colliderect(player2):
                player2_health += 1
                hp_spot[0] = -100
                hp_spot[1] = -100
                hp_tick = 0
            HP(hp_spot[0],hp_spot[1])
        if player1_health < .5:
            WIN.fill(GREEN)
            pygame.display.update()
            pygame.time.delay(1500)
            main()
        if player2_health < .5:
            WIN.fill(RED)
            pygame.display.update()
            pygame.time.delay(1500)
            main()
        if True: #hp bars
            hph = 60
            hpw = 35
            hps = 22
            pygame.draw.rect(WIN, BLACK, pygame.Rect(22,HEIGHT-82,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(79,HEIGHT-82,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(136,HEIGHT-82,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(22,HEIGHT-164,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(79,HEIGHT-164,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(136,HEIGHT-164,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(22+1160,HEIGHT-82,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(79+1160,HEIGHT-82,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(136+1160,HEIGHT-82,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(22+1160,HEIGHT-164,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(79+1160,HEIGHT-164,35,60))
            pygame.draw.rect(WIN, BLACK, pygame.Rect(136+1160,HEIGHT-164,35,60))
            #hp logic
            if player1_health > .5:
                pygame.draw.rect(WIN, RED, pygame.Rect(22+4,HEIGHT-78,27,52))
            if player1_health > 1.5:
                pygame.draw.rect(WIN, RED, pygame.Rect(79+4,HEIGHT-78,27,52))
            if player1_health > 2.5:
                pygame.draw.rect(WIN, RED, pygame.Rect(136+4,HEIGHT-78,27,52))
            if player1_health > 3.5:
                pygame.draw.rect(WIN, RED, pygame.Rect(22+4,HEIGHT-160,27,52))
            if player1_health > 4.5:
                pygame.draw.rect(WIN, RED, pygame.Rect(79+4,HEIGHT-160,27,52))
            if player1_health > 5.5:
                pygame.draw.rect(WIN, RED, pygame.Rect(136+4,HEIGHT-160,27,52))
            if player2_health > .5:
                pygame.draw.rect(WIN, GREEN, pygame.Rect(22+1164,HEIGHT-78,27,52))
            if player2_health > 1.5:
                pygame.draw.rect(WIN, GREEN, pygame.Rect(79+1164,HEIGHT-78,27,52))
            if player2_health > 2.5:
                pygame.draw.rect(WIN, GREEN, pygame.Rect(136+1164,HEIGHT-78,27,52))
            if player2_health > 3.5:
                pygame.draw.rect(WIN, GREEN, pygame.Rect(22+1164,HEIGHT-160,27,52))
            if player2_health > 4.5:
                pygame.draw.rect(WIN, GREEN, pygame.Rect(79+1164,HEIGHT-160,27,52))
            if player2_health > 5.5:
                pygame.draw.rect(WIN, GREEN, pygame.Rect(136+1164,HEIGHT-160,27,52))
        if True: #movement
            player1.x += player1_Xspeed
            player1.y += player1_Yspeed
            player2.x += player2_Xspeed
            player2.y += player2_Yspeed

            if player1.x + player1.width >= WIDTH-200:
                player1.x = WIDTH - player1.width - 201
                player1_Xspeed = 0
            if player1.x <= 200:
                player1.x = 201
                player1_Xspeed = 0
            if player1.y + player1.height >= HEIGHT:
                player1.y = HEIGHT - player1.height - 1
                player1_Yspeed = 0
            if player1.y <= 0:
                player1.y = 1
                player1_Yspeed = 0
            
            if player2.x + player2.width >= WIDTH-200:
                player2.x = WIDTH - player2.width - 201
                player2_Xspeed = 0
            if player2.x <= 200:
                player2.x = 201
                player2_Xspeed = 0
            if player2.y + player2.height >= HEIGHT:
                player2.y = HEIGHT - player2.height - 1
                player2_Yspeed = 0
            if player2.y <= 0:
                player2.y = 1
                player2_Yspeed = 0

            if keys_pressed[pygame.K_a]: #left acceleration
                player1_Xspeed -= player_acceleration
                if player1_Xspeed > 0:
                    player1_Xspeed -= player_acceleration
            if keys_pressed[pygame.K_d]: #right acceleration
                player1_Xspeed += player_acceleration
                if player1_Xspeed < 0:
                    player1_Xspeed += player_acceleration
            if keys_pressed[pygame.K_w]: #up acceleration
                player1_Yspeed -= player_acceleration
                if player1_Yspeed > 0:
                    player1_Yspeed -= player_acceleration
            if keys_pressed[pygame.K_s]: #down acceleration
                player1_Yspeed += player_acceleration
                if player1_Yspeed < 0:
                    player1_Yspeed += player_acceleration
            if keys_pressed[pygame.K_LSHIFT]: #stop
                player1_Yspeed = 0
                player1_Xspeed = 0
            
            if keys_pressed[pygame.K_LEFT]: #left acceleration
                player2_Xspeed -= player_acceleration
                if player2_Xspeed > 0:
                    player2_Xspeed -= player_acceleration
            if keys_pressed[pygame.K_RIGHT]: #right acceleration
                player2_Xspeed += player_acceleration
                if player2_Xspeed < 0:
                    player2_Xspeed += player_acceleration
            if keys_pressed[pygame.K_UP]: #up acceleration
                player2_Yspeed -= player_acceleration
                if player2_Yspeed > 0:
                    player2_Yspeed -= player_acceleration
            if keys_pressed[pygame.K_DOWN]: #down acceleration
                player2_Yspeed += player_acceleration
                if player2_Yspeed < 0:
                    player2_Yspeed += player_acceleration
            if keys_pressed[pygame.K_RSHIFT]: #stop
                player2_Xspeed = 0
                player2_Yspeed = 0
        if True: #sp tickers
            if sp1_p1 <350:
                sp1_p1 += 1
                SP1_indicator(22,HEIGHT-252,True)
            else:
                SP1_indicator(22,HEIGHT-252,False)
            if sp1_p2 <350:
                sp1_p2 += 1
                SP1_indicator(1182,HEIGHT-252,True)
            else:
                SP1_indicator(1182,HEIGHT-252,False)
            if sp2_p1 <500:
                sp2_p1 += 1
                SP2_indicator(105,HEIGHT-252,True)
            else:
                SP2_indicator(105,HEIGHT-252,False)
            if sp2_p2 <500:
                sp2_p2 += 1
                SP2_indicator(1265,HEIGHT-252,True)
            else:
                SP2_indicator(1265,HEIGHT-252,False)
            if sp3_p1 <500:
                sp3_p1 += 1
            if sp3_p2 <500:
                sp3_p2 += 1
        for event in pygame.event.get(): #special attacks
            if event.type == pygame.QUIT:
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK and sp1_p1 == 350: #sp1 p1
                    player1.x + player1.width/4 , player1.y + player1.width / 4
                    SP_P1_active = 0
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),0,4,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),3,3,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),4,0,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),3,-2.838,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),0,-4,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),-2.838,3,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),-4,0,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    bullets1.append([(pygame.Rect(0,0, 10, 10)),-2.828,-2.828,player1.x + player1.width/4 , player1.y + player1.width / 4])
                    sp1_p1 = 0
                if event.key == pygame.K_TAB and sp2_p1 == 500: #sp2 p1
                    SP_P1_active = -45
                    sp2_p1_active = 35
                    sp2_p1 = 0
                if event.key == pygame.K_BACKQUOTE: #sp3 p1
                    SP_P1_active = 0
                if event.key == pygame.K_COMMA and sp1_p2 == 350: #sp1 p2
                    SP_P2_active = 0
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),0,4,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),3,3,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),4,0,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),3,-2.838,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),0,-4,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),-2.838,3,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),-4,0,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    bullets2.append([(pygame.Rect(0,0, 10, 10)),-2.828,-2.828,player2.x + player2.width/4 , player2.y + player2.width / 4])
                    sp1_p2 = 0
                if event.key == pygame.K_k and sp2_p2 == 500: #sp2 p2
                    SP_P2_active = -45
                    sp2_p2_active = 35
                    sp2_p2 = 0
                if event.key == pygame.K_i: #sp3 p3   
                    SP_P2_active = 0
                if event.key == pygame.K_SPACE: #pause
                    WAIT = True
        if WAIT:
            pause_img()
        pygame.display.update()
        clock.tick(60)                    
        while WAIT: #pause
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.time.delay(60)
                        WAIT = False
if __name__== "__main__":
    main()
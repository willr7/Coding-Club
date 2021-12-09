import pygame
import random
pygame.font.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)

ORANGE_CREWMATE_IMG = pygame.image.load('orange crewmate.png')
RED_CREWMATE_IMG = pygame.image.load('red crewmate.png')

ORANGE_CREWMATE = pygame.transform.scale(ORANGE_CREWMATE_IMG, (40, 40))
ORANGE_CREWMATE = pygame.transform.flip(ORANGE_CREWMATE, True, False)
RED_CREWMATE = pygame.transform.scale(RED_CREWMATE_IMG, (40, 40))

ORANGE_IMPOSTOR_IMG = pygame.image.load('orange impostor.jpg')
RED_IMPOSTOR_IMG = pygame.image.load('red impostor.jpg')

ORANGE_IMPOSTOR = pygame.transform.scale(ORANGE_IMPOSTOR_IMG, (40, 40))
ORANGE_IMPOSTOR = pygame.transform.flip(ORANGE_IMPOSTOR, True, False)
RED_IMPOSTOR = pygame.transform.scale(RED_IMPOSTOR_IMG, (40, 40))

ORANGE_WIN_IMG = pygame.image.load('orange win.jpg')
RED_WIN_IMG = pygame.image.load('red win.jpg')

ORANGE_WIN = pygame.transform.scale(ORANGE_WIN_IMG, (WIDTH, HEIGHT))
RED_WIN = pygame.transform.scale(RED_WIN_IMG, (WIDTH, HEIGHT))

DEATH_SOUND = pygame.mixer.Sound('amogus death sound.mp3')
IMPOSTOR_SOUND = pygame.mixer.Sound('impostor sound.mp3')

def draw_health(health1, health2):
    draw_health1 = HEALTH_FONT.render("P1 HP: {}".format(health1), 1, (0, 0, 0))
    WIN.blit(draw_health1, (10, 10))
    
    draw_health2 = HEALTH_FONT.render("P2 HP: {}".format(health2), 1, (0, 0, 0))
    WIN.blit(draw_health2, (WIDTH - draw_health2.get_width() - 10, 10))

def main():
    pygame.mixer.music.load('among us background music.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    bullet_vel = 5
    run = True
    ticker = 0
    
    player1 = pygame.Rect(WIDTH // 4, HEIGHT // 2, 40, 40)
    player2 = pygame.Rect(WIDTH // 4 * 3, HEIGHT // 2, 40, 40)
    
    POWERUP_Homing = pygame.Rect(-100, -100, 20, 20)
    p1_homing = False
    p2_homing = False
    
    bullets_p1 = []
    bullets_p2 = []
    
    p1_health = 3
    p2_health = 3
    while run:
        WIN.fill((255, 255, 255))
        clock.tick(60)
        ticker += 1
        
        if not p1_homing:
            WIN.blit(RED_CREWMATE, (player1.x, player1.y))
        else:
            WIN.blit(RED_IMPOSTOR, (player1.x, player1.y))
        if not p2_homing:
            WIN.blit(ORANGE_CREWMATE, (player2.x, player2.y))
        else:
            WIN.blit(ORANGE_IMPOSTOR, (player2.x, player2.y))
        pygame.draw.rect(WIN, (122, 122, 0), POWERUP_Homing)
                
        draw_health(p1_health, p2_health)
        
        if ticker % 300 == 0 and POWERUP_Homing.y == -100:
            POWERUP_Homing.x = random.randrange(0, WIDTH - 20)
            POWERUP_Homing.y = random.randrange(0, HEIGHT - 20)
        
        for bullet in bullets_p1:
            if not p1_homing:
                bullet.x += bullet_vel
            else:
                if bullet.x < player2.x - 9:
                    bullet.x += bullet_vel // 2
                elif bullet.x > player2.x + 9:
                    bullet.x -= bullet_vel // 2
                if bullet.y < player2.y - 9:
                    bullet.y += bullet_vel // 2
                elif bullet.y > player2.y + 9:
                    bullet.y -= bullet_vel // 2
            pygame.draw.rect(WIN, (0, 0, 0), bullet)
            if bullet.colliderect(player2):
                bullets_p1.remove(bullet)
                p2_health -= 1
            if bullet.x > WIDTH or bullet.x < -10 or bullet.y > HEIGHT or bullet.y < -10:
                bullets_p1.remove(bullet)
                
        for bullet in bullets_p2:
            if not p2_homing:
                bullet.x -= bullet_vel
            else:
                if bullet.x < player1.x - 9:
                    bullet.x += bullet_vel // 2
                elif bullet.x > player1.x + 9:
                    bullet.x -= bullet_vel // 2
                if bullet.y < player1.y - 9:
                    bullet.y += bullet_vel // 2
                elif bullet.y > player1.y + 9:
                    bullet.y -= bullet_vel // 2
            pygame.draw.rect(WIN, (0, 0, 0), bullet)
            if bullet.colliderect(player1):
                bullets_p2.remove(bullet)
                p1_health -= 1
            if bullet.x > WIDTH or bullet.x < -10 or bullet.y > HEIGHT or bullet.y < -10:
                bullets_p2.remove(bullet)
                
        pygame.display.update()
        
        if p1_health <= 0:
            WIN.blit(ORANGE_WIN, (0, 0))
            pygame.display.update()
            pygame.mixer.Sound.play(DEATH_SOUND)
            pygame.mixer.music.stop()
            pygame.time.delay(1000)
            main()
        if p2_health <= 0:
            WIN.blit(RED_WIN, (0, 0))
            pygame.display.update()
            pygame.mixer.Sound.play(DEATH_SOUND)
            pygame.mixer.music.stop()
            pygame.time.delay(1000)
            main()
        
        if player1.colliderect(POWERUP_Homing):
            pygame.mixer.Sound.play(IMPOSTOR_SOUND)
            pygame.mixer.music.stop()
            p1_homing = True
            POWERUP_Homing.y = -100
            ticker = 1
        elif player2.colliderect(POWERUP_Homing):
            pygame.mixer.Sound.play(IMPOSTOR_SOUND)
            pygame.mixer.music.stop()
            p2_homing = True
            POWERUP_Homing.y = -100
            ticker = 1
        
        if ticker % 300 == 0 and (p1_homing or p2_homing):
            p1_homing = False
            p2_homing = False
        
        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    bullets_p1.append(pygame.Rect(player1.x + player1.width, player1.y + player1.width / 4, 10, 10))
                if event.key == pygame.K_RCTRL:
                    bullets_p2.append(pygame.Rect(player2.x, player2.y + player2.width / 4, 10, 10))
            
        if keys_pressed[pygame.K_a] and player1.x > 0: # LEFT
            player1.x -= 3
        if keys_pressed[pygame.K_d] and player1.x + player1.width < WIDTH: # RIGHT
            player1.x += 3
        if keys_pressed[pygame.K_w] and player1.y > 0: # UP
            player1.y -= 3
        if keys_pressed[pygame.K_s] and player1.y + player1.height < HEIGHT: # DOWN
            player1.y += 3
            
        if keys_pressed[pygame.K_LEFT] and player2.x > 0: # LEFT
            player2.x -= 3
        if keys_pressed[pygame.K_RIGHT] and player2.x + player2.width < WIDTH: # RIGHT
            player2.x += 3
        if keys_pressed[pygame.K_UP] and player2.y > 0: # UP
            player2.y -= 3
        if keys_pressed[pygame.K_DOWN] and player2.y + player2.height < HEIGHT: # DOWN
            player2.y += 3
        

        
if __name__ == "__main__":
    main()
import pygame
import random
pygame.font.init()
pygame.mixer.init()

WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sussy Baka Game")
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)

ORANGE_CREWMATE_IMG = pygame.image.load('orange crewmate.png')
RED_CREWMATE_IMG = pygame.image.load('red crewmate.png')

ORANGE_CREWMATE = pygame.transform.scale(ORANGE_CREWMATE_IMG, (40, 40))
RED_CREWMATE = pygame.transform.scale(RED_CREWMATE_IMG, (40, 40))

ORANGE_IMPOSTOR_IMG = pygame.image.load('orange impostor.jpg')
RED_IMPOSTOR_IMG = pygame.image.load('red impostor.jpg')

ORANGE_IMPOSTOR = pygame.transform.scale(ORANGE_IMPOSTOR_IMG, (40, 40))
RED_IMPOSTOR = pygame.transform.scale(RED_IMPOSTOR_IMG, (40, 40))

ORANGE_WIN_IMG = pygame.image.load('orange win.jpg')
RED_WIN_IMG = pygame.image.load('red win.jpg')

ORANGE_WIN = pygame.transform.scale(ORANGE_WIN_IMG, (WIDTH, HEIGHT))
RED_WIN = pygame.transform.scale(RED_WIN_IMG, (WIDTH, HEIGHT))

DEATH_SOUND = pygame.mixer.Sound('amogus death sound.mp3')
IMPOSTOR_SOUND = pygame.mixer.Sound('impostor sound.mp3')

# creates a class for the bullets so that every bullet can have different attributes
class Bullet:
    # the init function is used to initialize the bullet object
    # the parameters are passed in when the bullet is made. All of these variables are attributes of the bullet
    def __init__(self, direction, x, y, vel, homing):
        # the direction is a string that stores the direction that the player was facing when the bullet was shot
        self.direction = direction
        
        # the x and y position of the bullet
        self.x = x
        self.y = y
        
        # the velocity of the bullet
        self.vel = vel
        
        # a boolean that determines whether or not the bullet is homing
        self.homing = homing
        
        # a rect that stores the position of the bullet
        self.rect = pygame.Rect(x, y, 10, 10)
    
    # a function that updates the position of the bullet. the target variable is used if homing is true. it is the rect of the other player
    def update_pos(self, target):
        # if the bullet is not homing, it will move in the direction that the player was facing when the player shot the bullet
        if not self.homing:
            if self.direction == 'up':
                self.y -= self.vel
            elif self.direction == 'up right':
                self.x += self.vel
                self.y -= self.vel
            elif self.direction == 'up left':
                self.x -= self.vel
                self.y -= self.vel
            elif self.direction == 'down':
                self.y += self.vel
            elif self.direction == 'down right':
                self.x += self.vel
                self.y += self.vel
            elif self.direction == 'down left':
                self.x -= self.vel
                self.y += self.vel
            elif self.direction == 'right':
                self.x += self.vel
            else:
                self.x -= self.vel
        else:
            # otherwise the bullet will go towards the other player
            if self.rect.x < target.x - 9:
                self.x += self.vel // 2
            elif self.rect.x > target.x + 9:
                self.x -= self.vel // 2
            if self.rect.y < target.y - 9:
                self.y += self.vel // 2
            elif self.rect.y > target.y + 9:
                self.y -= self.vel // 2
        
        # updates the x and y attributes of the bullet
        self.rect.x = self.x
        self.rect.y = self.y
        
        # draws the bullet to the screen
        pygame.draw.rect(WIN, (0, 0, 0), self.rect)
        
def draw_health(health1, health2):
    draw_health1 = HEALTH_FONT.render("P1 HP: {}".format(health1), 1, (0, 0, 0))
    WIN.blit(draw_health1, (10, 10))
    
    draw_health2 = HEALTH_FONT.render("P2 HP: {}".format(health2), 1, (0, 0, 0))
    WIN.blit(draw_health2, (WIDTH - draw_health2.get_width() - 10, 10))

# function for drawing the player based off of the direction that the player is facing
def draw_player(img, direction, player):
    # rotates/flips the image 
    if direction == 'left':
        img = pygame.transform.flip(img, True, False)
    elif direction == 'up':
        img = pygame.transform.rotate(img, 90)
    elif direction == 'down':
        img = pygame.transform.rotate(img, 270)
    elif direction == 'up right':
        img = pygame.transform.rotate(img, 45)
    elif direction == 'up left':
        img = pygame.transform.flip(img, True, False)
        img = pygame.transform.rotate(img, 315)
    elif direction == 'down right':
        img = pygame.transform.rotate(img, 315)
    elif direction == 'down left':
        img = pygame.transform.flip(img, True, False)
        img = pygame.transform.rotate(img, 45)
    
    WIN.blit(img, (player.x, player.y))
        

def main():
    pygame.mixer.music.load('among us background music.mp3')
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    bullet_vel = 5
    run = True
    ticker = 0
    
    player1 = pygame.Rect(WIDTH // 4, HEIGHT // 2, 40, 40)
    player2 = pygame.Rect(WIDTH // 4 * 3, HEIGHT // 2, 40, 40)
    
    p1_direction = 'right'
    p2_direction = 'left'
    
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
            draw_player(RED_CREWMATE, p1_direction, player1)
            for bullet in bullets_p1:
                bullet.homing = False
        else:
            draw_player(RED_IMPOSTOR, p1_direction, player1)
        if not p2_homing:
            draw_player(ORANGE_CREWMATE, p2_direction, player2)
            for bullet in bullets_p2:
                bullet.homing = False
        else:
            draw_player(ORANGE_IMPOSTOR, p2_direction, player2)
        pygame.draw.rect(WIN, (122, 122, 0), POWERUP_Homing)
                
        draw_health(p1_health, p2_health)
        
        if ticker % 180 == 0 and POWERUP_Homing.y == -100 and not (p1_homing or p2_homing):
            POWERUP_Homing.x = random.randrange(0, WIDTH - 20)
            POWERUP_Homing.y = random.randrange(0, HEIGHT - 20)
        
        for bullet in bullets_p1:
            bullet.update_pos(player2)
            if bullet.rect.colliderect(player2):
                bullets_p1.remove(bullet)
                p2_health -= 1
            if bullet.rect.x > WIDTH or bullet.rect.x < -10 or bullet.rect.y > HEIGHT or bullet.rect.y < -10:
                bullets_p1.remove(bullet)
                
        for bullet in bullets_p2:
            bullet.update_pos(player1)
            if bullet.rect.colliderect(player1):
                bullets_p2.remove(bullet)
                p1_health -= 1
            if bullet.rect.x > WIDTH or bullet.rect.x < -10 or bullet.rect.y > HEIGHT or bullet.rect.y < -10:
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
            ticker = 1
        
        keys_pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    bullets_p1.append(Bullet(p1_direction, player1.x + player1.width // 2, player1.y + player1.height // 2, bullet_vel, p1_homing))
                if event.key == pygame.K_RCTRL:
                    bullets_p2.append(Bullet(p2_direction, player2.x + player2.width // 2, player2.y + player2.width // 2, bullet_vel, p2_homing))
            
        if keys_pressed[pygame.K_a] and player1.x > 0: # LEFT
            player1.x -= 3
            p1_direction = 'left'
        if keys_pressed[pygame.K_d] and player1.x + player1.width < WIDTH: # RIGHT
            player1.x += 3
            p1_direction = 'right'
        if keys_pressed[pygame.K_w] and player1.y > 0: # UP
            player1.y -= 3
            p1_direction = 'up'
            if keys_pressed[pygame.K_a]:
                p1_direction = 'up left'
            if keys_pressed[pygame.K_d]:
                p1_direction = 'up right'
        if keys_pressed[pygame.K_s] and player1.y + player1.height < HEIGHT: # DOWN
            player1.y += 3
            p1_direction = 'down'
            if keys_pressed[pygame.K_a]:
                p1_direction = 'down left'
            if keys_pressed[pygame.K_d]:
                p1_direction = 'down right'
            
        if keys_pressed[pygame.K_LEFT] and player2.x > 0: # LEFT
            player2.x -= 3
            p2_direction = 'left'
        if keys_pressed[pygame.K_RIGHT] and player2.x + player2.width < WIDTH: # RIGHT
            player2.x += 3
            p2_direction = 'right'
        if keys_pressed[pygame.K_UP] and player2.y > 0: # UP
            player2.y -= 3
            p2_direction = 'up'
            if keys_pressed[pygame.K_LEFT]:
                p2_direction = 'up left'
            if keys_pressed[pygame.K_RIGHT]:
                p2_direction = 'up right'
        if keys_pressed[pygame.K_DOWN] and player2.y + player2.height < HEIGHT: # DOWN
            player2.y += 3
            p2_direction = 'down'
            if keys_pressed[pygame.K_LEFT]:
                p2_direction = 'down left'
            if keys_pressed[pygame.K_RIGHT]:
                p2_direction = 'down right'
        

        
if __name__ == "__main__":
    main()
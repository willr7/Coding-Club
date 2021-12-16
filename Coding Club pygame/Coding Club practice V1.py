import pygame
import random
pygame.font.init()
pygame.mixer.init()

# Sets the width and height of the screen
WIDTH = 800
HEIGHT = 600

# Creates the window based off of the width and height variables. Don't forget the double parentheses
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Creates the font used to draw the health text
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)

# Start of creating the image variables
# image.load loads in the images from files in the folder. make sure the image files are in the same folder as the .py file
ORANGE_CREWMATE_IMG = pygame.image.load('orange crewmate.png')
RED_CREWMATE_IMG = pygame.image.load('red crewmate.png')

# transform and scale the images
# scale changes the width and height of the image. In this case every image is set to 40 by 40 pixels
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
# end of creating images

# load in the sounds for the death and the impostor
DEATH_SOUND = pygame.mixer.Sound('amogus death sound.mp3')
IMPOSTOR_SOUND = pygame.mixer.Sound('impostor sound.mp3')

# function for drawing the health of the players
# health1 is the integer that stores player 1's health, and health2 is for player 2
def draw_health(health1, health2):
    # draw_health1 renders the health font with the text for player 1's health
    # the first variable that is passed in to the render function is for the text, the second is for antialiasing (just put 1), the third variable is for the color of the text
    draw_health1 = HEALTH_FONT.render("P1 HP: {}".format(health1), 1, (0, 0, 0))
    # draws the text to the screen at the x and y
    WIN.blit(draw_health1, (10, 10))
    
    draw_health2 = HEALTH_FONT.render("P2 HP: {}".format(health2), 1, (0, 0, 0))
    WIN.blit(draw_health2, (WIDTH - draw_health2.get_width() - 10, 10))

# the main function for the program
def main():
    # loads the background music file
    pygame.mixer.music.load('among us background music.mp3')
    # plays the music, the -1 tells the program to replay the song forever
    pygame.mixer.music.play(-1)
    # creates the clock variable so that we can set the frame rate
    clock = pygame.time.Clock()
    
    bullet_vel = 5
    run = True
    
    # variable used to count frames
    # used to set the respawn rate of the powerup, and to set how long the powerup lasts
    ticker = 0
    
    # these variables are used to store the position of player one and player two
    player1 = pygame.Rect(WIDTH // 4, HEIGHT // 2, 40, 40)
    player2 = pygame.Rect(WIDTH // 4 * 3, HEIGHT // 2, 40, 40)
    
    # stores the rect for the powerup variable
    POWERUP_Homing = pygame.Rect(-100, -100, 20, 20)
    
    p1_homing = False
    p2_homing = False
    
    # lists to store the bullets
    bullets_p1 = []
    bullets_p2 = []
    
    p1_health = 3
    p2_health = 3
    
    # game loop
    while run:
        # sets the background as white
        WIN.fill((255, 255, 255))
        
        # sets the frame rate
        clock.tick(60)
        
        # counts the frames
        ticker += 1
        
        # draws the players to the screen
        # if the player has homing, the impostor sprite is used instead
        if not p1_homing:
            WIN.blit(RED_CREWMATE, (player1.x, player1.y))
        else:
            WIN.blit(RED_IMPOSTOR, (player1.x, player1.y))
        if not p2_homing:
            WIN.blit(ORANGE_CREWMATE, (player2.x, player2.y))
        else:
            WIN.blit(ORANGE_IMPOSTOR, (player2.x, player2.y))
        # draws the powerup to the screen. If the x and y coordinates are offscreen then you can't get to the powerup.
        pygame.draw.rect(WIN, (122, 122, 0), POWERUP_Homing)
                
        # draws the health text to the screen
        draw_health(p1_health, p2_health)
        
        # Every 300 frames, if the powerup is off screen, then the powerup is moved on screen
        if ticker % 300 == 0 and POWERUP_Homing.y == -100:
            POWERUP_Homing.x = random.randrange(0, WIDTH - 20)
            POWERUP_Homing.y = random.randrange(0, HEIGHT - 20)
        
        # moves the bullets
        for bullet in bullets_p1:
            # if the player does not have homing, the bullets just move to the right
            if not p1_homing:
                bullet.x += bullet_vel
            else:
                # if the player does have homing, then the bullet moves towards the other player
                if bullet.x < player2.x - 9:
                    bullet.x += bullet_vel // 2
                elif bullet.x > player2.x + 9:
                    bullet.x -= bullet_vel // 2
                if bullet.y < player2.y - 9:
                    bullet.y += bullet_vel // 2
                elif bullet.y > player2.y + 9:
                    bullet.y -= bullet_vel // 2
            # draws the bullets to the screen
            pygame.draw.rect(WIN, (0, 0, 0), bullet)
            # if the bullets collide with the player, it removes the bullet from the list and takes away one hp from player 2
            if bullet.colliderect(player2):
                bullets_p1.remove(bullet)
                p2_health -= 1
            # if the bullet goes off screen, it will be removed from the list
            if bullet.x > WIDTH or bullet.x < -10 or bullet.y > HEIGHT or bullet.y < -10:
                bullets_p1.remove(bullet)
        
        # does the same thing for bullets_p1 but the opposite
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
                
        # updates the display
        pygame.display.update()
        
        # if the player's health goes to 0, the end screen will be displayed, the death sound will be played, and the game will restart
        if p1_health <= 0:
            # changes the background to the orange win image
            WIN.blit(ORANGE_WIN, (0, 0))
            # updates the screen
            pygame.display.update()
            # plays the death sound
            pygame.mixer.Sound.play(DEATH_SOUND)
            pygame.mixer.music.stop()
            # sets a 1 second delay
            pygame.time.delay(1000)
            # calls the main function which restarts the game
            main()
        if p2_health <= 0:
            WIN.blit(RED_WIN, (0, 0))
            pygame.display.update()
            pygame.mixer.Sound.play(DEATH_SOUND)
            pygame.mixer.music.stop()
            pygame.time.delay(1000)
            main()
        
        # if the player collides with the powerup
        if player1.colliderect(POWERUP_Homing):
            # it plays the impostor sound
            pygame.mixer.Sound.play(IMPOSTOR_SOUND)
            pygame.mixer.music.stop()
            # sets p1_homing to True
            p1_homing = True
            # moves the rect off screen
            POWERUP_Homing.y = -100
            # resets the ticker to 1
            ticker = 1
        elif player2.colliderect(POWERUP_Homing):
            pygame.mixer.Sound.play(IMPOSTOR_SOUND)
            pygame.mixer.music.stop()
            p2_homing = True
            POWERUP_Homing.y = -100
            ticker = 1
        
        # if 300 frames have passed and either player one or player two have homing, it sets the homing to false
        if ticker % 300 == 0 and (p1_homing or p2_homing):
            p1_homing = False
            p2_homing = False
        
        # stores all of the keys that are pressed in the frame
        keys_pressed = pygame.key.get_pressed()
        
        # goes through all of the events in the pygame queue
        for event in pygame.event.get():
            # if the user closes the window, the program ends
            if event.type == pygame.QUIT:
                pygame.quit()
            
            # checks if the event is a key being pressed
            if event.type == pygame.KEYDOWN:
                # if the event key is left shift, it adds a bullet to the bullet list
                if event.key == pygame.K_LSHIFT:
                    # the bullet starts right in front of the player, and it is 10 by 10 pixels
                    bullets_p1.append(pygame.Rect(player1.x + player1.width, player1.y + player1.width / 4, 10, 10))
                if event.key == pygame.K_RCTRL:
                    bullets_p2.append(pygame.Rect(player2.x, player2.y + player2.width / 4, 10, 10))
                    
        # if the user presses w a s or d, then it moves player 1
        if keys_pressed[pygame.K_a] and player1.x > 0: # LEFT
            player1.x -= 3
        if keys_pressed[pygame.K_d] and player1.x + player1.width < WIDTH: # RIGHT
            player1.x += 3
        if keys_pressed[pygame.K_w] and player1.y > 0: # UP
            player1.y -= 3
        if keys_pressed[pygame.K_s] and player1.y + player1.height < HEIGHT: # DOWN
            player1.y += 3
        
        # if the user presses left right up or down, then it moves player 2
        if keys_pressed[pygame.K_LEFT] and player2.x > 0: # LEFT
            player2.x -= 3
        if keys_pressed[pygame.K_RIGHT] and player2.x + player2.width < WIDTH: # RIGHT
            player2.x += 3
        if keys_pressed[pygame.K_UP] and player2.y > 0: # UP
            player2.y -= 3
        if keys_pressed[pygame.K_DOWN] and player2.y + player2.height < HEIGHT: # DOWN
            player2.y += 3
        

# if the file is being ran locally without being imported, it will start the game
if __name__ == "__main__":
    main()

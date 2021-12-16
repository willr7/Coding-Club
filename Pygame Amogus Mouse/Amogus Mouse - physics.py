import pygame
import random
import math
import PyParticles
pygame.init()

WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

SCORE_FONT = pygame.font.SysFont('comicsans', 20)

class Obstacle:
    def __init__(self, vel, direction, size):
        self.size = size
        
        self.vel = vel
        
        if direction == 'up':
            x = random.randrange(0, WIDTH - self.size)
            y = HEIGHT - self.size
            self.angle = random.randrange(421, 521) / 100
        elif direction == 'down':
            x = random.randrange(0, WIDTH - self.size)
            y = 0
            self.angle = random.randrange(107, 207) / 100
        elif direction == 'left':
            x = WIDTH - self.size
            y = random.randrange(0, WIDTH - self.size)
            self.angle = random.randrange(264, 364) / 100
        elif direction == 'right':
            x = 0
            y = random.randrange(0, WIDTH - self.size)
            self.angle = random.randrange(-50, 50) / 100
        
        self.x = x
        self.y = y
        
        self.particle = PyParticles.Particle((self.x, self.y), self.size / 2)
        self.particle.speed = vel
        self.particle.angle = self.angle
        
        self.x_vel = math.cos(self.angle) * self.particle.speed
        self.y_vel = math.sin(self.angle) * self.particle.speed
        
        self.rect = pygame.Rect(x, y, self.size, self.size)
    
    def update_pos(self):
        self.vel = self.particle.speed
        self.angle = self.particle.angle
        
        self.particle.move()
        
        self.x = self.particle.x
        self.y = self.particle.y
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.particle.x = self.x
        self.particle.y = self.y

        pygame.draw.rect(WIN, (0, 0, 0), self.rect)

def draw_score(score):
    score_text = SCORE_FONT.render("Score: {}".format(score), 1, (0, 0, 0))
    WIN.blit(score_text, (10, 10))
        
def main():
    obstacles = []
    directions = ['up', 'down', 'left', 'right']
    score = 0
    
    ADD_OBSTACLE = pygame.USEREVENT + 0
    pygame.time.set_timer(ADD_OBSTACLE, 100)

    ADD_POINT = pygame.USEREVENT + 1
    pygame.time.set_timer(ADD_POINT, 1000)
    
    while True:
        WIN.fill((255, 255, 255))
        for i in obstacles:
            for j in obstacles[obstacles.index(i) + 1:]:
                PyParticles.collide(i.particle, j.particle)
            i.update_pos()
            if i.rect.x < 0 - i.size or i.rect.y < 0 - i.size:
                obstacles.remove(i)
            elif i.rect.x > WIDTH or i.rect.y > HEIGHT:
                obstacles.remove(i)
            if i.rect.collidepoint(pygame.mouse.get_pos()):
                pygame.time.delay(1000)
                main()


        clock.tick(60)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == ADD_OBSTACLE:
                obstacles.append(Obstacle(4, directions[random.randrange(4)], 30))
            if event.type == ADD_POINT and pygame.mouse.get_focused(): # amogus sussy baka impostor sus
                score += 1
        
        draw_score(score)
        pygame.display.update()
                
            
if __name__ == "__main__":
    main()
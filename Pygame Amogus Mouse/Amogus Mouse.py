import pygame
import random
import math
pygame.init()

WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

SCORE_FONT = pygame.font.SysFont('comicsans', 20)

class Obstacle:
    def __init__(self, vel, direction, size):
        self.vel = vel
        self.size = size
        
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
        
        self.x_vel = math.cos(self.angle) * vel
        self.y_vel = math.sin(self.angle) * vel
        
        self.rect = pygame.Rect(x, y, self.size, self.size)
    
    def update_pos(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
        self.rect.x = self.x
        self.rect.y = self.y

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
        for obstacle in obstacles:
            obstacle.update_pos()
            if obstacle.rect.x < 0 - obstacle.size or obstacle.rect.y < 0 - obstacle.size:
                obstacles.remove(obstacle)
            elif obstacle.rect.x > WIDTH or obstacle.rect.y > HEIGHT:
                obstacles.remove(obstacle)
            if obstacle.rect.collidepoint(pygame.mouse.get_pos()):
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
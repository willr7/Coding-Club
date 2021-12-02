import pygame

WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    clock = pygame.time.Clock()
    bullet_vel = 5
    run = True
    
    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 20, 20)
    
    bullets = []
    while run:
        WIN.fill((255, 255, 255))
        pygame.draw.rect(WIN, (0, 255, 0), player)
        for bullet in bullets:
            bullet.x += bullet_vel
            pygame.draw.rect(WIN, (0, 0, 0), bullet)
        pygame.display.update()
        clock.tick(60)
        
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.append(pygame.Rect(player.x + player.width, player.y + player.width / 4, 10, 10))
        
        if keys_pressed[pygame.K_a] and player.x > 0: # LEFT
            player.x -= 3
        if keys_pressed[pygame.K_d] and player.x + player.width < WIDTH: # RIGHT
            player.x += 3
        if keys_pressed[pygame.K_w] and player.y > 0: # UP
            player.y -= 3
        if keys_pressed[pygame.K_s] and player.y + player.height < HEIGHT: # DOWN
            player.y += 3
        
        
if __name__ == "__main__":
    main()
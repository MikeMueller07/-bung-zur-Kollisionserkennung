import os
import pygame
import random

class Settings:
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 400
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = 30
        self.original_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "basketball.jpg")).convert()
        self.original_image.set_colorkey("white")
        self.original_image = pygame.transform.scale(self.original_image, (self.size * 5, self.size * 5))
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (random.randint(0, Settings.WINDOW_WIDTH), random.randint(0, Settings.WINDOW_HEIGHT))

    def update_size(self, new_size):
        self.image = pygame.transform.scale(self.original_image, (new_size, new_size))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=50):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "knife.png")).convert_alpha()
        self.image.set_colorkey("white")
        self.image = pygame.transform.scale(self.image, (scale, scale))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.radius = scale // 2
        self.mask = pygame.mask.from_surface(self.image)

def check_collision(ball, obstacles_rect, obstacles_circle, obstacles_mask):
    if pygame.sprite.spritecollide(ball, obstacles_rect, False, pygame.sprite.collide_rect):
        return True
    if pygame.sprite.spritecollide(ball, obstacles_circle, False, pygame.sprite.collide_circle):
        return True
    if pygame.sprite.spritecollide(ball, obstacles_mask, False, pygame.sprite.collide_mask):
        return True
    return False

def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Basketball Game")
    clock = pygame.time.Clock()

    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "white.jpg")).convert()
    background_image = pygame.transform.scale(background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    ball = Ball()
    ball_size = ball.size

    obstacle_positions = [
        (50, 50),
        (500, 50),
        (50, 300),
        (500, 300),
        (250, 150),
        (350, 250)
    ]
    obstacles_rect = pygame.sprite.Group(Obstacle(*obstacle_positions[0]), Obstacle(*obstacle_positions[1]))
    obstacles_circle = pygame.sprite.Group(Obstacle(*obstacle_positions[2]), Obstacle(*obstacle_positions[3]))
    obstacles_mask = pygame.sprite.Group(Obstacle(*obstacle_positions[4]), Obstacle(*obstacle_positions[5]))

    running = True
    growth_rate = 0.2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ball_size += growth_rate
        ball.update_size(int(ball_size))

        if check_collision(ball, obstacles_rect, obstacles_circle, obstacles_mask):
            ball = Ball()
            ball_size = ball.size

        screen.blit(background_image, (0, 0))
        obstacles_rect.draw(screen)
        obstacles_circle.draw(screen)
        obstacles_mask.draw(screen)
        screen.blit(ball.image, ball.rect.topleft)

        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

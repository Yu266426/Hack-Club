import pygame

screen = pygame.display.set_mode((800, 800))
clock = pygame.Clock()

running = True
while running:
    clock.tick(60)
    pygame.display.set_caption(f"{round(clock.get_fps())}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill("dark green")

    pygame.display.flip()

import pygame

# PyGame setup
pygame.init()
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means user hit the X button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    # Vertical Lines
    for v in range(50, 451, 50):
        pygame.draw.line(screen, "black", (v, 50), (v, 450), width=2)
    

    # Horizontal Lines
    for h in range(50, 451, 50):
        pygame.draw.line(screen, "black", (50, h), (450, h), width=2)

    for row in range(8):
        for col in range(8):
            colour = "white" if ((row + col)%2==0) else "black"
            pygame.draw.rect(screen, colour, pygame.Rect(((51+50*col), (51+50*row)),(50, 50)))
    
    # flip() the display to show rendered work
    pygame.display.flip()

    clock.tick(60)  # Limits FPS to 60

pygame.quit()
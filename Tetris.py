import pygame

#Set up mot so thong so co ban
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
COLUMNS = SCREEN_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE

#Giao dien game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")


Run = True 
while Run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    screen.fill((128, 128, 128))
pygame.quit()
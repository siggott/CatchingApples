__author__ = 'JS'
import pygame


# Function: open_menu
# Opens the splash window for the game.
# Press right to play, left to exit.
# open_menu returns 1 to play and 0 to exit
def open_menu():
    # Menu window size
    menuWidth = 700
    menuHeight = 500
    menuSize = (menuWidth, menuHeight)
    pygame.display.set_mode((1,1),pygame.NOFRAME)

    exit_game = False

    pygame.display.set_caption("Apple catching")

    # Setup font
    WHITE = (255, 255, 255)
    ORANGE = (255,125,0)
    basicFont = pygame.font.SysFont('showcardgothic', 70)
    text = basicFont.render('Apple catching', True, ORANGE)
    text2 = basicFont.render('Apple catching', True, WHITE)

    background_sp = pygame.image.load('BG_tree.png').convert()  # recommened to add convert
    start_sp = pygame.image.load('start.png').convert_alpha()
    exit_sp = pygame.image.load('exit.png').convert_alpha()

    menuScreen = pygame.display.set_mode(menuSize)  # Open window
    menuScreen.fill(WHITE)  # the background
    menuScreen.blit(background_sp, [0, 0])
    menuScreen.blit(text2, (354 - text.get_width() // 2, 236 - text.get_height() // 2))
    menuScreen.blit(text, (360 - text.get_width() // 2, 240 - text.get_height() // 2))
    menuScreen.blit(start_sp, [510, 400])
    menuScreen.blit(exit_sp, [90, 400])

    pygame.display.update()

    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type is pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    exit_game = True
                if event.key == pygame.K_RIGHT:
                    return 1  # Start playing a game

    return 0  # Exit the game


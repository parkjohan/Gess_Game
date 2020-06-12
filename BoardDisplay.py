import pygame

pygame.init()

WIDTH = 950
HEIGHT = 950
MARGIN = 3
fps = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (252, 148, 2)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gess')
background_color = (0, 0, 0)
screen.fill(background_color)
clock = pygame.time.Clock()

game_board = []
for i in range(0, 20):
    game_board.append([])
    for j in range(0, 20):
        game_board[i].append(0)

done = False
while not done:
    screen.fill(BLACK)
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:      # Returns a tuple of mouse click position
            pos = pygame.mouse.get_pressed()
            col = pos[0] // 35
            row = pos[1] // 35
            print(row, col)

    # Draw game board
    for board_row in range(20):
        for board_column in range(20):
            color = WHITE
            if board_row == 0 or board_row == 19:
                game_board[board_row][board_column] = 1
            if board_column == 0 or board_column == 19:
                game_board[board_row][board_column] = 1
            if game_board[board_row][board_column] == 0:
                color = BEIGE
            pygame.draw.rect(screen,
                             color,
                             [45 * board_column + MARGIN + 23,         # Draws the columns
                              45 * board_row + MARGIN + 23,            # Draws the rows
                              40,
                              40])
    pygame.display.update()
pygame.quit()

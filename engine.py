import pygame, math, json, os

windowWidth = 500
windowHeight = 500
gridAmntView = 0
mouseDown = False
mouseX = 0
mouseY = 0
mouseXGrid = 0
mouseYGrid = 0
mutatedCells = []
window = pygame.display.set_mode((windowWidth, windowHeight))  # pygame.RESIZABLE
gridimg = pygame.image.load("grid.png").convert_alpha()
gridimg.set_alpha(100)

def drawgrid():
    global gridAmntView
    gridAmntView = 0
    gridimg1 = pygame.transform.scale(gridimg, (10, 10))
    for x in range(0, 500, 10):
        for y in range(0, 500, 10):
            gridAmntView += 1
            if x == mouseXGrid and y == mouseYGrid:
                gridimg1.set_alpha(255)
                window.blit(gridimg1, (x, y))
                gridimg1.set_alpha(100)
            else:
                window.blit(gridimg1, (x, y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseDown = False
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseXGrid = math.floor(mouseX/10)*10
    mouseYGrid = math.floor(mouseY/10)*10
    window.fill((255,255,255))
    drawgrid()
    pygame.display.set_caption(f'{gridAmntView} {mouseXGrid} {mouseYGrid}')
    pygame.display.update()
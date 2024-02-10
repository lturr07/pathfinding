import pygame, math, json, os

windowWidth = 500
windowHeight = 500
gridAmntView = 0
mouseX = 0
mouseY = 0
mouseXGrid = 0
mouseYGrid = 0
mouseType = -1
mouseDown = False
allCells = [[-1 for i in range(50)] for x in range(50)]  # 2d 50x50 array
window = pygame.display.set_mode((windowWidth, windowHeight))  # pygame.RESIZABLE
gridimg = pygame.image.load("grid.png")
gridimg = pygame.transform.scale(gridimg, (10, 10))
blockimg = pygame.image.load("block.png")
blockimg = pygame.transform.scale(blockimg, (10, 10))
startimg = pygame.image.load("start.png")
startimg = pygame.transform.scale(startimg, (10, 10))
endimg = pygame.image.load("end.png")
endimg = pygame.transform.scale(endimg, (10, 10))
todoimg = pygame.image.load("todo.png")
todoimg = pygame.transform.scale(todoimg, (10, 10))
doneimg = pygame.image.load("done.png")
doneimg = pygame.transform.scale(doneimg, (10, 10))

def drawgrid():
    global gridAmntView
    gridAmntView = 0
    for y, cells in enumerate(allCells):
        for x, cell in enumerate(cells):
            gridAmntView += 1
            if x == mouseXGrid and y == mouseYGrid:
                gridimg.set_alpha(100)
            else:
                gridimg.set_alpha(10)
            drawcell(x*10, y*10, cell)

def drawcell(x: int, y: int, cell: int):
    match cell:
        case -1:
            window.blit(gridimg, (x, y))
        case 0:
            window.blit(blockimg, (x, y))
        case 1:
            window.blit(startimg, (x, y))
        case 2:
            window.blit(endimg, (x, y))
        case 3:
            window.blit(todoimg, (x, y))
        case 4:
            window.blit(doneimg, (x, y))
        case _:
            window.blit(gridimg, (x, y))

while True:
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseXGrid = math.floor(mouseX/10)
    mouseYGrid = math.floor(mouseY/10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouseDown = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouseType = mouseType+1 if mouseType <= 3 else -1
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] and keys[pygame.K_c]:
                allCells = [[-1 for i in range(50)] for x in range(50)]
            if keys[pygame.K_LALT] and keys[pygame.K_c]:
                allCells = [[mouseType for i in range(50)] for x in range(50)]
            if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
                allCells  # save to json file ig... ＼（〇_ｏ）／
        
    if mouseDown:
        allCells[mouseYGrid][mouseXGrid] = mouseType
    window.fill((255,255,255))
    drawgrid()
    pygame.display.set_caption(f'{mouseType} x{mouseXGrid} y{mouseYGrid}')
    pygame.display.update()
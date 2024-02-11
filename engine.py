import pygame, math, json

windowWidth = 500
windowHeight = 600
gridAmntView = 0
mouseX = 0
mouseY = 0
mouseXGrid = 0
mouseYGrid = 0
mouseType = -1
mouseDown = False
allCells = [[[-1] for i in range(50)] for x in range(50)]  # 2d 50x50 array
startX, startY = (-1, -1)
endX, endY = (-1, -1)
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
pathimg = pygame.image.load("path.png")
pathimg = pygame.transform.scale(pathimg, (10, 10))
solveMode = False

# [type (3 to 5), cost, enddist, startdist, fromX, fromY]

def backtrack(x: int, y: int) -> None:
    if allCells[y][x][0] != 1:
        backtrack(allCells[y][x][4], allCells[y][x][5])
        allCells[y][x][0] = 5
    
def findNextTodo() -> tuple[int, int]:
    """returns (-1, -1) if not found"""
    lX = -1
    lY = -1
    lowest = -1
    lowest_heuristic = -1
    for y, cells in enumerate(allCells):
        for x, cell in enumerate(cells):
            if len(cell) > 1 and cell[0] == 3:
                if cell[1] < lowest or lowest == -1:
                    lowest = cell[1]
                    lowest_heuristic = cell[2]
                    lX, lY = x, y
                    # print(x, y, lowest, lowest_heuristic)
                elif cell[1] == lowest and cell[2] < lowest_heuristic:
                    lowest_heuristic = cell[2]
                    lX, lY = x, y
    # print(lowest, lowest_heuristic)
    return lX, lY

def createTodo(x: int, y: int) -> None:
    global solveMode, allCells
    a = [
        [1,0],
        [-1,0],
        [0,1],
        [0,-1]
        ]
    if not (x == startX and y == startY):
        allCells[y][x][0] = 4
    for b in a:
        _y, _x = b
        if y+_y < 0 or y+_y > 49 or x+_x < 0 or x+_x > 49:
            continue
        if allCells[y+_y][x+_x][0] == 2:
            solveMode = False
            backtrack(x, y)
            break
        if allCells[y+_y][x+_x][0] in [-1,3]:
            temp1 = round(math.sqrt((endX-(x+_x))**2+(endY-(y+_y))**2)*10)
            if not (x == startX and y == startY):
                temp2 = allCells[y][x][3] + 10
            else:
                temp2 = 10
            if (allCells[y+_y][x+_x][0] == 3 and temp1+temp2 < allCells[y+_y][x+_x][1]) or allCells[y+_y][x+_x][0] == -1:
                allCells[y+_y][x+_x] = [3, temp1+temp2, temp1, temp2, x, y]
            # print(allCells[y+_y][x+_x])

def findCellType(cellType: int) -> tuple[int, int]:
    """only finds first occurence and returns (-1, -1) if not found"""
    for y, cells in enumerate(allCells):
        for x, cell in enumerate(cells):
            if cell[0] == cellType:
                return x, y
    return -1, -1

def deleteCellType(cellType: int) -> None:
    global allCells
    allCells = list(map(lambda y: list(map(lambda x: [-1] if x[0] == cellType else x, y)) , allCells))

def drawpanel() -> None:
    drawcell(245,545,mouseType)

def drawgrid() -> None:
    global gridAmntView
    gridAmntView = 0
    for y, cells in enumerate(allCells):
        for x, cell in enumerate(cells):
            gridAmntView += 1
            if x == mouseXGrid and y == mouseYGrid:
                gridimg.set_alpha(100)
            else:
                gridimg.set_alpha(10)
            drawcell(x*10, y*10, cell[0])

def drawcell(x: int, y: int, cell: int) -> None:
    if x < 0 or y < 0:
        return  # if for example findCellType() returns -1, -1
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
        case 5:
            window.blit(pathimg, (x, y))
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
            mouseType = mouseType+1 if mouseType <= 1 else -1
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] and keys[pygame.K_c]:
                allCells = [[[-1] for i in range(50)] for x in range(50)]
                print("Cleared!")
            if keys[pygame.K_LALT] and keys[pygame.K_c]:
                deleteCellType(3)
                deleteCellType(4)
                deleteCellType(5)
                print("Cleared Solution!")
            if keys[pygame.K_LCTRL] and keys[pygame.K_s]:
                with open("save.json", "w") as a:
                    json.dump(allCells, a)
                print("Saved!")
            if keys[pygame.K_LCTRL] and keys[pygame.K_o]:
                with open("save.json", "r") as a:
                    allCells = json.load(a)
                # Clean save for dupe end or starts
                temp = findCellType(1)
                deleteCellType(1)
                if temp[0] != -1:
                    allCells[temp[1]][temp[0]][0] = 1
                temp = findCellType(2)
                deleteCellType(2)
                if temp[0] != -1:
                    allCells[temp[1]][temp[0]][0] = 2
                del temp
                print("Save Loaded!")
            if keys[pygame.K_LCTRL] and keys[pygame.K_BACKQUOTE]:
                startX, startY = findCellType(1)
                endX, endY = findCellType(2)
                if startX != -1 and endX != -1:
                    solveMode = False if solveMode else True
                    print("Solve Mode:",solveMode)
                else:
                    print("Both an end and start are needed")            
    if solveMode:
        solve = findNextTodo()
        # print(solve)
        if solve[0] == -1:
            createTodo(startX, startY)
        else:
            createTodo(solve[0], solve[1])
    if mouseDown and mouseYGrid <= 49 and mouseXGrid <= 49 and not solveMode:
        if mouseType > 0:
            deleteCellType(mouseType)
        allCells[mouseYGrid][mouseXGrid][0] = mouseType
    window.fill((255,255,255))
    drawgrid()
    drawpanel()
    pygame.display.set_caption(f'x{mouseXGrid} y{mouseYGrid} {allCells[mouseYGrid][mouseXGrid] if mouseYGrid <= 49 and mouseXGrid <= 49 else "select square"}')
    pygame.display.update()
import pygame,sys
def show_license():
    print("本程式依照 Creative Commons CC BY-NC-ND 4.0 授權")
    print("授權條款連結: https://creativecommons.org/licenses/by-nc-nd/4.0/")
    print("請遵守：必須署名、禁止商業用途、禁止修改")

TILE_SIZE = 40          #每個格子的大小（像素），越大越清楚
WALL_COLOR = (0, 0, 0)  #牆的顏色
PATH_COLOR = (255, 255, 255)  #路的顏色
END_COLOR = (180, 80, 80) #E的顏色
START_COLOR = (70, 130, 180) #S的顏色
ANS_COLOR = (51,255,153) #答案的顏色

MAZE_FILE = "maze.txt"  #迷宮檔案名稱


def load_origin_maze():  #讀取
    filename="maze.txt"
    maze=[[0]*17 for _ in range(17)]
    tmp=[]
    with open(filename, "r", encoding="utf-8") as f:
        for i,line in enumerate(f):
            tmp=line.split()
            for j in range(len(tmp)):
                try:
                    maze[i][j]=int(tmp[j])
                except:
                    maze[i][j]=tmp[j]
    return maze

def load_maze(filename):  #讀取
    filename="output.txt"
    maze=[[0]*17 for _ in range(17)]
    tmp=[]
    with open(filename, "r", encoding="utf-8") as f:
        for i,line in enumerate(f):
            tmp=line.split()
            for j in range(len(tmp)):
                try:
                    maze[i][j]=int(tmp[j])
                except:
                    maze[i][j]=tmp[j]
    return maze

def load_condition():
    with open("condition.txt", "r", encoding="utf-8") as f:
        line=f.readline()
        L=line.split(",")
        return int(L[0]),int(L[1])

def get_gradient_color(value, max_value):
    if max_value == 0:
        return START_COLOR  

    ratio = value / max_value  
    r = int(START_COLOR[0] + (END_COLOR[0] - START_COLOR[0]) * ratio)
    g = int(START_COLOR[1] + (END_COLOR[1] - START_COLOR[1]) * ratio)
    b = int(START_COLOR[2] + (END_COLOR[2] - START_COLOR[2]) * ratio)

    return (r, g, b)


def get_answer_path(maze):
    path = []
    start_y, start_x = 1, 0
    if maze[start_y][start_x] != 0:
        return path
    
    path.append((start_y, start_x))
    current_y, current_x = start_y, start_x
    
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    visited = {(start_y, start_x)}
    
    while True:
        found = False
        for dy, dx in directions:
            ny, nx = current_y + dy, current_x + dx
            if 0 <= ny < len(maze) and 0 <= nx < len(maze[0]):
                if maze[ny][nx] == 0 and (ny, nx) not in visited:
                    path.append((ny, nx))
                    visited.add((ny, nx))
                    current_y, current_x = ny, nx
                    found = True
                    break
        if not found:
            break 
    
    return path

def draw_maze(screen, maze,screen_height):  #畫出來
    a,b=load_condition()
    rows = len(maze)
    cols = len(maze[0])
    original=load_origin_maze()
   
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if original[y][x] == -1 :
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif y==1 and x==0:
                pygame.draw.rect(screen, START_COLOR, rect)
            elif maze[y][x] == "E":
                pygame.draw.rect(screen, END_COLOR, rect)
            elif maze[y][x] != -1:
                COLOR = get_gradient_color(maze[y][x], 60)
                pygame.draw.rect(screen, COLOR, rect)  
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)
            if maze[y][x] != -1:
                 font = pygame.font.SysFont("microsoftyahei", 20)
                 num = font.render(str(maze[y][x]), True, (0,0,0))    #鑲嵌數字
                 screen.blit(num, (x*TILE_SIZE+12, y*TILE_SIZE+7))
    font = pygame.font.SysFont("microsoftyahei", 20)
    text = font.render(f"探索步數：{b}", True, (200, 200, 200))
    screen.blit(text, (10, screen_height))
   
def draw_final_maze(screen, maze,screen_height,dt, path_index=0, path_timer=0):  #畫出結算
    a,b=load_condition()
    speed = 0.1                                  #跑馬燈速度
    people1=pygame.image.load("people1.png")
    people2=pygame.image.load("people2.png")
    global answer_path

    path_timer += dt
    answer_path = get_answer_path(maze)

    if path_timer >= speed:
        path_timer -= speed
        path_index += 1
        if path_index >= len(answer_path):
            path_index = len(answer_path)
    
    # 畫出跑馬燈
    for i in range(path_index + 1):
        if i < len(answer_path):
            y, x = answer_path[i]
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, ANS_COLOR, rect)
            if i==path_index :
                if i%2==0:
                    screen.blit(people1,(x * TILE_SIZE, y * TILE_SIZE))
                else:
                    screen.blit(people2,(x * TILE_SIZE, y * TILE_SIZE))
            if path_index == len(answer_path):
                if round(path_timer*5%2)==1:
                    y, x = answer_path[i]
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, ANS_COLOR, rect)
                else:
                    y, x = answer_path[i]
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, (255,255,255), rect)

    font = pygame.font.SysFont("microsoftyahei", 20)
    text = font.render(f"探索步數：{b}", True, (200, 200, 200))
    screen.blit(text, (10, screen_height))
    text = font.render(f"最短步數：{path_index-1}", True, (200, 200, 200))
    screen.blit(text, (10, screen_height+20))

    return path_index, path_timer

def main():
    maze=load_maze(MAZE_FILE)
    rows=len(maze)
    cols=len(maze[0])
    global answer_path, path_index, path_timer
    path_index = 0
    path_timer = 0
    answer_path = None
   
    screen_width=cols*TILE_SIZE
    screen_height=rows*TILE_SIZE
   
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height+50))
    pygame.display.set_caption("迷宮")
    clock = pygame.time.Clock()
   
    running = True
    while running:
        dt=clock.tick(5)/1000
        maze=load_maze(MAZE_FILE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
       
        screen.fill((30, 30, 30))  # 背景色
        a,b=load_condition()
        if b==131: 
            rows = len(maze)
            cols = len(maze[0])
            original=load_origin_maze()
            for y in range(rows):
                for x in range(cols):
                    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if original[y][x] == -1 : 
                        pygame.draw.rect(screen, WALL_COLOR, rect) 
                    else:
                        pygame.draw.rect(screen, PATH_COLOR, rect)  
            path_index, path_timer = draw_final_maze(screen, maze, screen_height, dt, path_index, path_timer) 
        else:
            draw_maze(screen, maze, screen_height)   
        font = pygame.font.SysFont("microsoftyahei", 40)
        text = font.render(f"BFS演算法", True, (200, 200, 200))
        screen.blit(text, (200, screen_height)) 
        pygame.display.flip()
   
    pygame.quit()
    sys.exit()
 
if __name__ == "__main__":
    show_license()
    main()

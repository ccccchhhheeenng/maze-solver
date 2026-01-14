import pygame,sys,time,threading,subprocess
lock=threading.Lock()
class Data:
    def __init__(self):
            self.bottom_txt_cond=0
            self.steps=0
            self.cond=0
            self.maze=[[0]*33 for _ in range(33)]
    def load_maze(self):  #讀取
        maze=self.maze
        bottom_txt_cond,steps,cond=self.load_condition()
        if cond==0:
            return bottom_txt_cond,steps,cond,maze
        filename="output.txt"
        tmp=[]
        try:
            with open(filename, "r", encoding="utf-8") as f:
                for i,line in enumerate(f):
                    tmp=line.split()
                    for j in range(len(tmp)):
                        try:
                            maze[i][j]=int(tmp[j])
                        except:
                            maze[i][j]=tmp[j]
        except:
            pass
        return bottom_txt_cond,steps,cond,maze
    def load_condition(self):
        try:
            with open("condition.txt", "r", encoding="utf-8") as f:
                line=f.readline()
                L=line.split(",")
                return int(L[0]),int(L[1]),int(L[2])
        except:
            print("condition load fail,data ignored")
            return 0,0,0
    def update_data(self):
        while True:
            bottom_txt_cond,steps,cond,maze=self.load_maze()
            if cond and cond!=3:
                with lock:
                    self.bottom_txt_cond=bottom_txt_cond
                    self.steps=steps
                    self.cond=cond
                    self.maze=maze
            else:
                if cond==3:continue
                print("data load failed, retrying...")
            time.sleep(0.1)
data=Data()


def show_license():
    print("")

TILE_SIZE = 20          #每個格子的大小（像素），越大越清楚
WALL_COLOR = (0, 0, 0)  #牆的顏色
PATH_COLOR = (255, 255, 255)  #路的顏色
END_COLOR = (180, 80, 80) #E的顏色
START_COLOR = (70, 130, 180) #S的顏色
ANS_COLOR = (51,255,153) #答案的顏色
button_bfs = pygame.Rect(50, 10, 180, 40)
button_flood = pygame.Rect(250, 10, 180, 40)
people1=pygame.image.load("people1.png")
people2=pygame.image.load("people2.png")

def draw_button(screen, rect, text):
    pygame.draw.rect(screen, (80,80,80), rect)
    pygame.draw.rect(screen, (200,200,200), rect, 3)
    font = pygame.font.SysFont("microsoftyahei", 24)
    txt = font.render(text, True, (255,255,255))
    screen.blit(txt, (rect.x + 10, rect.y + 8))

def run_bfs():
    subprocess.Popen(["bfs.exe"])   # 你的 BFS C 程式

def run_flood():
    subprocess.Popen(["floodfill.exe"]) # 你的 Flood Fill C 程式


def load_origin_maze():
    filename = "maze.txt"
    maze = [[0] * 33 for _ in range(33)]
    
    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            for j, ch in enumerate(line):
                if j >= 33:  # 防止超過
                    break
                maze[i][j] = int(ch)
    
    return maze
ORIGIN_MAZE = load_origin_maze()

def get_gradient_color(value, max_value):
    if max_value == 0:
        return START_COLOR  

    ratio = value / max_value  
    r = int(START_COLOR[0] + (END_COLOR[0] - START_COLOR[0]) * ratio)
    g = int(START_COLOR[1] + (END_COLOR[1] - START_COLOR[1]) * ratio)
    b = int(START_COLOR[2] + (END_COLOR[2] - START_COLOR[2]) * ratio)
    if r>=255 or g>=255 or b>255:
        r=END_COLOR[0]
        g=END_COLOR[1]
        b=END_COLOR[2]

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
    
def draw_maze(bottom_txt_cond,steps,screen, maze,screen_height):  #畫出來
    rows = len(maze)
    cols = len(maze[0])
    original=ORIGIN_MAZE
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if original[y][x] == 1 :
                pygame.draw.rect(screen, WALL_COLOR, rect)
            elif maze[y][x] == "S":
                pygame.draw.rect(screen, START_COLOR, rect)
            elif maze[y][x] == "E":
                pygame.draw.rect(screen, END_COLOR, rect)
            elif maze[y][x] != -1:
                COLOR = get_gradient_color(maze[y][x], 100)
                pygame.draw.rect(screen, COLOR, rect)  
            else:
                pygame.draw.rect(screen, PATH_COLOR, rect)
            if maze[y][x] != -1:
                 font = pygame.font.SysFont("microsoftyahei", 10)
                 num = font.render(str(maze[y][x]), True, (0,0,0))    #鑲嵌數字
                 screen.blit(num, (x*TILE_SIZE+8, y*TILE_SIZE+7))
    font = pygame.font.SysFont("microsoftyahei", 20)
    text = font.render(f"探索步數：{steps}", True, (200, 200, 200))
    screen.blit(text, (10, screen_height))
   
def draw_final_maze(steps,screen, maze,screen_height,dt, path_index=0, path_timer=0):  #畫出結算
    speed = 0.1      #跑馬燈速度
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
    text = font.render(f"探索步數：{steps}", True, (200, 200, 200))
    screen.blit(text, (10, screen_height))
    text = font.render(f"最短步數：{path_index-1}", True, (200, 200, 200))
    screen.blit(text, (10, screen_height+20))

    return path_index, path_timer

def main():
    with lock:
        bottom_txt_cond,steps,maze,bottom_txt_cond=data.bottom_txt_cond,data.steps,data.maze,data.bottom_txt_cond
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
        try:
            with lock:
                bottom_txt_cond = data.bottom_txt_cond
                steps = data.steps
                cond = data.cond
                maze = data.maze
        except:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: 
                mx, my = event.pos 
                if button_bfs.collidepoint(mx, my): run_bfs() 
                if button_flood.collidepoint(mx, my): run_flood()
        screen.fill((30, 30, 30))  # 背景色
        if cond==-1:
            draw_button(screen, button_bfs, "執行 BFS") 
            draw_button(screen, button_flood, "執行 Flood Fill")
            path_index = 0
            path_timer = 0
            answer_path = None
            font = pygame.font.SysFont("microsoftyahei", 60)
            text = font.render(f"等待中...", True, (200, 200, 200))
            screen.blit(text, (screen_width//2-100, screen_height//2-30))
        elif cond==2: 
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
            path_index, path_timer = draw_final_maze(steps,screen, maze, screen_height, dt, path_index, path_timer) 
        else:
            draw_maze(bottom_txt_cond,steps,screen, maze, screen_height)   
        bottom_text="目前演算法："
        if cond==-1:
            bottom_text+="等待C語言資料中..."
        elif bottom_txt_cond:
            bottom_text+="Flood Fill"
        else:
            bottom_text+="BFS"
        font = pygame.font.SysFont("microsoftyahei", 30)
        text = font.render(bottom_text, True, (200, 200, 200))
        screen.blit(text, (200, screen_height)) 
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    read_data=threading.Thread(target=data.update_data, daemon=True)
    read_data.start()
    show_license()
    main()


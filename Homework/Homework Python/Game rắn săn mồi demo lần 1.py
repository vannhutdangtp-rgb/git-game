import pygame, sys, random
from pygame.math import Vector2

# ================== HIGH SCORE (with names) ==================
def load_highscores():
    highscores = []
    try:
        with open("highscores.txt", "r", encoding="utf-8") as f:
            for line in f.readlines():
                parts = line.strip().split(",", 1)
                if len(parts) == 2:
                    name, score = parts[0], int(parts[1])
                    highscores.append((name, score))
        highscores.sort(key=lambda x: x[1], reverse=True)
        return highscores[:5]
    except:
        return []

def save_highscores(highscores):
    with open("highscores.txt", "w", encoding="utf-8") as f:
        for name, score in highscores[:5]:
            f.write(f"{name},{score}\n")

def add_highscore(name, score):
    highscores = load_highscores()
    highscores.append((name, score))
    highscores.sort(key=lambda x: x[1], reverse=True)
    save_highscores(highscores[:5])

def is_new_highscore(score):
    highscores = load_highscores()
    if len(highscores) < 5:
        return True
    return score > highscores[-1][1]

# ================== CLASS SNAKE ==================
class SNAKE:
    def __init__(self):
        snake_folder = [
            r"D:\Homework Python\img\snake1",
            r"D:\Homework Python\img\snake2",
            r"D:\Homework Python\img\snake3",
            r"D:\Homework Python\img\snake4",
            r"D:\Homework Python\img\snake5"
        ][selected_snake]

        self.body = [Vector2(7,5), Vector2(6,5), Vector2(5,5)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up    = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\rantren.png").convert_alpha(), (cell_size, cell_size))
        self.head_down  = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\randuoi.png").convert_alpha(), (cell_size, cell_size))
        self.head_right = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\ranphai.png").convert_alpha(), (cell_size, cell_size))
        self.head_left  = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\rantrai.png").convert_alpha(), (cell_size, cell_size))

        self.tail_up    = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\dtren.png").convert_alpha(), (cell_size, cell_size))
        self.tail_down  = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\dduoi.png").convert_alpha(), (cell_size, cell_size))
        self.tail_right = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\dphai.png").convert_alpha(), (cell_size, cell_size))
        self.tail_left  = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\dtrai.png").convert_alpha(), (cell_size, cell_size))

        self.body_vertical   = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\hcnngang.png").convert_alpha(), (cell_size, cell_size))
        self.body_horizontal = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\hcndung.png").convert_alpha(), (cell_size, cell_size))

        self.body_tr = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\quaytrai.png").convert_alpha(), (cell_size, cell_size))
        self.body_tl = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\quayphai.png").convert_alpha(), (cell_size, cell_size))
        self.body_br = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\quaytren.png").convert_alpha(), (cell_size, cell_size))
        self.body_bl = pygame.transform.scale(pygame.image.load(fr"{snake_folder}\quayxuong.png").convert_alpha(), (cell_size, cell_size))

        self.crunch_sound = pygame.mixer.Sound(r"D:\Homework Python\Sound\thoithoi2.mp3")

        self.head = self.head_right
        self.tail = self.tail_left

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect)
            else:
                screen.blit(self.body_vertical, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): 
            self.head = self.head_left
        elif head_relation == Vector2(-1,0): 
            self.head = self.head_right
        elif head_relation == Vector2(0,1): 
            self.head = self.head_up
        elif head_relation == Vector2(0,-1): 
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): 
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): 
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): 
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): 
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0]+self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

# ================== CLASS FRUIT ==================
class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

# ================== CLASS MAIN ==================
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0
        self.background = pygame.Surface((cell_number * cell_size, cell_number * cell_size))
        self.draw_background_pattern(selected_map)
        self.generate_obstacles(selected_map)

        # âm thanh khi đụng chướng ngại vật
        self.hit_sound = pygame.mixer.Sound(r"D:\Homework Python\Sound\va_cham.mp3")

    # ================== VẼ NỀN THEO MAP ==================
    def draw_background_pattern(self, map_index):
        color_sets = [
            [(167, 209, 61), (175, 215, 70)],   # Map 1
            [(93, 170, 232), (108, 190, 245)],  # Map 2
            [(232, 185, 93), (245, 200, 108)],  # Map 3
            [(200, 100, 150), (220, 130, 180)], # Map 4
            [(80, 80, 80), (120, 120, 120)],    # Map 5
        ]
        color1, color2 = color_sets[map_index % len(color_sets)]
        for row in range(cell_number):
            for col in range(cell_number):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.background, color1, rect)
                else:
                    pygame.draw.rect(self.background, color2, rect)

    # ================== SINH CHƯỚNG NGẠI VẬT ==================
    def generate_obstacles(self, map_index):
        self.obstacles = []

        if map_index == 0:  # hình vuông giữa
            for x in range(6, 14):
                self.obstacles.append(Vector2(x, 6))
                self.obstacles.append(Vector2(x, 13))
            for y in range(6, 14):
                self.obstacles.append(Vector2(6, y))
                self.obstacles.append(Vector2(13, y))

        elif map_index == 1:  # hai hàng ngang giữa
            for x in range(3, 17):
                self.obstacles.append(Vector2(x, 9))
                self.obstacles.append(Vector2(x, 10))

        elif map_index == 2:  # 4 cột dọc
            for y in range(4, 16):
                for x in [4, 8, 12, 16]:
                    self.obstacles.append(Vector2(x, y))

        elif map_index == 3:  # hình chữ X
            for i in range(cell_number):
                self.obstacles.append(Vector2(i, i))
                self.obstacles.append(Vector2(i, cell_number - i - 1))

        elif map_index == 4:  # vật cản ngẫu nhiên
            for _ in range(25):
                self.obstacles.append(Vector2(random.randint(0, cell_number - 1),
                                              random.randint(0, cell_number - 1)))

    # ================== CẬP NHẬT TRẠNG THÁI GAME ==================
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # ================== VẼ MỌI THỨ ==================
    def draw_elements(self):
        screen.blit(self.background, (0, 0))

        # vẽ obstacle
        obstacle_colors = [
            (100, 60, 60),   # map 1
            (60, 100, 160),  # map 2
            (160, 100, 50),  # map 3
            (180, 60, 100),  # map 4
            (120, 120, 120)  # map 5
        ]
        color = obstacle_colors[selected_map % len(obstacle_colors)]
        for obs in self.obstacles:
            rect = pygame.Rect(int(obs.x * cell_size), int(obs.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)

        self.fruit.draw_fruit()
        self.snake.draw_snake()

        score_text = game_font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    # ================== ĂN TRÁI CÂY ==================
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # tránh spawn trái cây trùng obstacle
            while True:
                self.fruit.randomize()
                if self.fruit.pos not in self.obstacles:
                    break
            self.snake.add_block()
            self.score += 1
            self.snake.play_crunch_sound()

    # ================== KIỂM TRA THUA GAME ==================
    def check_fail(self):
        head = self.snake.body[0]

        # ✅ Rắn xuyên tường
        if head.x >= cell_number:
            head.x = 0
        elif head.x < 0:
            head.x = cell_number - 1
        if head.y >= cell_number:
            head.y = 0
        elif head.y < 0:
            head.y = cell_number - 1

        # ❌ Đụng chướng ngại vật
        if head in self.obstacles:
            self.hit_sound.play()
            self.game_over()

        # ❌ Đụng thân
        for block in self.snake.body[1:]:
            if block == head:
                self.game_over()

    # ================== GAME OVER ==================
    def game_over(self):
        if is_new_highscore(self.score):
            name = input_name_screen(self.score)
            add_highscore(name, self.score)
        game_over_screen(self.score)


# ================== INPUT NAME SCREEN ==================
def input_name_screen(score):
    name = ""
    while True:
        screen.fill((0, 0, 0))
        prompt = game_font.render("🎉 NEW HIGHSCORE! 🎉", True, (255,255,0))
        name_text = game_font.render("Enter your name:", True, (255,255,255))
        input_box = game_font.render(name + "|", True, (0,255,0))
        score_text = game_font.render(f"Score: {score}", True, (200,200,200))
        screen.blit(prompt, (100, 100))
        screen.blit(score_text, (100, 160))
        screen.blit(name_text, (100, 220))
        screen.blit(input_box, (100, 280))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name.strip() if name.strip() else "Player"
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 15 and event.unicode.isprintable():
                    name += event.unicode

# ================== GAME OVER SCREEN ==================
def game_over_screen(score):
    highscores = load_highscores()
    while True:
        screen.fill((50,50,50))
        over_text = game_font.render(f"GAME OVER - Score: {score}", True, (255,0,0))
        screen.blit(over_text, (50,50))
        hs_text = game_font.render("TOP 5:", True, (255,255,0))
        screen.blit(hs_text, (50,120))
        for i, (name, s) in enumerate(highscores):
            line = game_font.render(f"{i+1}. {name} - {s}", True, (200,200,200))
            screen.blit(line, (50,160 + i*40))
        msg = game_font.render("Press SPACE to return to MENU, ESC to quit", True, (255,255,255))
        screen.blit(msg, (50, 400))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_screen()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

# ================== MENU SCREEN ==================
def menu_screen():
    global selected_snake, selected_map
    selected_snake = 0
    selected_map = 0

    pygame.display.set_caption("Snake Menu")
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    menu_font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 70)

    # --- Load ảnh preview cho snake ---
    snake_previews = []
    for i in range(1, 6):
        try:
            img = pygame.image.load(fr"D:\Homework Python\img\snake{i}\rantren.png").convert_alpha()
        except FileNotFoundError:
            img = pygame.Surface((80,80))
            img.fill((100+i*20,80,80))
        snake_previews.append(pygame.transform.scale(img, (80, 80)))

    # --- Preview cho map bằng màu bàn cờ ---
    color_sets = [
        [(167, 209, 61), (175, 215, 70)],
        [(93, 170, 232), (108, 190, 245)],
        [(232, 185, 93), (245, 200, 108)],
        [(200, 100, 150), (220, 130, 180)],
        [(80, 80, 80), (120, 120, 120)],
    ]
    map_previews = []
    for c1, c2 in color_sets:
        surf = pygame.Surface((150, 150))
        for r in range(5):
            for c in range(5):
                rect = pygame.Rect(c*30, r*30, 30, 30)
                pygame.draw.rect(surf, c1 if (r+c)%2==0 else c2, rect)
        map_previews.append(surf)

    while True:
        screen.fill((30, 30, 30))
        title = title_font.render("🐍 SNAKE GAME MENU 🐍", True, (255,255,0))
        screen.blit(title, (150, 50))

        # --- Snake ---
        snake_text = menu_font.render(f"Snake Type: {selected_snake + 1}", True, (200,200,200))
        screen.blit(snake_text, (100, 200))
        screen.blit(menu_font.render("<", True, (255,255,255)), (50, 200))
        screen.blit(menu_font.render(">", True, (255,255,255)), (400, 200))
        screen.blit(snake_previews[selected_snake], (500, 170))

        # --- Map ---
        map_text = menu_font.render(f"Map: {selected_map + 1}", True, (200,200,200))
        screen.blit(map_text, (100, 350))
        screen.blit(menu_font.render("<", True, (255,255,255)), (50, 350))
        screen.blit(menu_font.render(">", True, (255,255,255)), (250, 350))
        screen.blit(map_previews[selected_map], (500, 320))

        # --- Play/Quit ---
        play_text = menu_font.render("Press SPACE to PLAY", True, (0,255,0))
        quit_text = menu_font.render("Press ESC to QUIT", True, (255,0,0))
        screen.blit(play_text, (100, 500))
        screen.blit(quit_text, (100, 560))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_SPACE:
                    main()
                if event.key == pygame.K_a:
                    selected_snake = (selected_snake - 1) % 5
                if event.key == pygame.K_d:
                    selected_snake = (selected_snake + 1) % 5
                if event.key == pygame.K_w:
                    selected_map = (selected_map - 1) % 5
                if event.key == pygame.K_s:
                    selected_map = (selected_map + 1) % 5
        clock.tick(30)

# ================== MAIN LOOP ==================
def main():
    global cell_size, cell_number, screen, clock, apple, game_font
    cell_size = 40
    cell_number = 20
    screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font(None, 40)

    apple = pygame.image.load(r"D:\Homework Python\image\bn.png").convert_alpha()
    apple = pygame.transform.scale(apple, (cell_size, cell_size))

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE,150)

    main_game = MAIN()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0,1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1,0)

        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

# ================== START GAME ==================
if __name__ == "__main__":
    pygame.init()
    menu_screen()

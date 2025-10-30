import pygame, sys, random, os
from pygame.math import Vector2

# ================== HIGH SCORE ==================
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
            r"D:\Homework\Homework Python\img\snake1",
            r"D:\Homework\Homework Python\img\snake2",
            r"D:\Homework\Homework Python\img\snake3",
            r"D:\Homework\Homework Python\img\snake4",
            r"D:\Homework\Homework Python\img\snake5"
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

        # Âm thanh ăn thức ăn (theo loại đã chọn)
        self.eat_sound = pygame.mixer.Sound(fr"D:\Homework\Homework Python\Sound\eat{selected_food + 1}.mp3")
        self.hit_sound = pygame.mixer.Sound(fr"D:\Homework\Homework Python\Sound\va_cham.mp3")

    # ================== NỀN ==================
    def draw_background_pattern(self, map_index):
        color_sets = [
            [(167, 209, 61), (175, 215, 70)],
            [(93, 170, 232), (108, 190, 245)],
            [(232, 185, 93), (245, 200, 108)],
            [(200, 100, 150), (220, 130, 180)],
            [(80, 80, 80), (120, 120, 120)],
        ]
        color1, color2 = color_sets[map_index % len(color_sets)]
        for row in range(cell_number):
            for col in range(cell_number):
                rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                pygame.draw.rect(self.background, color1 if (row + col) % 2 == 0 else color2, rect)

    # ================== CHƯỚNG NGẠI VẬT ==================
    def generate_obstacles(self, map_index):
        self.obstacles = []
        self.obstacle_images = []

        obstacle_folder = r"D:\Homework\Homework Python\img\obstacles"
        all_images = [f for f in os.listdir(obstacle_folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
        if not all_images:
            all_images = [None]

        for _ in range(9):
            pos = Vector2(random.randint(0, cell_number - 1),
                          random.randint(0, cell_number - 1))
            while pos in self.snake.body:
                pos = Vector2(random.randint(0, cell_number - 1),
                              random.randint(0, cell_number - 1))
            self.obstacles.append(pos)

            chosen_img = random.choice(all_images)
            if chosen_img:
                img_path = os.path.join(obstacle_folder, chosen_img)
                img = pygame.image.load(img_path).convert_alpha()
                img = pygame.transform.scale(img, (cell_size, cell_size))
            else:
                img = pygame.Surface((cell_size, cell_size))
                img.fill((100, 100, 100))
            self.obstacle_images.append(img)

    # ================== CẬP NHẬT ==================
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # ================== VẼ ==================
    def draw_elements(self):
        screen.blit(self.background, (0, 0))
        for i, obs in enumerate(self.obstacles):
            rect = pygame.Rect(int(obs.x * cell_size), int(obs.y * cell_size), cell_size, cell_size)
            screen.blit(self.obstacle_images[i], rect)
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        score_text = game_font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

    # ================== ĂN TRÁI CÂY ==================
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            while True:
                self.fruit.randomize()
                if self.fruit.pos not in self.obstacles:
                    break
            self.snake.add_block()
            self.score += 1
            self.eat_sound.play()

    # ================== THUA GAME ==================
    def check_fail(self):
        head = self.snake.body[0]
        if head.x >= cell_number: head.x = 0
        elif head.x < 0: head.x = cell_number - 1
        if head.y >= cell_number: head.y = 0
        elif head.y < 0: head.y = cell_number - 1

        if head in self.obstacles:
            self.hit_sound.play()
            self.game_over()

        for block in self.snake.body[1:]:
            if block == head:
                self.game_over()

    def game_over(self):
        if is_new_highscore(self.score):
            name = input_name_screen(self.score)
            add_highscore(name, self.score)
        game_over_screen(self.score)

# ================== NHẬP TÊN ==================
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

# ================== GAME OVER ==================
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

# ================== MENU ==================
def menu_screen():
    pygame.key.set_repeat(200, 150)
    global selected_snake, selected_map, selected_food
    selected_snake = 0
    selected_map = 0
    selected_food = 0

    pygame.display.set_caption("Snake Menu")
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    menu_font = pygame.font.Font(None, 50)
    title_font = pygame.font.Font(None, 70)

    snake_previews = []
    for i in range(1, 6):
          try:
               #Tạo nhạc nền menu
               pygame.mixer.music.load(r"D:\Homework\Homework Python\Sound\menu_musiccc.mp3")
               pygame.mixer.music.set_volume(0.5)
               pygame.mixer.music.play(-1)

               snake_folder = fr"D:\Homework\Homework Python\img\snake{i}"
               head_img = pygame.image.load(fr"{snake_folder}\ranphai.png").convert_alpha()
               body_img = pygame.image.load(fr"{snake_folder}\hcndung.png").convert_alpha()
               tail_img = pygame.image.load(fr"{snake_folder}\dtrai.png").convert_alpha()

               # Scale đúng kích thước cell (giống trong game)
               cell_preview = 40
               head_img = pygame.transform.scale(head_img, (cell_preview, cell_preview))
               body_img = pygame.transform.scale(body_img, (cell_preview, cell_preview))
               tail_img = pygame.transform.scale(tail_img, (cell_preview, cell_preview))
              
               # Tạo surface chứa toàn bộ rắn (3 khối)
               snake_surf = pygame.Surface((cell_preview * 3, cell_preview), pygame.SRCALPHA)
               snake_surf.blit(tail_img, (0, 0))
               snake_surf.blit(body_img, (cell_preview, 0))
               snake_surf.blit(head_img, (cell_preview * 2, 0))
          except Exception as e:
               snake_surf = pygame.Surface((120, 40))
               snake_surf.fill((100 + i*25, 80, 80))
          snake_previews.append(snake_surf)


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

    # ====== Tải 5 loại thức ăn ======
    food_previews = []
    for i in range(1, 6):
        try:
            img = pygame.image.load(fr"D:\Homework\Homework Python\img\food{i}.png").convert_alpha()
        except FileNotFoundError:
            img = pygame.Surface((80,80))
            img.fill((200, 50+i*30, 50))
        food_previews.append(pygame.transform.scale(img, (80, 80)))

    while True:
        screen.fill((30, 30, 30))
        title = title_font.render("🐍 SNAKE GAME MENU 🐍", True, (255,255,0))
        screen.blit(title, (150, 50))

        # --- Snake chọn ---
        snake_text = menu_font.render(f"Snake Type: {selected_snake + 1}", True, (200,200,200))
        screen.blit(snake_text, (100, 200))
        screen.blit(menu_font.render("<", True, (255,255,255)), (50, 200))
        screen.blit(menu_font.render(">", True, (255,255,255)), (400, 200))
        screen.blit(snake_previews[selected_snake], (500, 170))

        # --- Map chọn ---
        map_text = menu_font.render(f"Map: {selected_map + 1}", True, (200,200,200))
        screen.blit(map_text, (100, 350))
        screen.blit(menu_font.render("<", True, (255,255,255)), (50, 350))
        screen.blit(menu_font.render(">", True, (255,255,255)), (250, 350))
        screen.blit(map_previews[selected_map], (500, 320))

        # --- Food chọn ---
        food_text = menu_font.render(f"Food Type: {selected_food + 1}", True, (200,200,200))
        screen.blit(food_text, (100, 500))
        screen.blit(menu_font.render("<", True, (255,255,255)), (50, 500))
        screen.blit(menu_font.render(">", True, (255,255,255)), (400, 500))
        screen.blit(food_previews[selected_food], (500, 470))

        play_text = menu_font.render("Press SPACE to PLAY", True, (0,255,0))
        quit_text = menu_font.render("Press ESC to QUIT", True, (255,0,0))
        screen.blit(play_text, (100, 650))
        screen.blit(quit_text, (100, 710))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()  # dừng nhạc nền
                    main()
                if event.key == pygame.K_a:
                    selected_snake = (selected_snake - 1) % 5
                if event.key == pygame.K_f:
                    selected_snake = (selected_snake + 1) % 5
                if event.key == pygame.K_w:
                    selected_map = (selected_map - 1) % 5
                if event.key == pygame.K_s:
                    selected_map = (selected_map + 1) % 5
                if event.key == pygame.K_j:
                    selected_food = (selected_food - 1) % 5
                if event.key == pygame.K_l:
                    selected_food = (selected_food + 1) % 5

# ================== MAIN GAME LOOP ==================
def main():
    global screen, game_font, cell_size, cell_number, apple

    cell_size = 40
    cell_number = 19
    screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
    pygame.display.set_caption("🐍 Snake Game")

    game_font = pygame.font.Font(None, 40)
    clock = pygame.time.Clock()

    food_path = fr"D:\Homework\Homework Python\img\food{selected_food + 1}.png"
    apple = pygame.image.load(food_path).convert_alpha()
    apple = pygame.transform.scale(apple, (cell_size, cell_size))

    main_game = MAIN()
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

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

# ================== KHỞI ĐỘNG ==================
pygame.init()
menu_screen()

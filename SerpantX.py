#Thanks Hemant Bhaiya for your Guidance and Support
import pygame
import random
import csv
import os

# ---------------- Setup ----------------
pygame.init()

CELL_SIZE = 24
COLS = 25
ROWS = 20
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE
FPS = 60             # keep this high - controls loop smoothness, not snake speed
SNAKE_MOVE_DELAY = 150       # ms between snake moves - raise this number to slow the snake down

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SerpantX")
clock = pygame.time.Clock()

# Aesthetic Palette: Retro CRT Green Matrix
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MATRIX_GREEN = (0, 255, 102)
MATRIX_DIM = (0, 80, 30)
RED = (220, 30, 30)

font_big = pygame.font.SysFont("arial", 48, bold=True)
font_med = pygame.font.SysFont("arial", 28)
font_small = pygame.font.SysFont("arial", 20)

CSV_FILE = "players.csv"

# Cached Surface for CRT Scanlines overlay
scanline_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for y in range(0, HEIGHT, 2):
    pygame.draw.line(scanline_surface, (0, 0, 0, 40), (0, y), (WIDTH, y))

# ---------------- Assets (safe-loading) ----------------
ASSET_PATH = r"D:\Projects 1st year\game\snake_assests\Graphics"

def asset(filename):
    """Build a full path to a file inside ASSET_PATH."""
    return os.path.join(ASSET_PATH, filename)

def load_image(filename):
    path = asset(filename)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))
        except Exception as e:
            print(f"[warn] Could not load image '{path}': {e}")
            return None
    else:
        print(f"[warn] Image not found: {path}")
        return None

def load_sound(filename):
    path = asset(filename)
    if os.path.exists(path):
        try:
            return pygame.mixer.Sound(path)
        except Exception as e:
            print(f"[warn] Could not load sound '{path}': {e}")
            return None
    else:
        print(f"[warn] Sound not found: {path}")
        return None

head_up = load_image("head_up.png")
head_down = load_image("head_down.png")
head_left = load_image("head_left.png")
head_right = load_image("head_right.png")

tail_up = load_image("tail_up.png")
tail_down = load_image("tail_down.png")
tail_left = load_image("tail_left.png")
tail_right = load_image("tail_right.png")

body_horizontal = load_image("body_horizontal.png")
body_vertical = load_image("body_vertical.png")
body_topleft = load_image("body_topleft.png")
body_topright = load_image("body_topright.png")
body_bottomleft = load_image("body_bottomleft.png")
body_bottomright = load_image("body_bottomright.png")

apple_img = load_image("apple.png")
eat_sound = load_sound("eat.wav")

# ---------------- Dynamic CRT Background ----------------
def draw_background():
    """Draws a pitch-black background with subtle 2px matrix dot grid and CRT scanlines."""
    screen.fill(BLACK)

    # Draw 2px dot grid at tile intersections
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            x = c * CELL_SIZE
            y = r * CELL_SIZE
            pygame.draw.rect(screen, MATRIX_DIM, (x - 1, y - 1, 2, 2))

    # Apply CRT Scanline Overlay
    screen.blit(scanline_surface, (0, 0))


def draw_text(text, font, color, x, y, center=False):
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)


# ---------------- CSV Save / Load ----------------
def load_player_data(user_id):
    """Look up a player by user_id, return (name, highscore) or None if not found."""
    if not os.path.exists(CSV_FILE):
        return None

    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id:
                return row["name"], int(row["highscore"])
    return None


def save_player_data(user_id, name, highscore):
    """Save or update a player's record in the CSV without wiping other players."""
    rows = []
    found = False

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

    for row in rows:
        if row["user_id"] == user_id:
            row["name"] = name
            row["highscore"] = str(highscore)
            found = True
            break

    if not found:
        rows.append({"user_id": user_id, "name": name, "highscore": str(highscore)})

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id", "name", "highscore"])
        writer.writeheader()
        writer.writerows(rows)


# ---------------- Leaderboard Screen ----------------
def get_leaderboard(limit=10):
    """Read the CSV and return a list of (name, highscore) sorted highest first."""
    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    rows.sort(key=lambda r: int(r["highscore"]), reverse=True)
    return [(r["name"], int(r["highscore"])) for r in rows[:limit]]


def show_leaderboard():
    """Full-screen leaderboard. Press ESC or ENTER to go back."""
    viewing = True

    while viewing:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    viewing = False

        draw_background()

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        draw_text("LEADERBOARD", font_big, MATRIX_GREEN, WIDTH // 2, 50, center=True)

        scores = get_leaderboard(limit=10)

        if not scores:
            draw_text("No scores yet - be the first!", font_med, WHITE,
                       WIDTH // 2, HEIGHT // 2, center=True)
        else:
            start_y = 120
            row_gap = 34
            for i, (player_name, player_score) in enumerate(scores):
                rank = i + 1
                line = f"{rank}. {player_name} - {player_score}"
                color = MATRIX_GREEN if rank == 1 else WHITE
                draw_text(line, font_med, color, WIDTH // 2, start_y + i * row_gap, center=True)

        draw_text("ESC / ENTER = Back", font_small, WHITE, WIDTH // 2, HEIGHT - 30, center=True)

        pygame.display.flip()


# ---------------- Name / ID Entry Screen ----------------
def get_player_info():
    """Simple text input screen. Returns (user_id, name)."""
    user_id = ""
    name = ""
    active_field = "id"
    entering = True

    while entering:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active_field = "name" if active_field == "id" else "id"

                elif event.key == pygame.K_RETURN:
                    if user_id.strip() and name.strip():
                        entering = False

                elif event.key == pygame.K_F1:
                    show_leaderboard()

                elif event.key == pygame.K_BACKSPACE:
                    if active_field == "id":
                        user_id = user_id[:-1]
                    else:
                        name = name[:-1]

                else:
                    char = event.unicode
                    if char.isprintable():
                        if active_field == "id":
                            user_id += char
                        else:
                            name += char

        draw_background()

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        draw_text("Enter your Player ID:", font_med, WHITE, WIDTH // 2, HEIGHT // 2 - 80, center=True)
        draw_text(user_id + ("|" if active_field == "id" else ""), font_med, MATRIX_GREEN,
                   WIDTH // 2, HEIGHT // 2 - 40, center=True)

        draw_text("Enter your Name:", font_med, WHITE, WIDTH // 2, HEIGHT // 2 + 10, center=True)
        draw_text(name + ("|" if active_field == "name" else ""), font_med, MATRIX_GREEN,
                   WIDTH // 2, HEIGHT // 2 + 50, center=True)

        draw_text("TAB = switch field | ENTER = start | F1 = Leaderboard", font_small, WHITE,
                   WIDTH // 2, HEIGHT // 2 + 110, center=True)

        pygame.display.flip()

    return user_id.strip(), name.strip()


# ---------------- Snake ----------------
class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(5, 7), (4, 7), (3, 7)]   # list of (col, row)
        self.direction = (1, 0)                 # moving right
        self.grow = False
        self.alive = True

    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    def update(self):
        if not self.alive:
            return

        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Wall collision
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            self.alive = False
            return

        # Self collision
        if new_head in self.body:
            self.alive = False
            return

        self.body.insert(0, new_head)

        if self.grow:
            self.grow = False
        else:
            self.body.pop()

    def eat(self):
        self.grow = True
        if eat_sound:
            eat_sound.play()

    def draw(self):
        for i, (x, y) in enumerate(self.body):
            pos = (x * CELL_SIZE, y * CELL_SIZE)

            # ----- HEAD -----
            if i == 0:
                if self.direction == (0, -1):
                    img = head_up
                elif self.direction == (0, 1):
                    img = head_down
                elif self.direction == (-1, 0):
                    img = head_left
                else:
                    img = head_right
                if img:
                    screen.blit(img, pos)
                else:
                    pygame.draw.rect(screen, MATRIX_GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
                continue

            # ----- TAIL -----
            if i == len(self.body) - 1:
                prev = self.body[i - 1]
                if prev[1] < y:
                    img = tail_down
                elif prev[1] > y:
                    img = tail_up
                elif prev[0] < x:
                    img = tail_right
                else:
                    img = tail_left
                if img:
                    screen.blit(img, pos)
                else:
                    pygame.draw.rect(screen, MATRIX_GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
                continue

            # ----- BODY -----
            prev = self.body[i - 1]
            next_seg = self.body[i + 1]

            if prev[1] == y and next_seg[1] == y:
                img = body_horizontal
            elif prev[0] == x and next_seg[0] == x:
                img = body_vertical
            else:
                if (prev[0] < x and next_seg[1] < y) or (next_seg[0] < x and prev[1] < y):
                    img = body_topleft
                elif (prev[0] > x and next_seg[1] < y) or (next_seg[0] > x and prev[1] < y):
                    img = body_topright
                elif (prev[0] < x and next_seg[1] > y) or (next_seg[0] < x and prev[1] > y):
                    img = body_bottomleft
                else:
                    img = body_bottomright

            if img:
                screen.blit(img, pos)
            else:
                pygame.draw.rect(screen, MATRIX_GREEN, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))


# ---------------- Food ----------------
class Food:
    def __init__(self):
        self.respawn([])

    def respawn(self, snake_body):
        while True:
            self.pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if self.pos not in snake_body:
                break

    def draw(self):
        if apple_img:
            screen.blit(apple_img, (self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE))
        else:
            pygame.draw.rect(screen, RED,
                             (self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


# ---------------- Main Game ----------------
def main():
    user_id, name = get_player_info()

    existing = load_player_data(user_id)
    if existing:
        _, high_score = existing
    else:
        high_score = 0

    snake = Snake()
    food = Food()
    score = 0
    running = True

    last_move_time = pygame.time.get_ticks()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_F1:
                    show_leaderboard()
                    last_move_time = pygame.time.get_ticks()

                if not snake.alive and event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    snake.reset()
                    food.respawn(snake.body)
                    score = 0
                    last_move_time = pygame.time.get_ticks()

                if snake.alive:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        snake.change_direction((0, -1))
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        snake.change_direction((0, 1))
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        snake.change_direction((-1, 0))
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        snake.change_direction((1, 0))

        if snake.alive:
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= SNAKE_MOVE_DELAY:
                last_move_time = current_time
                snake.update()

                if snake.body[0] == food.pos:
                    snake.eat()
                    food.respawn(snake.body)
                    score += 10
                    if score > high_score:
                        high_score = score
                        save_player_data(user_id, name, high_score)

        # Draw
        draw_background()
        food.draw()
        snake.draw()

        # HUD Text rendered in Matrix Green
        draw_text(f"Player: {name}", font_med, MATRIX_GREEN, 10, 8)
        draw_text(f"Score: {score}", font_med, MATRIX_GREEN, 10, 42)
        draw_text(f"High: {high_score}", font_med, MATRIX_GREEN, 10, 76)
        draw_text("F1 = Leaderboard", font_small, MATRIX_GREEN, 10, HEIGHT - 26)

        if not snake.alive:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            draw_text("GAME OVER", font_big, RED, WIDTH // 2, HEIGHT // 2 - 50, center=True)
            draw_text(f"Score: {score}", font_med, WHITE, WIDTH // 2, HEIGHT // 2 + 10, center=True)
            draw_text("SPACE / ENTER = Restart", font_small, MATRIX_GREEN, WIDTH // 2, HEIGHT // 2 + 60, center=True)
            draw_text("F1 = Leaderboard", font_small, MATRIX_GREEN, WIDTH // 2, HEIGHT // 2 + 90, center=True)

        pygame.display.flip()

    save_player_data(user_id, name, high_score)
    pygame.quit()


if __name__ == "__main__":
    main()
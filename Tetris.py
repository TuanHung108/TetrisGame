import pygame
import random
import sys
from dataclasses import dataclass

#Thông số cơ bản
GAME_WIDTH = 450
SCREEN_WIDTH = 660
SCREEN_HEIGHT = 750
BLOCK_SIZE = 30
COLUMNS = GAME_WIDTH // BLOCK_SIZE
ROWS = SCREEN_HEIGHT // BLOCK_SIZE
board = [0] * COLUMNS * ROWS  #0 present for no block

speed, level, score = 1000, 1, 0

#Cửa sổ giao diện
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris Game")
#Tạo font chữ
font = pygame.font.SysFont("Arial", 35, True)

#Nhạc nền
pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0)


#Load block
picture = []
for index in range(8):
    picture.append(pygame.transform.scale(pygame.image.load(f"T_{index}.jpg"), (BLOCK_SIZE, BLOCK_SIZE)))

#Tetromino cho các chữu O,I,J,L,S,Z,T qua ma tran 4x4 phẳng
tetrominos = [
    [0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0], #O
    [0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0], #I
    [0,0,0,0,3,3,3,0,0,0,3,0,0,0,0,0], #J
    [0,0,4,0,4,4,4,0,0,0,0,0,0,0,0,0], #L
    [0,5,5,0,5,5,0,0,0,0,0,0,0,0,0,0], #S
    [6,6,0,0,0,6,6,0,0,0,0,0,0,0,0,0], #Z
    [0,0,0,0,7,7,7,0,0,7,0,0,0,0,0,0]  #T
]

#Class đại diện cho các khối
@dataclass
class Tetromino():
    tetro : list #mảng đại diện cho 1 khối random
    row : int = 0
    column : int = 6

    def show(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                x = (self.column + n % 4) * BLOCK_SIZE
                y = (self.row + n // 4) * BLOCK_SIZE
                screen.blit(picture[color], (x, y))  #blit dung de ve 1 surface len 1 surface khac (ve picture len screen)
    
    def check(self, r, c):
        for n, color in enumerate(self.tetro):
            if color > 0:
                rs = r + n // 4
                cs = c + n % 4
                if cs < 0 or rs >= ROWS or cs >= COLUMNS or board[rs * COLUMNS + cs] > 0:
                    return False
        return True

    def update(self, r, c):
        if self.check(self.row + r, self.column + c):
            self.row += r
            self.column += c 
            return True
        return False
    
    def rotate(self):
        save_tetro = self.tetro.copy()
        for n, color in enumerate(save_tetro):
            self.tetro[(2 - (n % 4)) * 4 + (n // 4)] = color
        if not self.check(self.row, self.column):
            self.tetro = save_tetro.copy()


def LockBlockOnBoard():
    for n, color in enumerate(character.tetro):
        if color > 0:
            board[(character.row + n // 4) * COLUMNS + (character.column + n % 4)] = color

def ClearLines():
    full_rows = 0
    for row in range(ROWS):
        if all(board[row * COLUMNS + column] > 0 for column in range(COLUMNS)):
            del board[row * COLUMNS : (row + 1) * COLUMNS]  # Xóa cả hàng
            board[0:0] = [0] * COLUMNS  # Thêm hàng trống vào đầu bảng
            full_rows += 1
    return full_rows * full_rows * 100  # Tính điểm dựa trên số hàng bị xóa

def SpawnNewTetrominos():
    new_tetro = Tetromino(tetro = random.choice(tetrominos))
    if not new_tetro.check(0,0):
        return False
    return new_tetro

def CheckGameOVer():
    for column in range(COLUMNS):
        if board[column] > 0:
            return True
    return False    

#Class quản lý các nút
@dataclass
class Button():
    def __init__(self, x, y, width, height, text, color, text_color, action = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.action = action

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect, 4)

        text_surface = font.render(self.text, True, self.text_color)
        text_pos = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_pos)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                self.action()
                return True
        return False
    
def pause_game():
    print("PAUSE")
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.K_DOWN:
                if event.key == pygame.K_p:
                    paused = False

def reset_game():
    print("RESET")
    global score, character, next_tetro, board
    score = 0
    character = SpawnNewTetrominos()
    next_tetro = SpawnNewTetrominos()
    board = [0] * ROWS * COLUMNS

def exit_game():
    print("EXIT")
    pygame.quit()
    sys.exit() #thoát vòng lặp chính và kết thúc ctrinh, giải phóng tài nguyên

#Tạo các nút
pause_button = Button(GAME_WIDTH + 40, 450, 140, 90, "PAUSE", (255, 255, 255), (255, 255, 255), pause_game)
reset_button = Button(GAME_WIDTH + 40, 550, 140, 90, "RESET", (255, 255, 255), (255, 255, 255), reset_game)
exit_button = Button(GAME_WIDTH + 40, 650, 140, 90, "EXIT", (255, 255, 255), (255, 255, 255), exit_game)

#Vẽ giao diện game
def DrawBoard():
    tile_size = BLOCK_SIZE
    LIGHT_GREY = (30, 30, 30)
    GREY = (130, 130, 130)
    screen.fill(LIGHT_GREY)
    pygame.draw.rect(screen, (110, 110, 110), (0, 0, GAME_WIDTH, SCREEN_HEIGHT), 4)
    for row in range(ROWS):
        for column in range(COLUMNS):
            pygame.draw.rect(screen, GREY, (column * tile_size, row * tile_size, tile_size, tile_size), 1)

def DrawInfor(level, score, time, next_tetro):
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))
    screen.blit(level_text, (GAME_WIDTH + 30, 60))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (GAME_WIDTH + 30, 100))

    seconds = time // 1000
    minutes = seconds // 60
    seconds %= 60
    time_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, (255, 255, 255))
    screen.blit(time_text, (GAME_WIDTH + 30, 140))

    next__tetromino_text = font.render("Next:", True, (255, 255, 255))
    screen.blit(next__tetromino_text, (GAME_WIDTH + 30, 210))
    pygame.draw.rect(screen, (255, 255, 255), (GAME_WIDTH + 30, 250, 160, 180), 4)

    for n, color in enumerate(next_tetro.tetro):
        if color > 0:
            x = GAME_WIDTH + 60 + (n % 4)  * BLOCK_SIZE
            y = 290 + (n // 4) * BLOCK_SIZE
            screen.blit(picture[color], (x, y))

#Event 
tetromino_down = pygame.USEREVENT + 1
pygame.time.set_timer(tetromino_down, speed)
pygame.key.set_repeat(100, 100)


#Vòng lặp chính chạy game
character = SpawnNewTetrominos()
next_tetro = SpawnNewTetrominos()
start_time = pygame.time.get_ticks()
RunGame = True

while RunGame:
    DrawBoard()
    character.show()
    elapsed_time = pygame.time.get_ticks() - start_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RunGame = False

        if pause_button.is_clicked(event):
            pause_game()
        if reset_button.is_clicked(event):
            reset_game()
        if exit_button.is_clicked(event):
            exit_game()

        if event.type == tetromino_down:
            if not character.update(1, 0):
                LockBlockOnBoard()
                character= next_tetro
                next_tetro = SpawnNewTetrominos()
                if CheckGameOVer():
                    print("Game Over!")
                    RunGame = False
                score += ClearLines()
                if score > 0 and score // 500 >= level:
                    speed = int(speed * 0.7)
                    pygame.time.set_timer(tetromino_down, speed)
                    level = score // 500 + 1
        
        if event.type == pygame.KEYDOWN:  #sự kiện xra khi phím ấn xuống
            if event.key == pygame.K_LEFT:
                character.update(0, -1)
            if event.key == pygame.K_RIGHT:
                character.update(0, 1)
            if event.key == pygame.K_DOWN:
                character.update(1, 0)
            if event.key == pygame.K_SPACE:
                character.rotate()

    DrawInfor(level, score, elapsed_time, next_tetro)
    pause_button.draw(screen, font)
    reset_button.draw(screen, font)
    exit_button.draw(screen, font)

    for n, color in enumerate(board):
        if color > 0:
            x = n % COLUMNS * BLOCK_SIZE
            y = n // COLUMNS * BLOCK_SIZE
            screen.blit(picture[color], (x, y))

    pygame.display.flip()

pygame.quit()


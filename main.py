import pygame
import sys
import random
import math
from pygame.locals import *

NUM_FIREWORKS_MAX = 4
NUM_FIREWORKS_MIN = 2
SPEED_FLY_UP_MAX = 15
SPEED_FLY_UP_MIN = 10

# Các thông số cửa sổ
WINDOWWIDTH = 1000 # Kích thước cửa so game theo chieu rộng
WINDOWHEIGHT = 1000 # Kích thước cửa so game theo chiều cao
FPS = 120 # Số khung hình trên giây, tăng để chạy mượt hơn

# Các thông số cho pháo hoa
SIZE = 5 # Kích thước của viên đạn trong pháo hoa
SPEED_CHANGE_SIZE = 0.1 # Tốc độ thay đổi kích thước viên đạn
CHANGE_SPEED = 0.1 # Tốc độ thay đổi tốc độ viên đạn
RAD = math.pi / 180 # Chuyển đổi độ sang radian
A_FALL = 1.5 # Gia tốc rơi tự do
NUM_BULLET = 45 # Số lượng viên đạn trong mỗi quả pháo hoa
SPEED_MIN = 3 # Tốc độ tối thiểu của viên đạn
SPEED_MAX = 6 # Tốc độ tối đa của viên đạn
TIME_CREAT_FW = 10 # Thời gian tạo pháo hoa mới
NUM_FIREWORKS_MAX = 10 # Số pháo hoa tối đa xuất hiện cùng lúc
NUM_FIREWORKS_MIN = 5
SPEED_FLY_UP_MAX = 20 # Tốc độ bay lên toi đa của vien đạn
SPEED_FLY_UP_MIN = 15 # Tốc độ bay lên tối thiểu của viên đạn
NUM_PARTICLES = 30 # Số lượng hạt pháo hoa rơi xuống

# Hàm tạo màu sắc ngẫu nhiên
def random_color():
    return (random.randint(50, 255), random.randint(50, 255), random. randint(50, 255))

# Số pháo hoa tối thiểu xuất hiện cùng lúc

class Dot():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def update(self):
        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE
        else:
            self.size = 0

    def draw(self):
        if self.size > 0:
            pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), int(self.size))

class BulletFlyUp():
    def __init__(self, speed, x):
        self.speed = speed
        self.x = x
        self.y = WINDOWHEIGHT
        self.dots = []
        self.size = SIZE / 2
        self.color = random_color()

    def update(self):
        self.dots.append(Dot(self.x, self.y, self.size, self.color))
        self.y -= self.speed
        self.speed -= A_FALL * 0.1
        for dot in self.dots:
            dot.update()
        self.dots = [dot for dot in self.dots if dot.size > 0]

    def draw(self):
        pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), int(self.size))
        for dot in self.dots:
            dot.draw()

class Particle():
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(1, 3)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE
        else:
            self.size = 0

    def draw(self):
        if self.size > 0:
            pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), int(self.size))

class Bullet():
    def __init__(self, x, y, speed, angle, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.size = SIZE
        self.color = color

    def update(self):
        speedX = self.speed * math.cos(self.angle * RAD)
        speedY = self.speed * -math.sin(self.angle * RAD)
        self.x += speedX
        self.y += speedY
        self.y += A_FALL
        if self.size > 0:
            self.size -= SPEED_CHANGE_SIZE
        else:
            self.size = 0
        if self.speed > 0:
            self.speed -= CHANGE_SPEED
        else:
            self.speed = 0

    def draw(self):
        if self.size > 0:
            pygame.draw.circle(DISPLAYSURF, self.color, (int(self.x), int(self.y)), int(self.size))

class FireWork():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dots = []
        self.bullets = self.create_bullets()

    def create_bullets(self):
        bullets = []
        for i in range(NUM_BULLET):
            angle = (360 / NUM_BULLET) * i
            speed = random.uniform(SPEED_MIN, SPEED_MAX)
            color = random_color()
            bullets.append(Bullet(self.x, self.y, speed, angle, color))
        return bullets

    def update(self):
        for bullet in self.bullets:
            bullet.update()
            self.dots.append(Dot(bullet.x, bullet.y, bullet.size, bullet.color))
        self.dots = [dot for dot in self.dots if dot.size > 0]

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()
        for dot in self.dots:
            dot.draw()

def draw_happy_new_year():
    font = pygame.font.Font("Montserrat-Black.ttf", 50)
    text = font.render("Happy New Year 2024!", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.centerx = WINDOWWIDTH // 2
    text_rect.centery = WINDOWHEIGHT // 2

    text_rect.x += int(math.sin(pygame.time.get_ticks() / 50) * 5)
    DISPLAYSURF.blit(text, text_rect)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    pygame.display.set_caption('FIREWORKS')
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    fireWorks = []
    time = TIME_CREAT_FW
    bulletFlyUps = []
    particles = []

    while True:
        DISPLAYSURF.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
        if time == TIME_CREAT_FW:
            for i in range(random.randint(NUM_FIREWORKS_MIN, NUM_FIREWORKS_MAX)):
                bulletFlyUps.append(BulletFlyUp(random.uniform(SPEED_FLY_UP_MIN, SPEED_FLY_UP_MAX), random.randint(int(WINDOWWIDTH * 0.2), int(WINDOWHEIGHT * 0.8))))

        for bulletFlyUp in bulletFlyUps:
            bulletFlyUp.draw()
            bulletFlyUp.update()

        for fireWork in fireWorks:
            fireWork.draw()
            fireWork.update()

        for bulletFlyUp in bulletFlyUps:
            if bulletFlyUp.speed <= 0:
                fireWorks.append(FireWork(bulletFlyUp.x, bulletFlyUp.y))
                bulletFlyUps = [bu for bu in bulletFlyUps if bu != bulletFlyUp]

        for fireWork in fireWorks:
            if fireWork.bullets[0].size <= 0:
                fireWorks = [fw for fw in fireWorks if fw != fireWork]

        for bullet in fireWorks:
            if bullet.bullets[0].size <= 0:
                for _ in range(NUM_PARTICLES):
                    particle_x = bullet.bullets[0].x
                    particle_y = bullet.bullets[0].y
                    particle_size = random.uniform(1, 3)
                    particle_color = bullet.bullets[0].color
                    particles.append(Particle(particle_x, particle_y, particle_size, particle_color))

        for particle in particles:
            particle.update()
            particle.draw()

        draw_happy_new_year()

        if time <= TIME_CREAT_FW:
            time += 1
        else:
            time = 0
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()

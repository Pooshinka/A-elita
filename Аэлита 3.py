# Импорт и инициализация
import os
import csv
import pygame
import random
from os import path

pygame.init()  # Устанавливаем размеры окна
infoObject = pygame.display.Info()
size = width, height = infoObject.current_w, infoObject.current_h
pygame.display.set_mode((width, height))
screen = pygame.display.set_mode(size)  # screen — холст, на котором нужно рисовать:
pygame.mouse.set_visible(True)  # Скрываем курсор мыши
Mouse1, Mouse2, Flag, Flag2 = False, False, 0, 0  # Мышинные клавиши небыли нажаты, в текущий момент
clock = pygame.time.Clock()  # Задаем количество FPS
menuN, menu_y = 1, 1  # Переменная номера меню и выбора пункта меню
font_aelita = 100  # Размер шрифта для меню 1920/24/38 => 80, 50 // 1024 =>
font_menu = 50
font_qwest = 30
color_menu_cursor = ('black')
color_menu = pygame.Color('black')  # цвет меню
text = []  # Список меню
text1 = ["НОВАЯ ИГРА", "ЗАГРУЗКА УРОВНЕЙ", "НАСТРОЙКИ", "ВАШ СЧЕТ", "ДО ВСТРЕЧИ ПИЛОТ"]
text2 = ['ЭКРАН 800 х 600', 'ЭКРАН 1024х768', 'ЭКРАН 1600х900', 'ЭКРАН 1920x1080', 'ПОЛНЫЙ ЭКРАН']
text3 = ['1. земля первый полет', '2. путь на марс', '3. титан и его улучшения', '4. альфа-центавра',
         '5. планета мюл на связи',
         '6. роккот нас ждет', '7. на базе пиратов ', '8. битва за галактику']
img_dir = path.join(path.dirname(__file__), 'img\\image')
mp3_dir = path.join(path.dirname(__file__), 'img\\mp3')
data_font_dir = path.join(path.dirname(__file__), 'img\\data_font')
sprits_dir = path.join(path.dirname(__file__), 'img\\Sprits')
WIDTH = width
HEIGHT = height
FPS = 60
level = 0
POWERUP_TIME = 5000
game_time = 1 * 1000
font_name = pygame.font.match_font('arial')
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Космическое путешествие Аэлита!")

class Bot(pygame.sprite.Sprite):
    def __init__(self, health):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['bot1', 'bot2', 'bot3'])
        self.image = bot_anim[self.type][0]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(- 350, - 300)
        self.frame = 0
        self.frame_rate = 60
        self.speedy = random.randrange(1, 3)
        self.health_bot = health
        self.health_bot2 = health
        self.last_update = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.step = 0
        while self.step == 0:
            self.step = random.randrange(-2, 2)
        self.shoot_delay = 1500
        self.power = 1
        self.energy = 1
        self.step_y = 0
    def update(self):
        x, y, x1, y1 = self.rect
        if self.health_bot < self.health_bot2:
            pygame.draw.line(screen, 'red', [x, y], [x + (x1 / self.health_bot2) * self.health_bot, y - 5], 5)
        if self.rect.y < 100 + self.step_y:
            self.rect.y += self.speedy
        else:
            if self.step >= 0 and self.rect.x >= WIDTH - x1:
                self.step = (self.step + 1) * (-1)
                self.step_y += 150
            if self.step <= 0 and self.rect.x <= 0:
                self.step = (self.step - 1) * (-1)
                self.step_y += 150
            self.rect.x += self.step
            self.shoot_bot()
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(bot_anim[self.type]):
                self.frame = 0
            else:
                center = self.rect.center
                self.image = bot_anim[self.type][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        if self.rect.top > HEIGHT:
            self.kill()
            newbots(self.health_bot2)
    def shoot_bot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay / self.power:
            self.last_shot = now
            if self.power == 1:
                bullet_bot = Bullet_bot(self.rect.centerx, self.rect.bottom)
                all_sprites.add(bullet_bot)
                bullets_bot.add(bullet_bot)
                shoot_sound.play(0)
            if self.power >= 2:
                bullet_bot1 = Bullet_bot(self.rect.left, self.rect.centery)
                bullet_bot2 = Bullet_bot(self.rect.right, self.rect.centery)
                all_sprites.add(bullet_bot1)
                all_sprites.add(bullet_bot2)
                bullets_bot.add(bullet_bot1)
                bullets_bot.add(bullet_bot2)
                shoot_sound.play()
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    def energyup(self):
        self.energy += 1
        if self.step <= 15:
            self.step += 5
        self.energy_time = pygame.time.get_ticks()
class Bullet_bot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_bot_img
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.centerx = x
        self.speedy = 15
        self.bullet_health = 1
    def update(self):
        self.rect.y += self.speedy
        # уничтожить, если он заходит за нижнюю часть экрана
        if self.rect.bottom > HEIGHT:
            self.kill()
class Player(pygame.sprite.Sprite):
    def __init__(self, health):
        pygame.sprite.Sprite.__init__(self)
        self.size = 'stop'
        self.image = pygame.transform.scale(player_img, (120, 120))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.health_player = health
        self.health_player2 = health
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.step = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.energy = 1
        self.energy_time = pygame.time.get_ticks()
        self.bullet_health = 1
    def update(self):
        global bx, by, player_anim, player_img
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(player_anim[self.size]):
                self.frame = 0
            else:
                center = self.rect.center
                self.image = player_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
        x, y, x1, y1 = self.rect
        pygame.draw.line(screen, 'green', [x, y + y1 + 5],
                         [x + x1 / self.health_player2 * (int(self.health_player)), y + y1 + 5], 5)
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if self.speedy == 0 and self.speedx == 0:
            self.size = 'stop'
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -self.step
            self.size = 'left'
            if bx > -200:
                bx -= 1
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = self.step
            self.size = 'right'
            if bx <= 0:
                bx += 1
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy = -self.step
            self.size = 'up'
            if by < 0:
                by += 1
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy = self.step
            self.size = 'down'
            if by > -100:
                by -= 1
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.energy >= 2 and pygame.time.get_ticks() - self.energy_time > POWERUP_TIME:
            self.energy -= 1
            if self.step > 5:
                self.step -= 4
            self.energy_time = pygame.time.get_ticks()
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay / self.power:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                score.boolets[level] += 1
                shoot_sound.play(0)
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()
    def energyup(self):
        self.energy += 1
        if self.step <= 12:
            self.step += 4
        self.energy_time = pygame.time.get_ticks()
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(- 350, - 300)
        self.speedy_start = 1
        self.speedy_stop = 4
        self.speedy = random.randrange(self.speedy_start, self.speedy_stop)
        self.speedx_start = -1
        self.speedx_stop = 0
        self.speedx = random.randrange(self.speedx_start, self.speedx_stop)
        self.rot = 0
        self.rot_speed = random.randrange(-10, 10)
        self.last_update = pygame.time.get_ticks()
        self.health = self.radius // 10
        self.health2 = self.radius // 10
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            # image = pygame.transform.scale(self.image_orig, (50, 50))
            image = self.image_orig
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        x, y, x1, y1 = self.rect
        if self.health < self.health2:
            pygame.draw.line(screen, 'red', [x, y], [x + (x1 / self.health2) * self.health, y - 5], 3)
        if self.rect.top > HEIGHT + 250 or self.rect.left < -250 or self.rect.right > WIDTH + 250:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-350, -300)
            self.speedy = random.randrange(self.speedy_start, self.speedy_stop)
            self.speedx = self.speedx_stop
            self.health = self.radius // 10
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - 15
    def update(self):
        self.rect.y += self.speedy
        # уничтожить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['health', 'gun', 'energy'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2
    def update(self):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > HEIGHT:
            self.kill()
class Score:
    def __init__(self):
        self.level = [0, 0, 0, 0, 0, 0, 0, 0]
        self.score = [0, 0, 0, 0, 0, 0, 0, 0]
        self.mobs = [0, 0, 0, 0, 0, 0, 0, 0]
        self.boolets = [0, 0, 0, 0, 0, 0, 0, 0]
        self.accuracy = [0, 0, 0, 0, 0, 0, 0, 0]
        self.hits = [0, 0, 0, 0, 0, 0, 0, 0]
        self.death = [0, 0, 0, 0, 0, 0, 0, 0]
        self.bot_kill = [0, 0, 0, 0, 0, 0, 0, 0]
        self.time_game = [0, 0, 0, 0, 0, 0, 0, 0]
    def update(self, screen):
        global level
        # пишем новое значение счёта
        size = 18
        font = pygame.font.SysFont('monospace', size)
        text_screen = font.render('ОЧКИ: ' + str(self.score[level]), True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, 0))
        text_screen = font.render('УНИЧТОЖЕНО МЕТЕОРИТОВ: ' + str(self.mobs[level]), True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, size))
        text_screen = font.render('ПОПАДАНИЯ: ' + str(self.hits[level]), True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, size * 2))
        text_screen = font.render('ВСЕГО ВЫСТРЕЛОВ: ' + str(self.boolets[level]), True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, size * 3))
        if self.boolets[level] > 0:
            self.accuracy[level] = self.hits[level] / self.boolets[level] * 100
        text_screen = font.render('ТОЧНОСТЬ СТРЕЛЬБЫ: ' + str(int(self.accuracy[level])) + ' %', True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, size * 4))
        text_screen = font.render('УНИЧТОЖЕНО ПИРАТОВ: ' + str(int(self.bot_kill[level])), True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, size * 5))
        text_screen = font.render('ОСТАЛОСЬ ВРЕМЕНИ НА УРОВНЕ:' + str(int(self.time_game[level])), True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, size * 6))
        text_screen = font.render('СКОЛЬКО ПОМЕР: ' + str(int(self.death[level])), True,
                                  ((0, 255, 0)))  # Выдергиваем слово и рендерим
        screen.blit(text_screen, (10, size * 7))
        cherep = pygame.image.load(path.join(sprits_dir, "Череп.png")).convert_alpha()
        emodsi = pygame.transform.scale(cherep, (size, size))
        ddx, ddy, q, q1 = text_screen.get_rect()
        q1, q2 = 0, 0
        for i in range(self.death[level]):
            screen.blit(emodsi, (ddx + size + 10 + q + size * (i - q1), size * (7 + q2)))
        self.level = level
def load_level(level):
    global mp3_fon, fon_text, text_mp3, bonus, mp3_fon_list, Vstart_list, Vstop_list, health_bots, bonus_list, Health_player_list, \
        musik, game_time, last_time_game, now_game
    restart_game()
    # Уровни игры
    mp3_fon = mp3_fon_list[level]
    fon_text = Fon_text_list[level]
    text_mp3 = text_mp3_list[level]
    bonus = float(bonus_list[level])
    game_time = int(game_time_list[level])
    # Переменные бота
    for i in range(int(mob_list[level])):  # Добавление Моба
        newmob()
        Mob.speedy = random.randrange(int(Vstart_list[level]), int(Vstop_list[level]))
    for i in range(int(n_bots_list[level])):  # Добавление ботов
        newbots(int(health_bots[level]))
        b.health_bot = int(health_bots[level])
        b.health_bot2 = int(health_bots[level])
        b.bullet_health = level + 0.5
    player.health_player = float(Health_player_list[level])
    player.health_player2 = float(Health_player_list[level])
    player.bullet_health = level + 0.5
    musik = pygame.mixer.music.load(mp3_dir + '\\' + mp3_fon)
    now_game = pygame.time.get_ticks()
def restart_game():
    global now, n_bots, level, bx, by
    # Восстановление переменных плеера
    player.rect.centerx = WIDTH / 2
    player.rect.bottom = HEIGHT - 10
    player.speedx = 0
    player.speedy = 0
    player.health_player = int(Health_player_list[level])
    player.health_player2 = int(Health_player_list[level])
    player.frame = 0
    player.last_update = pygame.time.get_ticks()
    player.frame_rate = 50
    bx, by = -100, -100
    # Восстановление переменных Мобов метеоритов
    for i in bullets:
        i.kill()
    for i in mobs:
        i.kill()
        # newmob()
    now = pygame.time.get_ticks()
    for i in bots:
        i.kill()
        # newbots()
    for i in bullets:
        i.kill()
    for i in bullets_bot:
        i.kill()
def newbots(health_bot):
    global all_sprites
    b = Bot(health_bot)
    all_sprites.add(b)
    bots.add(b)
def newmob():
    global mobs, all_sprites
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
def show_go_screen():
    global clip, screen, clip_load, level, Health_player_list, size, now_game
    player.health_player = int(Health_player_list[level])
    # Музыкальное сопровождение
    pygame.mixer.music.load(mp3_dir + '\\' + "Меню1.mp3")
    pygame.mixer.music.play(-1)
    # Загрузка фона
    x1, y1 = 0, 0
    background2 = pygame.image.load(path.join(img_dir, "game_over.jpeg")).convert()
    background2_copy = background2.copy()
    for i in range(70):
        background2 = background2_copy
        background2 = pygame.transform.scale(background2, (WIDTH + i * 2, HEIGHT + i))
        screen.blit(background2, (x1, y1))
        x1 -= 1
        y1 -= 1
        pygame.display.flip()
        clock.tick(20)
        restart_game()
    screen.blit(background2, (x1, y1))
    draw_text(screen, "ВАШ ПЕРСОНЖ ПОГИБ!", 64, WIDTH / 2 + 3, HEIGHT / 4 + 3, 'black')
    draw_text(screen, "Начать заново - нажмите 'enter'!", 30,
              WIDTH / 2 + 3, HEIGHT / 2 + 3, 'black')
    draw_text(screen, 'Выйти из игры "ESC"', 30, WIDTH / 2 + 3, HEIGHT * 3 / 4 + 3, 'black')
    draw_text(screen, "ВАШ ПЕРСОНЖ ПОГИБ!", 64, WIDTH / 2, HEIGHT / 4, 'white')
    draw_text(screen, "Начать заново - нажмите 'enter'!", 30,
              WIDTH / 2, HEIGHT / 2, 'white')
    draw_text(screen, 'Выйти из игры "ESC"', 30, WIDTH / 2, HEIGHT * 3 / 4, 'white')
    pygame.display.flip()
    a = True
    now_game = pygame.time.get_ticks()
    while a:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                    a = False
    return
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
def game_over_():
    global game_over
    pygame.mixer.music.pause()
    # pygame.mixer.music.play(0)
    if game_over:
        show_go_screen()
        game_over = False
        load_level(level)
    pygame.mixer.music.pause()
    pygame.mixer.music.load(mp3_dir + '\\' + mp3_fon_list[level])
    pygame.mixer.music.play(-1)
# Разрешение экрана изменение размера
def resolution(width_, height_, full):
    global screen, width, height, font_aelita, font_menu, background_image, background_image_original, size, WIDTH, HEIGHT
    if full:
        # infoObject = pygame.display.Info()
        pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
        size = width, height = infoObject.current_w, infoObject.current_h
        WIDTH, HEIGHT = size
        screen = pygame.display.set_mode((width, height))
        font_aelita = int(width / 24)
        font_menu = int(width / 38)
    else:
        size = width_, height_
        font_aelita = int(width_ / 24)
        font_menu = int(width_ / 38)
        font_qwest = int(width_ / 64)
        screen = pygame.display.set_mode(size)  # screen — холст, на котором нужно рисовать:
        size = width, height = width_, height_
        WIDTH, HEIGHT = size
    background_image = background_image_original.copy()
# Загрузка картинок
def load_image(path, name, color_key=None):
    fullname = os.path.join(path, name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image
# Выход из игры
def quit_out():
    pygame.quit()
    exit()
# Обработка нажатий клавиш в меню
def key_menu():
    global menu_y, menuN, font_menu, font_aelita, Mouse1, Mouse2, text_mp3_list, level, mp3_fon_list, result_menu_show
    if Mouse2:
        Mouse2 = False
        if menuN == 2:
            menuN, menu_y = 1, 1
        else:
            quit_out()
    for event in pygame.event.get():  # Ждем события (действия пользователя)
        if event.type == pygame.QUIT:  # Если нажали на крестик, то закрываем окно
            quit_out()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if menu_y > 1:
                    menu_y -= 1
                else:
                    menu_y = len(text)
            elif event.key == pygame.K_DOWN:
                if menu_y < len(text):
                    menu_y += 1
                elif menu_y == len(text):
                    menu_y = 1
            elif event.key == pygame.K_ESCAPE:
                if menuN == 2 or menuN == 3 or result_menu_show == True:
                    menuN, menu_y = 1, 1
                    result_menu_show = False
                else:
                    quit_out()
            elif (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                choice_menu()
                pygame.mixer.music.load("img\\mp3\\" + mp3_fon_list[level])
                pygame.mixer.music.play(-1)
                return
def choice_menu():
    global menu_y, menuN, Mouse2, Mouse1, menu_show, level, result_menu_show
    Mouse2, Mouse1 = False, False
    if menuN == 1:
        if menu_y == 1:  # Начало игры
            # result_menu_show = True
            load_level(0)
            menu_show = False
            return
        if menu_y == 2:  # Настройка
            menuN, menu_y = 3, 1
        if menu_y == 3:  # Загрузка уровней
            menuN, menu_y = 2, 1
        if menu_y == 4:  # Рейтинг
            result_menu_show = True
            return
        if menu_y == 5:  # Выход
            quit_out()
    elif menuN == 2:
        if menu_y == 1:
            resolution(800, 600, False)
        if menu_y == 2:
            resolution(1024, 768, False)
        if menu_y == 3:
            resolution(1600, 900, False)
        if menu_y == 4:
            resolution(1920, 1080, False)
        if menu_y == 5:
            resolution(0, 0, True)
    elif menuN == 3:
        # result_menu_show = True
        level = menu_y - 1
        load_level(level)
        menu_show = False
        return


def mouse_click():
    global Mouse1, Mouse2, Flag
    num_buttons = pygame.mouse.get_pressed()
    if num_buttons[2]:  # Мышка нажата правая клавиша
        Flag = 2
    if num_buttons[0]:  # Мышка нажата левая клавиша
        Flag = 1
    if num_buttons[2] == False and Flag == 2:  # Мышка отнажата правая клавиша
        Mouse2, Flag = True, 0
    if num_buttons[0] == False and Flag == 1:  # Мышка отнажата левая клавиша
        Mouse1, Flag = True, 0


# Отображаем меню
def menu():
    global width, height, menu_y, text, menuN, color_menu, Mouse1
    pos_x, pos_y = pygame.mouse.get_pos()  # Проверка событий от мыши
    x, y = width // 2, height // 2  # Координаты центра экрана
    font = pygame.font.Font('img\\data_font\Cyberpunk_RUS_BY_LYAJKA.ttf', int(font_aelita))
    Aelite = font.render("AELITA", True, 'red')
    text_w, text_h = Aelite.get_width(), Aelite.get_height()  # Координаты названия
    text_x, text_y = x - text_w // 2, y - text_h // 2
    screen.blit(Aelite, (text_x, text_y - y // 2))
    if menuN == 1:  # Выбор номера меню
        text = text1
    elif menuN == 2:
        text = text2
    elif menuN == 3:
        text = text3
    font = pygame.font.Font('img\\data_font\\TunnelFront.ttf', int(font_menu))  # Рисуем меню
    for i in range(len(text)):
        menu = font.render(text[i], True, color_menu)
        text_x, text_y = x - menu.get_width() // 2, y - menu.get_height() // 2  # Координаты центра экрана
        text_w, text_h = menu.get_width(), menu.get_height()  # Координаты названия
        x1, y1 = text_x, int((y - (len(text) * text_h) // 2) + i * text_h)
        screen.blit(menu, (x1, y1))
        x_rec, y_rec = x1 - 30, y1 - 3 - text_h * len(text) + text_h * menu_y  # Координаты левого угла  прямоугольника
        x1_rec, y1_rec = text_w + 60, text_h + 3  # Координаты правого угла прямоугоьника
        if last_x != pos_y or last_y != pos_x:  # Если не равен. значит есть движение мышкой
            if (x_rec < pos_x < (x_rec + x1_rec) and
                    (y1 - 3) < pos_y < (y1 - 3) + y1_rec):  # Мышка попадает в прямоугольник
                menu_y = i + 1
                if Mouse1:
                    choice_menu()
    pygame.draw.rect(screen, color_menu_cursor, (x_rec, y_rec, x1_rec, y1_rec), 6)
    mouse_click()
    return pos_x, pos_y


def fon_move():
    global background_image, screen
    background_image = pygame.transform.scale(background_image, (width, height))
    # тряска
    x, y = 0, 0
    screen.blit(background_image, (- int(x), - int(y)))


def press_key():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return pygame.K_ESCAPE
            # elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return pygame.K_LEFT
            elif event.key == pygame.K_RIGHT:
                return pygame.K_RIGHT
            elif event.key == pygame.K_UP:
                return pygame.K_UP
            elif event.key == pygame.K_DOWN:
                return pygame.K_DOWN
            return pygame.KEYDOWN
        if event.type == pygame.MOUSEMOTION:
            return pygame.MOUSEMOTION


def key_():
    global Mouse1, Mouse2
    if Mouse2:
        Mouse2 = False
    for event in pygame.event.get():  # Ждем события (действия пользователя)
        if event.type == pygame.QUIT:  # Если нажали на крестик, то закрываем окно
            quit_out()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return pygame.K_LEFT
            elif event.key == pygame.K_RIGHT:
                return pygame.K_RIGHT
            elif event.key == pygame.K_ESCAPE:
                quit_out()
        return True


def result_itogo():
    score_, mobs, hits, boolets, accuracy, bot_kill, time_game, death = 0, 0, 0, 0, 0, 0, 0, 0
    # пишем новое значение счёта
    level = 7
    screen.fill((0, 0, 0), (int(500 / 2.08), int(200 / 2.08), WIDTH - int(1000 / 2.08), HEIGHT - int(400 / 2.08)))
    size = int(WIDTH / 50.5)
    font = pygame.font.SysFont('monospace', size)
    for i in range(level):
        score_ += score.score[i]
    text_screen = font.render('ОЧКИ: ' + str(score_), True, ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 - int(size * 4)))
    for i in range(level):
        mobs += score.mobs[i]
    text_screen = font.render('УНИЧТОЖЕНО МЕТЕОРИТОВ: ' + str(mobs), True,
                              ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 - size * 3))
    for i in range(level):
        hits += score.hits[i]
    text_screen = font.render('ПОПАДАНИЯ: ' + str(hits), True,
                              ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 - size * 2))
    for i in range(level):
        boolets += score.boolets[i]
    text_screen = font.render('ВСЕГО ВЫСТРЕЛОВ: ' + str(boolets), True,
                              ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 - size * 1))
    if score.boolets[level] > 0:
        score.accuracy[level] = (score.hits[level] / score.boolets[level]) * 100
    for i in range(level):
        accuracy += score.accuracy[i]
    text_screen = font.render('ТОЧНОСТЬ СТРЕЛЬБЫ: ' + str(int(accuracy)) + ' %', True,
                              ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 - size * 0))
    for i in range(level):
        bot_kill += score.bot_kill[i]
    text_screen = font.render('УНИЧТОЖЕНО ПИРАТОВ: ' + str(int(bot_kill)), True,
                              ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 + size * 1))
    for i in range(level):
        time_game += score.time_game[i]
    text_screen = font.render('ОСТАЛОСЬ ВРЕМЕНИ НА УРОВНЕ:' + str(int(time_game)), True,
                              ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 + size * 2))
    for i in range(level):
        death += score.death[i]
    text_screen = font.render('СКОЛЬКО ПОМЕР: ' + str(int(death)), True,
                              ((250, 250, 250)))  # Выдергиваем слово и рендерим
    screen.blit(text_screen, (int(WIDTH / 20) + int(500 / 2.08), HEIGHT // 2 + size * 3))
    cherep = pygame.image.load(path.join(sprits_dir, "Череп.png")).convert_alpha()
    emodsi = pygame.transform.scale(cherep, (size, size))
    ddx, ddy, q, q1 = text_screen.get_rect()
    q1, q2 = 0, 0
    for i in range(score.death[level]):
        screen.blit(emodsi,
                    (int(WIDTH / 20) + int(500 / 2.08) + ddx + size + 10 + q + size * (i - q1), size * (4 + q2)))

# Установка фона
background_image_original = load_image(img_dir, 'Заставка.jpg')
background_image = background_image_original.copy()
background_image = pygame.transform.scale(background_image, (width, height))
screen.blit(background_image, (0, 0))  # Закрашиваем фон черным
move_x, move_y = 0, 0
last_x, last_y = pygame.mouse.get_pos()
# Загрузка уровней
plan = []
with open("img\\Level_game.txt", encoding='utf-8') as r_file:
    file_reader = csv.DictReader(r_file, delimiter='\t')  # Создаем объект DictReader, указываем символ-разделитель "/t"
    for row in file_reader:
        plan.append(row)
# Загрузка всей игровой графики
# Загрузка фонов по уровням (всего 8 уровней)
Health_player_list = []
mob_list = []
Vstart_list = []
Vstop_list = []
bonus_list = []
n_bots_list = []
health_bots = []
background_list = []
mp3_fon_list = []
Fon_text_list = []
text_mp3_list = []
game_time_list = []
for i in plan:
    Health_player_list.append(i['Health_player'])
    mob_list.append((i['mob']))
    Vstart_list.append(i['Vstart'])
    Vstop_list.append(i['Vstop'])
    bonus_list.append(i['bonus'])
    n_bots_list.append(i['N_bots'])
    health_bots.append(i['Health_bots'])
    background_list.append(i['Fon'])
    mp3_fon_list.append(i['mp3'])
    Fon_text_list.append(i['Fon_text'])
    text_mp3_list.append(i['text_mp3'])
    game_time_list.append(i['game_time'])
background_img = []
for img in background_list:
    background_img.append(
        pygame.transform.scale((pygame.image.load(path.join(img_dir, img)).convert()), (WIDTH + 200, HEIGHT + 200)))
bx, by = -100, -100
# Загрузка анимации спрайта плеера
player_img = pygame.image.load(path.join(sprits_dir, "player3.png")).convert_alpha()
# Загружаем анимацию плеера
player_list = [['Player3.png', 'Player3.png', 'Player3.png', 'Player3.png'],
               ['PlUp1.png', 'PlUp2.png', 'PlUp3.png', 'PlUp4.png'],
               ['PlDown1.png', 'PlDown2.png', 'PlDown3.png', 'PlDown4.png'],
               ['PlLeft1.png', 'PlLeft2.png', 'PlLeft3.png', 'PlLeft4.png'],
               ['PlRight1.png', 'PlRight2.png', 'PlRight3.png', 'PlRight4.png']]
player_anim = {}
player_anim['up'] = []
player_anim['down'] = []
player_anim['left'] = []
player_anim['right'] = []
player_anim['stop'] = []
for i in range(len(player_list)):
    for img in player_list[i]:
        if i == 0:
            player_img = pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()),
                                                (120, 120))
            player_anim['stop'].append(player_img)
        if i == 1:
            player_img = pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()),
                                                (120, 120))
            player_anim['up'].append(player_img)
        if i == 2:
            player_img = pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()),
                                                (120, 120))
            player_anim['down'].append(player_img)
        if i == 3:
            player_img = pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()),
                                                (120, 120))
            player_anim['left'].append(player_img)
        if i == 4:
            player_img = pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()),
                                                (120, 120))
            player_anim['right'].append(player_img)
# Загрузка ракет  пеереворотом спрайта
bullet_img = pygame.image.load(path.join(sprits_dir, "Красный лазер.png")).convert_alpha()
bullet_bot_img = pygame.transform.flip(pygame.image.load(path.join(sprits_dir, "Синий лазер.png")).convert_alpha(),
                                       False, True)
# Загрузка метеоритов
meteor_images = []
meteor_list = ['Метеорит1.png', 'Метеорит2.png', 'Метеорит3.png', 'Метеорит4.png', 'Метеорит5.png', 'Метеорит6.png',
               'Метеорит7.png', 'Метеорит8.png', 'Метеорит9.png', 'Метеорит10.png', 'Метеорит11.png', 'Метеорит12.png',
               'Метеорит13.png', 'Метеорит14.png', 'Метеорит15.png']
for img in meteor_list:
    size_m = random.randrange(50, 150)
    meteor_images.append(
        pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()), (size_m, size_m)))
# Загрузка анимации взрывов
explosion_anim = {}
explosion_anim['bg75'] = []
explosion_anim['bg150'] = []
explosion_anim['bg250'] = []
explosion_anim['lg250'] = []
# Загрузка первой анимации взрыва
bah_list = ['bah0.png', 'bah1.png', 'bah2.png', 'bah3.png', 'bah4.png', 'bah5.png', 'bah6.png', 'bah7.png', 'bah8.png']
for img in bah_list:
    bah_images = pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()), (150, 150))
    explosion_anim['bg150'].append(bah_images)
    bah_images = pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()), (250, 250))
    explosion_anim['bg250'].append(bah_images)
# Загрузка второй анимации взрыва
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(sprits_dir, filename)).convert_alpha()
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['bg75'].append(img_lg)
    img_sm = pygame.transform.scale(img, (250, 250))
    explosion_anim['lg250'].append(img_sm)
# Загрузка Ботов
bot_anim = {}
bot_anim['bot1'] = []
bot_anim['bot2'] = []
bot_anim['bot3'] = []
# Загрузка анимации botov
bot_list = [['bot11.png', 'bot12.png', 'bot13.png', 'bot14.png', 'bot15.png', 'bot16.png'],
            ['bot21.png', 'bot22.png', 'bot23.png', 'bot22.png', 'bot21.png', 'bot22.png'],
            ['bot31.png', 'bot32.png', 'bot33.png', 'bot32.png', 'bot31.png', 'bot32.png']]
for i in range(len(bot_list)):
    for img in bot_list[i]:
        if i == 0:
            bot_images = pygame.transform.flip(
                pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()), (100, 100)),
                False, True)
            bot_anim['bot1'].append(bot_images)
        if i == 1:
            bot_images = pygame.transform.flip(
                pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()), (100, 100)),
                False, True)
            bot_anim['bot2'].append(bot_images)
        if i == 2:
            bot_images = pygame.transform.flip(
                pygame.transform.scale((pygame.image.load(path.join(sprits_dir, img)).convert_alpha()), (100, 100)),
                False, True)
            bot_anim['bot3'].append(bot_images)
# Апгрейд зороввья и оружия
powerup_images = {}
powerup_images['health'] = pygame.transform.scale(
    pygame.image.load(path.join(sprits_dir, 'Здоровье.png')).convert_alpha(),
    (20, 20))
powerup_images['gun'] = pygame.transform.scale(pygame.image.load(path.join(sprits_dir, 'Оружие.png')).convert_alpha(),
                                               (20, 20))
powerup_images['energy'] = pygame.transform.scale(
    pygame.image.load(path.join(sprits_dir, 'Молния.png')).convert_alpha(),
    (20, 20))
# Группы спрайтов
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bahs = pygame.sprite.Group()
bots = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bullets_bot = pygame.sprite.Group()
a = 0, 0
explosion = Explosion(a, 'bg75')
player = Player(int(Health_player_list[level]))
health_bot = health_bots[level]
b = Bot(health_bot)
all_sprites.add(player)
n = len(meteor_list)
load_level(level)

# Уровни игры
bonus = float(bonus_list[level])
score = Score()
# Загрузка мелодий игры
shoot_sound = pygame.mixer.Sound(path.join(mp3_dir, 'Выстрел3.mp3'))
musik = pygame.mixer.music.load(mp3_dir + '\\' + mp3_fon_list[level])
pygame.mixer.music.play(-1)
expl_sounds = []
power_sound = pygame.mixer.Sound(path.join(mp3_dir, 'Health.mp3'))
health_sound = pygame.mixer.Sound(path.join(mp3_dir, 'Power.mp3'))
energy_sound = pygame.mixer.Sound(path.join(mp3_dir, 'Energy.mp3'))
for snd in ['Бах1.mp3', 'Бах2.mp3', 'Бах3.mp3']:
    expl_sounds.append(pygame.mixer.Sound(path.join(mp3_dir, snd)))
now = pygame.time.get_ticks()
clip_load = True  # True -загружает анимацию? False нет
running = True
game_over = True
clock = pygame.time.Clock()
now_game = pygame.time.get_ticks()
menu_show = True
result_menu_show = False  # Если фальш, то результаты не выводятся
result_menu_show2 = True
# Установка музыки
pygame.mixer.music.load("img\\mp3\\Меню1.mp3")
pygame.mixer.music.play(-1)
# Цикл игры
while running:
    while menu_show:
        key_menu()  # Ждем события (действия пользователя)
        screen.fill((0, 0, 0))
        fon_move()  # Установка фона и тряски
        pos_x, pos_y = menu()  # Меню игры
        clock.tick(60)
        if result_menu_show:
            result_itogo()
            pygame.display.flip()
        pygame.display.update()
    if level <= 7:
        # Держим цикл на правильной скорости
        screen.blit(background_img[level], (bx, by))
    for event in pygame.event.get():                # Ввод процесса (события)
        if event.type == pygame.QUIT:           # проверка для закрытия окна
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                draw_text(screen, "ПАУЗА - нажмите 'enter' чтобы продолжить!", 30,
                          WIDTH / 2, HEIGHT / 2, 'white')
                draw_text(screen, 'Выйти из игры "ESC"', 30, WIDTH / 2, HEIGHT * 3 / 4, 'white')
                pygame.display.flip()
                a = True
                while a:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                menu_show = True
                                menuN, menu_y = 1, 1
                                a = False
                                pygame.mixer.music.load("img\\mp3\\Меню1.mp3")
                                pygame.mixer.music.play(-1)
                            elif (event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                                a = False
    all_sprites.update()
    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'health':
            player.health_player += player.health_player2 // 2
            if player.health_player >= player.health_player2:
                player.health_player = player.health_player2
            hit.kill()
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
            hit.kill()
        if hit.type == 'energy':
            player.energyup()
            energy_sound.play()
            hit.kill()
    # Обновление взаимодействие ракет ботов и ракет игрока
    hits = pygame.sprite.groupcollide(bullets_bot, bullets, True, True)
    if hits:
        for hit in hits:
            # Взрыв малый ракета и ракета
            expl = Explosion(hit.rect.center, 'bg250')
            all_sprites.add(expl)
            if random.random() > bonus:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
                random.choice(expl_sounds).play()

    # Обновление взаимодействие ракет ботов и мобов
    hits = pygame.sprite.groupcollide(bullets_bot, mobs, True, True)
    if hits:
        for hit in hits:
            # Взрыв малый ракета и ракета
            expl = Explosion(hit.rect.center, 'bg250')
            all_sprites.add(expl)
            if random.random() > bonus:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
                random.choice(expl_sounds).play()
            newmob()
    # Обновление взаимодействие мобов и ракет
    all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    if hits:
        for hit in hits:
            # Взрыв малый ракета и моб
            score.score[level] += hit.radius // 10
            score.hits[level] += 1
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'bg75')
            all_sprites.add(expl)
            if random.random() > bonus:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            hit.health -= player.bullet_health
            if hit.health <= 0:
                # Делаем нового моба
                score.mobs[level] += 1
                random.choice(expl_sounds).play()
                hit.kill()
                newmob()
    # Обновление взаимодействие ботов и ракет игрока
    hits = pygame.sprite.groupcollide(bots, bullets, False, True)
    if hits:
        for hit in hits:
            # Взрыв малый ракета и моб
            score.score[level] += int(hit.health_bot) * 20
            score.hits[level] += 1
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'bg75')
            all_sprites.add(expl)
            if random.random() > bonus:
                pow = Pow(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            hit.health_bot -= player.bullet_health
            if hit.health_bot <= 0:
                # Делаем нового моба
                score.bot_kill[level] += 1
                random.choice(expl_sounds).play()
                hit.kill()
                expl = Explosion(hit.rect.center, 'bg250')
                all_sprites.add(expl)
                newbots(int(health_bots[level]))
    # Проверка, взаимодействие игрока и Ракет ботов
    hits = pygame.sprite.spritecollide(player, bullets_bot, False, pygame.sprite.collide_circle)
    if hits:
        for hit in hits:
            # Взрыв малый ракета и мобd
            random.choice(expl_sounds).play()
            player.health_player -= hit.bullet_health
            # Взрыв большой моб и корабль
            expl = Explosion(hit.rect.center, 'bg150')
            all_sprites.add(expl)
            hit.kill()
            if player.health_player <= 0:
                # Уничтожаем ракету бота
                random.choice(expl_sounds).play()
                game_over = True
                game_over_()
    # Проверка, взаимодействие игрока и Ботов
    hits = pygame.sprite.spritecollide(player, bots, False, pygame.sprite.collide_circle)
    if hits:
        for hit in hits:
            # Взрыв малый ракета и мобd
            score.score[level] += hit.health_bot * 20
            score.bot_kill[level] += 1
            random.choice(expl_sounds).play()
            player.health_player -= hit.health_bot
            hit.health_bot -= player.health_player
            # Взрыв большой моб и корабль
            expl = Explosion(hit.rect.center, 'bg150')
            all_sprites.add(expl)
            if hit.health_bot <= 0:
                # Делаем нового моба
                random.choice(expl_sounds).play()
                hit.kill()
                score.bot_kill[level] += 1
                newbots(int(health_bots[level]))
                # Игрок уничтожен
            if player.health_player <= 0:
                game_over = True
                game_over_()
    # Проверка, взаимодействие игрока и мобов
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        for hit in hits:
            # Взрыв малый ракета и мобd
            score.score[level] += hit.radius // 10
            score.mobs[level] += 1
            random.choice(expl_sounds).play()
            player.health_player -= hit.health
            hit.health -= hit.health
            # Взрыв большой моб и корабль
            expl = Explosion(hit.rect.center, 'bg150')
            all_sprites.add(expl)
            if hit.health <= 0:
                # Делаем нового моба
                random.choice(expl_sounds).play()
                hit.kill()
                newmob()
            # Игрок уничтожен
            if player.health_player <= 0:
                game_over = True
                game_over_()
    last_shot = pygame.time.get_ticks()
    if now - last_shot > 5000:
        b.update()
    # Рендеринг
    all_sprites.draw(screen)
    score.update(screen)
    last_time_game = pygame.time.get_ticks()
    score.time_game[level] = game_time * 50000 - (last_time_game - now_game)
    if last_time_game - now_game < game_time * 5000:
        draw_text(screen, "ВЫ ПРОШЛИ НА " + str(level + 1) + ' УРОВЕНЬ!', 50,
                  WIDTH / 2, HEIGHT * 1 / 4, 'white')
        draw_text(screen, 'ПРОЧНОСТЬ ВАШЕГО КОРОБЛЯ ' + str(player.health_player2), 50, WIDTH / 2, HEIGHT * 3 / 4, 'white')
        draw_text(screen, 'ВАШЕ ВЕЗЕНИЕ' + str(int((1 - bonus) * 100)) + '%', 50, WIDTH / 2,
                  HEIGHT / 2, 'white')
    if last_time_game - now_game > game_time * 50000:
        if level < 7:
            level += 1
            load_level(level)
            pygame.mixer.music.load("img\\mp3\\" + mp3_fon_list[level])
            pygame.mixer.music.play(-1)
            now_game = pygame.time.get_ticks()
        elif level == 7:
            while result_menu_show2:
                draw_text(screen, "ВЫ ПРОШЛИ ВСЕ УРОВНИ!!!", 50,
                          WIDTH / 2, HEIGHT / 2, 'white')
                draw_text(screen, 'Выйти из игры 2 раза "ESC"', 50, WIDTH / 2, HEIGHT * 3 / 4, 'white')
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            result_menu_show2 = False
                pygame.display.flip()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
import pygame
import random


def shift(lst, steps):
    """
    Функция для циклического сдвига элементов списка на заданное количество шагов
    :param lst: список, в котором сдвигаем элементы
    :param steps: количество шагов для сдвига
    """
    if steps < 0:
        steps = abs(steps)
        for _ in range(steps):
            lst.append(lst.pop(0))
    else:
        for _ in range(steps):
            lst.insert(0, lst.pop())


def choose_bg_color(points_amount):
    """
    Выбор цвета фона игры в зависимости от количества очков
    (каждые 5 очков цвет меняется с темного на светлый и наоборот)
    :param points_amount: количества очков
    """
    if points_amount % 10 >= 5:
        screen.fill(BLACK)
    else:
        screen.fill(SKY)


# Настройки окна
WIDTH = 500
HEIGHT = 500
FPS = 60

# Цвета
SKY = (133, 193, 233)
YELLOW = (255, 215, 0)
GREEN = (46, 204, 113)
WHITE = (255, 255, 255)
VIOLET = (199, 21, 133)
MAROON = (128, 0, 0)
BLUE = (25, 25, 112)
BLACK = (16, 16, 16)
RED = (255, 99, 71)
GRAY = (211, 211, 211)
colors = [GREEN, YELLOW, VIOLET, MAROON, RED, BLUE]
color = random.choice(colors)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Floppy Bird')

# Настройки персонажа
bird = pygame.Rect(40, 250, 30, 23)
bird_img1 = pygame.image.load('assets/bird/fpbs1.png')
bird_img2 = pygame.image.load('assets/bird/fpbs2.png')
bird_img3 = pygame.image.load('assets/bird/fpbs3.png')
bird_images = [bird_img1, bird_img2, bird_img3]
points = 0

# Шрифты
DEFAULT_FONT = 'Arial Rounded'
menu_font = pygame.font.SysFont(DEFAULT_FONT, 20)
difficulty_font = pygame.font.SysFont(DEFAULT_FONT, 38)
points_font = pygame.font.SysFont(DEFAULT_FONT, 30)
game_over_font = pygame.font.SysFont(DEFAULT_FONT, 50)

# Текст
game_over_text = game_over_font.render('GAME OVER', True, WHITE)
title_text = game_over_font.render('Floppy Bird', True, WHITE)
play_text = menu_font.render('Play', True, BLACK)
difficulty_plus_text = difficulty_font.render("+", True, BLACK)
difficulty_minus_text = difficulty_font.render("-", True, BLACK)
exit_text = menu_font.render('Exit', True, BLACK)
back_to_menu_text = menu_font.render('Menu', True, BLACK)

# Фоновые изображения
menu_bg = pygame.image.load("assets/menu_bg.jpg")
game_over_bg = pygame.image.load("assets/GO_bg.png")

# Падение
GRAVITY = 0.3
y_change = 0

# Прыжок
is_jump = False
hop_count = 10

# Настройки труб
pipes = []
pipe_cd = 1500  # время, через которое будет отрисовываться новая труба (в мс)
pipe_cd_step = 500  # шаг, на который будем менять время отрисовки труб
pipe_speed = 2
space_between_pipe = 100  # расстояние между верхней и нижней трубой

# Добавление очков
check = []

# Временные параметры
clock = pygame.time.Clock()
current_time = 0
last_pipe_time = 0

# Счетчик времени для смены цвета труб
color_counter = 0

# Параметры игры
game_mode = 'MENU'
running = True
while running:

    # Меню игры
    if game_mode == 'MENU':
        # На случай, если изображение не подгрузится, будет заливка голубым цветом
        screen.fill(SKY)
        screen.blit(menu_bg, (0, 0))

        screen.blit(title_text, (120, 80))

        # Обрабатываем события, произошедшие за кадр
        for event in pygame.event.get():
            # Если нажали на крестик (на окне игры) - выходим из цикла (завершаем игру)
            if event.type == pygame.QUIT:
                running = False

            # Если нажали на кнопку мыши
            if event.type == pygame.MOUSEBUTTONDOWN:

                # В области зеленой кнопки - начинаем игру
                if 170 < event.pos[0] < 160 + 170 and 180 < event.pos[1] < 180 + 50:
                    game_mode = 'GAME'

                # В области левой серой кнопки - уменьшаем сложность
                if 100 < event.pos[0] < 100 + 50 and 250 < event.pos[1] < 250 + 50:
                    # проверяем, что нажали именно ЛКМ
                    if event.button == 1:
                        # Минимальная сложность (скорость движения труб) = 1
                        if pipe_speed > 1:
                            # С уменьшением сложности уменьшаем скорость птицы и скорость появления труб
                            pipe_speed -= 1
                            pipe_cd += pipe_cd_step

                # В области правой серой кнопки - увеличиваем сложность
                if 350 < event.pos[0] < 350 + 50 and 250 < event.pos[1] < 250 + 50:
                    # проверяем, что нажали именно ЛКМ
                    if event.button == 1:
                        # Максимальная сложность (скорость движения труб) = 5
                        if pipe_speed < 5:
                            # С увеличением сложности увеличиваем скорость птицы и скорость появления труб
                            pipe_speed += 1
                            pipe_cd -= pipe_cd_step

                # Если выбрали масимальную сложность, то меняется только скорость птицы
                # (скорость появления труб как на 4 уровне сложности)
                if pipe_speed == 5:
                    pipe_cd = 500

                # В области красной кнопки - закрываем игру (выходим из цикла)
                if 170 < event.pos[0] < 160 + 170 and 320 < event.pos[1] < 320 + 50:
                    running = False

        # Отрисовываем кнопки
        pygame.draw.rect(screen, GREEN, (170, 180, 160, 50))
        pygame.draw.rect(screen, YELLOW, (170, 250, 160, 50))
        pygame.draw.rect(screen, GRAY, (350, 250, 50, 50))  # увелечение сложности
        pygame.draw.rect(screen, GRAY, (100, 250, 50, 50))  # уменьшение сложности
        pygame.draw.rect(screen, RED, (170, 320, 160, 50))

        # Отрисовываем текст на кнопках
        screen.blit(play_text, (230, 192))
        difficulty_text = menu_font.render("Difficulty: " + str(pipe_speed), True, BLACK)
        screen.blit(difficulty_text, (197, 263))
        screen.blit(difficulty_plus_text, (365, 253))
        screen.blit(difficulty_minus_text, (118, 250))
        screen.blit(exit_text, (230, 332))

    # Сам процесс игры
    if game_mode == 'GAME':

        choose_bg_color(points)

        # Обрабатываем события, произошедшие за кадр
        for i in pygame.event.get():
            # Если нажали на крестик (на окне игры) - выходим из цикла (завершаем игру)
            if i.type == pygame.QUIT:
                running = False

            # Обработка событий нажатия клавиш клавиатуры
            if i.type == pygame.KEYDOWN:
                # Нажатие пробела = прыжок
                if i.key == pygame.K_SPACE:
                    is_jump = True
                    hop_count = 0

        # Прыжок
        if is_jump:
            hop_count += 1
            bird.top -= 6
            # начинаем падение после 5 прыжков подряд (как в оригинальлной игре)
            if hop_count == 5:
                y_change = 0
                is_jump = False
        # Падение
        else:
            y_change += GRAVITY
            bird.top += y_change

        # Текущее время
        current_time = pygame.time.get_ticks()

        # Создание труб
        if current_time - last_pipe_time > pipe_cd:
            width_pipe = 40
            # Создание верхней части трубы
            height_up_pipe = random.randint(50, 400)
            up_pipe = pygame.Rect(WIDTH, 0, width_pipe, height_up_pipe)

            # Создание нижней части трубы
            y_down_pipe = height_up_pipe + space_between_pipe
            height_down_pipe = HEIGHT - y_down_pipe
            down_pipe = pygame.Rect(WIDTH, y_down_pipe, width_pipe, height_down_pipe)

            # Создание промежуточного пространства
            y_middle_space = height_up_pipe
            height_middle_space = HEIGHT - height_up_pipe - height_down_pipe
            middle_space = pygame.Rect(WIDTH, y_middle_space, width_pipe, height_middle_space)
            check.append(middle_space)

            # Добавление в список
            pipes.append((up_pipe, down_pipe))

            # Перепись временых настроек
            last_pipe_time = current_time
            pipe_cd = random.randint(pipe_cd, pipe_cd + pipe_cd_step)

        # Меняем цвет труб каждые 5 секунд игры
        if color_counter == 300:
            color = random.choice(colors)
            color_counter = 0

        # Отрисовка труб на экране
        for pipe in pipes:
            # рисуем трубы
            pygame.draw.rect(screen, color, pipe[0])
            pygame.draw.rect(screen, color, pipe[1])
            # сдвигаем трубы
            pipe[0].left -= pipe_speed
            pipe[1].left -= pipe_speed

        # Столкновение
        # Столкновение птички с краями окна игры
        if bird.top < 0 or bird.bottom > HEIGHT:
            game_mode = 'GAME OVER'

        # Столкновение с трубами
        for pipe in pipes:
            up_pipe = pipe[0]
            down_pipe = pipe[1]

            if bird.colliderect(up_pipe):
                game_mode = 'GAME OVER'
            elif bird.colliderect(down_pipe):
                game_mode = 'GAME OVER'

        # Пролет между труб
        for flag in check:
            flag.left -= pipe_speed

            # Если "столкнулись" с пустым расстоянием между трубами, то добавляем очко
            if bird.colliderect(flag):
                points += 1
                check.remove(flag)

        # анимация полета за счет сменяющихся картинок
        shift(bird_images, 1)
        screen.blit(bird_images[0], (bird.left, bird.top))

        points_text = points_font.render("Points: " + str(points), True, WHITE)
        screen.blit(points_text, (10, 10))

        color_counter += 1

    # Если конец игры - отрисовываем экран с надписью "GAME OVER"
    if game_mode == 'GAME OVER':

        choose_bg_color(points)
        screen.blit(game_over_bg, (0, 0))

        screen.blit(game_over_text, (100, 100))

        final_points_text = game_over_font.render("Points: " + str(points), True, WHITE)
        screen.blit(final_points_text, (145, 180))

        # Кнопка возврата в меню
        pygame.draw.rect(screen, GREEN, (170, 300, 160, 50))
        screen.blit(back_to_menu_text, (222, 312))

        # Обрабатываем события, произошедшие за кадр
        for event in pygame.event.get():
            # Если нажали на крестик (на окне игры) - выходим из цикла
            if event.type == pygame.QUIT:
                running = False

            # Если нажали на кнопку мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                # В области зеленой кнопки - возвращаемся в меню
                if 170 < event.pos[0] < 160 + 170 and 300 < event.pos[1] < 300 + 50:
                    bird = pygame.Rect(40, 250, 30, 23)
                    points = 0
                    pipe_cd = 1500
                    pipe_speed = 2
                    pipes.clear()
                    check.clear()
                    y_change = 0

                    game_mode = 'MENU'

    clock.tick(FPS)
    pygame.display.update()
pygame.quit()

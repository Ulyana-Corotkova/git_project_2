import pygame
from math import sqrt
import sys

SIZE = (600, 600)  # Размер окна
FPS = 60  # Кол-во кадров в секунду
PLATFORMS = pygame.sprite.Group()  # Группа спрайтов платформ
OCHKI = [0, 0]  # Изначальное кол-во очков каждого игрока


# Класс взаимодействия с платформами
class Platform(pygame.sprite.Sprite):
    # Метод инициализации
    def __init__(self, x, y):
        super().__init__(PLATFORMS)
        self.image = pygame.Surface((20, 100))
        self.image.fill((139, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    # Метод отталкивания от верхней и нижней стенки
    def update_1(self, up, down):
        if up:
            if self.rect.top > 0:
                self.rect.y += -self.speed
        if down:
            if self.rect.bottom < SIZE[1]:
                self.rect.y += self.speed


# Класс взаимодействия с шариком
class Ball(pygame.sprite.Sprite):
    # Метод инициализации
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dy, self.dx = -1, 1
        self.speed = 3

    # Метод отталкивания от платформ
    def collide(self):
        for sprite in PLATFORMS:
            if pygame.sprite.collide_rect(self, sprite):
                if self.dx < 0:
                    sound_6.play()
                    delta_x = sprite.rect.right - self.rect.left
                if self.dx > 0:
                    sound_6.play()
                    delta_x = self.rect.right - sprite.rect.left
                if self.dy < 0:
                    sound_6.play()
                    delta_y = sprite.rect.bottom - self.rect.top
                if self.dy > 0:
                    sound_6.play()
                    delta_y = self.rect.bottom - sprite.rect.top
                if abs(delta_x - delta_y) < 20:
                    sound_6.play()
                    self.dy = -self.dy
                    self.dx = -self.dx
                elif delta_x > delta_y:
                    sound_6.play()
                    self.dy = -self.dy
                elif delta_y > delta_x:
                    sound_6.play()
                    self.dx = -self.dx

    # Метод отталкивания от стенок
    def update(self):
        if self.rect.top <= 0:
            self.dy = -self.dy
            self.rect.top = 0
        if self.rect.bottom >= SIZE[1]:
            self.dy = -self.dy
            self.rect.bottom = SIZE[1]
        if self.rect.left <= 0:
            OCHKI[1] += 1
            sound_1.play()
            self.dx = -self.dx
            self.rect.left = 0
        if self.rect.right >= SIZE[0]:
            OCHKI[0] += 1
            sound_1.play()
            self.dx = -self.dx
            self.rect.right = SIZE[0]
        self.collide()
        self.rect.x += self.speed * self.dx
        self.rect.y += self.speed * self.dy


# Метод преждевременного выхода из игры
def terminate():
    pygame.quit()
    sys.exit()


# Метод первоначального экрана
def start_screen():
    intro_text_1 = ["Ping-Pong"]
    intro_text_2 = ["нажмите для того, чтобы начать игру"]
    fon = pygame.image.load("data/пинг-понг.jpg").convert()
    screen.blit(fon, (0, 0))
    text_coord = 50
    for line in intro_text_1:
        font = pygame.font.Font(None, 70)
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    for line in intro_text_2:
        font = pygame.font.Font(None, 34)
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 430
        intro_rect.top = text_coord
        intro_rect.x = 80
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:  # После нажатия на экран начать игру
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                sound_3.play()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


pygame.init()  # Инициализируем pygame

# Заводим переменные музыки
sound_1 = pygame.mixer.Sound('очки.mp3')
sound_2 = pygame.mixer.Sound('конец.mp3')
sound_3 = pygame.mixer.Sound('начало_игры.mp3')
sound_4 = pygame.mixer.Sound('выход.mp3')
sound_5 = pygame.mixer.Sound('начать_заново.mp3')
sound_6 = pygame.mixer.Sound('отталкивания.mp3')
sound_7 = pygame.mixer.Sound('вверх_вниз.mp3')


# Функция для вывода очков
def print_ochki():
    one = OCHKI[0]  # Кол-во очков первого игрока
    two = OCHKI[1]  # Кол-во очков второго игрока
    score = f'{one}:{two}'  # Строка, содержащая счет
    text_coord = 550  # Координата по y
    font = pygame.font.Font(None, 50)  # Шрифт
    score = font.render(score, 1, pygame.Color('white'))  # Текст на полотне
    intro_rect = score.get_rect()  # Прямоугольник полотна
    intro_rect.top = text_coord
    intro_rect.x = 265
    screen.blit(score, intro_rect)  # Приклеиваем полотно со счётом на основной


def the_true_end():
    general_font = pygame.font.Font(None, 70)  # Шрифт главной надписи
    font = pygame.font.Font(None, 50)  # Шрифт обычных надписей
    # Генерация главной надписи
    general_text = general_font.render('Игра окончена', 1, pygame.Color('orange'))
    # Текст Обычных надписей
    texts = ['Начать заново', 'Выйти из игры']
    # Генерация обычных надписей
    texts = [font.render(i, 1, pygame.Color('orange')) for i in texts]
    # Координаты обычных надписей соответственно
    coords = [[SIZE[0] // 100, SIZE[1] // 4 + SIZE[1] // 5],
              [SIZE[0] // 100, SIZE[1] // 4 + SIZE[1] // 5 * 2]]
    # Значение курсора
    cursor = 0
    # Координаты значений курсора
    cursor_coords = {0: [SIZE[0] // 2, SIZE[1] // 4 + SIZE[1] // 5 * 1.1],
                     1: [SIZE[0] // 2, SIZE[1] // 4 + SIZE[1] // 5 * 2.1]}
    # Главный цикл
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                # Если нажата клавиша "вверх" или "вниз", то значение курсора изменится
                if event.key == pygame.K_UP:
                    sound_4.play()
                    cursor -= 1
                if event.key == pygame.K_DOWN:
                    sound_4.play()
                    cursor += 1
                # Если нажата клавиша "Enter", то возвращаем значение курсора
                if event.key == pygame.K_RETURN:
                    if cursor > 0:
                        sound_4.play()
                        terminate()
                    return cursor
        # Не даём значению курсора стать меньше 0 или больше 1
        cursor = abs(cursor % 2)
        # Клеим фон
        screen.blit(fon, (0, 0))
        # Клеим главную наадпись
        screen.blit(general_text, (SIZE[0] // 5, 0))
        # Клеим обычные надписи
        for i in range(len(texts)):
            screen.blit(texts[i], coords[i])
        # Рисуем курсор
        pygame.draw.rect(screen, pygame.Color('orange'), [*cursor_coords[cursor], 70, 20])
        pygame.display.flip()
        clock.tick(FPS)


# Создаём окно с заданным размером
pygame.display.init()
screen = pygame.display.set_mode(SIZE)
# Даём программе имя
pygame.display.set_caption('Пинг понг')
run = True  # Переменная регулирования игрового цикла
clock = pygame.time.Clock()  # Счётчик кадров в секунду
start_screen()

platform_1 = Platform(0, SIZE[1] // 2)  # Расположение 1 платформы
platform_2 = Platform(SIZE[0] - 20, SIZE[1] // 2)  # Расположение 2 платформы
ball = Ball(300, 300)  # Размер шарика
up = down = False  # Создание булевых значений для движения платформы 1
up_1 = down_1 = False  # Создание булевых значений для движения платформы 1

fon = pygame.image.load("data/fon.jpg").convert()  # Загрузка фото фона во время игры

# Игровой цикл
while run:
    screen.blit(fon, (0, 0))  # Приклеиваем фон
    for event in pygame.event.get():  # Обработка событий
        if event.type == pygame.QUIT:  # Событие выхода из игры
            run = False
        if event.type == pygame.KEYDOWN:  # События нажатых кнопок
            if event.key == pygame.K_w:  # Событие нажатия кнопки "w"
                up_1 = True
                down_1 = False
            if event.key == pygame.K_s:  # Событие нажатия кнопки "s"
                down_1 = True
                up_1 = False
            if event.key == pygame.K_UP:  # Событие нажатия кнопки вверх
                up = True
                down = False
            if event.key == pygame.K_DOWN:  # Событие нажатия кнопки вниз
                down = True
                up = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:  # Событие нажатия кнопки "w"
                up_1 = False
            if event.key == pygame.K_s:  # Событие нажатия кнопки "s"
                down_1 = False
            if event.key == pygame.K_UP:  # Событие нажатия кнопки вверх
                up = False
            if event.key == pygame.K_DOWN:  # Событие нажатия кнопки вниз
                down = False
    PLATFORMS.draw(screen)  # Рисуем платформы
    platform_1.update_1(up_1, down_1)  # Вызываем метод движения для 1 платформы
    platform_2.update_1(up, down)  # Вызываем метод движения для 2 платформы
    pygame.draw.circle(screen, (255, 127, 80), ball.rect.center, ball.rect.width // sqrt(2))  # Риусем шарик
    print_ochki()  # Выводим кол-во очков
    ball.update()  # Вызываем метод движения шарика
    pygame.display.flip()  # Отрисовка кадра
    clock.tick(FPS)  # Работа со временем
    if OCHKI[0] == 3 or OCHKI[1] == 3:  # Условие для окончания раунда игры
        # Получаем значение курсора финального окна
        sound_2.play()  # Запуск мелодии
        choice = the_true_end()  # Запуск метода финального экрана
        if choice == 0:  # Начало игры заново
            sound_5.play()  # Запуск мелодии
            PLATFORMS = pygame.sprite.Group()  # Обновление группы спрайтов
            platform_1 = Platform(0, SIZE[1] // 2)  # Расположение платформы 1
            platform_2 = Platform(SIZE[0] - 20, SIZE[1] // 2)  # Расположение платформы 2
            ball = Ball(300, 300)  # Размер шарика
            PLATFORMS.draw(screen)  # Рисуем платформы
            platform_1.update_1(up, down)  # Вызываем метод движения для 1 платформы
            platform_2.update_1(up_1, down_1)  # Вызываем метод движения для 2 платформы
            pygame.draw.circle(screen, (255, 127, 80), ball.rect.center, ball.rect.width // sqrt(2))  # Риусем шарик
            print_ochki()  # Выводим кол-во очков
            ball.update()  # Вызываем метод движения шарика
            OCHKI[0] = OCHKI[1] = 0  # Обнуляем очки
            pygame.display.flip()  # Отрисовка кадра
            clock.tick(FPS)  # Работа со временем
pygame.quit()  # Закрываем pygame
terminate()  # Метод преждевременного выхода из игры

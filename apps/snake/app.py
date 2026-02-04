import pygame
import random
import os


def run(screen):

    pygame.init()
    clock = pygame.time.Clock()

    base_path = os.path.dirname(__file__)

    GRID_SIZE = 20
    GRID_WIDTH = 20
    GRID_HEIGHT = 20

    head_img = pygame.image.load(os.path.join(base_path, "head.png"))
    body1_img = pygame.image.load(os.path.join(base_path, "body1.jpg"))
    body_img = pygame.image.load(os.path.join(base_path, "body.jpg"))
    apple_img = pygame.image.load(os.path.join(base_path, "apple.png"))

    head_img = pygame.transform.scale(head_img, (GRID_SIZE, GRID_SIZE))
    body1_img = pygame.transform.scale(body1_img, (GRID_SIZE, GRID_SIZE))
    body_img = pygame.transform.scale(body_img, (GRID_SIZE, GRID_SIZE))
    apple_img = pygame.transform.scale(apple_img, (GRID_SIZE, GRID_SIZE))

    eat_sound = pygame.mixer.Sound(os.path.join(base_path, "1.wav"))
    game_over_sound = pygame.mixer.Sound(os.path.join(base_path, "2.wav"))

    # إعداد الثعبان والتفاحة
    snake = [[10, 10], [10, 11], [10, 12]]
    direction = [0, -1]  # يبدأ متجهاً للأعلى
    apple = [random.randint(0, GRID_WIDTH - 1),
             random.randint(0, GRID_HEIGHT - 1)]

    running = True
    while running:
        screen.fill((0, 0, 0))  # مسح الشاشة

        # رسم حدود مرئية حول مساحة اللعب
        border_color = (255, 255, 255)  # لون الحدود (أبيض)
        border_rect = pygame.Rect(0, 0, GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
        pygame.draw.rect(screen, border_color, border_rect, 2)  # سمك الحدود = 2 بكسل

        # معالجة الأحداث (الحركة والخروج)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP and direction != [0, 1]:
                    direction = [0, -1]
                elif event.key == pygame.K_DOWN and direction != [0, -1]:
                    direction = [0, 1]
                elif event.key == pygame.K_LEFT and direction != [1, 0]:
                    direction = [-1, 0]
                elif event.key == pygame.K_RIGHT and direction != [-1, 0]:
                    direction = [1, 0]

        # حساب موقع
        new_head = [snake[0][0] + direction[0],
                    snake[0][1] + direction[1]]

        # تحقق من الاصطدام
        if (new_head in snake or
                not (0 <= new_head[0] < GRID_WIDTH) or
                not (0 <= new_head[1] < GRID_HEIGHT)):
            game_over_sound.play()
            pygame.time.wait(1000)
            return
        else:
            snake.insert(0, new_head)

        # تحقق من أكل التفاحة
        if new_head == apple:
            eat_sound.play()
            apple = [random.randint(0, GRID_WIDTH - 1),
                     random.randint(0, GRID_HEIGHT - 1)]
        else:
            snake.pop()

        # رسم التفاحة
        screen.blit(apple_img, (apple[0] * GRID_SIZE, apple[1] * GRID_SIZE))

        # رسم الثعبان
        for i, segment in enumerate(snake):
            x, y = segment[0] * GRID_SIZE, segment[1] * GRID_SIZE
            if i == 0:
                screen.blit(head_img, (x, y))
            elif i == 1:
                screen.blit(body1_img, (x, y))
            else:
                screen.blit(body_img, (x, y))

        pygame.display.flip()
        clock.tick(10)  # سرعة اللعبة

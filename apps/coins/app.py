import pygame
import random
import os

def run(screen):
    pygame.init()
    clock = pygame.time.Clock()

    #  تحميل الصور
    player_run_imgs = [
        pygame.image.load(os.path.join(os.path.dirname(__file__), "player_run1.png")),
        pygame.image.load(os.path.join(os.path.dirname(__file__), "player_run2.png")),
    ]
    player_jump_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "player_jump.png"))
    background_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "background.png"))
    background_img = pygame.transform.scale(background_img, screen.get_size())

    #  تحميل الأصوات
    jump_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "1.wav"))
    collision_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "2.wav"))

    #  اللاعب
    player_rect = player_run_imgs[0].get_rect(midbottom=(100, screen.get_height() - 50))
    gravity = 0
    is_jumping = False
    animation_index = 0

    #  العقبات
    obstacles = []
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)  # كل 1.5 ثانية عقبة جديدة

    running = True
    while running:
        screen.blit(background_img, (0, 0))

        #  رسم اللاعب
        if is_jumping:
            screen.blit(player_jump_img, player_rect)
        else:
            screen.blit(player_run_imgs[animation_index // 10], player_rect)
            animation_index = (animation_index + 1) % 20

        #  رسم العقبات
        for obstacle in obstacles:
            pygame.draw.rect(screen, (200, 50, 50), obstacle)

        #  تحديث العقبات
        for obstacle in obstacles[:]:
            obstacle.x -= 5
            if obstacle.right < 0:
                obstacles.remove(obstacle)

        #  الاصطدام
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                collision_sound.play()
                game_over_text = pygame.font.SysFont("Arial", 50).render("Game Over", True, (255, 0, 0))
                screen.blit(game_over_text, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 25))
                pygame.display.flip()
                pygame.time.delay(2000)
                return

        #  الجاذبية
        gravity += 1
        player_rect.y += gravity
        if player_rect.bottom >= screen.get_height() - 50:
            player_rect.bottom = screen.get_height() - 50
            gravity = 0
            is_jumping = False

        # تحديث الشاشة
        pygame.display.flip()
        clock.tick(30)

        #  التحكم
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == obstacle_timer:
                obstacle_height = random.randint(20, 50)
                obstacle = pygame.Rect(screen.get_width(), screen.get_height() - 50 - obstacle_height, 20, obstacle_height)
                obstacles.append(obstacle)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    gravity = -20
                    is_jumping = True
                    jump_sound.play()
                elif event.key == pygame.K_ESCAPE:
                    return
  
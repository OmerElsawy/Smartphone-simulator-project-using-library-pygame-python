import pygame
import os

def run(screen):
    pygame.mixer.init()  # لتشغيل الصوت
    clock = pygame.time.Clock()
    running = True

    # قائمة الأغاني
    music_files = ["1.wav", "2.wav", "3.wav"]
    selected_index = 0 

    font = pygame.font.SysFont("Arial", 28)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()  # توقف أي موسيقى
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.mixer.music.stop()  # توقف الموسيقى عند الخروج
                elif event.key == pygame.K_UP:
                    if selected_index > 0:
                        selected_index -= 1
                elif event.key == pygame.K_DOWN:
                    if selected_index < len(music_files) - 1:
                        selected_index += 1
                elif event.key == pygame.K_RETURN:
                    # تشغيل الأغنية المحددة
                    music_path = os.path.join("assets/music", music_files[selected_index])
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.play()

        # رسم الشاشة
        screen.fill((20, 20, 20))
        title = font.render("Music Player", True, (255, 255, 255))
        screen.blit(title, (50, 30))

        # رسم قائمة الأغاني
        for idx, music in enumerate(music_files):
            color = (0, 255, 0) if idx == selected_index else (255, 255, 255)
            label = font.render(f"{idx + 1}. {music}", True, color)
            screen.blit(label, (50, 100 + idx * 50))

        pygame.display.flip()
        clock.tick(30)

import pygame

def run(screen):
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 35)
    user_input = ""
    result = ""
    running = True

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RETURN:
                    try:
                        result = str(eval(user_input))
                    except:
                        result = "Error"
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

        # رسم واجهة الحاسبة
        screen.fill((0, 0, 0))
        text_surface = font.render(user_input, True, (0, 255, 0))
        result_surface = font.render(result, True, (255, 255, 255))
        screen.blit(text_surface, (10, 50))
        screen.blit(result_surface, (10, 150))
        pygame.display.flip()

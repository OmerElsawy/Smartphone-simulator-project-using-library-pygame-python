import pygame
import time

class LockScreen:
    def __init__(self, screen, password="omer2025"):
        self.screen = screen
        self.password = password  # كلمة المرور الصحيحة
        self.input_text = ""  # النص المدخل من المستخدم
        self.font = pygame.font.SysFont("Arial", 28)  # الخط الرئيسي
        self.clock_font = pygame.font.SysFont("Arial", 24)  # الخط المستخدم للساعة
        self.error_font = pygame.font.SysFont("Arial", 20)  # الخط لرسالة الخطأ

        # تحميل الأصوات
        self.key_sound = pygame.mixer.Sound("assets/sounds/key.wav")  # صوت عند كتابة حرف
        self.success_sound = pygame.mixer.Sound("assets/sounds/unlock.wav")  # صوت فتح القفل
        self.error_sound = pygame.mixer.Sound("assets/sounds/error.wav")  # صوت كلمة مرور خاطئة

        # تحميل الخلفية
        self.background = pygame.image.load("assets/backgrounds/lock_screen.jpg")
        self.background = pygame.transform.scale(self.background, screen.get_size())

        self.error_message = ""  # رسالة الخطأ عند إدخال كلمة مرور خاطئة

    def draw_clock(self):
        """عرض الساعة أعلى منتصف الشاشة"""
        current_time = time.strftime("%H:%M")
        clock_surface = self.clock_font.render(current_time, True, (255, 255, 255))
        clock_rect = clock_surface.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(clock_surface, clock_rect)

    def draw(self):
        """رسم شاشة القفل"""
        self.screen.fill((0, 0, 0))  # مسح الشاشة بلون أسود
        self.screen.blit(self.background, (0, 0))  # رسم الخلفية
        self.draw_clock()  # رسم الساعة

        # رسم مربع إدخال كلمة المرور
        box_width = 300
        box_height = 50
        box_x = (self.screen.get_width() - box_width) // 2
        box_y = self.screen.get_height() // 2

        pygame.draw.rect(self.screen, (50, 50, 50), (box_x, box_y, box_width, box_height), border_radius=10)  # خلفية المربع
        pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2, border_radius=10)  # الإطار

        # إظهار كلمة المرور المدخلة كنجوم
        hidden_text = "*" * len(self.input_text)
        text_surface = self.font.render(hidden_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, box_y + box_height // 2))
        self.screen.blit(text_surface, text_rect)

        # عرض رسالة الخطأ إن وجدت
        if self.error_message:
            error_surface = self.error_font.render(self.error_message, True, (255, 0, 0))
            error_rect = error_surface.get_rect(center=(self.screen.get_width() // 2, box_y + box_height + 30))
            self.screen.blit(error_surface, error_rect)

    def run(self):
        """تشغيل شاشة القفل"""
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # إغلاق البرنامج
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # التحقق عند الضغط على Enter
                        if self.input_text == self.password:
                            self.success_sound.play()
                            return True  # كلمة المرور صحيحة، الدخول
                        else:
                            self.error_sound.play()
                            self.error_message = "❌ Incorrect password"
                            self.input_text = ""  # إعادة تعيين النص
                    elif event.key == pygame.K_BACKSPACE:  # حذف آخر حرف
                        self.input_text = self.input_text[:-1]
                    elif len(self.input_text) < 12:  # الحد الأقصى للأحرف
                        if event.unicode.isprintable():
                            self.key_sound.play()
                            self.input_text += event.unicode

            self.draw()
            pygame.display.flip()
            clock.tick(30)  # تحديث الشاشة 30 مرة في الثانية

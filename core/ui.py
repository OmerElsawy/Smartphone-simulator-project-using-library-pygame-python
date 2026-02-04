import pygame
import time

class HomeScreen:
    def __init__(self, screen, app_manager):
        self.screen = screen  # الشاشة الرئيسية التي نرسم عليها
        self.app_manager = app_manager  # لإدارة التطبيقات عند فتحها
        self.font = pygame.font.SysFont("Arial", 20)  # الخط المستخدم للنصوص
        self.clock_font = pygame.font.SysFont("Arial", 24)  # الخط المستخدم للساعة
        self.background = pygame.image.load("assets/backgrounds/home_screen.jpg")  # تحميل خلفية الشاشة
        self.background = pygame.transform.scale(self.background, screen.get_size())  # ضبط حجم الخلفية

        # الأصوات
        self.move_sound = pygame.mixer.Sound("assets/sounds/move.wav")  # صوت التنقل بين التطبيقات
        self.open_sound = pygame.mixer.Sound("assets/sounds/open.wav")  # صوت فتح التطبيق

        # قائمة التطبيقات الموجودة على الشاشة الرئيسية
        self.apps = [
            {"name": "Snake", "icon": "assets/icons/snake.png", "module": "apps.snake.app"},
            {"name": "Calculator", "icon": "assets/icons/calculator.png", "module": "apps.calculator.app"},
            {"name": "Messages", "icon": "assets/icons/messages.png", "module": "apps.messages.app"},
            {"name": "YouTube", "icon": "assets/icons/youtube.png", "module": "apps.youtube.app"},
            {"name": "Music", "icon": "assets/icons/music.png", "module": "apps.music.app"},
            {"name": "Mu App", "icon": "assets/icons/mu_app.png", "module": "apps.mu_app.app"},
            {"name": "jump", "icon": "assets/icons/coins.png", "module": "apps.coins.app"}
        ]

        # تحميل الأيقونات لكل تطبيق
        for app in self.apps:
            app["icon_img"] = pygame.image.load(app["icon"])

        self.selected_index = 0  # التطبيق المحدد حاليًا
        self.grid_cols = 3       # عدد الأعمدة في شبكة التطبيقات

    def draw_clock(self):
        current_time = time.strftime("%H:%M")  # الوقت الحالي (ساعة:دقيقة)
        clock_surface = self.clock_font.render(current_time, True, (255, 255, 255))  # نص الساعة باللون الأبيض
        self.screen.blit(clock_surface, (self.screen.get_width() - 80, 10))  # وضع الساعة في أعلى يمين الشاشة

    def draw(self):
       
        self.screen.fill((0, 0, 0))  # مسح الشاشة بلون أسود قبل الرسم
        self.screen.blit(self.background, (0, 0))  # رسم الخلفية
        self.draw_clock()  # رسم الساعة في الزاوية

        # إعدادات شبكة التطبيقات
        padding = 30      # المسافة بين الأيقونات
        icon_size = 64    # حجم الأيقونة
        start_x = 50      # بداية رسم الأيقونات في المحور X
        start_y = 100     # بداية رسم الأيقونات في المحور Y

        # رسم جميع التطبيقات
        for idx, app in enumerate(self.apps):
            row = idx // self.grid_cols  # حساب الصف
            col = idx % self.grid_cols   # حساب العمود
            x = start_x + col * (icon_size + padding)  # حساب إحداثيات X لكل أيقونة
            y = start_y + row * (icon_size + 50)       # حساب إحداثيات Y لكل أيقونة

            # تكبير الأيقونة إلى الحجم المطلوب
            icon_img = pygame.transform.scale(app["icon_img"], (icon_size, icon_size))
            self.screen.blit(icon_img, (x, y))  # رسم الأيقونة

            # كتابة اسم التطبيق أسفل الأيقونة
            label = self.font.render(app["name"], True, (255, 255, 255))  # النص باللون الأبيض
            label_rect = label.get_rect(center=(x + icon_size / 2, y + icon_size + 15))  # ضبط النص في الوسط
            self.screen.blit(label, label_rect)  # رسم اسم التطبيق

            # إذا كان التطبيق هو المحدد حالي
            if idx == self.selected_index:
                pygame.draw.rect(self.screen, (0, 255, 0), (x - 5, y - 5, icon_size + 10, icon_size + 10), 2)

    def run(self):
     
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # الخروج من التطبيق
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False  # العودة إلى شاشة القفل
                    elif event.key == pygame.K_RETURN:
                        # تشغيل التطبيق المحدد عند الضغط على Enter
                        self.open_sound.play()  # تشغيل صوت فتح التطبيق
                        selected_app = self.apps[self.selected_index]
                        self.app_manager.launch_app(selected_app["module"])
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        prev_index = self.selected_index
                        if event.key == pygame.K_LEFT and self.selected_index > 0:
                            self.selected_index -= 1
                        elif event.key == pygame.K_RIGHT and self.selected_index < len(self.apps) - 1:
                            self.selected_index += 1
                        elif event.key == pygame.K_UP and self.selected_index - self.grid_cols >= 0:
                            self.selected_index -= self.grid_cols
                        elif event.key == pygame.K_DOWN and self.selected_index + self.grid_cols < len(self.apps):
                            self.selected_index += self.grid_cols
                        if self.selected_index != prev_index:
                            self.move_sound.play()  # تشغيل صوت عند تحريك المؤشر

            self.draw()  # إعادة رسم الشاشة بعد كل حدث
            pygame.display.flip()  # تحديث الشاشة
            clock.tick(30)  # ضبط التحديث على 30 إطارًا في الثانية

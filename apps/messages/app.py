import pygame
import threading
import telebot

#  توكن البوت من BotFather
BOT_TOKEN = "هنا الصق التكون "

#  قائمة الرسائل
messages = []

#  تليجرام بوت
bot = telebot.TeleBot(BOT_TOKEN)

#  تخزين آخر مستخدم لتسهيل الرد عليه
last_sender_chat_id = None

def start_telegram_listener():
    """🎧 استقبال الرسائل من التليجرام"""
    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        global last_sender_chat_id
        # حفظ chat_id للرد لاحقًا
        last_sender_chat_id = message.chat.id
        # إضافة الرسالة للقائمة
        messages.append((message.from_user.first_name, message.text, "received"))

    bot.polling(non_stop=True)

def run(screen):
    pygame.display.set_caption(" Messages")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20)

    # مربع كتابة الرسائل
    input_box = pygame.Rect(10, 430, 380, 32)
    color_inactive = pygame.Color('gray40')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    #  بدء الاستماع للرسائل في Thread منفصل
    threading.Thread(target=start_telegram_listener, daemon=True).start()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                # التبديل بين حالة مربع النص
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text.strip() != "":
                            # إضافة الرسالة المرسلة للقائمة
                            messages.append(("You", text, "sent"))
                            if last_sender_chat_id:
                                # إرسال الرد إلى آخر مرسل
                                bot.send_message(last_sender_chat_id, text)
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                if event.key == pygame.K_ESCAPE:
                    done = True

        #  رسم واجهة الرسائل
        screen.fill((30, 30, 30))  # خلفية غامقة

        #  رسم شريط أعلى الشاشة
        pygame.draw.rect(screen, (50, 50, 50), (0, 0, 400, 40))
        header_text = font.render("📱 Messages", True, (255, 255, 255))
        screen.blit(header_text, (10, 10))

        #  رسم الرسائل (فقاعات)
        y = 50
        for name, msg, msg_type in messages[-12:]:  # عرض آخر 12 رسالة فقط
            if msg_type == "received":
                bubble_color = (60, 60, 200)  # أزرق للرسائل المستلمة
                align = 10
            else:
                bubble_color = (0, 150, 0)    # أخضر للرسائل المرسلة
                align = 400 - 210

            # رسم الفقاعة
            pygame.draw.rect(screen, bubble_color, (align, y, 200, 30), border_radius=8)
            msg_surface = font.render(f"{name}: {msg}", True, (255, 255, 255))
            screen.blit(msg_surface, (align + 5, y + 5))
            y += 35

        #  رسم مربع الإدخال
        pygame.draw.rect(screen, (50, 50, 50), input_box, border_radius=6)
        txt_surface = font.render(text, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2, border_radius=6)

        pygame.display.flip()
        clock.tick(30)

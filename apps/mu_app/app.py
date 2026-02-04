import webview

def run(screen):
    # فتح موقع Mu App داخل نافذة مدمجة
    webview.create_window("Mu App", "https://disteducation.mashreq.edu.sd/login/index.php", width=400, height=700)
    webview.start()

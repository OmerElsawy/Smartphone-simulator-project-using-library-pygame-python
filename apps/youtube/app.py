import webview

def run(screen):
    # فتح موقع YouTube داخل نافذة مدمجة
    webview.create_window("YouTube", "https://www.youtube.com", width=400, height=700)
    webview.start()

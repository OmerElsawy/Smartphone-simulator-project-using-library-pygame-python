import importlib

class AppManager:
    def __init__(self, screen):
        self.screen = screen

    def launch_app(self, module_name):
        try:
            app_module = importlib.import_module(module_name)
            app_module.run(self.screen)
        except Exception as e:
            print(f"❌ Error loading {module_name}: {e}")

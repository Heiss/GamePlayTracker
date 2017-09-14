import threading
import pystray
from PIL import Image, ImageDraw

def thread_callback(icon):
        icon.visible = True

class IconTray(threading.Thread):
    icon = None
    root = None
    app = None

    def __init__(self, root, app):
        threading.Thread.__init__(self)

        self.root = root
        self.app = app

        self.setup_trayicon()

    def run(self):
        self.icon.run(thread_callback)
        print("done")

    def stop(self):
        self.icon.stop()

    def setup_trayicon(self):
        self.icon = pystray.Icon('GameTime Tracker Tray Icon')
        self.icon.icon = self.create_image()
        self.icon.Menu = pystray.Menu(
            pystray.MenuItem("Show window", self.show_window(), default=True))
            #pystray.MenuItem("Exit program", self.close_window()))
        self.icon.HAS_MENU = True
        self.icon.HAS_DEFAULT_ACTION = True

        self.icon.update_menu()

    def show_window(self):
        print("show")
        self.root.deiconify()

    def close_window(self):
        print("close")
        #self.app.destroy_application()

    def create_image(self):
        # Generate an image and draw a pattern
        image = Image.new('RGB', (32, 32), (200, 200, 200))
        dc = ImageDraw.Draw(image)
        dc.rectangle((32 // 2, 0, 32, 32 // 2), fill=(200, 200, 200))
        dc.rectangle((0, 32 // 2, 32 // 2, 32), fill=(200, 200, 200))

        return image
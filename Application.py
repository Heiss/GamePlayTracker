import tkinter as tk
from ProcessSearcher import ProcessSearcher
import sys
import pystray
from IconTray import IconTray

class Application(tk.Frame):
    ps = None
    icontray = None

    def __init__(self, master=None):
        super().__init__(master)

        #set custom close method
        master.protocol("WM_DELETE_WINDOW", self.destroy_application)

        self.pack()
        self.create_menu()
        self.create_widgets()

        self.ps = ProcessSearcher()
        self.ps.set_label(self.label_playtime)
        self.ps.start()

        self.icontray = IconTray(master, self)
        self.icontray.start()

    def destroy_application(self):
        self.ps.stop_loop()
        self.icontray.stop()

        self.ps.join()
        self.icontray.join()

        root.destroy()
        sys.exit()

    def minimize_window(self):
        self.master.iconify()

    def minimize_window_to_tray(self):
        pass

    def create_widgets(self):
        self.quit = tk.Button(
            self, text="QUIT", fg="red", command=self.destroy_application)
        self.quit.pack(side="bottom")

        self.label_playtime = tk.Label(self)
        self.label_playtime["text"] = "Placeholder"
        self.label_playtime.pack(side="top")

    def create_menu(self):
        menubar = tk.Menu(root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(
            label="Import playtime from raptr", command=self.say_hi)
        filemenu.add_command(label="Export playtime", command=self.say_hi)
        filemenu.add_separator()
        filemenu.add_command(label="Minimize to tray", command=self.minimize_window)
        filemenu.add_command(
            label="Close program", command=self.destroy_application)
        menubar.add_cascade(label="File", menu=filemenu)

        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Show statistics", command=self.say_hi)
        viewmenu.add_command(label="Show tracked games", command=self.say_hi)
        menubar.add_cascade(label="View", menu=viewmenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.say_hi)
        helpmenu.add_command(label="Update", command=self.say_hi)
        menubar.add_cascade(label="Help", menu=helpmenu)

        root.config(menu=menubar)

    def say_hi(self):
        print("hi there, everyone!")

def setup_window():
    global root, app

    root = tk.Tk()

    app = Application(master=root)
    app.master.title("GameTime Tracker")

    app.mainloop()


if __name__ == '__main__':
    setup_window()
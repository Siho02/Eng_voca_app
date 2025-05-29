# main.py
import tkinter as tk
from ui.home_screen import HomeScreen
from ui.register_screen import RegisterScreen
from ui.register_manual import RegisterManualScreen
from ui.register_csv import RegisterCSVScreen
from ui.word_list import WordListScreen

class MyVocaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #1. window setting
        self.title("My Voca App")
        self.geometry("480x700")  # 모바일 비율 느낌의 화면 크기

        # 전체 레이아웃
        self.container_frame = tk.Frame(self)
        self.container_frame.pack(fill="both", expand=True)

        self.container = tk.Frame(self.container_frame)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.nav_frame = tk.Frame(self, bg="lightgreen", height=50)
        self.nav_frame.pack(side="bottom", fill="x")

        #화면 등록
        self.screens = {}

        self.create_screens()
        self.create_navigation()
        self.show_screen("home")

    def create_screens(self):
        self.screens['home'] = HomeScreen(self.container, self)
        self.screens["register"] = RegisterScreen(self.container, self)
        self.screens["manual"] = RegisterManualScreen(self.container, self)
        self.screens["csv"] = RegisterCSVScreen(self.container, self)
        self.screens["word_list"] = WordListScreen(self.container, self)

        for screen in self.screens.values():
            screen.grid(row = 0, column = 0, sticky = 'nsew') 

    def show_screen(self, name):
        if name in self.screens:
            self.screens[name].tkraise()
        else:
            print(f"[Error] 화면 '{name}' 이(가) 존재하지 않아요!")

    def create_navigation(self):
        tk.Button(self.nav_frame, text="Home", bg="lightgreen", command=lambda: self.show_screen("home")).pack(side="left", expand=True, fill="x")
        tk.Button(self.nav_frame, text="Setting", bg="lightgreen", command=lambda: print("[TODO] Setting 페이지 연결 예정")).pack(side="left", expand=True, fill="x")


if __name__ == "__main__":
    app = MyVocaApp()
    app.mainloop()
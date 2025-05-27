import tkinter as tk

class RegisterScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="📋 단어 등록", font=("Arial", 20), bg="white").pack(pady=20)

        btn_style = {"bg": "orange", "fg": "white", "width": 30, "height": 2, "font": ("Arial", 12)}
        tk.Button(self, text="Register Manually", command=lambda: controller.show_screen("manual"), **btn_style).pack(pady=10)
        tk.Button(self, text="Register with CSV", command=lambda: controller.show_screen("csv"), **btn_style).pack(pady=10)

        tk.Button(self, text="← 홈으로", command=lambda: controller.show_screen("home")).pack(pady=20)

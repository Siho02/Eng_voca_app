import tkinter as tk

class RegisterCSVScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="📂 CSV 단어 등록 (구현 예정)", font=("Arial", 16), bg="white").pack(pady=20)
        tk.Button(self, text="← 뒤로", command=lambda: controller.show_screen("register")).pack(pady=10)
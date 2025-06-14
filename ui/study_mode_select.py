import tkinter as tk

class StudyModeSelect(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg = 'white')

        tk.Label(self, text='어떻게 공부해볼까요?', font = ('Arial',24), bg = "white").pack(pady=20)

        btn_style = {"width": 20, "height": 2, "bg": "white", "highlightbackground": "darkred"}

        tk.Button(self, text="영어 → 한국어", command=lambda: controller.show_study_screen("eng_to_kor"), **btn_style).pack(pady=10)
        tk.Button(self, text="한국어 → 영어", command=lambda: controller.show_study_screen("kor_to_eng"), **btn_style).pack(pady=10)

        tk.Button(self, text="← 홈으로", command=lambda: controller.show_screen("home")).pack(pady=20)
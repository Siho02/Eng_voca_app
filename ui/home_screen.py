import tkinter as tk

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="📘 단어장", font=("Arial", 24), bg="white").pack(pady=20)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=20)

        btn_style = {"bg": "orange", "fg": "white", "width": 25, "height": 2, "font": ("Arial", 12)}
        tk.Button(btn_frame, text="단어 등록하러 가기", command=lambda: controller.show_screen("register"), **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="단어 전체 보기", command=lambda: controller.show_screen('word_list'), **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="단어 공부하러 가기", **btn_style).pack(pady=5)

        record_frame = tk.Frame(self, bg="lightgray", width=400, height=200)
        record_frame.pack(pady=20)
        record_frame.pack_propagate(False)

        tk.Label(record_frame, text="📊 학습 기록 요약 (예시)", bg="lightgray", font=("Arial", 12)).pack(pady=10)
        tk.Label(record_frame, text="오늘 공부한 단어: 5개\n복습한 단어: 3개\n연속 학습일: 2일", bg="lightgray").pack()

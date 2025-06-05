import tkinter as tk
from datetime import datetime, timedelta
import os 
import json
from ui.calendar_view import StudyCalendar

DATA_PATH = "data/words.json"

def calculate_study_summary(words_data):
    today = datetime.now().date()  
    studied_today = 0
    reviewed_today = 0
    reviewed_dates = set()

    for entry in words_data:
        last_reviewed = entry.get('last_reviewed')
        if last_reviewed:
            reviewed_date = datetime.strptime(last_reviewed, "%Y-%m-%d %H:%M").date()
            reviewed_dates.add(reviewed_date)
            if reviewed_date == today:
                studied_today += 1
                if entry.get('correct_cnt', 0) > 0 or entry.get("incorrect_cnt", 0) > 0:
                    reviewed_today += 1

    # 연속 학습일
    streak = 0
    current_day = today
    while current_day in reviewed_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return studied_today, reviewed_today, streak 


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        #self.configure(bg="white")

        tk.Label(self, text="📘 단어장", font=("Arial", 24), bg="white").pack(pady=20)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=10)

        btn_style = {"bg": "orange", "fg": "white", "width": 25, "height": 2, "font": ("Arial", 12)}
        tk.Button(btn_frame, text="단어 등록하러 가기", command=lambda: controller.show_screen("register"), **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="단어 전체 보기", command=lambda: controller.show_screen('word_list'), **btn_style).pack(pady=5)
        tk.Button(btn_frame, text="단어 공부하러 가기", command = lambda: controller.show_screen('study'),**btn_style).pack(pady=5)

        # ✅ 홈화면에 달력 뷰 바로 배치
        self.calendar_frame = StudyCalendar(self, controller)
        self.calendar_frame.pack(pady=10)

        # 오늘의 학습 요약
        record_frame = tk.Frame(self, bg="lightgray", width=400, height=200)
        record_frame.pack(pady=20)
        record_frame.pack_propagate(False)

        #tk.Button(btn_frame, text="📅 학습 달력 보기", command=lambda: controller.show_screen("calendar"), **btn_style).pack(pady=5)

        self.summary_label = tk.Label(self, text="", bg='lightgray', font = ('Arial', 12))
        self.summary_label.pack(pady=10)
        self.update_summary()
    
    def update_summary(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                try:
                    word_data = json.load(f)
                except json.JSONDecodeError:
                    word_data = []
        else:
            word_data = []

        studied, reviewed, streak = calculate_study_summary(word_data)
        if streak >= 3:
            self.summary_label.config(
                text=f"오늘 공부한 단어: {studied}개\n복습한 단어: {reviewed}개\n연속 학습일: {streak}일"
            )
        else:
            self.summary_label.config(
                text="3일 이상 공부하면 학습 기록이 표시됩니다."
            ) 

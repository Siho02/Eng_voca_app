import tkinter as tk
from tkcalendar import Calendar
import json
import os
from datetime import datetime

DATA_PATH = "data/study_log.json"

class StudyCalendar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        #self.pack()

        tk.Label(self, text="📅 학습 달력", font=("Arial", 20)).pack(pady=10)

        # 캘린더 생성
        self.cal = Calendar(self, selectmode="day", year=datetime.now().year,
                            month=datetime.now().month, date_pattern="yyyy-mm-dd")
        self.cal.pack(pady=10)

        # 공부 기록 불러오기
        self.load_study_data()

        # 홈으로 버튼
        tk.Button(self, text="← 홈으로", command=lambda: controller.show_screen("home")).pack(pady=10)

    def load_study_data(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                log_data = json.load(f)
        else:
            log_data = {}

        # 공부한 날짜에 배경색 설정
        for date_str, info in log_data.items():
            if info.get("studied_word_count", 0) > 0:
                # 예: 파란색으로 배경 강조
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                self.cal.calevent_create(date_obj, "공부함", "study")
                self.cal.tag_config("study", background="lightblue")

# 예시로 Tkinter 단독 실행 테스트
if __name__ == "__main__":
    root = tk.Tk()
    StudyCalendar(root, None)
    root.mainloop()

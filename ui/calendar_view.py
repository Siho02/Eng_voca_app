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
        self.cal.bind("<<CalendarSelected>>", self.on_date_click)

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
    
    def on_date_click(self, event):
        selected_date = self.cal.get_date()  # 문자열 "YYYY-MM-DD"
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            log_data = json.load(f)

        info = log_data.get(selected_date)
        if info:
            details = (
                f"날짜: {selected_date}\n"
                f"공부한 단어 수: {info.get('studied_word_count', 0)}\n"
                f"등록한 단어 수: {info.get('registered_word_count', 0)}\n"
                f"삭제한 단어 수: {info.get('deleted_word_count', 0)}\n"
                f"맞춘 개수: {info.get('correct_count', 0)}\n"
                f"틀린 개수: {info.get('incorrect_count', 0)}\n"
                f"공부 시간(분): {info.get('study_minutes', 0)}"
            )
            tk.messagebox.showinfo("공부 기록 상세", details)
        else:
            tk.messagebox.showinfo("공부 기록 상세", "이 날은 공부 기록이 없습니다.")
            
# 예시로 Tkinter 단독 실행 테스트
if __name__ == "__main__":
    root = tk.Tk()
    StudyCalendar(root, None)
    root.mainloop()

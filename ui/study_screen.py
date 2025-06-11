import tkinter as tk
import random
import json
import os
import time 
from datetime import datetime, timedelta
import math
from study_log import update_study_log

DATA_PATH = "data/words.json"

def calculate_after_min(cor, inc):
    total = cor + inc 

    #처음 복습은 무조건 3시간 후에
    if total==0: return 180

    acc = cor / total
    log_factor = math.log(total+1)
    acc_adj = (2*acc) - 1 #정답률이 0.5보다 작으면 음수가 나옴
    
    after_min = 180 * log_factor * (1 + acc_adj)

    #15번 이상 복습하면 복습 주기를 좀 더 길게 해줍니다.
    if total >= 20:
        after_min *= 1.2

    after_min = max(3, min(after_min, 43200))
    return after_min

class StudyScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")        

        #공부 시작 시간 기록 
        self.start_study()

        tk.Label(self, text="🎯 단어 퀴즈", font=('Arial', 20), bg='white').pack(pady=10)
        self.question_label = tk.Label(self, text='', font=('Arial', 15), bg='white')
        self.question_label.pack(pady=15)

        #보기 버튼
        self.option_buttons = []
        for _ in range(4):
            btn = tk.Button(self, text='', width=30, height=2, command=lambda b=_: self.check_answer(b))
            btn.pack(pady=5)
            self.option_buttons.append(btn)
        
        #결과 표시 라벨
        self.feedback_label = tk.Label(self, text='', font=('Arial', 12), bg='white', fg='blue')
        self.feedback_label.pack(pady=10)

        #다음 문제 버튼
        tk.Button(self, text='다음 문제', command=self.next_question).pack(pady=10)

        # 홈으로 돌아가기
        tk.Button(self, text="← 홈으로", command=self.go_home).pack(pady=10)

        # 단어 데이터 불러오기
        self.load_data()
        self.current_answer = None

        # 첫 문제 출제
        self.next_question()

    def load_data(self):
        # ✅ words.json에서 단어들을 불러옴
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                try:
                    self.word_data = json.load(f)
                except json.JSONDecodeError:
                    self.word_data = []
        else:
            self.word_data = []

    def next_question(self):
        self.clear_subjective_widgets()

        self.feedback_label.config(text="")
        now = datetime.now() 

        # 복습 가능한 단어 필터링
        reviewable_words = [] 
        
        for entry in self.word_data:
            next_review_str = entry.get('next_review')
            if next_review_str:
                next_review_dt = datetime.strptime(next_review_str, '%Y-%m-%d %H:%M')
                if now >= next_review_dt:
                    reviewable_words.append(entry)
        
        # 복습할 단어가 없으면 안내
        if len(reviewable_words) == 0:
            self.question_label.config(text='🥳복습을 모두 마쳤습니다.')
            for btn in self.option_buttons:
                btn.config(text='', state='disabled')
            return 

        #문제 단어 선택
        self.quiz_word = random.choice(reviewable_words)

        #주관식 모드 전환 조건
        cor = self.quiz_word.get("correct_cnt", 0)
        inc = self.quiz_word.get("incorrect_cnt", 0)
        total = cor + inc
        accuracy = cor / total if total > 0 else 0

        #복습횟수(total)이 20 초과이고, accuracy > 0.85 이상이면 주관식으로 전환
        if total > 20 and accuracy >= 0.85:
            self.quiz_word['mode'] = 'subjective'
        else:
            self.quiz_word['mode'] = 'objective'
        
        if self.quiz_word['mode'] == 'objective':
            self.show_objective_question()
        else:
            self.show_subjective_question()

    def show_objective_question(self):
        correct_meaning = random.choice(self.quiz_word['meaning'])
        self.current_answer = correct_meaning

        other_meanings = [m for e in self.word_data if e!=self.quiz_word for m in e.get("meaning", [])]
        wrong_choices = random.sample(other_meanings, 3) if len(other_meanings) >= 3 else other_meanings
        options = wrong_choices + [correct_meaning]
        random.shuffle(options)

        self.question_label.config(text=f"'{self.quiz_word['word']}'의 뜻은?")
        for i, option in enumerate(options):
            self.option_buttons[i].config(text=option, state="normal")

    def show_subjective_question(self):
        self.question_label.config(text=f"'{self.quiz_word['word']}'의 뜻을 입력하세요:")
        self.entry_answer = tk.Entry(self, width=30)
        self.entry_answer.pack(pady=5)
        self.submit_btn = tk.Button(self, text="제출", command=self.check_subjective_answer)
        self.submit_btn.pack(pady=5)
        for btn in self.option_buttons:
            btn.pack_forget()  # 객관식 버튼 숨김
    
    

    def check_answer(self, selected_index):
        selected_text = self.option_buttons[selected_index].cget("text")
        correct = selected_text == self.current_answer

        if correct: 
            self.feedback_label.config(text="✅ 정답입니다!", fg="green")
            self.quiz_word["correct_cnt"] += 1
            update_study_log("study", correct=True)
        else:
            self.feedback_label.config(text=f"❌ 오답입니다. 정답: {self.current_answer}", fg="red")
            self.quiz_word["incorrect_cnt"] += 1
            update_study_log("study", incorrect=True)

        # ✅ 복습한 시간과 다음 복습일 갱신
        self.update_review_schedule()

        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self.word_data, f, ensure_ascii=False, indent=2)

        for btn in self.option_buttons:
            btn.config(state="disabled")

    def check_subjective_answer(self):
        user_answer = self.entry_answer.get().strip()
        correct_meanings = [m.replace(" ", "") for m in self.quiz_word["meaning"]]
        
        user_input = user_answer.replace(" ", "")

        if user_input in correct_meanings:
            self.feedback_label.config(text="✅ 정답입니다!", fg="green")
            self.quiz_word["correct_cnt"] += 1
            update_study_log("study", correct=True)
        else:
            self.feedback_label.config(text=f"❌ 오답입니다. 정답: {correct_meanings}", fg="red")
            self.quiz_word["incorrect_cnt"] += 1
            update_study_log("study", incorrect=True)
        
        self.update_review_schedule()
        
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(self.word_data, f, ensure_ascii=False, indent=2)

        self.entry_answer.destroy()
        self.submit_btn.destroy()
    
    def update_review_schedule(self):
        now = datetime.now()
        self.quiz_word["last_reviewed"] = now.strftime("%Y-%m-%d %H:%M")
        cor = self.quiz_word["correct_cnt"]
        inc = self.quiz_word["incorrect_cnt"]
        after_min = calculate_after_min(cor, inc)
        next_review_dt = now + timedelta(minutes=after_min)
        self.quiz_word["next_review"] = next_review_dt.strftime("%Y-%m-%d %H:%M")

    def clear_subjective_widgets(self):
        if hasattr(self, "entry_answer"):
            self.entry_answer.destroy()
        if hasattr(self, "submit_btn"):
            self.submit_btn.destroy()
        for btn in self.option_buttons:
            btn.pack(pady=5)
    
    def go_home(self):
        study_end_time = datetime.now().strftime("%H:%M")
        update_study_log("study", session_time=(self.study_start_time, study_end_time))
        self.controller.show_screen("home")

    def start_study(self):
        self.study_start_time = datetime.now().strftime("%H:%M")
        print(f"공부 시작 시간 : {self.study_start_time}")

    
    
        
    
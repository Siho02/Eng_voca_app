import tkinter as tk
import random
import json
import os
import time 
from datetime import datetime, timedelta
import math

DATA_PATH = "data/words.json"

class StudyScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")
        
        tk.Label(self, text="🎯 단어 퀴즈", font=('Arial', 20), bg='white').pack(pady=10)

        #문제 영역
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
        tk.Button(self, text="← 홈으로", command=lambda: controller.show_screen("home")).pack(pady=10)

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
    def calculate_after_min(cor, inc):
        total = cor + inc
        
        #처음 복습은 무조건 3시간 후에
        if total==0: return 180

        acc = cor / total
        log_factor = math.log(total+1)
        acc_adj = (2*acc) - 1 #정답률이 0.5보다 작으면 음수가 나옴
        
        after_min = 180 * log_factor * (1 + acc_adj)

        #15번 이상 복습하면 복습 주기를 좀 더 길게 해줍니다.
        if total >= 15:
            after_min *= 1.2

        after_min = max(3, min(after_min, 43200))
        return after_min

    def next_question(self):
        self.feedback_label.config(text='') #??
        if len(self.word_data) < 4:
            self.question_label.config(text='최소 4개 이상의 단어가 있어야 퀴즈를 시작할 수 있어요.')
            for btn in self.option_buttons:
                btn.config(text='', state='disabled')
            return 

        self.quiz_word = random.choice(self.word_data)
        correct_meaning = random.choice(self.quiz_word['meaning'])
        self.current_answer = correct_meaning

        #오답 추출
        other_meanings= []
        for entry in self.word_data:
            if entry != self.quiz_word:
                other_meanings.extend(entry.get('meaning', []))
        
        wrong_choices = random.sample(other_meanings, 3)
        options = wrong_choices + [correct_meaning]
        random.shuffle(options)

        self.question_label.config(text=f"'{self.quiz_word['word']}'의 뜻은?")
        for i, option in enumerate(options):
            self.option_buttons[i].config(text=option, state="normal")


    def check_answer(self, selected_index):
        selected_text = self.option_buttons[selected_index].cget("text")
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        print(now_str)
        if selected_text == self.current_answer:
            self.feedback_label.config(text="✅ 정답입니다!", fg="green")
            self.quiz_word['correct_cnt'] += 1
        else:
            self.feedback_label.config(text=f"❌ 오답입니다. 정답: {self.current_answer}", fg="red")
            self.quiz_word['incorrect_cnt'] += 1
        
        # last_reivews 
        self.quiz_word['last_reviewed'] = now_str

        # next_review
        correct = self.quiz_word['correct_cnt']
        incorrect = self.quiz_word['incorrect_cnt']


        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.word_data, f, ensure_ascii=False, indent=2)
        
        for btn in self.option_buttons:
            btn.config(state="disabled")

        
        
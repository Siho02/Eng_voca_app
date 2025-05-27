# ui/register_manual.py
import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_PATH = "data/words.json"

class RegisterManualScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # 제목
        tk.Label(self, text="✍️ 수동 단어 등록", font=("Arial", 20), bg="white").pack(pady=20)

        # 단어 등록 
        tk.Label(self, text="Enter the word:", bg="white").pack()
        self.word_entry = tk.Entry(self, width=30)
        self.word_entry.pack(pady=5)

        # 뜻 등록 
        tk.Label(self, text="Enter the meanings (comma-separated):", bg="white").pack()
        self.meaning_entry = tk.Entry(self, width=30)
        self.meaning_entry.pack(pady=5)

        # 예문 등록 
        tk.Label(self, text="Enter example sentence (optional):", bg="white").pack()
        self.example_entry = tk.Entry(self, width=30)
        self.example_entry.pack(pady=5)

        # 저장 버튼
        tk.Button(self, text="💾 저장하기", bg="orange", fg="white", command=self.save_word).pack(pady=10)

        # 뒤로 버튼 
        tk.Button(self, text="← 뒤로", command=lambda: controller.show_screen("register")).pack(pady=10)

    def save_word(self):
        # 1. Entry에서 텍스트 가져오기
        word = self.word_entry.get().strip()
        meaning_raw = self.meaning_entry.get().strip()
        example = self.example_entry.get().strip()

        # 2. 비어 있는 항목 확인 → 경고창 띄우기
        if not word or not meaning_raw:
            messagebox.showwarning("입력 오류", "단어와 뜻은 반드시 입력해야 합니다.")
            return

        # 3. 뜻을 리스트로 분리 (쉼표 기준)
        meanings = [m.strip() for m in meaning_raw.split(",") if m.strip()]

        # 4. 저장할 딕셔너리 구성
        new_entry = {
            "word": word,
            "meaning": meanings,
            "example": example,
            "correct_cnt": 0,
            "incorrect_cnt": 0,
            "last_reviewed": None,
            "mode": "objective",
            "next_review": None
        }

        # 5. 기존 데이터 불러오기 (파일 없으면 빈 리스트)
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, 'r', encoding='utf-8') as f:
                try: 
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []

        # 6. 리스트에 새 단어 추가
        data.append(new_entry)        

        # 7. 다시 파일로 저장 (json.dump)
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            f = json.dump(data, f, ensure_ascii=False, indent=2)

            
        # 8. 성공 메시지 + 입력 필드 초기화
        messagebox.showinfo("저장 완료", f"'{word}' 단어가 저장되었습니다.")
        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)
        self.example_entry.delete(0, tk.END)
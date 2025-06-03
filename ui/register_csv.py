# ui/register_csv.py
import tkinter as tk
from tkinter import filedialog, messagebox
import csv, json, os, shutil
from datetime import datetime, timedelta
from study_log import update_study_log 

DATA_PATH = "data/words.json"
TEMPLATE_PATH = "data/sample_template.csv"

class RegisterCSVScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        # --- 제목 ---
        tk.Label(self, text="📂 CSV로 단어 등록", font=("Arial", 20), bg="white").pack(pady=20)

        # --- 템플릿 다운로드 버튼 ---
        tk.Button(self, text="📄 템플릿 파일 다운로드", command=self.download_template).pack(pady=10)

        # --- 파일 선택 버튼 ---
        tk.Button(self, text="📁 CSV 파일 선택", command=self.load_csv_file).pack(pady=10)

        # --- 완료 후 메시지를 띄울 Label or messagebox 사용 가능 ---
        self.result_label = tk.Label(self, text="", bg="white", fg="green")
        self.result_label.pack(pady=10)

        # --- 뒤로가기 버튼 ---
        tk.Button(self, text="← 뒤로", command=lambda: controller.show_screen("register")).pack(pady=10)

    def download_template(self):
        # sample_template.csv를 복사/저장
        # → filedialog.asksaveasfilename() 으로 저장 위치 선택
        save_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[('CSV files', '*.csv')],
            title = '템플릿 파일 저장'
        )
        # → with open(TEMPLATE_PATH, 'r') → with open(save_path, 'w') 로 복사
        if save_path:
            try:
                shutil.copy(TEMPLATE_PATH, save_path)
                messagebox.showinfo("완료", "템플릿 파일이 저장되었습니다.")
            except Exception as e:
                messagebox.showerror("오류 발생", f'파일 저장 중 오류 발생 : {e}')

    def load_csv_file(self):
        # 1. 사용자가 CSV 파일 선택
        file_path = filedialog.askopenfilename(
            filetypes=[('CSV files', '*.csv')],
            title = "CSV 파일 선택"
        )
        #print("📄 선택된 파일:", file_path)
        if not file_path: return
        
        # 2. 기존 데이터 불러오기
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        else: data = []

        existing_words = {entry["word"].strip().lower(): entry for entry in data}
        added_count = 0
        updated_count = 0
        skipped_count = 0

        new_entries = []

        try:
            # 2. csv.reader 로 파일 읽기
            #print("📂 파일 여는 중...")
            with open(file_path, 'r', encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                # 3. 각 줄을 new_entry 형태로 변환
                for row in reader:
                    word = row.get("word", "").strip()
                    meaning_raw = row.get("meaning", "").strip()
                    example = row.get("example", "").strip()
                    if not word or not meaning_raw:
                        continue

                    word_lower = word.lower()
                    meanings = [m.strip() for m in meaning_raw.split(",") if m.strip()]

                    if word_lower in existing_words:
                        entry = existing_words[word_lower]
                        updated = False

                        for m in meanings:
                            if m not in entry['meaning']:
                                entry['meaning'].append(m)
                                updated = True
                        if not entry.get('example') and example:
                            entry['example'] = example
                            updated = True
                        
                        if updated: updated_count+=1
                        else: skipped_count += 1
                        continue

                    # 새로운 단어로 추가 
                    new_entry = {
                        "created_at" : datetime.now().strftime("%Y-%m-%d %H:%M"),
                        'word' : word,
                        'meaning': meanings,
                        "example": example,
                        "correct_cnt": 0,
                        "incorrect_cnt": 0,
                        "last_reviewed": None,
                        "mode": "objective",
                        "next_review": (datetime.now() + timedelta(minutes=180)).strftime("%Y-%m-%d %H:%M")  # ✅ 3시간 후로 설정!
                    }
                    data.append(new_entry)
                    added_count += 1

        except Exception as e:
            messagebox.showerror("오류", f"CSV 읽기 중 오류 발생: {e}")
            return
        #print("📥 파싱된 단어 수:", len(new_entries))

         #5. 몇 개 등록되었는지 메시지 띄우기
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        update_study_log("register")

        msg = f"{added_count}개 새로 등록됨 / {updated_count}개 병합됨 / {skipped_count}개 중복으로 무시됨"
        self.result_label.config(text=msg)
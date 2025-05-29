# ui/word_list.py
import tkinter as tk
from tkinter import messagebox
import json
import os

DATA_PATH = "data/words.json"

class WordListScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="white")

        tk.Label(self, text="📖 저장된 단어 목록", font=("Arial", 20), bg="white").pack(pady=10)

        self.word_listbox = tk.Listbox(self, width=40, height=20)
        self.word_listbox.pack(pady=10)

        self.detail_label = tk.Label(self, text="", bg="white", justify="left")
        self.detail_label.pack(pady=10)

        self.delete_button = tk.Button(self, text='🗑️ 단어 삭제', bg='red', fg='white', command=self.delete_selected_word, state='disabled')
        self.delete_button.pack(pady=10)
        
        self.edit_button = tk.Button(self, text='🛠️ 단어 수정', bg='gold', command=self.edit_selected_word, state='disabled')
        self.edit_button.pack(pady=5)

        tk.Button(self, text="← 홈으로", command=lambda: controller.show_screen("home")).pack(pady=10)

        self.load_words()
        self.word_listbox.bind("<<ListboxSelect>>", self.show_word_details)

    def load_words(self):
        if os.path.exists(DATA_PATH):
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                try:
                    self.data = json.load(f)
                except json.JSONDecodeError:
                    self.data = []
        else:
            self.data = []

        self.word_listbox.delete(0, tk.END)
        for entry in self.data:
            self.word_listbox.insert(tk.END, entry["word"])

        self.detail_label.config(text='')
        self.delete_button.config(state='disabled')

    def show_word_details(self, event):
        selection = self.word_listbox.curselection()
        if selection:
            index = selection[0]
            entry = self.data[index]
            word = entry.get("word", "")
            meanings = ", ".join(entry.get("meaning", []))
            example = entry.get("example", "")

            if example:
                detail_text = f"📘 단어: {word}\n📚 뜻: {meanings}\n✏️예문: {example}"
            else:
                detail_text = f"📘 단어: {word}\n📚 뜻: {meanings}"

            self.detail_label.config(text=detail_text)
            self.delete_button.config(state='normal')
            self.edit_button.config(state='normal')

    def delete_selected_word(self):
        selection = self.word_listbox.curselection()

        if not selection: return

        index = selection[0]
        word_to_delete = self.data[index]['word']

        confirm = messagebox.askyesno('삭제 확인', f'"{word_to_delete}" 단어를 삭제하시겠습니까?')
        if not confirm: return

        #삭제 후 저장
        del self.data[index]
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("삭제 완료", f'"{word_to_delete}" 단어가 삭제 되었습니다.')
        self.load_words()

    def edit_selected_word(self):
        selection = self.word_listbox.curselection()
        if not selection : return

        index = selection[0]
        entry = self.data[index]

        popup = tk.Toplevel(self)
        popup.title(f'✏️ {entry["word"]} 수정')
        popup.geometry("300x200")

        tk.Label(popup, text='뜻 (쉼표로 구분)').pack(pady=5)
        meaning_entry = tk.Entry(popup, width=40)
        meaning_entry.insert(0, ', '.join(entry.get("meaning", [])))
        meaning_entry.pack()

        tk.Label(popup, text="예문").pack(pady=5)
        example_entry = tk.Entry(popup, width=40)
        example_entry.insert(0, entry.get("example", ""))
        example_entry.pack()

        def save_changes():
            new_meanings = [m.strip() for m in meaning_entry.get().split(",") if m.strip()]
            new_example = example_entry.get().strip()

            self.data[index]["meaning"] = new_meanings
            self.data[index]["example"] = new_example

            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("수정 완료", f"'{entry['word']}' 단어가 수정되었습니다.")
            popup.destroy()
            self.load_words()
        
        tk.Button(popup, text="저장", bg="orange", fg="white", command=save_changes).pack(pady=10)
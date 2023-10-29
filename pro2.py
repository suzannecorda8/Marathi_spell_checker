import tkinter as tk
from nltk.metrics.distance import edit_distance
import re

class SpellingCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Marathi Spelling Checker")
        self.root.configure(bg="#1E1E1E")

        self.label = tk.Label(root, text="Enter a sentence in Marathi:", font=("Helvetica", 12), fg="#FFFFFF", bg="#1E1E1E")
        self.label.pack(pady=15)

        self.entry = tk.Entry(root, font=("Helvetica", 11), bg="#2E2E2E", fg="#FFFFFF")
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Check Spelling", command=self.check_spelling, font=("Helvetica", 11), bg="#3498DB", fg="#FFFFFF")
        self.button.pack(pady=15)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 11), fg="#FFFFFF", bg="#1E1E1E", wraplength=380)
        self.result_label.pack()

        self.marathi_words_database = self.load_marathi_words()

    def check_spelling(self):
        sentence = self.entry.get()
        words = self.extract_words(sentence)
        corrected_sentence = []

        for word in words:
            corrected_word = self.correct_spelling(word)
            corrected_sentence.append(corrected_word)

        corrected_text = " ".join(corrected_sentence)
        self.result_label.config(text=corrected_text)

    def extract_words(self, text):
        return re.findall(r'\b\w+\b', text, flags=re.UNICODE)

    def correct_spelling(self, word):
        if word in self.marathi_words_database:
            return word

        suggestions = self.get_context_based_suggestions(word)
        closest_match = min(suggestions, key=lambda sug: edit_distance(word, sug))
        return closest_match
        

    def load_marathi_words(self):
        with open("marathi_words.txt", "r", encoding="utf-8") as file:
            return set(line.strip() for line in file)

    def get_context_based_suggestions(self, word):
        return [sug for sug in self.marathi_words_database if edit_distance(word, sug) <= 2]

root = tk.Tk()
app = SpellingCheckerApp(root)
root.mainloop()

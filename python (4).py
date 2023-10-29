import tkinter as tk
from tkinter import messagebox
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset of correctly spelled Marathi words
def load_marathi_words_dataset():
    try:
        df = pd.read_csv('marathi_words.csv', encoding='utf-8')
        df['filt_Stopword'] = df['Marathi_Words'].apply(filt_stopword)
        df['clean_text'] = df['filt_Stopword'].apply(remove_unwanted_characters_marathi)
        dataset = df['clean_text']
        dataset = {item for item in dataset if item is not None}
        return set(dataset)
    except FileNotFoundError:
        messagebox.showerror("Error", "Dataset file not found. Make sure to specify the correct path.")
        return set()

stop_words = ["हे", "आणि", "आहे", "आहेत", "आहोत", "व", "हा", "ही", "हे", "होत", "होतं", "होता", "मी", "मला", "तुला"]

def filt_stopword(word):
    if word not in stop_words:
        return word
    else:
        print("Filtered word:" + word)

def remove_unwanted_characters_marathi(input_string):
    if input_string is not None:
        pattern = re.compile(r'[^ऀ-ॿ ]')
        clean_string = re.sub(pattern, '', input_string)
        clean_string = clean_string.strip()
        if clean_string != input_string:
            print(f"Original string '{input_string}' was dirty and has been cleaned.")
        else:
            print("The string is clean.")
        return clean_string

# Check the spelling of a word
def check_marathi_spelling(word, marathi_words_set):
    if word.lower() in marathi_words_set:
        return word.lower()

def check_sentence_spelling():
    sentence = entry.get()
    sentence = sentence.strip()  # Remove leading/trailing spaces
    words = sentence.split()  # Split the sentence into words

    results = []
    for word_to_check in words:
        pattern = re.compile(r'[^ऀ-ॿ ]')
        word_to_check = re.sub(pattern, '', word_to_check)
        if word_to_check.lower() == 'exit':
            app.destroy()
            return
        if check_marathi_spelling(word_to_check, marathi_words_set):
            results.append((word_to_check, "Spelled correctly", "green"))
        else:
            correction = get_correction(word_to_check)
            if correction!="Not found":
                results.append((word_to_check, f"Misspelled. Did you mean?: {correction}", "red"))
            else:
                results.append((word_to_check,f"Word not in dictionary","red"))

    result_text = "\n".join([f"{word}: {message}" for word, message, color in results])
    result_label.config(text=result_text)

vectorizer = TfidfVectorizer()
marathi_words_list = list(load_marathi_words_dataset())

# Function to get correction (you can replace this with your own correction logic)
def get_correction(word):
    # In this simple example, we just return the first matching word from the dataset
    word_lower = word.lower()  # Ensure word_to_check is a string in lowercase
    tfidf_matrix = vectorizer.fit_transform(marathi_words_list)
    input_vector = vectorizer.transform([word_lower])
    similarities = cosine_similarity(input_vector, tfidf_matrix)
    threshold =0.5
    similar_words = [marathi_words_list[i] for i, score in enumerate(similarities[0]) if score >= threshold]
    first_three_similar_words = similar_words[:3]
    if similar_words:
        return first_three_similar_words
    else:
        return "Not found"

# Create the tkinter app
app = tk.Tk()
app.geometry("400x300")
app.title("Marathi Spelling Checker")

# Load the dataset
marathi_words_set = load_marathi_words_dataset()
print(marathi_words_set)

# Create and pack GUI elements
label = tk.Label(app, text="Enter a word in Marathi (or 'exit' to quit):")
label.pack(pady=10)

entry = tk.Entry(app)
entry.pack(pady=5)

check_button = tk.Button(app, text="Check Spelling", command=check_sentence_spelling)
check_button.pack(pady=10)

result_label = tk.Label(app, text="")
result_label.pack(pady=10)

correction_label = tk.Label(app, text="", fg="blue")
correction_label.pack(pady=10)

app.configure(bg="#f0f0f0")
label.configure(bg="#f0f0f0")
entry.configure(bg="white")
check_button.configure(bg="#4CAF50", fg="white")

def display_thank_you_window():
    thank_you_window = tk.Toplevel(app)
    thank_you_window.title("Thank You")
    thank_you_window.geometry("400x300")
    thank_you_label = tk.Label(thank_you_window, text="Thank You!", font=("Helvetica", 24))
    thank_you_label.pack(padx=20, pady=20)
    
    # Automatically close the "Thank You" window after 3 seconds (3000 milliseconds)
    app.after(1000, app.destroy)

# Create an "Exit" button
exit_button = tk.Button(app, text="Exit", command=display_thank_you_window)
exit_button.pack(pady=10)
# Start the GUI main loop
app.mainloop()

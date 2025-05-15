import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq
import os

nltk.download('punkt')
nltk.download('stopwords')

def summarize(text, max_sentences=3):
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)
    
    word_frequencies = {}
    for word in words:
        word = word.lower()
        if word not in stop_words and word.isalpha():
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    
    max_freq = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_scores = {}
    sentences = sent_tokenize(text)
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    return " ".join(best_sentences)

def read_pdf(file_path):
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF: {e}")
    return text

def summarize_input():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showinfo("Info", "Please enter text or upload a PDF file.")
        return
    summary = summarize(input_text)
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, summary)

def load_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        text = read_pdf(file_path)
        text_input.delete("1.0", tk.END)
        text_input.insert(tk.END, text)

root = tk.Tk()
root.title("Text & PDF Summarizer")
root.geometry("800x600")
root.config(bg="#2C3E50")  

frame = tk.Frame(root, bg="#2C3E50")
frame.pack(pady=20)

def rounded_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command, bg="#3498DB", fg="white", font=("Helvetica", 14, "bold"),
                       relief="flat", height=2, width=15, bd=0, activebackground="#2980B9")
    button.pack(side=tk.LEFT, padx=10)
    return button

btn_pdf = rounded_button(frame, "Load PDF", load_pdf)
btn_summarize = rounded_button(frame, "Summarize", summarize_input)

text_input = tk.Text(root, height=10, wrap=tk.WORD, font=("Arial", 12), bd=0, relief="solid", bg="#ECF0F1", fg="black", padx=10, pady=10)
text_input.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

summary_label = tk.Label(root, text="Summary:", font=("Helvetica", 16, "bold"), fg="white", bg="#2C3E50")
summary_label.pack(pady=10)

text_output = tk.Text(root, height=10, wrap=tk.WORD, bg="#BDC3C7", fg="black", font=("Arial", 12), padx=10, pady=10, bd=0, relief="solid")
text_output.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

footer = tk.Label(root, text="© 2025 Text Summarizer. All rights reserved.", font=("Helvetica", 10), fg="white", bg="#2C3E50")
footer.pack(side=tk.BOTTOM, pady=10)

# Run the Tkinter event loop
root.mainloop()

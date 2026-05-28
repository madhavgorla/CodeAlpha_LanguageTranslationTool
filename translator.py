import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyttsx3
import pyperclip
import threading

# ─── Language List ───────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
    "Japanese": "ja",
    "Korean": "ko",
    "Portuguese": "pt",
    "Russian": "ru",
    "Italian": "it",
    "Turkish": "tr",
    "Dutch": "nl",
    "Greek": "el",
    "Bengali": "bn",
    "Urdu": "ur",
}

# ─── Translation Function ────────────────────────────────────────
def translate_text():
    source_text = input_box.get("1.0", tk.END).strip()
    if not source_text:
        messagebox.showwarning("Empty Input", "Please enter text to translate.")
        return

    src_lang = LANGUAGES[source_var.get()]
    tgt_lang = LANGUAGES[target_var.get()]

    if src_lang == tgt_lang and src_lang != "auto":
        messagebox.showinfo("Same Language", "Source and target languages are the same.")
        return

    try:
        status_label.config(text="⏳ Translating...", fg="#f0a500")
        root.update()

        translated = GoogleTranslator(source=src_lang, target=tgt_lang).translate(source_text)

        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, translated)
        output_box.config(state="disabled")

        status_label.config(text="✅ Translation complete!", fg="#00e676")
        char_count_label.config(text=f"Characters: {len(source_text)}")

    except Exception as e:
        status_label.config(text="❌ Error occurred!", fg="#ff5252")
        messagebox.showerror("Translation Error", str(e))

# ─── Copy Function ───────────────────────────────────────────────
def copy_text():
    result = output_box.get("1.0", tk.END).strip()
    if result:
        pyperclip.copy(result)
        status_label.config(text="📋 Copied to clipboard!", fg="#00e676")
    else:
        messagebox.showwarning("Nothing to Copy", "No translated text to copy.")

# ─── Text to Speech Function (FINAL FIX) ─────────────────────────
def speak_text():
    result = output_box.get("1.0", tk.END).strip()
    if result:
        status_label.config(text="🔊 Speaking...", fg="#f0a500")
        root.update()
        def run_tts():
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[0].id)
                engine.say(result)
                engine.runAndWait()
                engine.stop()
                status_label.config(text="✅ Done speaking!", fg="#00e676")
            except Exception as e:
                status_label.config(text="❌ Speak failed!", fg="#ff5252")
        t = threading.Thread(target=run_tts, daemon=True)
        t.start()
    else:
        messagebox.showwarning("Nothing to Speak", "No translated text to speak.")

# ─── Clear Function ──────────────────────────────────────────────
def clear_all():
    input_box.delete("1.0", tk.END)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")
    status_label.config(text="🗑️ Cleared!", fg="#aaaaaa")
    char_count_label.config(text="Characters: 0")

# ─── UI Setup ────────────────────────────────────────────────────
root = tk.Tk()
root.title("🌐 Language Translation Tool — CodeAlpha")
root.geometry("850x620")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

# Title
title_label = tk.Label(root, text="🌐 Language Translation Tool",
                        font=("Helvetica", 20, "bold"),
                        bg="#1e1e2e", fg="#cba6f7")
title_label.pack(pady=15)

subtitle = tk.Label(root, text="Powered by Google Translate • CodeAlpha Internship",
                    font=("Helvetica", 9), bg="#1e1e2e", fg="#6c6f85")
subtitle.pack()

# ─── Language Selection Frame ─────────────────────────────────────
lang_frame = tk.Frame(root, bg="#1e1e2e")
lang_frame.pack(pady=12)

tk.Label(lang_frame, text="Source Language:", font=("Helvetica", 11, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").grid(row=0, column=0, padx=10)

source_var = tk.StringVar(value="Auto Detect")
source_menu = ttk.Combobox(lang_frame, textvariable=source_var,
                            values=list(LANGUAGES.keys()), width=20,
                            state="readonly", font=("Helvetica", 10))
source_menu.grid(row=0, column=1, padx=10)

tk.Label(lang_frame, text="➡️", font=("Helvetica", 16),
         bg="#1e1e2e", fg="#cba6f7").grid(row=0, column=2, padx=10)

tk.Label(lang_frame, text="Target Language:", font=("Helvetica", 11, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").grid(row=0, column=3, padx=10)

target_var = tk.StringVar(value="Hindi")
target_menu = ttk.Combobox(lang_frame, textvariable=target_var,
                            values=list(LANGUAGES.keys()), width=20,
                            state="readonly", font=("Helvetica", 10))
target_menu.grid(row=0, column=4, padx=10)

# ─── Text Boxes Frame ─────────────────────────────────────────────
boxes_frame = tk.Frame(root, bg="#1e1e2e")
boxes_frame.pack(pady=5)

# Input
tk.Label(boxes_frame, text="Enter Text:", font=("Helvetica", 11, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").grid(row=0, column=0, sticky="w", padx=10)

input_box = tk.Text(boxes_frame, height=10, width=42, font=("Helvetica", 11),
                    bg="#313244", fg="#cdd6f4", insertbackground="white",
                    relief="flat", padx=8, pady=8, wrap="word",
                    highlightthickness=2, highlightbackground="#cba6f7")
input_box.grid(row=1, column=0, padx=10)

# Output
tk.Label(boxes_frame, text="Translated Text:", font=("Helvetica", 11, "bold"),
         bg="#1e1e2e", fg="#cdd6f4").grid(row=0, column=1, sticky="w", padx=10)

output_box = tk.Text(boxes_frame, height=10, width=42, font=("Helvetica", 11),
                     bg="#313244", fg="#a6e3a1", insertbackground="white",
                     relief="flat", padx=8, pady=8, wrap="word",
                     highlightthickness=2, highlightbackground="#a6e3a1",
                     state="disabled")
output_box.grid(row=1, column=1, padx=10)

# ─── Character Count ──────────────────────────────────────────────
char_count_label = tk.Label(root, text="Characters: 0",
                             font=("Helvetica", 9), bg="#1e1e2e", fg="#6c6f85")
char_count_label.pack()

# ─── Buttons ──────────────────────────────────────────────────────
btn_frame = tk.Frame(root, bg="#1e1e2e")
btn_frame.pack(pady=12)

btn_style = {"font": ("Helvetica", 11, "bold"), "relief": "flat",
             "cursor": "hand2", "padx": 18, "pady": 8, "bd": 0}

translate_btn = tk.Button(btn_frame, text="🌐 Translate", bg="#cba6f7", fg="#1e1e2e",
                           command=translate_text, **btn_style)
translate_btn.grid(row=0, column=0, padx=8)

copy_btn = tk.Button(btn_frame, text="📋 Copy", bg="#89dceb", fg="#1e1e2e",
                      command=copy_text, **btn_style)
copy_btn.grid(row=0, column=1, padx=8)

speak_btn = tk.Button(btn_frame, text="🔊 Speak", bg="#a6e3a1", fg="#1e1e2e",
                       command=speak_text, **btn_style)
speak_btn.grid(row=0, column=2, padx=8)

clear_btn = tk.Button(btn_frame, text="🗑️ Clear", bg="#f38ba8", fg="#1e1e2e",
                       command=clear_all, **btn_style)
clear_btn.grid(row=0, column=3, padx=8)

# ─── Status Bar ───────────────────────────────────────────────────
status_label = tk.Label(root, text="Ready to translate 🚀",
                         font=("Helvetica", 10), bg="#1e1e2e", fg="#aaaaaa")
status_label.pack(pady=5)

# Footer
footer = tk.Label(root, text="CodeAlpha AI Internship — Task 1",
                  font=("Helvetica", 8), bg="#1e1e2e", fg="#45475a")
footer.pack(side="bottom", pady=8)

root.mainloop()
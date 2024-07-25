import tkinter as tk
import random as r
from time import time

# List of test sentences
test = [
    "As the sun set behind the mountains, the sky transformed into a stunning canvas of colors, with shades of orange, pink, and purple blending together in perfect harmony.",
    "The technological advancements in artificial intelligence are revolutionizing the way we interact with machines, making them smarter and more intuitive than ever before.",
    "Despite the challenges we faced during our journey, we persevered and learned valuable lessons about teamwork, resilience, and the importance of staying focused on our goals.",
    "In a world where information is constantly at our fingertips, the ability to discern fact from fiction has become more important than ever in order to make informed decisions.",
    "The intricate details of the artwork captivated the viewers, drawing them in with its vibrant colors and emotional depth that told a powerful story of love and loss.",
    "As she walked through the bustling city streets, she couldn't help but marvel at the diversity of cultures, languages, and traditions that coexisted in such a vibrant urban landscape.",
    "The impact of climate change on our planet is becoming increasingly evident, prompting scientists and policymakers to work together to develop innovative solutions for a sustainable future.",
]

test1 = r.choice(test)

# Set up the main window
root = tk.Tk()
root.title("Typing Speed Test")
root.config(bg="lightblue")

# Heading label
heading_label = tk.Label(root, text="*** Typing Speed Test Calculator ***", font=('Helvetica', 16, 'bold'), bg='lightblue', fg='white')
heading_label.pack(pady=10)

# Time limit selection
time_limit_label = tk.Label(root, text="Select Time Limit (seconds):", font=('Helvetica', 14, 'bold'), bg='lightblue', fg='white')
time_limit_label.pack(pady=10)

time_limit_var = tk.IntVar()
time_limit_var.set(30)
time_limit_menu = tk.OptionMenu(root, time_limit_var, 30, 60, 90, 120)
time_limit_menu.pack(pady=10)

# Function to start the test
def start_test():
    global start_time, time_limit
    start_time = None
    time_limit = time_limit_var.get()
    entry.config(state=tk.NORMAL)
    entry.delete(0, tk.END)
    entry.focus()
    wpm_label.config(text="")
    timer_label.config(text="")
    error_label.config(text="")
    message_label.config(text="")
    typed_display.config(state=tk.NORMAL)
    typed_display.delete(1.0, tk.END)
    typed_display.config(state=tk.DISABLED)

# Start button
start_button = tk.Button(root, text="Start Test", command=start_test, font=('Helvetica', 14, 'bold'), bg='white', fg='black')
start_button.pack(pady=10)

# Sentence display
sentence_display = tk.Text(root, font=('Helvetica', 16, 'bold'), bg='lightblue', fg='white', wrap='word', height=5, highlightthickness=0, bd=0, borderwidth=0)
sentence_display.pack(pady=10)
sentence_display.insert(tk.END, test1)
sentence_display.config(state=tk.DISABLED)

# Entry for typing
entry = tk.Entry(root, font=('Helvetica', 16, 'bold'), bg='white', fg='black', width=70)
entry.pack(pady=10)

# Typed text display
typed_display = tk.Text(root, font=('Helvetica', 16, 'bold'), bg='lightblue', fg='white', wrap='word', height=5, highlightthickness=0, bd=0, borderwidth=0)
typed_display.pack(pady=10)
typed_display.config(state=tk.DISABLED)

# Error label
error_label = tk.Label(root, text="", font=('Helvetica', 14, 'bold'), bg='lightblue', fg='red')
error_label.pack(pady=10)

# Timer label
timer_label = tk.Label(root, text="", font=('Helvetica', 14, 'bold'), bg='lightblue', fg='white')
timer_label.pack(pady=10)

# WPM label
wpm_label = tk.Label(root, text="", font=('Helvetica', 14, 'bold'), bg='lightblue', fg='white')
wpm_label.pack(pady=10)

# Message label
message_label = tk.Label(root, text="", font=('Helvetica', 14, 'bold'), bg='lightblue', fg='white')
message_label.pack(pady=10)

start_time = None
time_limit = None

# Function to compare text and display errors
def compare_text(*args):
    global start_time
    if not start_time:
        start_time = time()
        root.after(1000, update_timer)

    typed_text = entry.get()
    correct_text = test1
    
    sentence_display.config(state=tk.NORMAL)
    sentence_display.delete(1.0, tk.END)
    sentence_display.insert(tk.END, correct_text)
    
    sentence_display.tag_remove("error", 1.0, tk.END)
    sentence_display.tag_configure("error", background="red", foreground="white")
    
    errors = 0
    min_length = min(len(typed_text), len(correct_text))
    for i in range(min_length):
        if typed_text[i] != correct_text[i]:
            errors += 1
            sentence_display.tag_add("error", f"1.{i}", f"1.{i+1}")
    
    if len(typed_text) > len(correct_text):
        errors += len(typed_text) - len(correct_text)
        sentence_display.tag_add("error", f"1.{len(correct_text)}", f"1.{len(typed_text)}")

    sentence_display.config(state=tk.DISABLED)
    
    typed_display.config(state=tk.NORMAL)
    typed_display.delete(1.0, tk.END)
    typed_display.insert(tk.END, typed_text)
    typed_display.config(state=tk.DISABLED)
    
    error_label.config(text=f"Errors: {errors}")

    if typed_text == correct_text:
        end_test()

# Function to update the timer
def update_timer():
    global start_time, time_limit
    elapsed_time = int(time() - start_time)
    remaining_time = time_limit - elapsed_time
    if remaining_time > 0:
        timer_label.config(text=f"Time left: {remaining_time} seconds")
        root.after(1000, update_timer)
    else:
        end_test()

# Function to end the test and calculate WPM
def end_test():
    entry.config(state=tk.DISABLED)
    elapsed_time = time() - start_time
    typed_text = entry.get()
    word_count = len(typed_text.split())
    wpm = (word_count / elapsed_time) * 60
    wpm_label.config(text=f"WPM: {wpm:.2f}")
    message_label.config(text="Test completed! Well done!")

# Function to update the width of the text widget based on the window size
def update_text_widget_width(event=None):
    entry_width = entry.winfo_width()
    text_width = int(entry_width / 10)
    sentence_display.config(width=text_width)
    typed_display.config(width=text_width)

entry.bind("<KeyRelease>", compare_text)
root.bind("<Configure>", update_text_widget_width)
update_text_widget_width()

root.mainloop()

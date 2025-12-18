import tkinter as tk
from tkinter import messagebox
import json
import random

with open("questions.json", "r") as file:
    all_questions = json.load(file)

questions = []
current_question = 0
score = 0
time_left = 10
timer_id = None

BG_COLOR = "#f4f6ff"
CARD_COLOR = "#ffffff"
BTN_COLOR = "#6c63ff"
TEXT_COLOR = "#333333"

def start_quiz():
    global username, questions
    username = name_entry.get().strip()
    level = level_var.get()

    if username == "":
        messagebox.showwarning("Input Error", "Please enter your name")
        return

    if level == "":
        messagebox.showwarning("Input Error", "Please select difficulty level")
        return

    random.shuffle(all_questions)

    if level == "Easy":
        questions = all_questions[:3]
    elif level == "Medium":
        questions = all_questions[:5]
    else:
        questions = all_questions

    start_frame.pack_forget()
    quiz_frame.pack()
    load_question()
    update_score()
    start_timer()

def load_question():
    global time_left
    time_left = 10

    question_label.config(text=questions[current_question]["question"])

    for i in range(4):
        option_buttons[i].config(
            text=questions[current_question]["options"][i],
            state=tk.NORMAL
        )

    timer_label.config(text=f"⏱ Time: {time_left}s")

def check_answer(selected):
    global score, current_question, timer_id
    root.after_cancel(timer_id)

    correct = questions[current_question]["answer"]
    if selected == correct:
        score += 1
        messagebox.showinfo("Correct ✅", "Correct Answer!")
    else:
        messagebox.showinfo("Wrong ❌", f"Correct Answer: {correct}")

    update_score()
    current_question += 1

    if current_question < len(questions):
        load_question()
        start_timer()
    else:
        show_result()

def update_score():
    score_label.config(text=f"⭐ Score: {score}")

def start_timer():
    global time_left, timer_id
    if time_left > 0:
        timer_label.config(text=f"⏱ Time: {time_left}s")
        time_left -= 1
        timer_id = root.after(1000, start_timer)
    else:
        messagebox.showinfo("Time Up ⏰", "Next Question")
        next_question()

def next_question():
    global current_question
    current_question += 1
    if current_question < len(questions):
        load_question()
        start_timer()
    else:
        show_result()

def show_result():
    messagebox.showinfo(
        "Quiz Completed 🎉",
        f"{username}, your score: {score} / {len(questions)}"
    )
    root.destroy()

# GUI
root = tk.Tk()
root.title("Python Quiz Application")
root.geometry("500x450")
root.config(bg=BG_COLOR)

# Start Screen
start_frame = tk.Frame(root, bg=BG_COLOR)
start_frame.pack(pady=60)

tk.Label(start_frame, text="🎯 Python Quiz App",
         font=("Arial", 20, "bold"),
         bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

tk.Label(start_frame, text="Enter your name",
         bg=BG_COLOR).pack()

name_entry = tk.Entry(start_frame, font=("Arial", 12))
name_entry.pack(pady=5)

tk.Label(start_frame, text="Select Difficulty Level",
         bg=BG_COLOR).pack(pady=10)

level_var = tk.StringVar()
tk.Radiobutton(start_frame, text="Easy (3 Questions)", variable=level_var,
               value="Easy", bg=BG_COLOR).pack(anchor="w")
tk.Radiobutton(start_frame, text="Medium (5 Questions)", variable=level_var,
               value="Medium", bg=BG_COLOR).pack(anchor="w")
tk.Radiobutton(start_frame, text="Hard (All Questions)", variable=level_var,
               value="Hard", bg=BG_COLOR).pack(anchor="w")

tk.Button(start_frame, text="Start Quiz 🚀",
          bg=BTN_COLOR, fg="white",
          font=("Arial", 11, "bold"),
          command=start_quiz).pack(pady=15)

# Quiz Screen
quiz_frame = tk.Frame(root, bg=BG_COLOR)

score_label = tk.Label(quiz_frame, text="⭐ Score: 0",
                       bg=BG_COLOR, font=("Arial", 11, "bold"))
score_label.pack(pady=5)

timer_label = tk.Label(quiz_frame, text="⏱ Time: 10s",
                       bg=BG_COLOR, fg="red",
                       font=("Arial", 11, "bold"))
timer_label.pack()

card = tk.Frame(quiz_frame, bg=CARD_COLOR, padx=20, pady=20)
card.pack(pady=20)

question_label = tk.Label(card, text="", wraplength=420,
                          bg=CARD_COLOR, font=("Arial", 13, "bold"))
question_label.pack(pady=10)

option_buttons = []
for i in range(4):
    btn = tk.Button(card, text="", width=35,
                    bg=BTN_COLOR, fg="white",
                    command=lambda opt=i: check_answer(
                        questions[current_question]["options"][opt]
                    ))
    btn.pack(pady=5)
    option_buttons.append(btn)

root.mainloop()

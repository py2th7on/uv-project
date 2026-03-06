import tkinter as tk
import random
import time

# 題庫
NORMAL = ["apple", "kiwi", "python", "window", "keyboard", "river", "flower"]

HARD = ["good morning", "open the door", "learn python", "write code"]

NIGHTMARE = [
    "practice makes perfect",
    "never give up your dreams",
    "python is a powerful language",
]


class TypingGame:
    def __init__(self, root):

        self.total_chars = 0

        self.root = root
        self.root.title("Speed Typing Challenge")
        self.root.geometry("700x500")
        self.root.configure(bg="#2c3e50")

        self.rounds = 5
        self.current_round = 0
        self.score = 0
        self.start_time = 0
        self.time_limit = 10

        self.difficulty = "NORMAL"

        self.build_ui()

    def build_ui(self):

        title = tk.Label(
            self.root,
            text="Speed Typing Challenge",
            font=("Arial", 28, "bold"),
            bg="#2c3e50",
            fg="white",
        )
        title.pack(pady=20)

        control = tk.Frame(self.root, bg="#2c3e50")
        control.pack()

        tk.Label(
            control, text="Rounds:", bg="#2c3e50", fg="white", font=("Arial", 14)
        ).grid(row=0, column=0, padx=5)

        self.round_entry = tk.Entry(
            control, width=5, font=("Arial", 14), justify="center"
        )
        self.round_entry.insert(0, "5")
        self.round_entry.grid(row=0, column=1, padx=10)

        diff_frame = tk.Frame(self.root, bg="#2c3e50")
        diff_frame.pack(pady=10)

        tk.Button(
            diff_frame, text="Normal", width=10, command=lambda: self.set_diff("NORMAL")
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            diff_frame, text="Hard", width=10, command=lambda: self.set_diff("HARD")
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            diff_frame,
            text="Nightmare",
            width=10,
            command=lambda: self.set_diff("NIGHTMARE"),
        ).grid(row=0, column=2, padx=10)

        self.start_btn = tk.Button(
            self.root, text="Start Game", font=("Arial", 14), command=self.start_game
        )

        self.start_btn.pack(pady=20)

        self.word_display = tk.Text(
            self.root,
            height=1,
            width=30,
            font=("Courier", 40, "bold"),
            bg="#2c3e50",
            fg="white",
            bd=0,
            highlightthickness=0,
        )

        self.word_display.pack(pady=20)
        self.word_display.config(state="disabled")

        self.word_display.tag_config("center", justify="center")
        self.word_display.tag_config("correct", foreground="#2ecc71")
        self.word_display.tag_config("wrong", foreground="red")

        self.timer_label = tk.Label(
            self.root, text="", font=("Arial", 14), bg="#2c3e50", fg="white"
        )

        self.timer_label.pack()

        self.entry = tk.Entry(self.root, font=("Arial", 18), width=30, justify="center")

        self.entry.pack(pady=20)
        self.entry.bind("<KeyRelease>", self.check_input)

        self.result_label = tk.Label(
            self.root, text="", font=("Arial", 12), bg="#2c3e50", fg="white"
        )

        self.result_label.pack()

    def set_diff(self, d):
        self.difficulty = d

    def start_game(self):

        self.game_start_time = time.time()

        self.rounds = int(self.round_entry.get())
        self.current_round = 0
        self.score = 0

        self.next_round()

    def next_round(self):

        self.current_round += 1

        if self.current_round > self.rounds:
            self.show_result()
            return

        if self.difficulty == "NORMAL":
            self.target = random.choice(NORMAL)
            self.time_limit = 10

        elif self.difficulty == "HARD":
            self.target = random.choice(HARD)
            self.time_limit = 10

        else:
            self.target = random.choice(NIGHTMARE)
            self.time_limit = 15

        self.word_display.config(state="normal")
        self.word_display.delete("1.0", tk.END)
        self.word_display.insert("1.0", self.target, "center")
        self.word_display.config(state="disabled")
        self.entry.delete(0, tk.END)
        self.entry.focus()

        self.start_time = time.time()

        self.update_timer()

    def update_timer(self):

        elapsed = time.time() - self.start_time
        remain = round(self.time_limit - elapsed, 1)

        self.timer_label.config(text=f"Time: {remain}s")

        if remain <= 0:
            self.result_label.config(text="Time Up!", fg="red")
            self.root.after(1000, self.next_round)

        else:
            self.root.after(100, self.update_timer)

    def check_input(self, event):

        typed = self.entry.get()

        self.word_display.config(state="normal")
        self.word_display.delete("1.0", tk.END)

        for i, char in enumerate(self.target):
            if i < len(typed):
                if typed[i] == char:
                    self.word_display.insert(tk.END, char, ("correct", "center"))

                else:
                    self.word_display.insert(tk.END, char, ("wrong", "center"))

            else:
                self.word_display.insert(tk.END, char, "center")

        self.word_display.config(state="disabled")

        if typed == self.target:
            self.total_chars += len(self.target)
            self.score += 1
            self.result_label.config(text="Correct!", fg="#2ecc71")

            self.root.after(800, self.next_round)

    def show_result(self):

        self.timer_label.pack_forget()

        self.word_display.config(state="normal")
        self.word_display.delete("1.0", tk.END)
        self.word_display.insert("1.0", "Game Over", "center")
        self.word_display.config(state="disabled")

        elapsed = time.time() - self.game_start_time
        minutes = elapsed / 60

        wpm = int((self.total_chars / 5) / minutes) if minutes > 0 else 0

        self.result_label.config(
            text=f"Score: {self.score}/{self.rounds}   WPM: {wpm}", fg="white"
        )


root = tk.Tk()
game = TypingGame(root)
root.mainloop()

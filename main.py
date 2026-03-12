import tkinter as tk
import random
import json
import time
import platform

class UpsideDownTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Upside Down Terminal")
        self.root.geometry("520x650")
        self.root.configure(bg="#0f0f0f")
        
        self.signal = 0
        self.is_flipped = False
        self.last_input_time = time.time()
        
        try:
            with open('settings.json', 'r') as f:
                self.config = json.load(f)
        except:
            self.config = {"glitch_symbols": ["̴","̶"],"creepy_replies": ["..."],"vecna_lines": ["..."]}

        self.setup_ui()
        self.check_idle()
        self.add_message("⚡ Connection established...", "bot")
        
       
        self.entry.focus_set()
        
        
        self.root.bind('<Motion>', self.move_eye)

    def setup_ui(self):
        self.main_container = tk.Frame(self.root, bg="#0f0f0f")
        self.main_container.pack(fill="both", expand=True)

        self.top_canvas = tk.Canvas(self.main_container, width=520, height=120, bg="black", highlightthickness=0)
        self.top_canvas.pack(side="top")

       
        self.eye_outer = self.top_canvas.create_oval(230, 30, 290, 90, fill="white", outline="gray", width=2)
        self.pupil = self.top_canvas.create_oval(250, 50, 270, 70, fill="black")
        
        self.signal_label = tk.Label(self.main_container, text="Signal: ░░░░░░", bg="#0f0f0f", fg="cyan", font=("Courier", 12))
        self.signal_label.pack(side="top")

        self.main_canvas = tk.Canvas(self.main_container, bg="#0f0f0f", highlightthickness=0)
        self.chat_frame = tk.Frame(self.main_canvas, bg="#0f0f0f")
        self.main_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.main_canvas.pack(side="top", fill="both", expand=True)

        self.input_frame = tk.Frame(self.main_container, bg="#0f0f0f")
        self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

        
        self.entry = tk.Entry(self.input_frame, bg="#1c1c1c", fg="white", insertbackground="white", font=("Courier", 12))
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_button = tk.Button(self.input_frame, text="SEND", command=self.send_message, bg="#333", fg="lime", font=("Courier", 10, "bold"), relief="flat")
        self.send_button.pack(side="right")

    def move_eye(self, event):
        """Calculates pupil movement to follow the mouse cursor."""
        cx, cy = 260, 60
        mx = event.x_root - self.root.winfo_rootx()
        my = event.y_root - self.root.winfo_rooty()
        
        dx = mx - cx
        dy = my - cy
        dist = (dx**2 + dy**2)**0.5
        max_move = 15
        
        if dist > 0:
            move_x = (dx / dist) * min(dist, max_move)
            move_y = (dy / dist) * min(dist, max_move)
            self.top_canvas.coords(self.pupil, cx+move_x-10, cy+move_y-10, cx+move_x+10, cy+move_y+10)

    def add_message(self, text, sender):
        is_user = (sender == "user")
        color = "#2979ff" if is_user else "#1c1c1c"
        frame = tk.Frame(self.chat_frame, bg="#0f0f0f")
        frame.pack(fill="x", side="top", pady=2)
        lbl = tk.Label(frame, text=text, bg=color, fg="white" if is_user else "lime", padx=10, pady=5, wraplength=300)
        lbl.pack(anchor="e" if is_user else "w", padx=10)
        self.main_canvas.update_idletasks()
        self.main_canvas.yview_moveto(1)

    def send_message(self):
        msg = self.entry.get()
        if not msg.strip(): return
        self.entry.delete(0, tk.END)
        self.last_input_time = time.time()
        self.add_message(msg, "user")
        self.signal += 1
        
        bar = "█" * self.signal + "░" * (6 - self.signal)
        self.signal_label.config(text=f"Signal: {bar}")
        
        if self.signal == 6:
            self.root.after(500, self.vecna_takeover)
        
        pool = self.config['vecna_lines'] if self.signal >= 6 else self.config['creepy_replies']
        reply = random.choice(pool)
        self.root.after(800, lambda: self.add_message(self.glitch_text(reply), "bot"))
        
       
        self.entry.focus_set()

    def glitch_text(self, text):
        return "".join([ch + random.choice(self.config['glitch_symbols']) if random.random() < 0.1 else ch for ch in text])

    def flip_ui(self):
        self.is_flipped = not self.is_flipped
        w, h = self.root.winfo_width(), self.root.winfo_height()
        for i in range(h, 50, -60):
            self.root.geometry(f"{w}x{i}"); self.root.update(); time.sleep(0.01)

        widgets = self.main_container.pack_slaves()
        for widget in widgets: widget.pack_forget()
        
        new_side = "bottom" if self.is_flipped else "top"
        if self.is_flipped:
            self.top_canvas.itemconfig(self.eye_outer, fill="red", outline="white")
            self.send_button.config(fg="red", text="BREACH")
            self.input_frame.pack(side="top", fill="x", padx=10, pady=10)
            self.main_canvas.pack(side="top", fill="both", expand=True)
            self.signal_label.pack(side="top", pady=5)
            self.top_canvas.pack(side="top")
        else:
            self.send_button.config(fg="lime", text="SEND")
            self.top_canvas.pack(side="top")
            self.signal_label.pack(side="top")
            self.main_canvas.pack(side="top", fill="both", expand=True)
            self.input_frame.pack(side="top", fill="x", padx=10, pady=10)

        for i in range(50, h, 60):
            self.root.geometry(f"{w}x{i}"); self.root.update(); time.sleep(0.01)
        self.root.geometry(f"{w}x{h}")
        self.entry.focus_set() 

    def check_idle(self):
        if time.time() - self.last_input_time > 30 and self.signal >= 2:
            self.add_message("👾 I'm watching you...", "bot")
            self.last_input_time = time.time()
        self.root.after(5000, self.check_idle)

    def vecna_takeover(self):
        self.root.configure(bg="darkred")
        self.main_container.configure(bg="darkred")
        self.chat_frame.configure(bg="darkred")
        self.main_canvas.configure(bg="darkred")
        self.flip_ui()
        self.add_message(f"👁 SYSTEM COMPROMISED ON {platform.system().upper()}.", "bot")
    

    def shake_screen(self):
        orig_pos = self.root.geometry()
        for _ in range(10):
         x_shift = random.randint(-10, 10)
         y_shift = random.randint(-10, 10)
        self.root.geometry(f"+{self.root.winfo_x() + x_shift}+{self.root.winfo_y() + y_shift}")
        self.root.update()
        time.sleep(0.02)
        self.root.geometry(orig_pos)
if __name__ == "__main__":
    root = tk.Tk()
    app = UpsideDownTerminal(root)
    root.mainloop()
import datetime
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import bcrypt
import customtkinter as ctk

# Setup Dark Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

DB_FILE = "secure_todo.db"


def init_db():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    """)
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            page_name TEXT,
            task TEXT,
            date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
  conn.commit()
  conn.close()


init_db()


class SecureTodoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Secure Keep-Style Checklist To-Do (Dark)")
    self.root.geometry("900x650")
    self.root.configure(fg_color="#121212")

    self.current_user_id = None
    self.current_username = None
    self.mini_window = None

    self.show_login_screen()

  def clear_window(self):
    if self.mini_window:
      self.mini_window.destroy()
      self.mini_window = None
    for widget in self.root.winfo_children():
      widget.destroy()

  def show_login_screen(self):
    self.clear_window()

    title = ctk.CTkLabel(
        self.root,
        text="Welcome Back 🖤",
        font=("Arial", 22, "bold"),
        text_color="#E0E0E0",
    )
    title.pack(pady=40)

    self.user_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Username",
        width=250,
        height=40,
        fg_color="#1E1E1E",
        text_color="#E0E0E0",
        border_width=1,
        border_color="#333333",
    )
    self.user_entry.pack(pady=10)

    self.pass_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Password",
        show="*",
        width=250,
        height=40,
        fg_color="#1E1E1E",
        text_color="#E0E0E0",
        border_width=1,
        border_color="#333333",
    )
    self.pass_entry.pack(pady=10)

    login_btn = ctk.CTkButton(
        self.root,
        text="Login",
        command=self.login_user,
        fg_color="#2A2A2A",
        hover_color="#3A3A3A",
        text_color="#E0E0E0",
        width=250,
        height=40,
    )
    login_btn.pack(pady=15)

    reg_btn = ctk.CTkButton(
        self.root,
        text="Create New Account",
        command=self.show_register_screen,
        fg_color="transparent",
        text_color="#888888",
        hover_color="#1E1E1E",
        width=250,
        height=30,
    )
    reg_btn.pack(pady=5)

  def show_register_screen(self):
    self.clear_window()

    title = ctk.CTkLabel(
        self.root,
        text="Create Account 🔒",
        font=("Arial", 22, "bold"),
        text_color="#E0E0E0",
    )
    title.pack(pady=40)

    self.reg_user_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Choose Username",
        width=250,
        height=40,
        fg_color="#1E1E1E",
        text_color="#E0E0E0",
        border_width=1,
        border_color="#333333",
    )
    self.reg_user_entry.pack(pady=10)

    self.reg_pass_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Choose Password",
        show="*",
        width=250,
        height=40,
        fg_color="#1E1E1E",
        text_color="#E0E0E0",
        border_width=1,
        border_color="#333333",
    )
    self.reg_pass_entry.pack(pady=10)

    register_btn = ctk.CTkButton(
        self.root,
        text="Register",
        command=self.register_user,
        fg_color="#2A2A2A",
        hover_color="#3A3A3A",
        text_color="#E0E0E0",
        width=250,
        height=40,
    )
    register_btn.pack(pady=15)

    back_btn = ctk.CTkButton(
        self.root,
        text="Back to Login",
        command=self.show_login_screen,
        fg_color="transparent",
        text_color="#888888",
        hover_color="#1E1E1E",
        width=250,
        height=30,
    )
    back_btn.pack(pady=5)

  def register_user(self):
    username = self.reg_user_entry.get().strip()
    password = self.reg_pass_entry.get().encode("utf-8")

    if not username or not password:
      messagebox.showerror("Error", "All fields are required!")
      return

    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    try:
      conn = sqlite3.connect(DB_FILE)
      cursor = conn.cursor()
      cursor.execute(
          "INSERT INTO users (username, password) VALUES (?, ?)",
          (username, hashed_password),
      )
      conn.commit()
      conn.close()
      messagebox.showinfo(
          "Success", "Account created successfully! Please login."
      )
      self.show_login_screen()
    except sqlite3.IntegrityError:
      messagebox.showerror("Error", "Username already exists!")

  def login_user(self):
    username = self.user_entry.get().strip()
    password_val = self.pass_entry.get().encode("utf-8")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, password FROM users WHERE username = ?", (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password_val, user[1]):
      self.current_user_id = user[0]
      self.current_username = username
      self.show_todo_dashboard()
    else:
      messagebox.showerror("Error", "Invalid Username or Password!")

  def show_todo_dashboard(self):
    self.clear_window()
    self.root.geometry("920x650")

    header_frame = ctk.CTkFrame(
        self.root, fg_color="#1A1A1A", corner_radius=0, height=50
    )
    header_frame.pack(fill=ctk.X, padx=0, pady=0)

    welcome_lbl = ctk.CTkLabel(
        header_frame,
        text=f"Welcome, {self.current_username} 🖤",
        font=("Arial", 14, "bold"),
        text_color="#E0E0E0",
    )
    welcome_lbl.pack(side=ctk.LEFT, padx=15, pady=10)

    logout_btn = ctk.CTkButton(
        header_frame,
        text="Logout",
        command=self.show_login_screen,
        fg_color="#2A2A2A",
        hover_color="#3A3A3A",
        text_color="#E0E0E0",
        width=70,
        height=25,
    )
    logout_btn.pack(side=ctk.RIGHT, padx=15)

    grid_frame = ctk.CTkFrame(self.root, fg_color="#121212")
    grid_frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)

    self.default_pages = ["Daily Tasks", "Work Notes", "Personal / Ideas"]
    self.card_data = {}

    for i, page in enumerate(self.default_pages):
      card = ctk.CTkFrame(
          grid_frame,
          fg_color="#1E1E1E",
          corner_radius=10,
          border_width=1,
          border_color="#2A2A2A",
      )
      card.grid(row=0, column=i, sticky="nsew", padx=8, pady=5)
      grid_frame.grid_columnconfigure(i, weight=1)
      grid_frame.grid_rowconfigure(0, weight=1)

      title_lbl = ctk.CTkLabel(
          card,
          text=page,
          font=("Arial", 13, "bold"),
          text_color="#E0E0E0",
      )
      title_lbl.pack(anchor="w", padx=12, pady=(10, 5))

      task_scroll = ctk.CTkScrollableFrame(
          card, fg_color="#161616", corner_radius=6, height=350
      )
      task_scroll.pack(fill=ctk.BOTH, expand=True, padx=10, pady=5)

      input_row = ctk.CTkFrame(card, fg_color="transparent")
      input_row.pack(fill=ctk.X, padx=10, pady=(5, 10))

      task_entry = ctk.CTkEntry(
          input_row,
          placeholder_text="Add item...",
          height=30,
          fg_color="#1E1E1E",
          text_color="#E0E0E0",
          border_width=1,
          border_color="#333333",
      )
      task_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(0, 5))
      task_entry.bind(
          "<Return>", lambda event, p=page: self.add_task_from_entry(p)
      )

      add_btn = ctk.CTkButton(
          input_row,
          text="+",
          width=30,
          height=30,
          fg_color="#2A2A2A",
          hover_color="#3A3A3A",
          text_color="#E0E0E0",
          command=lambda p=page: self.add_task_from_entry(p),
      )
      add_btn.pack(side=ctk.RIGHT)

      self.card_data[page] = {
          "scroll_frame": task_scroll,
          "entry": task_entry,
          "tasks": [],
      }

    self.load_all_todos()

    bottom_frame = ctk.CTkFrame(
        self.root, fg_color="transparent", height=50
    )
    bottom_frame.pack(fill=ctk.X, padx=15, pady=(0, 15))

    save_btn = ctk.CTkButton(
        bottom_frame,
        text="Save All Cards & Collapse to Widget 🖤",
        command=self.save_and_collapse,
        fg_color="#2A2A2A",
        hover_color="#3A3A3A",
        text_color="#E0E0E0",
        height=40,
    )
    save_btn.pack(fill=ctk.X, expand=True)

  def add_task_from_entry(self, page_name, task_text=None, is_checked=False):
    if task_text is None:
      entry = self.card_data[page_name]["entry"]
      task_text = entry.get().strip()
      if not task_text:
        return
      entry.delete(0, ctk.END)

    self.card_data[page_name]["tasks"].append(
        {"text": task_text, "checked": is_checked}
    )
    self.refresh_task_ui(page_name)

  def refresh_task_ui(self, page_name):
    scroll_frame = self.card_data[page_name]["scroll_frame"]

    for widget in scroll_frame.winfo_children():
      widget.destroy()

    tasks = self.card_data[page_name]["tasks"]
    # Automatically sort unchecked tasks on top, checked tasks at the bottom
    tasks.sort(key=lambda x: x["checked"])

    for idx, item in enumerate(tasks):
      row = ctk.CTkFrame(
          scroll_frame, fg_color="#1E1E1E", corner_radius=6
      )
      row.pack(fill=ctk.X, pady=3, padx=2)

      var = ctk.BooleanVar(value=item["checked"])
      text_color = "#666666" if item["checked"] else "#E0E0E0"

      chk = ctk.CTkCheckBox(
          row,
          text=item["text"],
          variable=var,
          text_color=text_color,
          fg_color="#333333",
          hover_color="#444444",
          corner_radius=4,
          command=lambda it=item, p=page_name, v=var: self.on_check_toggle(
              it, p, v
          ),
      )
      chk.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=6, pady=4)

      # Delete button
      del_btn = ctk.CTkButton(
          row,
          text="✕",
          width=24,
          height=24,
          fg_color="transparent",
          text_color="#666666",
          hover_color="#2A2A2A",
          font=("Arial", 10, "bold"),
          command=lambda it=item, p=page_name: self.delete_task(it, p),
      )
      del_btn.pack(side=ctk.RIGHT, padx=2)

      # Move Down button (▼)
      if idx < len(tasks) - 1:
        down_btn = ctk.CTkButton(
            row,
            text="▼",
            width=24,
            height=24,
            fg_color="transparent",
            text_color="#888888",
            hover_color="#2A2A2A",
            font=("Arial", 10),
            command=lambda i=idx, p=page_name: self.move_task(p, i, 1),
        )
        down_btn.pack(side=ctk.RIGHT, padx=1)

      # Move Up button (▲)
      if idx > 0:
        up_btn = ctk.CTkButton(
            row,
            text="▲",
            width=24,
            height=24,
            fg_color="transparent",
            text_color="#888888",
            hover_color="#2A2A2A",
            font=("Arial", 10),
            command=lambda i=idx, p=page_name: self.move_task(p, i, -1),
        )
        up_btn.pack(side=ctk.RIGHT, padx=1)

  def move_task(self, page_name, idx, direction):
    tasks = self.card_data[page_name]["tasks"]
    new_idx = idx + direction
    if 0 <= new_idx < len(tasks):
      tasks[idx], tasks[new_idx] = tasks[new_idx], tasks[idx]
      self.refresh_task_ui(page_name)

  def on_check_toggle(self, item, page_name, var):
    item["checked"] = var.get()
    # Refreshes UI and instantly pushes checked items to the bottom
    self.refresh_task_ui(page_name)

  def delete_task(self, item, page_name):
    if item in self.card_data[page_name]["tasks"]:
      self.card_data[page_name]["tasks"].remove(item)
      self.refresh_task_ui(page_name)

  def save_and_collapse(self):
    today = str(datetime.date.today())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for page_name, data in self.card_data.items():
      lines = []
      for item in data["tasks"]:
        status = "1" if item["checked"] else "0"
        lines.append(f"{status}||{item['text']}")

      content = "\n".join(lines)

      cursor.execute(
          "SELECT id FROM page_todos WHERE user_id = ? AND page_name = ? AND"
          " date = ?",
          (self.current_user_id, page_name, today),
      )
      row = cursor.fetchone()

      if row:
        cursor.execute(
            "UPDATE page_todos SET task = ? WHERE id = ?", (content, row[0])
        )
      else:
        cursor.execute(
            "INSERT INTO page_todos (user_id, page_name, task, date) VALUES"
            " (?, ?, ?, ?)",
            (self.current_user_id, page_name, content, today),
        )

    conn.commit()
    conn.close()

    self.root.withdraw()
    self.show_floating_widget()

  def show_floating_widget(self):
    if self.mini_window:
      self.mini_window.destroy()

    self.mini_window = ctk.CTkToplevel(self.root)
    self.mini_window.overrideredirect(True)
    self.mini_window.geometry("180x45+100+100")
    self.mini_window.configure(fg_color="#1E1E1E")

    def start_move(event):
      self.mini_window.x = event.x
      self.mini_window.y = event.y

    def do_move(event):
      deltax = event.x - self.mini_window.x
      deltay = event.y - self.mini_window.y
      new_x = self.mini_window.winfo_x() + deltax
      new_y = self.mini_window.winfo_y() + deltay
      self.mini_window.geometry(f"+{new_x}+{new_y}")

    btn = ctk.CTkButton(
        self.mini_window,
        text="🖤 Open To-Do Notes",
        command=self.restore_main_window,
        fg_color="#2A2A2A",
        hover_color="#3A3A3A",
        text_color="#E0E0E0",
        font=("Arial", 11, "bold"),
        corner_radius=6,
    )
    btn.pack(fill=ctk.BOTH, expand=True, padx=4, pady=4)

    btn.bind("<Button-1>", start_move)
    btn.bind("<B1-Motion>", do_move)

  def restore_main_window(self, event=None):
    if self.mini_window:
      self.mini_window.destroy()
      self.mini_window = None
    self.root.deiconify()

  def load_all_todos(self):
    today = str(datetime.date.today())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT page_name, task FROM page_todos WHERE user_id = ? AND date = ?",
        (self.current_user_id, today),
    )
    rows = cursor.fetchall()
    conn.close()

    for page_name, task in rows:
      if page_name in self.card_data and task:
        for line in task.split("\n"):
          if "||" in line:
            parts = line.split("||", 1)
            is_checked = parts[0] == "1"
            text = parts[1]
            self.add_task_from_entry(
                page_name, task_text=text, is_checked=is_checked
            )


if __name__ == "__main__":
  root = ctk.CTk()
  app = SecureTodoApp(root)
  root.mainloop()
import datetime
import os
import sqlite3
import tkinter as tk
from tkinter import messagebox
import bcrypt
import customtkinter as ctk

# Setup Theme
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("green")

DB_FILE = "secure_todo.db"


# Database Setup
def init_db():
  conn = sqlite3.connect(DB_FILE)
  cursor = conn.cursor()
  # Users table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    """)
  # Todos table linked with user_id
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
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
    self.root.title("Secure Sticky To-Do Software")
    self.root.geometry("400x500")
    self.root.configure(fg_color="#F4F1EA")  # Neutral aesthetic background

    self.current_user_id = None
    self.current_username = None

    self.show_login_screen()

  def clear_window(self):
    for widget in self.root.winfo_children():
      widget.destroy()

  # ================= LOGIN / REGISTER SCREENS =================
  def show_login_screen(self):
    self.clear_window()

    title = ctk.CTkLabel(
        self.root,
        text="Welcome Back ☕",
        font=("Arial", 22, "bold"),
        text_color="#2C2C2C",
    )
    title.pack(pady=40)

    self.user_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Username",
        width=250,
        height=40,
        fg_color="#E8E4D9",
        text_color="#2C2C2C",
        border_width=0,
    )
    self.user_entry.pack(pady=10)

    self.pass_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Password",
        show="*",
        width=250,
        height=40,
        fg_color="#E8E4D9",
        text_color="#2C2C2C",
        border_width=0,
    )
    self.pass_entry.pack(pady=10)

    login_btn = ctk.CTkButton(
        self.root,
        text="Login",
        command=self.login_user,
        fg_color="#3D3A36",
        hover_color="#57534E",
        width=250,
        height=40,
    )
    login_btn.pack(pady=15)

    reg_btn = ctk.CTkButton(
        self.root,
        text="Create New Account",
        command=self.show_register_screen,
        fg_color="transparent",
        text_color="#57534E",
        hover_color="#E8E4D9",
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
        text_color="#2C2C2C",
    )
    title.pack(pady=40)

    self.reg_user_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Choose Username",
        width=250,
        height=40,
        fg_color="#E8E4D9",
        text_color="#2C2C2C",
        border_width=0,
    )
    self.reg_user_entry.pack(pady=10)

    self.reg_pass_entry = ctk.CTkEntry(
        self.root,
        placeholder_text="Choose Password",
        show="*",
        width=250,
        height=40,
        fg_color="#E8E4D9",
        text_color="#2C2C2C",
        border_width=0,
    )
    self.reg_pass_entry.pack(pady=10)

    register_btn = ctk.CTkButton(
        self.root,
        text="Register",
        command=self.register_user,
        fg_color="#3D3A36",
        hover_color="#57534E",
        width=250,
        height=40,
    )
    register_btn.pack(pady=15)

    back_btn = ctk.CTkButton(
        self.root,
        text="Back to Login",
        command=self.show_login_screen,
        fg_color="transparent",
        text_color="#57534E",
        hover_color="#E8E4D9",
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
    password = self.user_entry.get().encode("utf-8")
    # Using specific entry widget for password
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

  # ================= SECURE TO-DO DASHBOARD =================
  def show_todo_dashboard(self):
    self.clear_window()
    self.root.geometry("450x600")

    # Header section
    header_frame = ctk.CTkFrame(
        self.root, fg_color="#E8E4D9", corner_radius=0, height=50
    )
    header_frame.pack(fill=ctk.X, padx=0, pady=0)

    welcome_lbl = ctk.CTkLabel(
        header_frame,
        text=f"Welcome, {self.current_username} 📌",
        font=("Arial", 14, "bold"),
        text_color="#2C2C2C",
    )
    welcome_lbl.pack(side=ctk.LEFT, padx=15, pady=10)

    logout_btn = ctk.CTkButton(
        header_frame,
        text="Logout",
        command=self.show_login_screen,
        fg_color="#D9C3B0",
        text_color="#2C2C2C",
        width=70,
        height=25,
    )
    logout_btn.pack(side=ctk.RIGHT, padx=15)

    # Main Sticky Note Container
    note_frame = ctk.CTkFrame(
        self.root, fg_color="#F4F1EA", corner_radius=10, border_width=1
    )
    note_frame.pack(fill=ctk.BOTH, expand=True, padx=20, pady=20)

    lbl = ctk.CTkLabel(
        note_frame,
        text="Today's Tasks (Auto-clears at midnight)",
        font=("Arial", 12, "italic"),
        text_color="#57534E",
    )
    lbl.pack(anchor="w", padx=15, pady=(15, 5))

    # Text area for notes
    self.todo_text = ctk.CTkTextbox(
        note_frame,
        fg_color="#FFFDF9",
        text_color="#2C2C2C",
        font=("Arial", 12),
        corner_radius=8,
    )
    self.todo_text.pack(fill=ctk.BOTH, expand=True, padx=15, pady=5)

    save_btn = ctk.CTkButton(
        note_frame,
        text="Save Notes",
        command=self.save_todos,
        fg_color="#3D3A36",
        hover_color="#57534E",
        height=35,
    )
    save_btn.pack(fill=ctk.X, padx=15, pady=15)

    self.load_todos()

  def save_todos(self):
    today = str(datetime.date.today())
    content = self.todo_text.get("1.0", "end-1c")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Check if entry for today exists for this user
    cursor.execute(
        "SELECT id FROM todos WHERE user_id = ? AND date = ?",
        (self.current_user_id, today),
    )
    row = cursor.fetchone()

    if row:
      cursor.execute(
          "UPDATE todos SET task = ? WHERE id = ?", (content, row[0])
      )
    else:
      cursor.execute(
          "INSERT INTO todos (user_id, task, date) VALUES (?, ?, ?)",
          (self.current_user_id, content, today),
      )

    conn.commit()
    conn.close()
    messagebox.showinfo("Saved", "Your notes are securely saved!")

  def load_todos(self):
    today = str(datetime.date.today())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT task FROM todos WHERE user_id = ? AND date = ?",
        (self.current_user_id, today),
    )
    row = cursor.fetchone()
    conn.close()

    if row:
      self.todo_text.insert("1.0", row[0])


if __name__ == "__main__":
  root = ctk.CTk()
  app = SecureTodoApp(root)
  root.mainloop()
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
  # Updated table to support multiple pages/tabs per user
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
    self.root.title("Secure Multi-Page Sticky To-Do")
    self.root.geometry("550x650")
    self.root.configure(fg_color="#F4F1EA")

    self.current_user_id = None
    self.current_username = None

    self.show_login_screen()

  def clear_window(self):
    for widget in self.root.winfo_children():
      widget.destroy()

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
    self.root.geometry("600x650")

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

    # Multi-page Tabview container
    self.tab_view = ctk.CTkTabview(
        self.root,
        fg_color="#F4F1EA",
        segmented_button_fg_color="#E8E4D9",
        segmented_button_selected_color="#3D3A36",
        segmented_button_selected_color_text="#FFFFFF",
        segmented_button_unselected_color="#E8E4D9",
        segmented_button_unselected_color_text="#2C2C2C",
    )
    self.tab_view.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)

    # Default Pages
    self.default_pages = ["Daily Tasks", "Work Notes", "Personal / Ideas"]
    self.textboxes = {}

    for page in self.default_pages:
      self.tab_view.add(page)
      tb = ctk.CTkTextbox(
          self.tab_view.tab(page),
          fg_color="#FFFDF9",
          text_color="#2C2C2C",
          font=("Arial", 12),
          corner_radius=8,
      )
      tb.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
      self.textboxes[page] = tb

    # Load data for all pages
    self.load_all_todos()

    # Bottom Action Frame
    bottom_frame = ctk.CTkFrame(
        self.root, fg_color="transparent", height=50
    )
    bottom_frame.pack(fill=ctk.X, padx=15, pady=(0, 15))

    save_btn = ctk.CTkButton(
        bottom_frame,
        text="Save All Pages",
        command=self.save_all_todos,
        fg_color="#3D3A36",
        hover_color="#57534E",
        height=40,
    )
    save_btn.pack(fill=ctk.X, expand=True)

  def save_all_todos(self):
    today = str(datetime.date.today())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for page_name, textbox in self.textboxes.items():
      content = textbox.get("1.0", "end-1c")
      cursor.execute(
          "SELECT id FROM users WHERE id = ?", (self.current_user_id,)
      )  # sanity check

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
    messagebox.showinfo("Saved", "All sticky pages saved securely!")

  def load_all_todos(self):
    today = str(datetime.date.today())
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for page_name, textbox in self.textboxes.items():
      cursor.execute(
          "SELECT task FROM page_todos WHERE user_id = ? AND page_name = ? AND"
          " date = ?",
          (self.current_user_id, page_name, today),
      )
    row = cursor.fetchone()
    # Fixed loading logic for all tabs properly
    cursor.execute(
        "SELECT page_name, task FROM page_todos WHERE user_id = ? AND date = ?",
        (self.current_user_id, today),
    )
    rows = cursor.fetchall()
    conn.close()

    for page_name, task in rows:
      if page_name in self.textboxes:
        self.textboxes[page_name].delete("1.0", "end")
        self.textboxes[page_name].insert("1.0", task)


if __name__ == "__main__":
  root = ctk.CTk()
  app = SecureTodoApp(root)
  root.mainloop()
Secure Desktop To-Do Application 🖤
A private, secure, multi-user, and aesthetic desktop to-do application built with Python and CustomTkinter. Designed with a minimalist dark theme (Black/Grey) inspired by Google Keep, it features a floating desktop widget for seamless daily productivity.

✨ Features

- Minimalist Dark Theme: Sleek black and grey aesthetic designed to reduce eye strain and look professional on any desktop.
- Multi-User Authentication: Secure user registration and login system powered by bcrypt password hashing to keep individual notes private and isolated.
- Keep-Style Checklists: Add tasks easily, check them off to automatically push them to the bottom with a dimmed styling, and manage items with delete or up/down reordering controls.
- Smart Floating Desktop Widget: Collapse the main app into a compact status bar that sits right on your desktop. It features smart positional memory—remembering its exact screen coordinates when collapsing and expanding.
- Local SQLite Storage: Fast, reliable, and localized data storage per user.

🛠 Tech Stack

- Python (Core application logic)
- CustomTkinter (Modern UI framework)
- SQLite3 (Local user-specific database storage)
- Bcrypt (Secure password hashing)
- PyInstaller (Packaging the application into a standalone Windows .exe)

🚀 Getting Started

Prerequisites
Ensure you have Python installed on your system (Python 3.8 or higher recommended).

Installation & Running Locally
Clone the repository:

Bash
git clone https://github.com/krutipeepre/CustomTkinter-To-Do-Software.git
cd CustomTkinter-To-Do-Software
Install the required dependencies:

Bash
pip install customtkinter bcrypt
Run the application:

Bash
python app.py
📦 Building a Standalone Executable (.exe)
To package the application into a standalone Windows executable file so you can run it directly from your desktop:

Install PyInstaller:

Bash
pip install pyinstaller
Generate the executable:

Bash
pyinstaller --noconsole --onefile app.py
Locate your compiled application inside the newly created dist/ folder (app.exe), right-click to send it to your desktop as a shortcut, and you're good to go!

📄 License
This project is open-source and available for use and modification.

❄️ ColdCompress – Smart File Compression Tool

ColdCompress is a Python-based desktop application with a GUI (Tkinter) that automatically identifies old/unused files and compresses them to save disk space. It also allows decompression, logging, and progress tracking.

⚙️ Run as Desktop App (Executable)

Navigate to the dist/ folder in this repository.

Download and Double-click ColdCompress.exe to launch the application like a regular desktop app.


🚀 Features

📂 Folder Selection & Validation – Choose a folder and validate its accessibility.

⏱ Threshold-based File Scanning – Detect files not accessed in the last N days (default: 30).

🔒 Compression Engine – Compress files into .zz format using zlib.

🔓 Decompression Engine – Restore .zz files back to their original state.

📊 Progress & Logging – Real-time progress updates, detailed logs, and space-saving statistics.

🖥 User-Friendly GUI – Built using Tkinter with a simple workflow.

🛠️ Tech Stack

Language: Python 3.x

Libraries: zlib, tkinter, pathlib, threading, os, time


⚙️ Installation

Clone the repository:

git clone https://github.com/Parthib17/Cold-Compress-A-Smart-File-Compression-and-Storage-Optimizer-for-Windows

cd ColdCompress


Run the application:

python src/main.py

🎮 Usage

Open the application.

Select a folder to scan.

Choose threshold days (default = 30).

Click Compress to compress old files into .zz.

Click Decompress to restore .zz files.

View logs and statistics directly in the GUI.

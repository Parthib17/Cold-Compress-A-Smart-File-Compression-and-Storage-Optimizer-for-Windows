import time
import tkinter as tk
from tkinter import ttk
from config import STYLES, LOG_COLORS


class LogWidget(ttk.LabelFrame):
    """Widget for displaying log messages with color coding and scrolling."""

    def __init__(self, parent):
        super().__init__(parent, text="Activity Log", padding="10")

        self._create_widgets()

    def _create_widgets(self):
        """Create log area widgets."""
        # Create a frame for log and scrollbar
        log_container = ttk.Frame(self)
        log_container.pack(fill=tk.BOTH, expand=True)

        # Text area for log messages
        self.log_area = tk.Text(
            log_container,
            wrap=tk.WORD,
            font=STYLES['log']['font'],
            bg=STYLES['log']['bg'],
            fg=STYLES['log']['fg'],
            height=STYLES['log']['height']
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_area.yview)
        self.log_area.configure(yscrollcommand=scrollbar.set)

        # Pack log area and scrollbar
        self.log_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Clear log button
        ttk.Button(
            self,
            text="🗑️ Clear Log",
            command=self.clear_log
        ).pack(pady=(10, 0))

    def log_message(self, message: str, level: str = "INFO"):
        """
        Add a message to the log with timestamp and color coding.

        Args:
            message: The message to log
            level: Log level (INFO, SUCCESS, ERROR, WARNING)
        """
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"

        self.log_area.insert(tk.END, formatted_message)

        # Apply color to the last line
        line_start = self.log_area.index("end-2c linestart")
        line_end = self.log_area.index("end-2c")
        self.log_area.tag_add(level, line_start, line_end)
        self.log_area.tag_config(level, foreground=LOG_COLORS.get(level, "black"))

        # Auto-scroll to the bottom
        self.log_area.see(tk.END)

        # Update the display
        self.update_idletasks()

    def clear_log(self):
        """Clear all messages from the log area."""
        self.log_area.delete(1.0, tk.END)
        self.log_message("📝 Log cleared", "INFO")
import tkinter as tk
from tkinter import ttk


class ActionButtonsWidget(ttk.Frame):
    """Widget containing the main action buttons for compress/decompress operations."""

    def __init__(self, parent, compress_callback, decompress_callback):
        super().__init__(parent)

        self.compress_callback = compress_callback
        self.decompress_callback = decompress_callback

        self._create_widgets()

    def _create_widgets(self):
        """Create action button widgets."""
        self.compress_btn = ttk.Button(
            self,
            text="🗜️ Scan & Compress Old Files",
            command=self.compress_callback,
            style='Action.TButton'
        )
        self.compress_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)

        self.decompress_btn = ttk.Button(
            self,
            text="📂 Decompress All .zz Files",
            command=self.decompress_callback,
            style='Action.TButton'
        )
        self.decompress_btn.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)

    def set_buttons_enabled(self, enabled: bool):
        """Enable or disable both action buttons."""
        state = tk.NORMAL if enabled else tk.DISABLED
        self.compress_btn.configure(state=state)
        self.decompress_btn.configure(state=state)
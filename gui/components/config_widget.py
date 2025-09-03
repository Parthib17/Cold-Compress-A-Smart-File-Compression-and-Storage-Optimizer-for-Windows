import tkinter as tk
from tkinter import ttk, filedialog
from config import STYLES


class ConfigWidget(ttk.LabelFrame):
    """Widget for configuration settings (folder and threshold)."""

    def __init__(self, parent, folder_path_var, threshold_var):
        super().__init__(parent, text="Configuration", padding="15")

        self.folder_path_var = folder_path_var
        self.threshold_var = threshold_var

        self._create_widgets()

    def _create_widgets(self):
        """Create configuration widgets."""
        # Folder selection section
        self._create_folder_selection()

        # Threshold setting section
        self._create_threshold_setting()

    def _create_folder_selection(self):
        """Create folder selection widgets."""
        folder_frame = ttk.Frame(self)
        folder_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(folder_frame, text="Target Folder:", style='Heading.TLabel').pack(anchor=tk.W)

        folder_entry_frame = ttk.Frame(folder_frame)
        folder_entry_frame.pack(fill=tk.X, pady=(5, 0))

        self.folder_entry = ttk.Entry(
            folder_entry_frame,
            textvariable=self.folder_path_var,
            font=STYLES['entry']['font']
        )
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        ttk.Button(
            folder_entry_frame,
            text="📁 Browse",
            command=self._choose_folder
        ).pack(side=tk.RIGHT)

    def _create_threshold_setting(self):
        """Create threshold setting widgets."""
        threshold_frame = ttk.Frame(self)
        threshold_frame.pack(fill=tk.X)

        ttk.Label(threshold_frame, text="Compress files older than:",
                  style='Heading.TLabel').pack(side=tk.LEFT)

        threshold_spinbox = ttk.Spinbox(
            threshold_frame,
            from_=1,
            to=365,
            textvariable=self.threshold_var,
            width=5,
            font=STYLES['entry']['font']
        )
        threshold_spinbox.pack(side=tk.LEFT, padx=(10, 5))

        ttk.Label(threshold_frame, text="days").pack(side=tk.LEFT)

    def _choose_folder(self):
        """Open folder selection dialog."""
        folder = filedialog.askdirectory(title="Select folder to process")
        if folder:
            self.folder_path_var.set(folder)
            # Emit event for logging (if parent has log capability)
            if hasattr(self.master.master, 'log_widget'):
                log_widget = self.master.master.log_widget
                log_widget.log_message(f"📁 Selected folder: {folder}", "INFO")
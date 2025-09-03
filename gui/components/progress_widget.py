import tkinter as tk
from tkinter import ttk


class ProgressWidget(ttk.LabelFrame):
    """Widget for displaying progress information and statistics."""

    def __init__(self, parent):
        super().__init__(parent, text="Progress", padding="10")

        self._create_widgets()

    def _create_widgets(self):
        """Create progress widgets."""
        # Progress status label
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(self, textvariable=self.progress_var)
        self.progress_label.pack(anchor=tk.W)

        # Progress bar
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))

        # Statistics frame
        stats_frame = ttk.Frame(self)
        stats_frame.pack(fill=tk.X, pady=(10, 0))

        self.files_processed_var = tk.StringVar(value="Files processed: 0")
        ttk.Label(stats_frame, textvariable=self.files_processed_var).pack(side=tk.LEFT)

        self.space_saved_var = tk.StringVar(value="Space saved: 0 MB")
        ttk.Label(stats_frame, textvariable=self.space_saved_var).pack(side=tk.RIGHT)

    def start_progress(self):
        """Start the progress bar animation."""
        self.progress_bar.start()

    def stop_progress(self):
        """Stop the progress bar animation."""
        self.progress_bar.stop()

    def set_status(self, status: str):
        """Update the progress status text."""
        self.progress_var.set(status)

    def update_stats(self, files_processed: int, space_saved_mb: float):
        """Update the statistics display."""
        self.files_processed_var.set(f"Files processed: {files_processed}")
        self.space_saved_var.set(f"Space saved: {space_saved_mb:.2f} MB")

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from config import WINDOW_CONFIG, STYLES, THRESHOLD_DAYS
from services.compression_service import CompressionService
from gui.components.log_widget import LogWidget
from gui.components.progress_widget import ProgressWidget
from gui.components.config_widget import ConfigWidget
from gui.components.action_buttons import ActionButtonsWidget


class ColdCompressGUI:
    """Main GUI class for the ColdCompress application."""

    def __init__(self, root):
        self.root = root
        self.compression_service = CompressionService()

        # Configure main window
        self._setup_window()
        self._setup_styles()

        # Initialize variables
        self.folder_path = tk.StringVar()
        self.threshold_days = tk.IntVar(value=THRESHOLD_DAYS)

        # Create UI components
        self._create_widgets()

    def _setup_window(self):
        """Configure the main window properties."""
        self.root.title(WINDOW_CONFIG['title'])
        self.root.geometry(WINDOW_CONFIG['geometry'])
        self.root.configure(bg=WINDOW_CONFIG['bg_color'])

    def _setup_styles(self):
        """Configure ttk styles."""
        self.style = ttk.Style()
        self.style.theme_use(STYLES['theme'])

        self.style.configure('Title.TLabel',
                             font=STYLES['title']['font'],
                             background=STYLES['title']['background'])

        self.style.configure('Heading.TLabel',
                             font=STYLES['heading']['font'],
                             background=STYLES['heading']['background'])

        self.style.configure('Action.TButton',
                             font=STYLES['action_button']['font'],
                             padding=STYLES['action_button']['padding'])

    def _create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="🗜️ ColdCompress", style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        # Configuration widget
        self.config_widget = ConfigWidget(main_frame, self.folder_path, self.threshold_days)
        self.config_widget.pack(fill=tk.X, pady=(0, 20))

        # Action buttons widget
        self.action_widget = ActionButtonsWidget(
            main_frame,
            self.start_compression_thread,
            self.start_decompression_thread
        )
        self.action_widget.pack(fill=tk.X, pady=(0, 20))

        # Progress widget
        self.progress_widget = ProgressWidget(main_frame)
        self.progress_widget.pack(fill=tk.X, pady=(0, 20))

        # Log widget
        self.log_widget = LogWidget(main_frame)
        self.log_widget.pack(fill=tk.BOTH, expand=True)

        # Initialize log
        self.log_widget.log_message("🚀 ColdCompress initialized. Select a folder to begin.", "INFO")

    def start_compression_thread(self):
        """Start compression in a separate thread."""
        if not self._validate_folder():
            return

        self._start_operation("compression")
        thread = threading.Thread(target=self._compression_worker, daemon=True)
        thread.start()

    def start_decompression_thread(self):
        """Start decompression in a separate thread."""
        if not self._validate_folder():
            return

        self._start_operation("decompression")
        thread = threading.Thread(target=self._decompression_worker, daemon=True)
        thread.start()

    def _start_operation(self, operation_type: str):
        """Common setup for starting an operation."""
        self.action_widget.set_buttons_enabled(False)
        self.progress_widget.start_progress()
        self.progress_widget.set_status(f"Starting {operation_type}...")

    def _compression_worker(self):
        """Worker thread for compression operations."""
        try:
            self._scan_and_compress()
        except Exception as e:
            self.log_widget.log_message(f"❌ Compression failed: {e}", "ERROR")
        finally:
            self.root.after(0, self._reset_ui)

    def _decompression_worker(self):
        """Worker thread for decompression operations."""
        try:
            self._scan_and_decompress()
        except Exception as e:
            self.log_widget.log_message(f"❌ Decompression failed: {e}", "ERROR")
        finally:
            self.root.after(0, self._reset_ui)

    def _scan_and_compress(self):
        """Scan folder and compress old files."""
        folder = Path(self.folder_path.get())
        threshold_days = self.threshold_days.get()

        self.log_widget.log_message(
            f"🔍 Scanning {folder} recursively for files older than {threshold_days} days...",
            "INFO"
        )

        # Find old files
        old_files = self.compression_service.find_old_files(folder, threshold_days)

        if not old_files:
            self.log_widget.log_message("⚠️ No files found to process", "WARNING")
            return

        self.log_widget.log_message(f"📊 Found {len(old_files)} files to compress", "INFO")

        # Compress files
        total_space_saved = 0
        files_compressed = 0

        for i, filepath in enumerate(old_files, 1):
            progress_text = f"Processing {i}/{len(old_files)}: {filepath.name}"
            self.progress_widget.set_status(progress_text)

            result = self.compression_service.compress_file(filepath)
            if result['success']:
                files_compressed += 1
                total_space_saved += result['space_saved']
                self.log_widget.log_message(result['message'], "SUCCESS")
            else:
                self.log_widget.log_message(result['message'], "ERROR")

        # Final summary
        space_saved_mb = total_space_saved / (1024 * 1024)
        self.log_widget.log_message(f"✨ Compression completed!", "SUCCESS")
        self.log_widget.log_message(f"📈 Files compressed: {files_compressed}", "INFO")
        self.log_widget.log_message(f"💾 Total space saved: {space_saved_mb:.2f} MB", "SUCCESS")

        self.progress_widget.update_stats(files_compressed, space_saved_mb)

    def _scan_and_decompress(self):
        """Scan folder and decompress .zz files."""
        folder = Path(self.folder_path.get())

        self.log_widget.log_message(f"🔍 Scanning {folder} recursively for .zz files...", "INFO")

        # Find compressed files
        compressed_files = self.compression_service.find_compressed_files(folder)

        if not compressed_files:
            self.log_widget.log_message("ℹ️ No .zz compressed files found", "INFO")
            return

        # Decompress files
        files_decompressed = 0
        for i, filepath in enumerate(compressed_files, 1):
            progress_text = f"Processing {i}/{len(compressed_files)}: {filepath.name}"
            self.progress_widget.set_status(progress_text)

            result = self.compression_service.decompress_file(filepath)
            if result['success']:
                files_decompressed += 1
                self.log_widget.log_message(result['message'], "SUCCESS")
            else:
                self.log_widget.log_message(result['message'], "ERROR")

        self.log_widget.log_message(
            f"✨ Decompression completed! {files_decompressed} files decompressed",
            "SUCCESS"
        )
        self.progress_widget.update_stats(files_decompressed, 0)

    def _validate_folder(self) -> bool:
        """Validate the selected folder."""
        folder = self.folder_path.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please select a valid folder!")
            return False
        return True

    def _reset_ui(self):
        """Reset UI after operation completes."""
        self.progress_widget.stop_progress()
        self.progress_widget.set_status("Ready")
        self.action_widget.set_buttons_enabled(True)

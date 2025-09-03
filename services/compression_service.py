import os
import time
import zlib
from pathlib import Path
from typing import Dict, Any, List, Tuple
from config import COMPRESSED_EXTENSION


class CompressionService:
    """Service class for handling file compression and decompression operations."""

    def __init__(self):
        self.compression_level = 9  # Maximum compression

    def compress_file(self, filepath: Path) -> Dict[str, Any]:
        """
        Compress a single file using zlib.

        Args:
            filepath: Path to the file to compress

        Returns:
            Dictionary containing operation result and metadata
        """
        try:
            original_size = filepath.stat().st_size

            # Read and compress file data
            with open(filepath, "rb") as f:
                data = f.read()
            compressed = zlib.compress(data, level=self.compression_level)

            # Write compressed file
            compressed_path = filepath.with_suffix(filepath.suffix + COMPRESSED_EXTENSION)
            with open(compressed_path, "wb") as f:
                f.write(compressed)

            # Remove original file
            os.remove(filepath)

            # Calculate compression statistics
            compressed_size = compressed_path.stat().st_size
            space_saved = original_size - compressed_size
            compression_ratio = (space_saved / original_size) * 100 if original_size > 0 else 0

            return {
                'success': True,
                'message': f"✅ Compressed: {filepath.name} ({compression_ratio:.1f}% reduction)",
                'space_saved': space_saved,
                'original_path': filepath,
                'compressed_path': compressed_path,
                'compression_ratio': compression_ratio
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Error compressing {filepath}: {e}",
                'space_saved': 0,
                'error': str(e)
            }

    def decompress_file(self, filepath: Path) -> Dict[str, Any]:
        """
        Decompress a .zz file.

        Args:
            filepath: Path to the compressed file

        Returns:
            Dictionary containing operation result and metadata
        """
        try:
            # Read and decompress file data
            with open(filepath, "rb") as f:
                data = f.read()
            decompressed = zlib.decompress(data)

            # Write decompressed file (remove .zz suffix)
            original_path = filepath.with_suffix("")
            with open(original_path, "wb") as f:
                f.write(decompressed)

            # Remove compressed file
            os.remove(filepath)

            return {
                'success': True,
                'message': f"✅ Decompressed: {filepath.name} → {original_path.name}",
                'original_path': original_path,
                'compressed_path': filepath
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"❌ Error decompressing {filepath}: {e}",
                'error': str(e)
            }

    def find_old_files(self, folder: Path, threshold_days: int) -> List[Path]:
        """
        Find files older than the specified threshold.

        Args:
            folder: Root folder to scan
            threshold_days: Age threshold in days

        Returns:
            List of file paths that are older than threshold
        """
        now = time.time()
        threshold_seconds = threshold_days * 24 * 60 * 60
        old_files = []

        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = Path(root) / file

                # Skip already compressed files
                if filepath.suffix.endswith(COMPRESSED_EXTENSION):
                    continue

                try:
                    atime = os.stat(filepath).st_atime
                    if now - atime > threshold_seconds:
                        old_files.append(filepath)
                except Exception:
                    # Skip files that can't be accessed
                    continue

        return old_files

    def find_compressed_files(self, folder: Path) -> List[Path]:
        """
        Find all compressed .zz files in the folder.

        Args:
            folder: Root folder to scan

        Returns:
            List of compressed file paths
        """
        compressed_files = []

        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = Path(root) / file
                if filepath.suffix.endswith(COMPRESSED_EXTENSION):
                    compressed_files.append(filepath)

        return compressed_files

    def get_folder_stats(self, folder: Path) -> Tuple[int, int]:
        """
        Get statistics about files in the folder.

        Args:
            folder: Root folder to analyze

        Returns:
            Tuple of (total_files, compressed_files)
        """
        total_files = 0
        compressed_files = 0

        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = Path(root) / file
                total_files += 1
                if filepath.suffix.endswith(COMPRESSED_EXTENSION):
                    compressed_files += 1

        return total_files, compressed_files

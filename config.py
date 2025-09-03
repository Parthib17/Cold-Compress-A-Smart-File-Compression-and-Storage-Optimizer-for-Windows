# Default threshold for file age in days
THRESHOLD_DAYS = 30

# UI Configuration
WINDOW_CONFIG = {
    'title': "ColdCompress - Smart File Compression Tool",
    'geometry': "900x700",
    'bg_color': "#f0f0f0"
}

# Style configuration
STYLES = {
    'theme': 'clam',
    'title': {
        'font': ('Arial', 16, 'bold'),
        'background': "#f0f0f0"
    },
    'heading': {
        'font': ('Arial', 12, 'bold'),
        'background': "#f0f0f0"
    },
    'action_button': {
        'font': ('Arial', 10, 'bold'),
        'padding': 10
    },
    'entry': {
        'font': ('Arial', 10)
    },
    'log': {
        'font': ('Consolas', 9),
        'bg': "white",
        'fg': "black",
        'height': 15
    }
}

# Log level colors
LOG_COLORS = {
    "INFO": "blue",
    "SUCCESS": "green",
    "ERROR": "red",
    "WARNING": "orange"
}

# File extensions
COMPRESSED_EXTENSION = ".zz"
import shutil

def get_terminal_size() -> tuple[int, int]:
    """Get the size of the terminal window."""
    try:
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    except Exception as e:
        print(f"Error getting terminal size: {e}")
        return 80, 24  # Default size if unable to get terminal size
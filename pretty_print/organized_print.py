from pretty_print.utils.terminal_size import get_terminal_size

class Cell:
    """Class representing a cell in the organized print table."""
    
    def __init__(self, content: str = "", size: tuple[int, int] = (1, 1)):
        self.content = content
        self.size = size

    def __repr__(self):
        return f"{self.content}"

class OrganizedPrint(list):
    """Class for organized printing in the terminal."""

    def __init__(self, cell_width: int = 1, cell_height: int = 1):
        """Initialize the OrganizedPrint with the number of divisions."""
        table = [[Cell() for _ in range(cell_width)] for _ in range(cell_height)]
        self.cell_width = cell_width
        self.cell_height = cell_height
        super().__init__(table)

    def add_content(self, row: int, col: int, content: str):
        """Add content to a specific cell in the organized print table."""
        if row < self.cell_width and col < self.cell_height:
            self[row][col].content = content

    def __repr__(self):
        """Return a string representation of the organized print table."""
        output = []
        
        for row in self:
            row_output = []
            for cell in row:
                # Ensure the content fits within the cell width
                cell_content = cell.content.ljust(self.get_max_length_colums(row.index(cell)))
                row_output.append(cell_content)
            output.append(" | ".join(row_output))

        return "\n".join(output)
    
    def get_max_length_colums(self, column_index: int) -> int:
        """Get the maximum element length in a specific column."""
        maximum_length = 0

        for y in range(self.cell_height):
            if maximum_length < len(self[y][column_index].content):
                maximum_length = len(self[y][column_index].content)
        
        return maximum_length

def main():
    """Main function to demonstrate organized printing."""
    op = OrganizedPrint(4, 5)
    op.add_content(0, 0, "Header 1")
    op.add_content(0, 1, "Header 2")
    print(op)

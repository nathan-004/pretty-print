from typing import Optional

from pretty_print.utils.terminal_size import get_terminal_size

class Cell:
    """Class representing a cell in the organized print table."""
    
    def __init__(self, content: str = "", size: tuple[int, int] = (1, 1)):
        self.content = content
        self.size = size

    def __repr__(self):
        return f"{self.content}"

class Row(list):
    """Class representing a row in the organized print table."""
    
    def __init__(self, cells: list[Cell]):
        super().__init__(cells)
    
    def __repr__(self):
        return " | ".join(str(cell) for cell in self)
    
    def __setitem__(self, index, value):
        """Set a cell at a specific index."""
        if isinstance(value, Cell):
            super().__setitem__(index, value)
        elif isinstance(value, str):
            super().__setitem__(index, Cell(value))
        else:
            raise ValueError("Value must be an instance of Cell or a string")

class OrganizedPrint(list):
    """Class for organized printing in the terminal."""

    def __init__(self, cell_width: int = 1, cell_height: int = 1, width:Optional[int] = None, height:Optional[int] = None):
        """
        Initialize the OrganizedPrint with the number of divisions.
        
        Args:
            cell_width (int): Number of cells in each row.
            cell_height (int): Number of rows.
            width (int): Width of the organized print table in percentage -> default is content width
            height (int): Height of the organized print table in percentage -> default is content height
        """
        table = [Row([Cell() for _ in range(cell_width)]) for _ in range(cell_height)]
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.percent_width, self.percent_height = width,  height
        super().__init__(table)

    def current_cell_width(self, column_index: int) -> int:
        """Get the width of a specific cell."""
        if self.percent_width is None:
            w_size = self.get_max_length_colums(column_index)
        else:
            w_size = int(self.percent_width * get_terminal_size()[0] / 100 / self.cell_width)

        return w_size

    def add_content(self, row: int, col: int, content: str):
        """Add content to a specific cell in the organized print table."""
        if row < self.cell_width and col < self.cell_height:
            self[row][col].content = content

    # -----------------------------------------------------
    # Properties for cell width and height
    # -----------------------------------------------------

    def __repr__(self):
        """Return a string representation of the organized print table."""
        output = []
        
        for row in self:
            row_output = []
            for cell in row:
                # Ensure the content fits within the cell width
                cell_content = cell.content.ljust(self.current_cell_width(row.index(cell)))
                row_output.append(cell_content)
            output.append("   ".join(row_output))

        return "\n".join(output)
    
    def __setitem__(self, index, value):
        """Set a row at a specific index."""
        if isinstance(value, Row):
            super().__setitem__(index, value)
        elif isinstance(value, str):
            super().__setitem__(index, Row([Cell(value) for _ in range(self.cell_width)]))
        elif isinstance(value, list):
            super().__setitem__(index, Row([Cell(content) for content in value]))
        else:
            raise ValueError("Value must be an instance of Row")
    
    def get_max_length_colums(self, column_index: int) -> int:
        """Get the maximum element length in a specific column."""
        maximum_length = 0

        for y in range(self.cell_height):
            if maximum_length < len(self[y][column_index].content):
                maximum_length = len(self[y][column_index].content)
        
        return maximum_length

def main():
    """Main function to demonstrate organized printing."""
    op = OrganizedPrint(4, 5, width=50)
    op[0] = ["Header 1", "Header 2", "Header 3", "Header 4"]
    op[1][0] = "Test"
    op[2][1] = "This is a test"
    op[3][2] = "Another test"
    op[4][3] = "Final test"
    print(op)
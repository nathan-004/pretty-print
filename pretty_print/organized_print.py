from typing import Optional, Union

from pretty_print.utils.terminal_size import get_terminal_size

class Cell:
    """Class representing a cell in the organized print table."""
    
    def __init__(self, content: str = "", size: tuple[int, int] = (1, 1)):
        self.content = content
        self.size = size

    def __repr__(self):
        return f"{self.content}"

class RowRangeView:
    """Vue sur plusieurs lignes (row slice)."""
    def __init__(self, parent, row_slice: slice):
        self.parent = parent
        self.row_slice = row_slice

    def __getitem__(self, col_slice: int | slice):
        # Retourne les cellules de chaque ligne dans la plage
        result = []
        for row in range(*self.row_slice.indices(self.parent.cell_height)):
            if isinstance(col_slice, slice):
                result.append([
                    self.parent.find_cell(row, col)
                    for col in range(*col_slice.indices(self.parent.cell_width))
                ])
            else:
                result.append(self.parent.find_cell(row, col_slice))
        return result

    def __setitem__(self, col_slice: Union[int, slice], value: str):
        # Assigne une valeur dans toutes les cellules de la plage
        for row in range(*self.row_slice.indices(self.parent.cell_height)):
            if isinstance(col_slice, slice):
                for col in range(*col_slice.indices(self.parent.cell_width)):
                    self.parent[row][col] = value
            else:
                self.parent[row][col_slice]

class Row(list):
    """Class representing a row in the organized print table."""
    
    def __init__(self, cells: list[Cell]):
        super().__init__(cells)
    
    def __setitem__(self, index, value):
        """Set a cell at a specific index."""
        if isinstance(value, Cell):
            self.set_item(index, value)
        elif isinstance(value, str):
            self.set_item(index, Cell(value))
        else:
            raise ValueError("Value must be an instance of Cell or a string")
    
    def set_item(self, index:Union[int, slice], value):
        """Set an item"""
        if isinstance(index, int):
            super().__setitem__(index, value)
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            
            for i in range(start, stop, step):
                super().__setitem__(i, value)

class OrganizedPrint(list):
    """Class for organized printing in the terminal."""

    def __init__(self, cell_width: int = 1, cell_height: int = 1, width:Optional[int] = None, height:Optional[int] = None, cell_overflow: Optional[str] = "normal") -> None:
        """
        Initialize the OrganizedPrint with the number of divisions.
        
        Args:
            cell_width (int): Number of cells in each row.
            cell_height (int): Number of rows.
            width (int): Width of the organized print table in percentage -> default is content width
            height (int): Height of the organized print table in percentage -> default is content height
            cell_overflow (str): How to handle overflow in cells. Options: "normal", "truncate". Default is "normal".
        """
        table = [Row([Cell() for _ in range(cell_width)]) for _ in range(cell_height)]
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.percent_width, self.percent_height = width,  height
        self.cell_overflow = cell_overflow
        super().__init__(table)

        self.between_cell_col = " | " 

    def current_cell_width(self, column_index: int) -> int:
        """Get the width of a specific cell."""
        if self.percent_width is None:
            w_size = self.get_max_length_colums(column_index)
        else:
            w_size = int(self.percent_width * (get_terminal_size()[0] - len(self.between_cell_col) * (self.cell_width - 1)) / 100 / self.cell_width)

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
        
        for row_idx, row in enumerate(self):
            row_output = []
            for cell_idx, cell in enumerate(row):
                # Ensure the content fits within the cell width
                cell_content = self.get_value(row_idx, cell_idx)
                row_output.append(cell_content)
            output.append(" | ".join(row_output))

        return "\n".join(output)
    
    def __setitem__(self, index, value):
        """Set a row at a specific index."""
        if isinstance(value, Row):
            self.set_item(index, value)
        elif isinstance(value, str):
            self.set_item(index, Row([Cell(value) for _ in range(self.cell_width)]))
        elif isinstance(value, list):
            self.set_item(index, Row([Cell(content) for content in value]))
        else:
            raise ValueError(f"Value must be an instance of Row not {type(value)}")

    def set_item(self, index:Union[int, slice], value):
        """Set an item"""
        if isinstance(index, int):
            super().__setitem__(index, value)
        elif isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            
            for i in range(start, stop, step):
                super().__setitem__(i, value)

    def __getitem__(self, index: int | slice):
        if isinstance(index, slice):
            return RowRangeView(self, index)
        else:
            return super().__getitem__(index)
    
    # -----------------------------------------------------
    # Helper methods
    # -----------------------------------------------------

    def get_max_length_colums(self, column_index: int) -> int:
        """Get the maximum element length in a specific column."""
        maximum_length = 0

        for y in range(self.cell_height):
            if maximum_length < len(self[y][column_index].content):
                maximum_length = len(self[y][column_index].content)
        
        return maximum_length
    
    def get_value(self, row: int, col: int) -> str:
        """Get the content of a specific cell."""
        if not (row < self.cell_height and col < self.cell_width):
            return ""
        
        cell = self[row][col]
        col_size = self.current_cell_width(col)

        if col_size < len(cell.content):
            if self.percent_width is None:
                return cell.content.ljust(col_size)
        
        return cell.content.ljust(col_size)

def main():
    """Main function to demonstrate organized printing."""
    op = OrganizedPrint(4, 5, width=100)
    op[0] = ["Header 1", "Header 2", "Header 3", "Header 4"]
    op[1][0:] = "Test"
    op[2][1] = "This is a test"
    op[3][2] = "Another test"
    op[4][3] = "Final test"
    op[3:5][0:2] = "Test"
    print(op)
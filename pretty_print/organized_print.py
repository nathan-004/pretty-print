from typing import Optional

from pretty_print.utils.terminal_size import get_terminal_size

class Cell:
    """Class representing a cell in the organized print table."""
    
    def __init__(
        self, 
        content: str = "", 
        position: tuple[int, int] = (0, 0), 
        size: tuple[int, int] = (1, 1)
    ):
        self.content = content
        self.position = position  # (row, col)
        self.size = size          # (height, width)

    def __repr__(self):
        return f"{self.content}"


class OrganizedPrint(list):
    """Class for organized printing in the terminal."""

    def __init__(
        self, 
        cell_width: int = 1, 
        cell_height: int = 1, 
        width: Optional[int] = None, 
        height: Optional[int] = None, 
        cell_overflow: Optional[str] = "normal"
    ) -> None:
        """
        Initialize the OrganizedPrint with the number of divisions.
        
        Args:
            cell_width (int): Number of cells per row.
            cell_height (int): Number of rows.
            width (int): Width of the organized print table in percentage.
            height (int): Height of the organized print table in percentage.
            cell_overflow (str): How to handle overflow in cells. Options: "normal", "truncate".
        """
        self.max_cells_width = cell_width
        self.max_cells_height = cell_height
        self.percent_width, self.percent_height = width, height
        self.cell_overflow = cell_overflow

        # Initialise toutes les cellules avec positions
        cells = []
        for row in range(cell_height):
            for col in range(cell_width):
                cells.append(Cell("", (row, col), (1, 1)))
        super().__init__(cells)

    # -----------------------------------------------------
    # Recherche d’une cellule
    # -----------------------------------------------------

    def find_cell(self, row: int, col: int) -> Optional[Cell]:
        """Retourne la cellule à la position donnée (row, col)."""
        for cell in self:
            if cell.position == (row, col):
                return cell
        return None

    def set_value(self, row: int, col: int, value: str):
        """Met à jour le contenu d’une cellule donnée."""
        cell = self.find_cell(row, col)
        if cell:
            cell.content = value

    def get_value(self, row: int, col: int) -> str:
        """Retourne le contenu d’une cellule donnée."""
        cell = self.find_cell(row, col)
        if not cell:
            return ""

        col_size = self.current_cell_width(col)
        content = cell.content

        if self.cell_overflow == "truncate" and len(content) > col_size:
            return content[: col_size - 1] + "…"
        return content.ljust(col_size)

    # -----------------------------------------------------
    # Largeur d'une cellule
    # -----------------------------------------------------

    def current_cell_width(self, column_index: int) -> int:
        """Get the width of a specific column."""
        if self.percent_width is None:
            # calcule largeur max selon contenu de la colonne
            return self.get_max_length_colums(column_index)
        else:
            return int(
                self.percent_width * get_terminal_size()[0] / 100 / self.max_cells_width
            )

    def get_max_length_colums(self, column_index: int) -> int:
        """Get the maximum element length in a specific column."""
        maximum_length = 0
        for cell in self:
            if cell.position[1] == column_index:  # même colonne
                maximum_length = max(maximum_length, len(cell.content))
        return maximum_length

    # -----------------------------------------------------
    # Affichage
    # -----------------------------------------------------

    def __repr__(self):
        output = []
        for row in range(self.max_cells_height):
            row_cells = [
                self.get_value(row, col) for col in range(self.max_cells_width)
            ]
            output.append(" | ".join(row_cells))
        return "\n".join(output)


def main():
    """Main function to demonstrate organized printing."""
    op = OrganizedPrint(cell_width=3, cell_height=2, cell_overflow="truncate")

    op.set_value(0, 0, "Hello")
    op.set_value(0, 1, "World")
    op.set_value(1, 2, "Ceci est un texte très long")

    print(op)
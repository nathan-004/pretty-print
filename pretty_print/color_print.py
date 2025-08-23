from pretty_print.utils.styles import TextColors, Styles, BackgroundColors

def style_print(*args, format:bool = False, end:str = "\n", separator:str = " ", styles:list[str] = [], reset:bool = True):
    """
    Print elements on the console with colors from TextColors, Styles, BackgroundColors

    Parameters
    ----------
    format:bool
        If True, the given string contains the styles as variables like `Start {Styles.BOLD}`
    end:str
        End of the print, default is '\n'
    separator:str
        print argument, default is ' '
    styles:list[str]
        Contains a list of styles placed at the start of the value
    reset:bool
        whether applied styles should be deleted, default is True

    Returns
    -------
    str: The string that is going to be printed
    """
    to_print = separator.join(args)
    to_print = ''.join(styles) + to_print

    if format:
        to_print = to_print.format(TextColors=TextColors)

    if reset:
        to_print += Styles.RESET

    print(to_print, end=end)
    return to_print + end

def main():
    style_print("{TextColors.BLUE} test", format=True)
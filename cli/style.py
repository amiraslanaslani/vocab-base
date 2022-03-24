class styles:
    BLACK = '\033[30m'
    WHITE = '\033[37m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    BG_YELLOW = '\033[103m'
    BG_WHITE = '\033[47m'
    BG_GREY = '\033[100m'
    BG_BWHITE = '\033[107m'


def single_style(text: str, style):
    return style + text + styles.END

def style(text: str, styles):
    if not isinstance(styles, list):
        styles = [styles]
    if len(styles) == 0:
        return text
    return style(single_style(text, styles[0]), styles[1:])

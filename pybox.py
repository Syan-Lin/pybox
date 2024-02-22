from utils import text_style, text_wrap, text_width

def __text_line__(
        text: str,
        text_width: int,
        box_width: int,
        text_align: str,
        placeholder: str,
        margin: int) -> str:
    box_width -= 2 * margin
    if 'left' in text_align:
        text = text + (box_width - text_width) * placeholder
    elif 'right' in text_align:
        text = (box_width - text_width) * placeholder + text
    elif 'center' in text_align:
        half, mod = divmod(box_width - text_width, 2)
        if mod == 0:
            text = half * placeholder + text + half * placeholder
        else:
            text = half * placeholder + text + (half + 1) * placeholder
    else:
        raise ValueError(f'Text align: {text_align} is unsupported!')

    return placeholder * margin + text + placeholder * margin

def pybox(
        texts: str | list[str],           # The texts in box
        title: str = '',                  # The title of box, any string
        title_style: str = 'normal',      # ['normal', 'bold', 'italic']
        title_align: str = 'innercenter', # ['inner', 'up', 'down'] conbined with ['left', 'right', 'center']
        title_color: str = '',            # ['green', 'yellow', 'blue', 'black', 'cyan', 'magenta', 'red', 'white']
        box_color: str = '',              # ['green', 'yellow', 'blue', 'black', 'cyan', 'magenta', 'red', 'white']
        box_style: str = 'normal',        # ['normal', 'double', 'bold', 'round']
        box_width: int = 0,               # The width of the box, 0 is auto
        color: str = '',                  # ['green', 'yellow', 'blue', 'black', 'cyan', 'magenta', 'red', 'white']
        style: str = 'normal',            # ['normal', 'bold', 'italic']
        align: str = 'center',            # ['center', 'left', 'right']
        margin: int = 3) -> None:         # The margin of the box
    # Set box style
    NORMAL = ' ┌┐└┘│─'
    DOUBLE = ' ╔╗╚╝║═'
    BOLD   = ' ┏┓┗┛┃━'
    ROUND  = ' ╭╮╰╯│─'

    if box_style == 'normal':
        STYLE = NORMAL
    elif box_style == 'double':
        STYLE = DOUBLE
    elif box_style == 'bold':
        STYLE = BOLD
    elif box_style == 'round':
        STYLE = ROUND

    AUTO_WIDTH = False
    if box_width == 0:
        MAX_BOX_LEN = 100
        AUTO_WIDTH = True

    # Set box color
    SPACE       = text_style(STYLE[0], color=box_color)
    UPLEFT      = text_style(STYLE[1], color=box_color)
    UPRIGHT     = text_style(STYLE[2], color=box_color)
    DOWNLEFT    = text_style(STYLE[3], color=box_color)
    DOWNRIGHT   = text_style(STYLE[4], color=box_color)
    COL         = text_style(STYLE[5], color=box_color)
    ROW         = text_style(STYLE[6], color=box_color)

    # Set title style
    title_width = text_width(title)
    print_title = 'inner' in title_align and title
    title = text_style(title, title_style, title_color)

    # Calculate the width of the box
    if isinstance(texts, str):
        texts = [texts]
    if AUTO_WIDTH:
        for text in texts:
            box_width = max(text_width(text), box_width)
        box_width = min(MAX_BOX_LEN, box_width)
    box_width += 2 * margin

    # Draw the top of the box
    if 'up' in title_align:
        box_up = UPLEFT + __text_line__(title, title_width, box_width, title_align, ROW, 0) + UPRIGHT
    else:
        box_up = UPLEFT + box_width * ROW + UPRIGHT
    print(box_up)
    for _ in range(0, int(margin / 3)):
        print(COL + box_width * SPACE + COL)

    # Print the texts in box
    if print_title:
        print(COL + __text_line__(title, title_width, box_width, title_align, SPACE, margin) + COL)
    for text in texts:
        if len(text) == 0:
            print(COL + SPACE * box_width + COL)
            continue
        text = text_wrap(text, box_width)
        for text_line in text:
            content = text_style(text_line[0], style, color)
            width = text_line[1]
            print(COL + __text_line__(content, width, box_width, align, SPACE, margin) + COL)

    # Draw the bottom of the box
    if 'down' in title_align:
        box_up = DOWNLEFT + __text_line__(title, title_width, box_width, title_align, ROW, 0) + DOWNRIGHT
    else:
        box_up = DOWNLEFT + box_width * ROW + DOWNRIGHT
    for _ in range(0, int(margin / 3)):
        print(COL + box_width * SPACE + COL)
    print(box_up)
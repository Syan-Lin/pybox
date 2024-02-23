from pyboxmaker.boxmaker import box

if __name__ == '__main__':
    text = [
        '✨ A CLI Box Maker in Python ✨',
        '',
        '✅ Support Emoji ',
        '✅ 支持中英文输入',
        '✅ 支持自定义颜色',
        '✅ 支持自定义样式',
    ]
    title = 'PyBoxMaker v1.0'
    title_style = 'normal'
    title_align = 'upleft'
    title_color = 'green'
    text_color = 'yellow'
    box_style = 'round'
    box_color = 'green'

    box(text, title,
        margin=3,
        box_color=box_color,
        box_style=box_style,
        title_align=title_align,
        title_style=title_style,
        title_color=title_color,
        color=text_color)
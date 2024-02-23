from pyboxmaker import box

if __name__ == '__main__':
    # Default
    box('Hello PyBoxMaker!')

    # Text has 3 types: ['normal', 'bold', 'italic']
    # Title Align has 9 types:
    #   ['upleft',    'upcenter',    'upright']
    #   ['downleft',  'downcenter',  'downright']
    #   ['innerleft', 'innercenter', 'innerright']
    # Add a bold green title
    box('Hello PyBoxMaker!',
        title='PyBoxMaker',
        title_align='upleft',
        title_style='bold',
        title_color='green')

    # Box has 4 types: ['normal', 'round', 'double', 'bold']
    # Set box to 'round'
    box('Hello PyBoxMaker!', box_style='round')

    # Set the box color to red and text color to yellow
    box('Hello PyBoxMaker!', box_color='red', color='yellow')

    # Multiple lines are supported, empty stands for a new line
    box(['Hello PyBoxMaker', '', 'This is a box maker, enjoy!'], style='italic')

    # Text align has 3 types: ['left', 'center', 'right']
    # Margin is also supported
    box(['Hello PyBoxMaker', '', 'This is a box maker, enjoy!'],
        style='italic', margin=3, align='left')

    # You can also set the width of the box, the default width(0) is auto
    box(['Hello PyBoxMaker', '', 'This is a box maker, 随意使用吧！'],
        style='italic', margin=3, align='left', box_width=16)

    # Give it a try!
    box(['🌅 When grace is lost from life, come with a burst of song.', '',
         '当生命失去恩宠，请惠我以欢歌。'], title='Rabindranath Tagore',
         title_align='downright', margin=3, align='left', title_color='yellow',
         box_style='double', color='green')
from colorama import Fore, Style
import re

def is_chinese(ch: str) -> bool:
    return '\u4e00' <= ch <= '\u9fff'

def is_english(ch) -> bool:
    return (u'\u0041'<= ch <= u'\u005a') or (u'\u0061'<= ch <= u'\u007a')

def is_tab(ch) -> bool:
    return re.match('[\t\n\r\b\a\f]', ch) != None

def is_emoji(ch):
    return re.match("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    u"\U00002702-\U000027B0"
                    u"\U000024C2-\U0001F251"
                    "]+", ch, flags=re.UNICODE) != None

def text_width(text: str) -> int:
    width = 0
    for ch in text:
        if is_chinese(ch) or is_emoji(ch):
            width += 2
        elif is_tab(ch):
            pass
        else:
            width += 1
    return width

def extract_words(text: str) -> list[tuple[str, int]]:
    '''
    Automatically split words from mixed Chinese and English strings

    Args:
        text:  The string to be extracted

    Return:
        words: The list of tuples of the word and its width
    '''
    begin = 0
    words = []
    eng_word = False
    for i, ch in enumerate(text):
        if is_chinese(ch) or is_emoji(ch):
            if eng_word:
                eng_word = False
                words.append((text[begin:i], i - begin))
            words.append((ch, 2))
        elif is_english(ch):
            if not eng_word:
                begin = i
            eng_word = True
        elif is_tab(ch):
            if eng_word:
                eng_word = False
                words.append((text[begin:i], i - begin))
        else:
            if eng_word:
                eng_word = False
                words.append((text[begin:i], i - begin))
            words.append((ch, 1))

        if i == len(text) - 1 and eng_word:
            words.append((text[begin:i+1], i + 1 - begin))
    return words

def lstrip(line: str, width: int) -> tuple[str, int]:
    begin = 0
    for ch in line:
        if not ch.isspace():
            break
        begin += 1
    return (line[begin:], width - begin)

def text_wrap(text: str, width: int) -> list[tuple[str, int]]:
    '''
    Automatically wrap text so that the width of each line does not exceed `width`

    Args:
        text:  The string to be wraped
        width: Max width of a line

    Return:
        lines: The list of tuples of the line and its width
    '''
    lines = []
    words = extract_words(text)
    line = ''
    text_width = 0
    for i, word in enumerate(words):
        text_width += word[1]
        if text_width > width:
            text_line = lstrip(line, text_width - word[1])
            if text_line[0]:
                lines.append(text_line)
            line = ''
            text_width = word[1]
        line += word[0]
        if i == len(words) - 1:
            text_line = lstrip(line, text_width)
            if text_line[0]:
                lines.append(text_line)
    return lines

def text_style(text: str, style: str = '', color: str = ''):
    '''
    Add ansi escape sequences to string

    Args:
        text:
        style: 'bold' or 'italic'
        color: ['green', 'yellow', 'blue', 'black', 'cyan', 'magenta', 'red', 'white']
    '''
    if style == 'bold':
        text = '\x1b[1m' + text
    elif style == 'italic':
        text = '\x1b[3m' + text

    if color == 'green':
        text = Fore.GREEN + text
    elif color == 'yellow':
        text = Fore.YELLOW + text
    elif color == 'blue':
        text = Fore.BLUE + text
    elif color == 'black':
        text = Fore.BLACK + text
    elif color == 'cyan':
        text = Fore.CYAN + text
    elif color == 'magenta':
        text = Fore.MAGENTA + text
    elif color == 'red':
        text = Fore.RED + text
    elif color == 'white':
        text = Fore.WHITE + text

    return text + Style.RESET_ALL

if __name__ == '__main__':
    # unit test
    assert is_chinese('中')
    assert is_chinese('中文')
    assert not is_chinese('!')
    assert not is_chinese('!@')
    assert not is_chinese('e')
    assert not is_chinese('eng')

    assert is_english('e')
    assert is_english('eng')
    assert not is_english('中')
    assert not is_english('中文')
    assert not is_english('!')
    assert not is_english('!@')

    assert is_tab('\t')
    assert is_tab('\n')
    assert is_tab('\r')
    assert is_tab('\b')
    assert is_tab('\a')
    assert is_tab('\f')
    assert not is_tab('e')
    assert not is_tab('eng')
    assert not is_tab('中')
    assert not is_tab('中文')
    assert not is_tab('!')
    assert not is_tab('!@')

    assert is_emoji('😊')
    assert is_emoji('✨')
    assert is_emoji('✋')
    assert is_emoji('🐲')
    assert not is_emoji('A')
    assert not is_emoji('!')
    assert not is_emoji('!@')
    assert not is_emoji('ABC')

    text = 'hello你好world!@'
    words = extract_words(text)
    assert words[0] == ('hello', 5)
    assert words[1] == ('你', 2)
    assert words[2] == ('好', 2)
    assert words[3] == ('world', 5)
    assert words[4] == ('!', 1)
    assert words[5] == ('@', 1)

    text = 'hello 你好 world ! @'
    words = extract_words(text)
    assert words[0] == ('hello', 5)
    assert words[1] == (' ', 1)
    assert words[2] == ('你', 2)
    assert words[3] == ('好', 2)
    assert words[4] == (' ', 1)
    assert words[5] == ('world', 5)
    assert words[6] == (' ', 1)
    assert words[7] == ('!', 1)
    assert words[8] == (' ', 1)
    assert words[9] == ('@', 1)

    text = 'hello你好world!@'
    lines = text_wrap(text, 5)
    assert lines[0][0] == 'hello'
    assert lines[0][1] == 5
    assert lines[1][0] == '你好'
    assert lines[1][1] == 4
    assert lines[2][0] == 'world'
    assert lines[2][1] == 5
    assert lines[3][0] == '!@'
    assert lines[3][1] == 2

    text = 'hello 你好 world ! @'
    lines = text_wrap(text, 5)
    assert lines[0][0] == 'hello'
    assert lines[0][1] == 5
    assert lines[1][0] == '你好'
    assert lines[1][1] == 4
    assert lines[2][0] == 'world'
    assert lines[2][1] == 5
    assert lines[3][0] == '! @'
    assert lines[3][1] == 3

    text = 'hello你好world!@'
    lines = text_wrap(text, 10)
    assert lines[0][0] == 'hello你好'
    assert lines[0][1] == 9
    assert lines[1][0] == 'world!@'
    assert lines[1][1] == 7

    text = 'hello 你好 world ! @'
    lines = text_wrap(text, 10)
    assert lines[0][0] == 'hello 你好'
    assert lines[0][1] == 10
    assert lines[1][0] == 'world ! @'
    assert lines[1][1] == 9

    text = 'hello\n  ! @你好\t world'
    lines = text_wrap(text, 10)
    assert lines[0][0] == 'hello  ! @'
    assert lines[0][1] == 10
    assert lines[1][0] == '你好 world'
    assert lines[1][1] == 10

    print(text_style('hello', 'bold', 'red'))
    print(text_style('hello', 'italic', 'blue'))
    print(text_style('hello', '', 'yellow'))
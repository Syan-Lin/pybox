# utils for pybox

def is_chinese(ch: str) -> bool:
    return '\u4e00' <= ch <= '\u9fff'

def is_english(ch) -> bool:
    return (u'\u0041'<= ch <= u'\u005a') or (u'\u0061'<= ch <= u'\u007a')

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
        if is_chinese(ch):
            if eng_word:
                eng_word = False
                words.append((text[begin:i], i-begin))
            words.append((ch, 2))
        elif is_english(ch):
            if not eng_word:
                begin = i
            eng_word = True
        elif ch.isspace():
            if eng_word:
                eng_word = False
                words.append((text[begin:i], i-begin))
            words.append((ch, 1))
        else:
            if eng_word:
                eng_word = False
                words.append((text[begin:i], i-begin))
            words.append((ch, 1))

        if i == len(text) - 1 and eng_word:
            words.append((text[begin:i+1], i-begin))
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
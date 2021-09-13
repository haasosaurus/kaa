class Colors:
    kaa = 0xfed142
    error = 0x7c0a02
    success = 0x4cbb17


class Chars:
    U2060 = '\u2060'
    """WORD JOINER"""

    U202F = '\u202f'
    """NARROW NO-BREAK SPACE"""

    U00A0 = '\u00a0'
    """NO BREAK SPACE"""

    U2007 = '\u2007'
    """FIGURE SPACE"""

    U2011 = '\u2011'
    """NON-BREAKING HYPHEN"""

    U200B = '\u200b'
    """ZERO WIDTH SPACE"""
    BLANK = U200B
    """ZERO WIDTH SPACE"""
    EMPTY = U200B
    """ZERO WIDTH SPACE"""

    U3000 = '\u3000'
    """IDEOGRAPHIC SPACE"""

    EXPANDER = f'{U3000 * 30}{U200B}'
    NEWLINE_LEFT = f'{U200B}\n'
    NEWLINE_RIGHT = f'{U200B}\n{U200B}'
    SPACE = f'{U00A0}{U202F}'
    BLANK_LINE = f'{U200B}\n{U200B}\n'

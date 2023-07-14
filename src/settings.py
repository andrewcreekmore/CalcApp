"""
settings.py: formatting + positional data
- element sizes, text attributes, layout styling
- color definitions, button metadata, key mappings 
"""

# basic layout sizing
WINDOW_SIZE = (400, 700)
STD_MAIN_ROWS = 7
STD_MAIN_COLUMNS = 4
PROG_MAIN_ROWS = 7
PROG_MAIN_COLUMNS = 4

# text attributes
FONT = 'Helvetica'
MODE_SWITCH_FONT_SIZE = 14
STD_OUTPUT_FONT_SIZE = 70
STD_NORMAL_FONT_SIZE = 32
PROG_OUTPUT_FONT_SIZE = 70
PROG_NORMAL_FONT_SIZE = 32

# color definitions
BLACK = '#000000'
WHITE = '#EEEEEE'
LIGHT_GRAY = '#E8E8E8'
DARK_GRAY = '#505050'
GRAY = '#D9D9D9'
TITLE_BAR_HEX_COLORS = {
    'dark': 0x00000000,
    'light': 0x00EEEEEE
}

COLORS = {
    'lightGray': {'fg': ('#505050', '#D4D4D2'), 'hover': ('#686868', '#EFEFED'), 'text': ('white', 'black')},
    'darkGray': {'fg': ('#D4D4D2', '#505050'), 'hover': ('#EFEFED', '#686868'), 'text': ('black', 'white')},        
    'orange': {'fg': '#FF9500', 'hover': '#FFB143', 'text': ('black', 'white')},    
    'orangeHighlight': {'fg': 'white', 'hover': 'white', 'text': ('black', 'FF9500')}       
}

# button layout definitions

BUTTON_STYLING = { 'gap': 0.5, 'corner-radius': 0}

NUMBER_BUTTONS = {
    '.': {'column': 2, 'row': 6, 'span': 1},
    0: {'column': 0, 'row': 6, 'span': 2},
    1: {'column': 0, 'row': 5, 'span': 1},
    2: {'column': 1, 'row': 5, 'span': 1},
    3: {'column': 2, 'row': 5, 'span': 1},
    4: {'column': 0, 'row': 4, 'span': 1},
    5: {'column': 1, 'row': 4, 'span': 1},
    6: {'column': 2, 'row': 4, 'span': 1},
    7: {'column': 0, 'row': 3, 'span': 1},
    8: {'column': 1, 'row': 3, 'span': 1},
    9: {'column': 2, 'row': 3, 'span': 1},
}

OPERATOR_BUTTONS = {
    'clear': {'column': 0, 'row': 2, 'text': 'AC', 'image path': None},
    'invert': {'column': 1, 'row': 2, 'text': '', 'image path': {'light': 'images/invertLight.png', 'dark': 'images/invertDark.png'}},
    'percent': {'column': 2, 'row': 2, 'text': '%', 'image path': None}
    }

MATH_BUTTONS = {
    '/': {'column': 3, 'row': 2, 'character': '', 'image path': {'light': 'images/divideLight.png', 'dark': 'images/divideDark.png'}},
    '*': {'column': 3, 'row': 3, 'character': 'x', 'image path': None},
    '-': {'column': 3, 'row': 4, 'character': '-', 'image path': None},
    '=': {'column': 3, 'row': 6, 'character': '=', 'image path': None},
    '+': {'column': 3, 'row': 5, 'character': '+', 'image path': None}
}

# map of input keycodes to corresponding CalcApp function and argument
KEY_FUNCTION_MAP = {
    'Delete': {'function': 'clearAll'},
    'BackSpace': {'function': 'clearLast'},
    'Return': {'function': 'mathPressed', 'arg': '='},
    'plus': {'function': 'mathPressed', 'arg': '+'},
    'minus': {'function': 'mathPressed', 'arg': '-'},
    'asterisk': {'function': 'mathPressed', 'arg': '*'},
    'slash': {'function': 'mathPressed', 'arg': '/'},
    'period': {'function': 'numberPressed', 'arg': '.'},
    '0': {'function': 'numberPressed', 'arg': '0'},
    '1': {'function': 'numberPressed', 'arg': '1'},
    '2': {'function': 'numberPressed', 'arg': '2'},
    '3': {'function': 'numberPressed', 'arg': '3'},
    '4': {'function': 'numberPressed', 'arg': '4'},
    '5': {'function': 'numberPressed', 'arg': '5'},
    '6': {'function': 'numberPressed', 'arg': '6'},
    '7': {'function': 'numberPressed', 'arg': '7'},
    '8': {'function': 'numberPressed', 'arg': '8'},
    '9': {'function': 'numberPressed', 'arg': '9'}
}
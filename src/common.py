"""
common.py: mode definitions, formatting + positional data
- element sizes, text attributes, layout styling
- color definitions, button metadata, key mappings 
"""

from enum import Enum

class CalcMode(Enum):
    """ Represents possible modes of Calculator operation. """
    CM_STANDARD = "Standard"
    CM_PROGRAMMING = "Programming"
    CM_SCIENTIFIC = "Scientific"

# basic layout sizing
WINDOW_SIZE = (400, 700)
NUM_ROWS_COLUMNS = {
    'Standard': {'rows': 7, 'columns': 4},
    'Programming': {'rows': 8, 'columns': 5},
    'Scientific': {'rows': 9, 'columns': 5}
} 

# text attributes
FONT = 'Helvetica'
MODE_SWITCH_FONT_SIZE = 14
FONT_SIZES = {
    'Standard': {'largerFont': 70, 'smallerFont': 32},
    'Programming': {'largerFont': 70, 'smallerFont': 32},
    'Scientific': {'largerFont': 70, 'smallerFont': 32}
}

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

BUTTON_STYLING = { 'gap': 0.5, 'corner-radius': 0}

# map of input keycodes to corresponding Calculator function and argument
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

# standard CalcMode: button layout definitions
STANDARD_NUMBER_BUTTONS = {
    '.': {'column': 2, 'row': 6, 'span': 1, 'state': 'normal'},
    0: {'column': 1, 'row': 6, 'span': 1, 'state': 'normal'},
    1: {'column': 0, 'row': 5, 'span': 1, 'state': 'normal'},
    2: {'column': 1, 'row': 5, 'span': 1, 'state': 'normal'},
    3: {'column': 2, 'row': 5, 'span': 1, 'state': 'normal'},
    4: {'column': 0, 'row': 4, 'span': 1, 'state': 'normal'},
    5: {'column': 1, 'row': 4, 'span': 1, 'state': 'normal'},
    6: {'column': 2, 'row': 4, 'span': 1, 'state': 'normal'},
    7: {'column': 0, 'row': 3, 'span': 1, 'state': 'normal'},
    8: {'column': 1, 'row': 3, 'span': 1, 'state': 'normal'},
    9: {'column': 2, 'row': 3, 'span': 1, 'state': 'normal'},
}

STANDARD_OPERATOR_BUTTONS = {
    'clear': {'column': 1, 'row': 2, 'text': 'AC', 'image path': None},
    'backspace':{'column': 2, 'row': 2, 'text': '\u232B', 'image path': None},
    'invert': {'column': 0, 'row': 6, 'text': '', 'image path': {'light': 'images/invertLight.png', 'dark': 'images/invertDark.png'}},
    'percent': {'column': 0, 'row': 2, 'text': '%', 'image path': None}
    }

STANDARD_MATH_BUTTONS = {
    '/': {'column': 3, 'row': 2, 'character': '', 'image path': {'light': 'images/divideLight.png', 'dark': 'images/divideDark.png'}},
    '*': {'column': 3, 'row': 3, 'character': 'x', 'image path': None},
    '-': {'column': 3, 'row': 4, 'character': '-', 'image path': None},
    '=': {'column': 3, 'row': 6, 'character': '=', 'image path': None},
    '+': {'column': 3, 'row': 5, 'character': '+', 'image path': None}
}

# programming CalcMode: button layout definitions
PROG_NUMBER_BUTTONS = {
    'A': {'column': 0, 'row': 2, 'span': 1, 'state': 'disabled'},
    'B': {'column': 0, 'row': 3, 'span': 1, 'state': 'disabled'},
    'C': {'column': 0, 'row': 4, 'span': 1, 'state': 'disabled'},
    'D': {'column': 0, 'row': 5, 'span': 1, 'state': 'disabled'},
    'E': {'column': 0, 'row': 6, 'span': 1, 'state': 'disabled'},
    'F': {'column': 0, 'row': 7, 'span': 1, 'state': 'disabled'},
    '.': {'column': 3, 'row': 7, 'span': 1, 'state': 'normal'},
    0: {'column': 2, 'row': 7, 'span': 1, 'state': 'normal'},
    1: {'column': 1, 'row': 6, 'span': 1, 'state': 'normal'},
    2: {'column': 2, 'row': 6, 'span': 1, 'state': 'normal'},
    3: {'column': 3, 'row': 6, 'span': 1, 'state': 'normal'},
    4: {'column': 1, 'row': 5, 'span': 1, 'state': 'normal'},
    5: {'column': 2, 'row': 5, 'span': 1, 'state': 'normal'},
    6: {'column': 3, 'row': 5, 'span': 1, 'state': 'normal'},
    7: {'column': 1, 'row': 4, 'span': 1, 'state': 'normal'},
    8: {'column': 2, 'row': 4, 'span': 1, 'state': 'normal'},
    9: {'column': 3, 'row': 4, 'span': 1, 'state': 'normal'},
    '(': {'column': 1, 'row': 3, 'span': '1', 'state': 'normal'},
    ')': {'column': 2, 'row': 3, 'span': '1', 'state': 'normal'}
}

PROG_OPERATOR_BUTTONS = {
    'clear': {'column': 3, 'row': 2, 'text': 'AC', 'image path': None},
    'backspace':{'column': 4, 'row': 2, 'text': '\u232B', 'image path': None},
    'invert': {'column': 1, 'row': 7, 'text': '', 'image path': {'light': 'images/invertLight.png', 'dark': 'images/invertDark.png'}},
    'percent': {'column': 3, 'row': 3, 'text': '%', 'image path': None},
    'leftShift': {'column': 1, 'row': 2, 'text': '<<', 'image path': None},
    'rightShift': {'column': 2, 'row': 2, 'text': '>>', 'image path': None}
    }

PROG_MATH_BUTTONS = {
    '/': {'column': 4, 'row': 3, 'character': '', 'image path': {'light': 'images/divideLight.png', 'dark': 'images/divideDark.png'}},
    '*': {'column': 4, 'row': 4, 'character': 'x', 'image path': None},
    '-': {'column': 4, 'row': 5, 'character': '-', 'image path': None},
    '=': {'column': 4, 'row': 7, 'character': '=', 'image path': None},
    '+': {'column': 4, 'row': 6, 'character': '+', 'image path': None}
}

# scientific CalcMode: button layout definitions
SCI_NUMBER_BUTTONS = {
    '.': {'column': 3, 'row': 8, 'span': 1, 'state': 'normal'},
    0: {'column': 2, 'row': 8, 'span': 1, 'state': 'normal'},
    1: {'column': 1, 'row': 7, 'span': 1, 'state': 'normal'},
    2: {'column': 2, 'row': 7, 'span': 1, 'state': 'normal'},
    3: {'column': 3, 'row': 7, 'span': 1, 'state': 'normal'},
    4: {'column': 1, 'row': 6, 'span': 1, 'state': 'normal'},
    5: {'column': 2, 'row': 6, 'span': 1, 'state': 'normal'},
    6: {'column': 3, 'row': 6, 'span': 1, 'state': 'normal'},
    7: {'column': 1, 'row': 5, 'span': 1, 'state': 'normal'},
    8: {'column': 2, 'row': 5, 'span': 1, 'state': 'normal'},
    9: {'column': 3, 'row': 5, 'span': 1, 'state': 'normal'}
}

SCI_SPECIAL_NUMBER_BUTTONS = {
    f'\N{MATHEMATICAL ITALIC SMALL PI}': {'column': 1, 'row': 2, 'span': '1', 'state': 'normal', 'value': '3.14159'},
    f'\N{MATHEMATICAL ITALIC SMALL E}': {'column': 2, 'row': 2, 'span': '1', 'state': 'normal', 'value': '2.71828'},
    f'\N{MEDIUM LEFT PARENTHESIS ORNAMENT}': {'column': 1, 'row': 4, 'span': '1', 'state': 'normal', 'value': '('},
    f'\N{MEDIUM RIGHT PARENTHESIS ORNAMENT}': {'column': 2, 'row': 4, 'span': '1', 'state': 'normal', 'value': ')'}
}

SCI_OPERATOR_BUTTONS = {
    'clear': {'column': 3, 'row': 2, 'text': 'AC', 'image path': None},
    'backspace':{'column': 4, 'row': 2, 'text': '\u232B', 'image path': None},
    'invert': {'column': 1, 'row': 8, 'text': '', 'image path': {'light': 'images/invertLight.png', 'dark': 'images/invertDark.png'}},
    'percent': {'column': 3, 'row': 4, 'text': '%', 'image path': None},
    'exponentiate': {'column': 1, 'row': 3, 'text': f'\N{LATIN SMALL LETTER X}\N{SUPERSCRIPT LATIN SMALL LETTER N}', 'image path': None, 'font': 'italic'},
    'square': {'column': 2, 'row': 3, 'text': f'\N{LATIN SMALL LETTER X}\N{SUPERSCRIPT TWO}', 'image path': None, 'font': 'italic'},
    'log': {'column': 0, 'row': 7, 'text': 'log', 'image path': None, 'font': None},
    'ln': {'column': 0, 'row': 8, 'text': 'ln', 'image path': None, 'font': None}
    }

SCI_MATH_BUTTONS = {
    '/': {'column': 4, 'row': 4, 'character': '', 'image path': {'light': 'images/divideLight.png', 'dark': 'images/divideDark.png'}},
    '*': {'column': 4, 'row': 5, 'character': 'x', 'image path': None},
    '-': {'column': 4, 'row': 6, 'character': '-', 'image path': None},
    '=': {'column': 4, 'row': 8, 'character': '=', 'image path': None},
    '+': {'column': 4, 'row': 7, 'character': '+', 'image path': None}
}

# button layout data lookup table
BUTTON_LAYOUT_DATA = {
    'Standard': {'numberButtons': STANDARD_NUMBER_BUTTONS, 'mathButtons': STANDARD_MATH_BUTTONS, 'operatorButtons': STANDARD_OPERATOR_BUTTONS},
    'Programming': {'numberButtons': PROG_NUMBER_BUTTONS, 'mathButtons': PROG_MATH_BUTTONS, 'operatorButtons': PROG_OPERATOR_BUTTONS},
    'Scientific': {'numberButtons': SCI_NUMBER_BUTTONS, 'mathButtons': SCI_MATH_BUTTONS, 'operatorButtons': SCI_OPERATOR_BUTTONS}
}

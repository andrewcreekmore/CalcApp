"""
settings.py: formatting + positional data
- element sizes, text attributes, layout styling
- button positions, color definitions
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

NUMBER_POSITIONS = {
    '.': {'col': 2, 'row': 6, 'span': 1},
    0: {'col': 0, 'row': 6, 'span': 2},
    1: {'col': 0, 'row': 5, 'span': 1},
    2: {'col': 1, 'row': 5, 'span': 1},
    3: {'col': 2, 'row': 5, 'span': 1},
    4: {'col': 0, 'row': 4, 'span': 1},
    5: {'col': 1, 'row': 4, 'span': 1},
    6: {'col': 2, 'row': 4, 'span': 1},
    7: {'col': 0, 'row': 3, 'span': 1},
    8: {'col': 1, 'row': 3, 'span': 1},
    9: {'col': 2, 'row': 3, 'span': 1},
}
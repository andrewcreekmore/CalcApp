"""
calculator.py: 
- primary app logic / entry-point
- creates instance of CalcApp and loops
"""

import enum
import customtkinter as ctk
import darkdetect
try: # windows only
    from ctypes import windll, byref, sizeof, c_int
except:
    pass
from settings import *


class CalcMode(enum.IntEnum):
    """ modes of operation """
    Standard = 1
    Programming = 2


class CalcApp(ctk.CTk):
    """ main / core application class """
    
    def __init__(self, isDark):
        """ """

        # setup window
        super().__init__(fg_color = (WHITE, BLACK)) 
        self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}') # default window size
        self.resizable(False, False) # non-resizable

        # hide title and icon
        self.title('')
        self.iconbitmap('images/empty.ico')

        # set light/dark based on system settings
        ctk.set_appearance_mode(f'{"dark" if isDark else "light"}')
        self.changeTitleBarColor(isDark) # change title bar to match rest of window

        # default to Standard operating mode
        self.currentMode = CalcMode(1)

        # run
        self.mainloop()

    def changeTitleBarColor(self, isDark):
        """ """
        try: # windows only
            HWND = windll.user32.GetParent(self.winfo_id()) # get current window
            DWMA_ATTRIBUTE = 35 # target color attribute of window's title bar
            TITLE_BAR_COLOR = TITLE_BAR_HEX_COLORS['dark'] if isDark else TITLE_BAR_HEX_COLORS['light'] # define color
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMA_ATTRIBUTE, byref(c_int(TITLE_BAR_COLOR)), sizeof(c_int)) # set attribute
        except:
            pass


if __name__ == '__main__':
    CalcApp(darkdetect.isDark())
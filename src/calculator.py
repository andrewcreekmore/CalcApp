"""
calculator.py: 
- primary app logic / entry-point
- creates instance of CalcApp, which runs main loop
"""

from enum import Enum
import customtkinter as ctk
import darkdetect
from PIL import Image
try: # windows only
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

from buttons import *
from settings import *

class CalcMode(Enum):
    """ Represents possible modes of CalcApp operation. """
    CM_STANDARD = "Standard"
    CM_PROGRAMMING = "Programming"


class CalcApp(ctk.CTk):
    """ Main / core application class. """
    
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
        self.currentMode = CalcMode('Standard')
        
        # setup grid layout
        self.rowconfigure(list(range(STD_MAIN_ROWS)), weight = 1, uniform= 'a')
        self.columnconfigure(list(range(STD_MAIN_COLUMNS)), weight = 1, uniform= 'a')

        # data
        self.resultString = ctk.StringVar(value = '0')
        self.lastOperationString = ctk.StringVar(value = '')

        # setup mode menu
        ModeOptionMenu(self)

        # setup widgets
        match self.currentMode:
            case CalcMode.CM_STANDARD:
                self.initStandardWidgets()

            case CalcMode.CM_PROGRAMMING:
                self.initProgrammingWidgets()

        # run
        self.mainloop()

    def changeTitleBarColor(self, isDark):
        """ If on Windows platform, changes app's title bar color to match rest of window. """
        try: # windows only
            HWND = windll.user32.GetParent(self.winfo_id()) # get current window
            DWMA_ATTRIBUTE = 35 # target color attribute of window's title bar
            TITLE_BAR_COLOR = TITLE_BAR_HEX_COLORS['dark'] if isDark else TITLE_BAR_HEX_COLORS['light'] # define color
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMA_ATTRIBUTE, byref(c_int(TITLE_BAR_COLOR)), sizeof(c_int)) # set attribute
        except:
            pass

    def initStandardWidgets(self):
        """ Initializes Standard CalcMode widgets: OutputLabels, operator buttons, number buttons. """

        # setup widget fonts
        mainWidgetFont = ctk.CTkFont(family = FONT, size = STD_NORMAL_FONT_SIZE)
        resultFont = ctk.CTkFont(family = FONT, size = STD_OUTPUT_FONT_SIZE)

        # setup output labels
        OutputLabel(self, 0, 'se', mainWidgetFont, self.lastOperationString) # last entered operation
        OutputLabel(self, 1, 'e', resultFont, self.resultString) # result

        # setup clear (AC) button
        Button(parent = self,
               text = OPERATOR_BUTTONS['clear']['text'],
               function = self.clear,
               column = OPERATOR_BUTTONS['clear']['column'],
               row = OPERATOR_BUTTONS['clear']['row'],
               font = mainWidgetFont)
        
        # setup percentage (%) button
        Button(parent = self,
               text = OPERATOR_BUTTONS['percent']['text'],
               function = self.percentage,
               column = OPERATOR_BUTTONS['percent']['column'],
               row = OPERATOR_BUTTONS['percent']['row'],
               font = mainWidgetFont)
        
        # setup invert (+/-) button
        # create image
        invertImage = ctk.CTkImage( # 'dark' img contrasts with 'light' bg, & vice versa
            light_image = Image.open(OPERATOR_BUTTONS['invert']['image path']['dark']),
            dark_image = Image.open(OPERATOR_BUTTONS['invert']['image path']['light']))
        # create button
        ImageButton(parent = self, 
                    text = OPERATOR_BUTTONS['invert']['text'],
                    image = invertImage,
                    function = self.invert,
                    column = OPERATOR_BUTTONS['invert']['column'],
                    row = OPERATOR_BUTTONS['invert']['row'])
        
        # setup number buttons
        for number, data in NUMBER_BUTTONS.items():
            NumberButton(
                parent = self,
                text = number,
                function = self.numberPressed,
                column = data['column'],
                span = data['span'],
                row = data['row'],
                font = mainWidgetFont)
            
        # setup math buttons
        for operator, data in MATH_BUTTONS.items():
            if data['image path']: # if image assigned (CM_STANDARD: division button only)
                # create image
                divisionImage = ctk.CTkImage( # 'dark' img contrasts with 'light' bg, & vice versa
                    light_image = Image.open(data['image path']['dark']),
                    dark_image = Image.open(data['image path']['light']))
                # create button
                MathImageButton(
                    parent = self,
                    operator = operator,
                    function = self.mathPressed,
                    column = data['column'],
                    row = data['row'],
                    image = divisionImage)
                
            else: # no image assigned
                MathButton(
                    parent = self,
                    text = data['character'],
                    operator = operator,
                    function = self.mathPressed,
                    column = data['column'],
                    row = data['row'],
                    font = mainWidgetFont)
        
    def clear(self):
        """ """
        print('cleared!')

    def percentage(self):
        """ """
        print('percentage!')

    def invert(self):
        """ """
        print('invert!')

    def numberPressed(self, value):
        """ """
        print(value)

    def mathPressed(self, value):
        """ """
        print(value)

    def initProgrammingWidgets(self):
        """ Initializes Programming CalcMode widgets... """
        pass


class ModeOptionMenu(ctk.CTkOptionMenu):
    """ Drop-down menu allowing CalcApp operating modes (i.e., Standard, Programming). """

    def __init__(self, parent):
        """ """
        super().__init__(master = parent, width = 105, fg_color = (LIGHT_GRAY, DARK_GRAY), button_color = COLORS['orange']['fg'], button_hover_color = COLORS['orange']['hover'],
                         text_color = (BLACK, WHITE), font = ctk.CTkFont(family = FONT, size = MODE_SWITCH_FONT_SIZE),
                         values = [e.value for e in CalcMode], command = self.modeOptionMenuCallback)
        self.place(relx = 0.05, rely = 0.02, anchor = 'nw') # place in top-right; northeast anchor

    def modeOptionMenuCallback(self, selection):
        """ Sets CalcApp's currentMode variable to be equivalent to the selected string menu option. """
        self.master.currentMode = CalcMode(selection)

        match self.master.currentMode:

            case CalcMode.CM_STANDARD:
                print("switched to Standard CalcMode!")
                self.master.initStandardWidgets()

            case CalcMode.CM_PROGRAMMING:
                print("switched to Programming CalcMode!")
                self.master.initProgrammingWidgets()


class DebugCheckModeButton(ctk.CTkButton):
    """ DEBUG ONLY: returns CalcApp's currentMode. """

    def __init__(self, parent):
        """ """
        super().__init__(master = parent, text = "DEBUG: get currentMode", command = self.printCurrentMode)
        self.grid(column = 0, columnspan = 4, row = 4)

    def printCurrentMode(self):
        print(self.master.currentMode.value)


class OutputLabel(ctk.CTkLabel):
    """ Label representing calculator output: last performed operation, operation result, etc. """
    def __init__(self, parent, row, anchor, font, stringVar):

        super().__init__(master = parent, font = font, textvariable = stringVar)
        self.grid(column = 0, columnspan = 4, row = row, sticky = anchor, padx = 15)


if __name__ == '__main__':
    CalcApp(darkdetect.isDark)

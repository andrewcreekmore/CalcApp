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
    CM_SCIENTIFIC = "Scientific"


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

        # data
        self.cumulativeInputDisplayString = ctk.StringVar(value = '0')
        self.cumulativeOperationDisplayString = ctk.StringVar(value = '')
        self.cumulativeNumInputList = []
        self.lastCumulativeNumInputList = []
        self.cumulativeOperationList = []

        # data flags
        self.lastInputWasNum = False
        self.lastOperationWasEval = False
        self.skipAddingLastNumInputToOperation = False

        # create menu frame + mode menu
        self.menuFrame = Frame(self)
        self.menuFrame.pack(side = 'top', anchor = 'w', padx = 10) # place in top-left
        ModeOptionMenu(self.menuFrame) # create CalcMode option menu w/ menuFrame parent
        
        # create default (Standard mode) activeFrame + setup its widgets
        self.initStandardWidgets()
        
        # setup keyboard event binding
        keyEventSequence = '<KeyPress>'
        self.bind(keyEventSequence, self.keyEventHandle)

        # run
        self.mainloop()

    def keyEventHandle(self, event):
        """ Calls appropriate function based on input keyboard event. """

        lookupKey = event.keysym
        if 'arg' in KEY_FUNCTION_MAP[lookupKey]:
            getattr(self, KEY_FUNCTION_MAP[lookupKey]['function'])(KEY_FUNCTION_MAP[lookupKey]['arg'])
            
        else: # no args passed
            getattr(self, KEY_FUNCTION_MAP[lookupKey]['function'])()

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
        
        # setup active frame (container for current CalcMode's contents)
        self.activeFrame = Frame(self)
        self.activeFrame.pack(side = 'bottom', expand = True, fill = 'both', anchor = 's')

        # setup widget fonts
        mainWidgetFont = ctk.CTkFont(family = FONT, size = STD_NORMAL_FONT_SIZE)
        resultFont = ctk.CTkFont(family = FONT, size = STD_OUTPUT_FONT_SIZE)

        # setup frame grid layout
        self.activeFrame.rowconfigure(list(range(STD_MAIN_ROWS)), weight = 1, uniform = 'a')
        self.activeFrame.columnconfigure(list(range(STD_MAIN_COLUMNS)), weight = 1, uniform = 'a')
        
        # setup output labels
        OutputLabel(self.activeFrame, 0, 'se', mainWidgetFont, self.cumulativeOperationDisplayString) # last entered operation
        OutputLabel(self.activeFrame, 1, 'e', resultFont, self.cumulativeInputDisplayString) # result

        # setup clear (AC) button
        Button(parent = self.activeFrame,
            text = OPERATOR_BUTTONS['clear']['text'],
            function = self.clearAll,
            column = OPERATOR_BUTTONS['clear']['column'],
            row = OPERATOR_BUTTONS['clear']['row'],
            font = mainWidgetFont)
        
        # setup percentage (%) button
        Button(parent = self.activeFrame,
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
        ImageButton(parent = self.activeFrame, 
                    text = OPERATOR_BUTTONS['invert']['text'],
                    image = invertImage,
                    function = self.invert,
                    column = OPERATOR_BUTTONS['invert']['column'],
                    row = OPERATOR_BUTTONS['invert']['row'])
        
        # setup number buttons
        for number, data in NUMBER_BUTTONS.items():
            NumberButton(
                parent = self.activeFrame,
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
                    parent = self.activeFrame,
                    operator = operator,
                    function = self.mathPressed,
                    column = data['column'],
                    row = data['row'],
                    image = divisionImage)
                
            else: # no image assigned
                MathButton(
                    parent = self.activeFrame,
                    text = data['character'],
                    operator = operator,
                    function = self.mathPressed,
                    column = data['column'],
                    row = data['row'],
                    font = mainWidgetFont)
        
    def clearAll(self):
        """ Resets output and data to default state. """

        # clear display output - set to defaults
        self.cumulativeInputDisplayString.set(0) 
        self.cumulativeOperationDisplayString.set('')

        # clear data
        self.cumulativeNumInputList.clear()
        self.cumulativeOperationList.clear()

    def clearLast(self):
        """ Removes single most recent input (number or operator). """

        # if last input was '=', do nothing
        if self.lastOperationWasEval and not self.lastInputWasNum:
            return 

        if self.lastInputWasNum:
            # remove last num input from data
            *self.cumulativeNumInputList,_ = self.cumulativeNumInputList
            
            # update display output
            cumulativeNumInputToDisplay = ''.join(self.cumulativeNumInputList) 
            self.cumulativeInputDisplayString.set(cumulativeNumInputToDisplay)

        else: # last input was non-(=) math operator

            # remove last operator input from data
            *self.cumulativeOperationList,_ = self.cumulativeOperationList

            # update relevant data
            self.cumulativeNumInputList = list(self.lastCumulativeNumInputList) # restore previous, prior to clear when math operated pressed
            self.skipAddingLastNumInputToOperation = True # avoiding duplicates

            # update display output
            self.cumulativeOperationDisplayString.set(' '.join(self.cumulativeOperationList))
        
    def percentage(self):
        """ Divides current number input / result value by 100. """

        if self.cumulativeNumInputList:
            # get current number input as float
            currentNumInputFloat = float(''.join(self.cumulativeNumInputList))

            # convert to percentage
            currentPercentFloat = currentNumInputFloat / 100
            self.cumulativeNumInputList[0] = str(currentPercentFloat)

            # update display output
            self.cumulativeInputDisplayString.set(''.join(self.cumulativeNumInputList))

    def invert(self):
        """ Flips sign of current number input / result. """

        # get current number input as str
        currentNumInput = ''.join(self.cumulativeNumInputList)

        def flipSign(numInputStr):
            """ Helper function: given a string representing a number, return its sign inverse as a string. """
            return ' '.join(str(-int(each)) for each in numInputStr.split())

        if currentNumInput:
            self.cumulativeNumInputList[0] = flipSign(self.cumulativeNumInputList[0])
            # update display output
            self.cumulativeInputDisplayString.set(''.join(self.cumulativeNumInputList))

    def numberPressed(self, value):
        """ Handles numerical input. """

        # each input value added to list as string
        self.cumulativeNumInputList.append(str(value))
        # from list, convert to displayed format (w/ new inputs added to end of list (positioned to right of last input)) 
        cumulativeNumInputToDisplay = ''.join(self.cumulativeNumInputList) 
        self.cumulativeInputDisplayString.set(cumulativeNumInputToDisplay)

        # update tracking data
        self.lastInputWasNum = True

    def mathPressed(self, value):
        """
        Handles math operator input. 
        This includes processing duplicate inputs and additional (but different) operator inputs back to back.
        """

        # check if last input was also a non-evaluating math operation
        if not self.lastInputWasNum and not self.lastOperationWasEval:
            if self.cumulativeOperationList[-1] == value:
                return # can't input same operation twice
            
            else:
                # replace last input operation with new operation
                self.clearLast()
                self.skipAddingLastNumInputToOperation = False

                # update data
                self.cumulativeOperationList.append(value)
                self.cumulativeNumInputList.clear()
                
                # update display output
                self.cumulativeInputDisplayString.set('')
                self.cumulativeOperationDisplayString.set(' '.join(self.cumulativeOperationList))
    
                return

        # get the cumulative number input + append to cumulative operation list
        currentCumulativeNumInput = ''.join(self.cumulativeNumInputList)
        if not self.skipAddingLastNumInputToOperation:
            self.cumulativeOperationList.append(currentCumulativeNumInput)

        else: # reset flag
            self.skipAddingLastNumInputToOperation = False

        # update input tracking flag
        self.lastInputWasNum = False 

        if currentCumulativeNumInput: # do not proceed if no num input exists
            if value != '=': # special case

                # update data
                self.cumulativeOperationList.append(value)
                self.lastCumulativeNumInputList = list(self.cumulativeNumInputList) # store in case operation is canceled
                self.cumulativeNumInputList.clear()
                self.lastOperationWasEval = False
                
                # update display output
                self.cumulativeInputDisplayString.set('')
                self.cumulativeOperationDisplayString.set(' '.join(self.cumulativeOperationList))

            else: # value was '='
                # get operation and evaluate
                currentCumulativeOperation = ''.join(self.cumulativeOperationList)
                currentResult = eval(currentCumulativeOperation)

                # format evaluated result, if float
                if isinstance(currentResult, float):
                    
                    # if result is a float, but has no fractional part, convert to int
                    if currentResult.is_integer():
                        currentResult = int(currentResult)
                    
                    else: # has fractional part; manage precision
                        currentResult = round(currentResult, 3)
                        # TODO: expose precision as a variable in an app settings menu

                # update data
                self.lastOperationWasEval = True
                self.cumulativeOperationList.clear()
                self.cumulativeNumInputList = [str(currentResult)] # empty + update by creating new w/ result

                # update display output
                self.cumulativeInputDisplayString.set(currentResult)
                self.cumulativeOperationDisplayString.set(currentCumulativeOperation)

    def initProgrammingWidgets(self):
        """ Initializes Programming CalcMode widgets... """
        pass

    def initScientificWidgets(self):
        """ Initializes Scientific CalcMode widgets... """
        pass


class ModeOptionMenu(ctk.CTkOptionMenu):
    """ Drop-down menu allowing CalcApp operating modes (i.e., Standard, Programming, Scientific). """

    def __init__(self, parent):
        """ """
        super().__init__(master = parent, width = 105, fg_color = (LIGHT_GRAY, DARK_GRAY), button_color = COLORS['orange']['fg'], button_hover_color = COLORS['orange']['hover'],
                         text_color = (BLACK, WHITE), font = ctk.CTkFont(family = FONT, size = MODE_SWITCH_FONT_SIZE),
                         values = [e.value for e in CalcMode], command = self.modeOptionMenuCallback)
        self.pack()

    def modeOptionMenuCallback(self, selection):
        """ Sets CalcApp's currentMode variable to be equivalent to the selected string menu option, if != current. """

        rootApp = self.master.master
        if rootApp.currentMode != CalcMode(selection):
            rootApp.currentMode = CalcMode(selection)

            match rootApp.currentMode:
                case CalcMode.CM_STANDARD:
                    print("switched to Standard CalcMode!")
                    rootApp.initStandardWidgets()

                case CalcMode.CM_PROGRAMMING:
                    print("switched to Programming CalcMode!")
                    rootApp.activeFrame.destroy()
                    rootApp.initProgrammingWidgets()

                case CalcMode.CM_SCIENTIFIC:
                    print("switched to Scientific CalcMode!")
                    rootApp.activeFrame.destroy()
                    rootApp.initScientificWidgets()


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
        """ """
        super().__init__(master = parent, font = font, textvariable = stringVar)
        self.grid(column = 0, columnspan = 4, row = row, sticky = anchor, padx = 15)


class Frame(ctk.CTkFrame):
    """ Represents a generic container for widgets. """
    def __init__(self, parent):
        """ """
        super().__init__(master = parent, fg_color = "transparent")


if __name__ == '__main__':
    CalcApp(darkdetect.isDark)

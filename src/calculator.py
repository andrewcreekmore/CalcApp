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
        #self.currentMode = CalcMode('Standard')
        # DEBUG
        self.currentMode = CalcMode('Programming')

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
        self.initCommonStandardWidgets()
        # DEBUG
        self.initProgrammingWidgets()
        
        # setup keyboard event binding
        keyEventSequence = '<KeyPress>'
        self.bind(keyEventSequence, self.keyEventHandle)

        # run
        self.mainloop()

    def keyEventHandle(self, event):
        """ Calls appropriate function based on input keyboard event. """

        lookupKey = event.keysym
        try:
            if 'arg' in KEY_FUNCTION_MAP[lookupKey]:
                getattr(self, KEY_FUNCTION_MAP[lookupKey]['function'])(KEY_FUNCTION_MAP[lookupKey]['arg'])
                
            else: # no args passed
                getattr(self, KEY_FUNCTION_MAP[lookupKey]['function'])()
        except:
            pass

    def changeTitleBarColor(self, isDark):
        """ If on Windows platform, changes app's title bar color to match rest of window. """
        try: # windows only
            HWND = windll.user32.GetParent(self.winfo_id()) # get current window
            DWMA_ATTRIBUTE = 35 # target color attribute of window's title bar
            TITLE_BAR_COLOR = TITLE_BAR_HEX_COLORS['dark'] if isDark else TITLE_BAR_HEX_COLORS['light'] # define color
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMA_ATTRIBUTE, byref(c_int(TITLE_BAR_COLOR)), sizeof(c_int)) # set attribute
        except:
            pass

    def initCommonStandardWidgets(self):
        """ Initializes common/Standard-CalcMode widgets: OutputLabels + number, operator, and math buttons. """

        # setup active frame (container for current CalcMode's contents)
        self.activeFrame = Frame(self)
        self.activeFrame.pack(side = 'bottom', expand = True, fill = 'both', anchor = 's')

        # setup widget fonts
        self.smallerWidgetFont = ctk.CTkFont(family = FONT, size = FONT_SIZES[self.currentMode.value]['smallerFont'])
        self.largerWidgetFont = ctk.CTkFont(family = FONT, size = FONT_SIZES[self.currentMode.value]['largerFont'])

        # setup frame grid layout
        self.activeFrame.rowconfigure(list(range(NUM_ROWS_COLUMNS[self.currentMode.value]['rows'])), weight = 1, uniform = 'a')
        self.activeFrame.columnconfigure(list(range(NUM_ROWS_COLUMNS[self.currentMode.value]['columns'])), weight = 1, uniform = 'a')
        
        # setup output labels
        OutputLabel(self.activeFrame, 0, 'se', self.smallerWidgetFont, self.cumulativeOperationDisplayString) 
        OutputLabel(self.activeFrame, 1, 'e', self.largerWidgetFont, self.cumulativeInputDisplayString)

        # get mode-relevant button layout data
        NUMBER_BUTTONS = BUTTON_LAYOUT_DATA[self.currentMode.value]['numberButtons']
        OPERATOR_BUTTONS = BUTTON_LAYOUT_DATA[self.currentMode.value]['operatorButtons']
        MATH_BUTTONS = BUTTON_LAYOUT_DATA[self.currentMode.value]['mathButtons']

        # setup number buttons
        for number, data in NUMBER_BUTTONS.items():
            NumberButton(
                parent = self.activeFrame,
                text = number,
                function = self.numberPressed,
                column = data['column'],
                span = data['span'],
                row = data['row'],
                font = self.smallerWidgetFont,
                state = data['state'])

        # setup clear (AC) button
        Button(parent = self.activeFrame,
            text = OPERATOR_BUTTONS['clear']['text'],
            function = self.clearAll,
            column = OPERATOR_BUTTONS['clear']['column'],
            row = OPERATOR_BUTTONS['clear']['row'],
            font = self.smallerWidgetFont)
        
        # setup backspace button
        Button(parent = self.activeFrame,
            text = OPERATOR_BUTTONS['backspace']['text'],
            function = self.clearLast,
            column = OPERATOR_BUTTONS['backspace']['column'],
            row = OPERATOR_BUTTONS['backspace']['row'],
            font = self.smallerWidgetFont)
        
        # setup percentage (%) button
        Button(parent = self.activeFrame,
            text = OPERATOR_BUTTONS['percent']['text'],
            function = self.percentage,
            column = OPERATOR_BUTTONS['percent']['column'],
            row = OPERATOR_BUTTONS['percent']['row'],
            font = self.smallerWidgetFont)
        
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
                    font = self.smallerWidgetFont)
        
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
            if len(self.cumulativeNumInputList) > 0:
                *self.cumulativeNumInputList,_ = self.cumulativeNumInputList

                # handle case where -(num value) had all numvalues backspaced out, so only '-' left in list
                if len(self.cumulativeNumInputList) == 1 and self.cumulativeNumInputList[0] == '-':
                    self.cumulativeNumInputList.clear()
                    self.cumulativeInputDisplayString.set(0)
                
                # if still values present, update display output appropriately
                if len(self.cumulativeNumInputList) > 0:
                    cumulativeNumInputToDisplay = ''.join(self.cumulativeNumInputList) 
                    self.cumulativeInputDisplayString.set(cumulativeNumInputToDisplay)
                else: # if now empty, set to 0 default display value
                    self.cumulativeInputDisplayString.set('0')

        # if there's been no input at all, do nothing
        elif len(self.cumulativeOperationList) == 0: 
            return

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

        if currentNumInput: # if input exists
            isPositive = currentNumInput[0].isnumeric()
            # flip sign + update data
            flippedNumInput = list('-' + currentNumInput) if isPositive else list(currentNumInput[1:])
            self.cumulativeNumInputList = flippedNumInput
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
        if not self.lastInputWasNum and not self.lastOperationWasEval and ''.join(self.cumulativeNumInputList): # do not proceed if no num input exists:
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
                
                # get operation
                currentCumulativeOperation = ''.join(self.cumulativeOperationList)
                # parse
                currentCumulativeOperation = self.parseParentheses(currentCumulativeOperation)
                # evaluate
                try:
                    currentResult = eval(currentCumulativeOperation)
                # error catching
                except (SyntaxError, KeyError):
                    self.cumulativeInputDisplayString.set('ERROR')
                    return

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

    def parseParentheses(self, currentCumulativeOperation):
        """ 
        Parses operation for instances of parentheses without adjacent operators, e.g., '2(3)' or '2(3)2.'
        When such instances are found, inserts '*' operator before/after as needed.
        """

        outerIndex = 0 
        while outerIndex < 2:
            isLeft = outerIndex # first pass = false, 2nd pass = true
            parenth = '(' if isLeft else ')'
            # get indices of all parenth instances
            parenthList = [pos for pos, char in enumerate(currentCumulativeOperation) if char == parenth]
            parenthCount = len(parenthList)

            innerIndex = 0
            while innerIndex < parenthCount:
                # if '(', ensure there's a left-adjacent value to check
                if ((parenthList[innerIndex] > 0) if isLeft else True): 
                    if currentCumulativeOperation[parenthList[innerIndex] - 1].isnumeric(): # left-adjacent numeric?
                        # if ')', ensure there's a right-adjacent value to check
                        if (True if isLeft else (parenthList[innerIndex] != len(currentCumulativeOperation) - 1)): 
                            if currentCumulativeOperation[parenthList[innerIndex] + 1].isnumeric(): # right-adjacent numeric?
                                # no adjacent operator found; insert '*' appropriately
                                posAdjustment = 0 if isLeft else 1
                                slice = parenthList[innerIndex] + posAdjustment
                                currentCumulativeOperation = currentCumulativeOperation[:slice] + '*' + currentCumulativeOperation[slice:]
                                # adjust parenthList indices to account for the insertion
                                if innerIndex != parenthCount: # if not at end
                                    for each in range(0, parenthCount):
                                        parenthList[each] += 1
                innerIndex += 1
            outerIndex += 1

        return currentCumulativeOperation

    def initProgrammingWidgets(self):
        """ Initializes Programming CalcMode widgets... """
        
        # setup bit-shift operator (<< / >>) buttons
        Button(parent = self.activeFrame,
            text = PROG_OPERATOR_BUTTONS['leftShift']['text'],
            function = self.percentage,
            column = PROG_OPERATOR_BUTTONS['leftShift']['column'],
            row = PROG_OPERATOR_BUTTONS['leftShift']['row'],
            font = self.smallerWidgetFont)
        Button(parent = self.activeFrame,
            text = PROG_OPERATOR_BUTTONS['rightShift']['text'],
            function = self.percentage,
            column = PROG_OPERATOR_BUTTONS['rightShift']['column'],
            row = PROG_OPERATOR_BUTTONS['rightShift']['row'],
            font = self.smallerWidgetFont)

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
        """ 
        Sets CalcApp's currentMode variable to be equivalent to the selected string menu option, if != current.
        Destroy current activeFrame, inits a new one + all common/standard widgets, then any mode-specific widgets.
        """

        rootApp = self.master.master
        if rootApp.currentMode != CalcMode(selection):
            rootApp.currentMode = CalcMode(selection)

            rootApp.activeFrame.destroy()
            rootApp.initCommonStandardWidgets()

            if rootApp.currentMode != CalcMode.CM_STANDARD:

                match rootApp.currentMode:
                    case CalcMode.CM_PROGRAMMING:
                        rootApp.initProgrammingWidgets()

                    case CalcMode.CM_SCIENTIFIC:
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

        # column span depends on CalcMode
        currentMode = self.master.master.currentMode.value
        colSpan = NUM_ROWS_COLUMNS[currentMode]['columns']
        self.grid(column = 0, columnspan = colSpan, row = row, sticky = anchor, padx = 15)


class Frame(ctk.CTkFrame):
    """ Represents a generic container for widgets. """
    def __init__(self, parent):
        """ """
        super().__init__(master = parent, fg_color = "transparent")


if __name__ == '__main__':
    CalcApp(darkdetect.isDark)

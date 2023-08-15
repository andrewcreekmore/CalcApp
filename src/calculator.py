"""
calculator.py: 
- handles domain-specific app functionality
- creates/manages two output displays + mode-dependent buttons
"""

import customtkinter as ctk
from decimal import Decimal
import math
from PIL import Image

from buttons import *


class Calculator():
    """ Main / core functionality class. """

    def __init__(self, parentApp):
        """ """

        self.app = parentApp

        # set calculator operating mode
        self.currentMode = CalcMode(self.app.userSettings['defaultCalcMode'])

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

        # create default (Standard mode) activeFrame + setup its widgets
        self.initCommonStandardWidgets()
        # create any additional widgets if applicable
        if self.currentMode is not CalcMode.CM_STANDARD:
            modeInitFunction = self.initProgrammingWidgets if self.currentMode is CalcMode.CM_PROGRAMMING else self.initScientificWidgets
            modeInitFunction()

    def clearAll(self):
        """ Resets output and data to default state. """

        # clear display output - set to defaults
        self.cumulativeInputDisplayString.set('0') 
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
                    self.cumulativeInputDisplayString.set('0')
                
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
        # format any instances of exponentiation prior to displaying
        formattedDisplayString = cumulativeNumInputToDisplay.replace('**', '^')
        self.cumulativeInputDisplayString.set(formattedDisplayString)

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
                except (SyntaxError, KeyError, TypeError):
                    self.cumulativeInputDisplayString.set('ERROR')
                    return

                # update data
                self.lastOperationWasEval = True
                self.cumulativeOperationList.clear()
                self.cumulativeNumInputList = [str(currentResult)] # empty + update by creating new w/ result
                
                # update display output: result
                resultDisplayStr = self.getResultDisplayStr(currentResult)
                self.cumulativeInputDisplayString.set(resultDisplayStr)
                # update display output: cumulative operation
                operationDisplayStr = self.getOperationDisplayStr(currentCumulativeOperation)
                self.cumulativeOperationDisplayString.set(operationDisplayStr)

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
            parenthPosList = [pos for pos, char in enumerate(currentCumulativeOperation) if char is parenth]
            parenthCount = len(parenthPosList)

            for innerIndex, parenthPos in enumerate(parenthPosList):
                if (parenthPos > 0): # ensure there's a left-adjacent value to check
                    if currentCumulativeOperation[parenthPos - 1].isnumeric(): # left-adjacent numeric?
                        # ensure there's a right-adjacent value to check
                        if (parenthPos != len(currentCumulativeOperation) - 1):
                            if currentCumulativeOperation[parenthPos + 1].isnumeric(): # right-adjacent numeric?
                                # no adjacent operator found; insert '*' appropriately
                                posAdjustment = 0 if isLeft else 1
                                slice = parenthPos + posAdjustment
                                currentCumulativeOperation = currentCumulativeOperation[:slice] + '*' + currentCumulativeOperation[slice:]
                                # adjust parenthList indices to account for the insertion
                                if innerIndex != parenthCount: # if not at end
                                    for eachIndex in range(0, parenthCount):
                                            parenthPosList[eachIndex] += 1
            outerIndex += 1

        return currentCumulativeOperation

    def initCommonStandardWidgets(self):
        """ Initializes common/Standard-CalcMode widgets: OutputLabels + number, operator, and math buttons. """

        # setup active frame (container for current CalcMode's contents)
        self.activeFrame = ctk.CTkFrame(self.app, fg_color = 'transparent')
        self.activeFrame.pack(side = 'bottom', expand = True, fill = 'both', anchor = 's')

        # setup widget fonts
        self.smallerWidgetFont = ctk.CTkFont(family = FONT, size = FONT_SIZES[self.currentMode.value]['smallerFont'])
        self.largerWidgetFont = ctk.CTkFont(family = FONT, size = FONT_SIZES[self.currentMode.value]['largerFont'])

        # setup frame grid layout
        self.activeFrame.rowconfigure(list(range(NUM_ROWS_COLUMNS[self.currentMode.value]['rows'])), weight = 1, uniform = 'a')
        self.activeFrame.columnconfigure(list(range(NUM_ROWS_COLUMNS[self.currentMode.value]['columns'])), weight = 1, uniform = 'a')
        
        # setup output labels
        OutputDisplayLabel(self.activeFrame, 0, 'se', self.smallerWidgetFont, self.cumulativeOperationDisplayString, self.currentMode) 
        OutputDisplayLabel(self.activeFrame, 1, 'e', self.largerWidgetFont, self.cumulativeInputDisplayString, self.currentMode)

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
        
        # setup widget fonts
        self.smallestWidgetFont = ctk.CTkFont(family = FONT, size = 18)
        self.smallestWidgetFontItalic = ctk.CTkFont(family = FONT, size = 18, slant = 'italic')
        
        # setup special number buttons
        for specialNumber, data in SCI_SPECIAL_NUMBER_BUTTONS.items():
            SpecialNumberButton(parent = self.activeFrame,
                                text = specialNumber,
                                value = data['value'],
                                function = self.numberPressed,
                                column = data['column'],
                                span = data['span'],
                                row = data['row'],
                                font = self.smallerWidgetFont,
                                state = data['state'])
            
        # setup unique operator buttons
        funcLookup = {'exponentiate': self.exponentiate, 'square': self.square, 'log': lambda: self.logarithms(10), 'ln': lambda: self.logarithms()}
        uniqueOperators = ['exponentiate', 'square', 'log', 'ln']
        for operator, data in SCI_OPERATOR_BUTTONS.items():
            if operator in uniqueOperators:
                Button(parent = self.activeFrame,
                    text = data['text'],
                    function = funcLookup[operator],
                    column = data['column'],
                    row = data['row'],
                    font = self.smallestWidgetFontItalic if data['font'] == 'italic' else self.smallestWidgetFont)

    def exponentiate(self):
        """ Appends an '**' operator to cumulative input, and updates display output with a formatted ('^') version. """

        if self.cumulativeNumInputList: # ensure input exists
            self.cumulativeNumInputList.append('**')
        
            # update display output
            displayString = ''.join(self.cumulativeNumInputList)
            formattedDisplayString = displayString.replace('**', '^')
            self.cumulativeInputDisplayString.set(formattedDisplayString)

    def square(self):
        """ Appends an '*' operator + the current cumulative input *to* the current cumulative input, and forces an immediate evaluation. """

        if self.cumulativeNumInputList: # ensure input exists
            cumulativeInputStr = ''.join(self.cumulativeNumInputList)
            self.cumulativeNumInputList.append('*' + cumulativeInputStr)

            # evaluate immediately
            self.mathPressed('=')

    def logarithms(self, base = None):
        """ Evaluates base 10 or natural logarithm, rounds to keep result on screen, and updates data/display. """

        if self.cumulativeNumInputList: # ensure input exists
            try:
                # get current number input as float
                currentNumInputFloat = float(''.join(self.cumulativeNumInputList))
                # evaluate log10 at maximum visible digits
                logFunc = math.log10 if base == 10 else math.log
                logResult = self.getResultDisplayStr(logFunc(currentNumInputFloat))

            # error catching
            except (SyntaxError, KeyError, ValueError):
                    self.cumulativeInputDisplayString.set('ERROR')
                    return

            # update data
            self.cumulativeNumInputList[0] = str(logResult)
            # update display output
            self.cumulativeInputDisplayString.set(str(logResult))

    def roundToMaxDigits(self, currentResult):
        """ Formats evaluated result prior to display so as not to exceed window width. """

        # format evaluated result, if float
        if isinstance(currentResult, float):
            
            # if result is a float, but has no fractional part, convert to int
            if currentResult.is_integer():
                currentResult = int(currentResult)
  
        numDigits = len(str(currentResult))
        maxDigits = 8 if currentResult < 0 else 9
        if numDigits > maxDigits:
            allowedDigits = maxDigits - len(str(int(currentResult)))
            currentResult = '{:.{precision}f}'.format(currentResult, precision = allowedDigits)
  
        return currentResult
    
    def convertToSciNotation(self, value):
        """ """
        
        # determine num digits in value, exponent once converted
        valueStr = str(value)
        numDigitsValue = len(valueStr)
        exponent = numDigitsValue - 1
        numDigitsExponent = len(str(exponent))
        
        # 9 is max visible in window; less 2 to account for 'e+' display
        maxDigits = 8 if value < 0 else 9
        allowedDigits = maxDigits - 2 - numDigitsExponent
        
        # get sci notation at allowed max visible digits
        sciNotation = f"{Decimal(f'{value}'):.{allowedDigits}E}"
        
        # break up and format return string
        significand = sciNotation.split('E')[0].rstrip('0').rstrip('.')
        exponentSign = sciNotation.split('E')[1][0]
        exponentValue = sciNotation.split('E')[1][1:]
        strippedExponent = exponentValue.strip('0')
        
        return significand + 'e' + exponentSign + strippedExponent
              
    def getResultDisplayStr(self, currentResult) -> str:
        """ Formats string of evaluated result prior to display so as not to exceed window width. """
        
        # format evaluated result, if float
        if isinstance(currentResult, float):
            
            # if result is a float, but has no fractional part, convert to int
            if currentResult.is_integer():
                currentResult = int(currentResult)
                
        # determine length; convert to sci notation for display if necessary
        numDigits = len(str(currentResult))
        maxDigits = 8 if currentResult < 0 else 9
        if numDigits > maxDigits:
            
                sciNotation =  f'%E' % Decimal(f'{currentResult}')
                exponentSign = sciNotation.split('E')[1][0]
                exponentValue = sciNotation.split('E')[1][1:]
                
                if exponentValue == '00':
                    currentResult = self.roundToMaxDigits(currentResult)
                elif exponentSign == '-' and exponentValue[1] < '4':
                    currentResult = self.roundToMaxDigits(currentResult)
                else:
                    currentResult = self.convertToSciNotation(currentResult)
        
        return str(currentResult)  
    
    def getOperationDisplayStr(self, currentOperation) -> str:
        """ """     
        
        # format any instances of exponentiation
        formattedOperationStr = currentOperation.replace('**', '^')
        
        return formattedOperationStr
        

class OutputDisplayLabel(ctk.CTkLabel):
    """ Label representing calculator output: last performed operation, operation result, etc. """
    def __init__(self, parent, row, anchor, font, stringVar, currentMode):
        """ """
        super().__init__(master = parent, font = font, textvariable = stringVar)

        # column span depends on CalcMode
        colSpan = NUM_ROWS_COLUMNS[currentMode.value]['columns']
        self.grid(column = 0, columnspan = colSpan, row = row, sticky = anchor, padx = 15)
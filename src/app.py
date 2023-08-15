"""
app.py: 
- general application logic / entry-point
- creates instance of App, which:
--- initializes/manages a window + user settings
--- sets up app menu options (mode drop-down, settings)
--- captures relevant keyboard events
--- creates instance of Calculator + runs main loop
"""

import customtkinter as ctk
import darkdetect
from functools import partial
import json
import os
from pathlib import Path
try: # windows only
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

from calculator import *


class App(ctk.CTk):
    """ Main / core application class. """
    
    def __init__(self):
        """ """

        # setup window
        super().__init__(fg_color = (WHITE, BLACK)) 
        self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}') # default window size
        self.resizable(False, False) # non-resizable

        # hide title and icon
        self.title('')
        self.iconbitmap('images/empty.ico')

        # get user settings data; if not defined, create w/ defaults
        self.loadUserSettings()

        # set light/dark appearance
        ctk.set_appearance_mode(self.userSettings['appearance'])
        isDarkMode = True if self.userSettings['appearance'] == 'dark' else False
        self.changeTitleBarColor(isDarkMode) # change title bar to match rest of window

        # set always on top + app opacity
        self.wm_attributes('-topmost', self.userSettings['onTop'])
        self.wm_attributes('-alpha', self.userSettings['opacity'])

        # create menu frame + menu buttons
        self.menuFrame = ctk.CTkFrame(self, fg_color = 'transparent')
        self.menuFrame.pack(side = 'top', fill = 'x') # place along top of app window
        
        # create CalcMode option menu w/ menuFrame parent
        ModeOptionMenu(
            parent = self.menuFrame, 
            mode = self.userSettings['defaultCalcMode'], 
            command = self.modeOptionMenuCallback) 
        
        # create settings menu button
        SettingsButton(parent = self.menuFrame, command = self.initSettingsMenu) 

        # create calculator instance
        self.calculator = Calculator(self)

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

    def setAppearanceSetting(self, value):
        """ Updates app appearance based on passed value and saves to appropriate user setting. """

        ctk.set_appearance_mode(value)
        isDark = True if value == 'Dark' else False
        self.exitToAppButton._hover_color = BLACK if isDark else WHITE
        self.changeTitleBarColor(isDark)
        # update corresponding persistent saved data
        self.saveUserSetting('appearance', value.lower())

    def toggleOnTopSetting(self):
        """ Flips current onTop value, sets window attribute, and updates the saved user setting accordingly. """
        newOnTop = not self.userSettings['onTop']
        self.wm_attributes('-topmost', newOnTop)
        self.saveUserSetting('onTop', newOnTop)

    def setOpacitySetting(self, value):
        """ Adjusts window opacity to the passed value, and saves the value to user settings. """

        self.wm_attributes('-alpha', value)
        self.saveUserSetting('opacity', value)

    def setDefaultModeSetting(self, value):
        """ Routes passed calcMode value to appropriate user setting. """

        self.saveUserSetting('defaultCalcMode', value)
    
    def modeOptionMenuCallback(self, selection):
        """ 
        Sets CalcApp's currentMode variable to be equivalent to the selected string menu option, if != current.
        Destroy current activeFrame, inits a new one + all common/standard widgets, then any mode-specific widgets.
        """

        calculator: Calculator = self.calculator
        if calculator.currentMode != CalcMode(selection):
            calculator.currentMode = CalcMode(selection)

            calculator.activeFrame.destroy()
            calculator.initCommonStandardWidgets()

            if calculator.currentMode != CalcMode.CM_STANDARD:

                match calculator.currentMode:
                    case CalcMode.CM_PROGRAMMING:
                        calculator.initProgrammingWidgets()

                    case CalcMode.CM_SCIENTIFIC:
                        calculator.initScientificWidgets()
    
    def initSettingsMenu(self):
        """ Initializes settings menu overlay widgets. """

        # invisible button filling window behind settingsMenuSubFrame, allows exiting to main app
        invisibleButtonColor = BLACK if ctk.get_appearance_mode() == 'Dark' else WHITE
        self.exitToAppButton = ctk.CTkButton(self, fg_color = 'transparent', bg_color= 'transparent', hover_color = invisibleButtonColor, text = '', width = 400, height = 700, command = self.exitSettingsMenu)
        self.exitToAppButton.place(x = 0, y = 0)

        # setup widget fonts
        self.smallerWidgetFont = ctk.CTkFont(family = FONT, size = 14)
        self.largerWidgetFont = ctk.CTkFont(family = FONT, size = 16)

        # container for actual settings menu overlay
        self.settingsMenuSubFrame = ctk.CTkFrame(self, width = 300, height = 285, border_color = (BLACK, WHITE), border_width = 2)
        self.settingsMenuSubFrame.pack_propagate(False)
        self.settingsMenuSubFrame.place(relx = 0.125, rely = 0.2)

        # create appearance setting label
        self.appearanceLabel = ctk.CTkLabel(self.settingsMenuSubFrame, text = 'Appearance:', font = self.smallerWidgetFont)
        self.appearanceLabel.pack(padx = 10, pady = 10, anchor = 'w')
        # create appearance setting button
        self.appearanceButton = ctk.CTkSegmentedButton(self.settingsMenuSubFrame, 
                                                        values=["Dark", "Light"],
                                                        command=self.setAppearanceSetting, 
                                                        font = self.smallerWidgetFont, 
                                                        selected_color = '#FF9500', 
                                                        selected_hover_color = '#FFB143')
        # set to current mode
        self.appearanceButton.set(ctk.get_appearance_mode())
        self.appearanceButton.pack()

        # create default calculator mode setting label
        self.defaultModeLabel = ctk.CTkLabel(self.settingsMenuSubFrame, text = 'Default Calculator Mode:', font = self.smallerWidgetFont)
        self.defaultModeLabel.pack(padx = 10, pady = 10, anchor = 'w')

        # create default calculator mode setting button
        self.defaultModeButton = ctk.CTkSegmentedButton(self.settingsMenuSubFrame, 
                                                        values=["Standard", "Programming", "Scientific"],
                                                        command=self.setDefaultModeSetting, 
                                                        font = self.smallerWidgetFont, 
                                                        selected_color = '#FF9500', 
                                                        selected_hover_color = '#FFB143')
        self.defaultModeButton.set(self.userSettings['defaultCalcMode'])
        self.defaultModeButton.pack()

        # create opacity setting label
        self.opacitySettingLabel = ctk.CTkLabel(self.settingsMenuSubFrame, text = 'Opacity:', font = self.smallerWidgetFont)
        self.opacitySettingLabel.pack(padx = 10, pady = 10, anchor = 'w')

        # create opacity slider
        self.opacitySlider = ctk.CTkSlider(self.settingsMenuSubFrame, width = 150, button_color = (DARK_GRAY, WHITE), button_hover_color = '#FFB143',
                                            from_ = int(0.1), to = int(1.0), command = self.setOpacitySetting)
        self.opacitySlider.set(self.userSettings['opacity'])
        self.opacitySlider.pack(padx = 15, pady = 0, anchor = 'center')

        # create always on top setting switch
        self.alwaysOnTopSwitch = ctk.CTkSwitch(self.settingsMenuSubFrame, text = 'Keep app on top', 
                                               font = self.smallerWidgetFont, command = self.toggleOnTopSetting, progress_color = '#FF9500')
        if self.userSettings['onTop']: self.alwaysOnTopSwitch.select() 
        else: self.alwaysOnTopSwitch.deselect() 
        self.alwaysOnTopSwitch.pack(padx = 10, pady = 12, anchor = 'w')

    def exitSettingsMenu(self):
        """ Cleans up when closing the settingsMenu overlay. """
        self.settingsMenuSubFrame.destroy()
        self.exitToAppButton.destroy()

    def loadUserSettings(self):
        """ Loads user settings data from external JSON file, creating w/ defaults if necessary. Updates local data accordingly. """
        
        defaultSettings = {'appearance': f'{"dark" if darkdetect.isDark else "light"}', 
                           'defaultCalcMode': 'Standard', 'onTop': False,
                           'opacity': 0.9}

        # load saved settings, if present
        settingsData = {}
        settingsFile = Path('settings.json')
        if settingsFile.is_file():
            with open('settings.json', 'r') as file:
                settingsData = json.load(file)
        else:
            with open('settings.json', 'w') as file:
                json.dump(defaultSettings, file, indent = 4)
            with open('settings.json', 'r') as file:
                settingsData = json.load(file)

        # update local settings data
        self.userSettings = settingsData

    def saveUserSetting(self, key, value):
        """ Updates a single user setting in external JSON file, as well as locally.  """

        # update persistent settings data
        fileName = 'settings.json'
        with open(fileName, 'r') as file:
            settingsData = json.load(file)
            settingsData[key] = value

        os.remove(fileName)
        with open(fileName, 'w') as file:
            json.dump(settingsData, file, indent = 4)

        # update local settings data
        self.userSettings[key] = value


class ModeOptionMenu(ctk.CTkOptionMenu):
    """ Drop-down menu allowing CalcApp operating modes (i.e., Standard, Programming, Scientific). """

    def __init__(self, parent, mode, command):
        
        super().__init__(master = parent, width = 105, fg_color = (LIGHT_GRAY, DARK_GRAY), button_color = COLORS['orange']['fg'], button_hover_color = COLORS['orange']['hover'],
                         text_color = (BLACK, WHITE), font = ctk.CTkFont(family = FONT, size = MODE_SWITCH_FONT_SIZE),
                         values = [e.value for e in CalcMode], command = command)
        self.grid(column = 0, row = 0, padx = 10)
        self.set(mode) # set drop-down menu's displayed value to be the current calculator mode (defined by user settings or defaults)


class SettingsButton(ctk.CTkButton):
    def __init__(self, parent, command):
        """ """
        super().__init__(master = parent, fg_color = "transparent", hover_color = LIGHT_GRAY, width = 1, text = "\u2699", text_color = (BLACK, WHITE), command = command)
        self.grid(column = 1, row = 0)


if __name__ == '__main__':
    App()

"""
button.py: 
- all single-function CalcApp buttons
- Button/ImageButton base classes, NumberButton, MathButton, & MathImageButton children
"""

from customtkinter import CTkButton
from settings import *

class Button(CTkButton):
    """ Represents a CTkButton base class, with generic defaults. """

    def __init__(self, parent, text, function, column, row, font, span = 1, color = 'darkGray'):
        """ """

        super().__init__(
            master = parent,
            text = text,
            command = function,
            corner_radius = BUTTON_STYLING['corner-radius'],
            font = font,
            fg_color = COLORS[color]['fg'],
            hover_color = COLORS[color]['hover'],
            text_color = COLORS[color]['text'])

        # place button
        self.grid(column = column, columnspan = span, row = row, sticky = 'nsew', padx = BUTTON_STYLING['gap'], pady = BUTTON_STYLING['gap'])


class NumberButton(Button):
    """ Represents a button for entering numerical input (0-9). Inherits from Button. """

    def __init__(self, parent, text, function, column, row, font, span, color = 'lightGray'):
        """ """

        super().__init__(
            parent = parent,
            text = text,
            function = lambda: function(text),
            column = column,
            row = row,
            font = font,
            color = color,
            span = span)


class MathButton(Button):
    """ Represents a button for selecting math operations (*, -, +, =) that can be denoted with text. Inherits from Button. """

    def __init__(self, parent, text, operator, function, column, row, font, color = 'orange'):
        """ """
    
        super().__init__(
            parent = parent,
            text = text,
            function = lambda: function(operator),
            column = column,
            row = row,
            font = font,
            color = color)


class ImageButton(CTkButton):
    """ Represents a CTkButton base class, with generic defaults and an added image variable. """

    def __init__(self, parent, image, function, column, row, text = '', color = 'darkGray'):
        """ """

        super().__init__(
            master = parent,
            text = text,
            image = image,
            command = function,
            corner_radius = BUTTON_STYLING['corner-radius'],
            fg_color = COLORS[color]['fg'],
            hover_color = COLORS[color]['hover'],
            text_color = COLORS[color]['text'])

        # place button
        self.grid(column = column, row = row, sticky = 'nsew', padx = BUTTON_STYLING['gap'], pady = BUTTON_STYLING['gap'])


class MathImageButton(ImageButton):
    """ Represents a button for selecting math operations that require an image for visual denotation. Inherits from ImageButton. """

    def __init__(self, parent, operator, function, column, row, image, color = 'orange'):
        """  """
    
        super().__init__(
            parent = parent,
            function = lambda: function(operator),
            column = column,
            row = row,
            image = image,
            color = color)
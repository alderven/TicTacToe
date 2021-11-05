import arcade

import constants


class Cell(object):
    def __init__(self, cell_id, center_x, center_y):
        """ Create Cell at (X, Y) coordinates
        :param center_x: x coordinate of Cell
        :param center_y: y coordinate of Cell
        """

        # 1. Cell Id
        self.id = cell_id

        # 2. Cell coordinates
        self.center_x = center_x
        self.center_y = center_y

        # 3. Cell size
        self.width = constants.WIDTH/3
        self.height = constants.HEIGHT/3

        # 4. "On hover" flag
        self.on_hover = False

        # 5. Text value
        self.text = None

    def draw(self, mouse_x, mouse_y, state):
        """ Draw Cell """

        # 1. Draw text if there is a text
        if self.text:
            arcade.draw_text(text=self.text, start_x=self.center_x, start_y=self.center_y, color=arcade.color.BLACK, font_size=76, anchor_x='center', anchor_y='center')

        # 2. Draw "on hover" cell
        elif state == constants.STATE_PLAYER_MAKES_TURN:
            if self.center_x-self.width/2 < mouse_x < self.center_x + self.width/2 and\
               self.center_y-self.height/2 < mouse_y < self.center_y+self.height/2:
                self.on_hover = True
                arcade.draw_rectangle_filled(center_x=self.center_x, center_y=self.center_y, width=self.width, height=self.height, color=arcade.color.LIGHT_GRAY)
            else:
                self.on_hover = False

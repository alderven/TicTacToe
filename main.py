import arcade
import arcade.gui

import helpers
import constants
from cell import Cell
from stats import Stats


class App(arcade.Window):
    def __init__(self):
        """ Initialize App """

        super().__init__(width=constants.WIDTH, height=constants.HEIGHT, title='Tic Tac Toe')

        # 1. Get statistics
        self.stats = Stats()

        # 2. Set background color
        arcade.set_background_color(arcade.color.WHITE)

        # 3. Mouse position
        self.mouse_x = 0
        self.mouse_y = 0

        # 4. Game Cells
        self.cells = []

        # 5. Game over text
        self.game_over_text = ''

        # 6. Game state
        self.state = constants.STATE_PLAYER_MAKES_TURN
        self.frames_counter = 0

        # 7. "New game" button
        button = arcade.gui.UIFlatButton(text='New game', width=110, height=40, style={'font_size': 10, 'font_color': arcade.color.BLACK, 'bg_color': arcade.color.LIGHT_GRAY, 'border_color_pressed': arcade.color.BLACK, 'border_width': 1, 'bg_color_pressed': arcade.color.GRAY})
        button.on_click = self.new_game_btn
        box = arcade.gui.UIBoxLayout()
        box.add(button.with_space_around(bottom=10))
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x='right', anchor_y='top', child=box))

        # 8. "Whose turn" text
        self.whose_turn_text = ''

        # 8. Setup new game
        self.setup()

    def setup(self):
        """ Setup new game """

        # 1. Create game Cells
        self.cells = []
        cell_id = 1
        cell_width = constants.GAME_FIELD_WIDTH/3
        cell_height = constants.GAME_FIELD_HEIGHT/3
        for i in range(3):
            for j in range(3):
                center_x = int(i * cell_width + cell_width/2)
                center_y = int(constants.GAME_FIELD_Y_START + j * cell_height + cell_height/2)
                cell = Cell(cell_id, center_x, center_y)
                self.cells.append(cell)
                cell_id += 1

        # 2. Game over text
        self.game_over_text = ''

        # 3. Game state
        self.state = constants.STATE_PLAYER_MAKES_TURN
        self.frames_counter = 0

        # 4. "Whose turn" text
        self.whose_turn_text = 'Your turn [X]...'

    def new_game_btn(self, event):
        self.setup()

    def on_update(self, delta_time):
        """ Update """

        # 1. Delay before Bot makes turn
        if self.state == constants.STATE_WAITING_FOR_BOT_TO_TURN:
            self.frames_counter += 1
            if self.frames_counter > 50:
                self.frames_counter = 0
                self.state = constants.STATE_BOT_MAKES_TURN

        # 2. Bot makes turn
        elif self.state == constants.STATE_BOT_MAKES_TURN:

            # Bot's turn
            helpers.bot_makes_turn(self.cells)
            self.state = constants.STATE_PLAYER_MAKES_TURN
            self.whose_turn_text = 'Your turn [X]...'

            # Check for bot's victory
            if helpers.check_for_victory(self.cells, 'O'):
                self.game_over_text = 'Bot win!'
                self.stats.bot_win()
                self.state = constants.STATE_WAITING_FOR_GAME_OVER

        # 3. Waiting for "Game Over" state
        if self.state == constants.STATE_WAITING_FOR_GAME_OVER:
            self.whose_turn_text = ''
            self.frames_counter += 1
            if self.frames_counter > 20:
                self.frames_counter = 0
                self.state = constants.STATE_GAME_OVER

    def on_draw(self):
        """ Render the screen """

        # 1. Start render
        arcade.start_render()

        # 2. Draw "on hover" Cells
        for cell in self.cells:
            cell.draw(mouse_x=self.mouse_x, mouse_y=self.mouse_y, state=self.state)

        # 3. Draw cells
        # Draw border
        arcade.draw_rectangle_outline(center_x=constants.GAME_FIELD_WIDTH/2, center_y=constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT/2, width=constants.GAME_FIELD_WIDTH-4, height=constants.GAME_FIELD_HEIGHT-4, color=arcade.color.BLACK, border_width=4)

        # Draw vertical lines
        arcade.draw_line(start_x=constants.GAME_FIELD_WIDTH/3, start_y=constants.GAME_FIELD_Y_START, end_x=constants.GAME_FIELD_WIDTH/3, end_y=constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT, color=arcade.color.BLACK, line_width=4)
        arcade.draw_line(start_x=constants.GAME_FIELD_WIDTH*2/3, start_y=constants.GAME_FIELD_Y_START, end_x=constants.GAME_FIELD_WIDTH*2/3, end_y=constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT, color=arcade.color.BLACK, line_width=4)

        # Draw horizontal lines
        arcade.draw_line(start_x=0, start_y=constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT/3, end_x=constants.GAME_FIELD_WIDTH, end_y=constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT/3, color=arcade.color.BLACK, line_width=4)
        arcade.draw_line(start_x=0, start_y=constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT*2/3, end_x=constants.GAME_FIELD_WIDTH, end_y=constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT*2/3, color=arcade.color.BLACK, line_width=4)

        # 4. Draw game over text
        if self.state == constants.STATE_GAME_OVER:
            arcade.draw_text(text=self.game_over_text, start_x=constants.GAME_FIELD_WIDTH/2, start_y=constants.GAME_FIELD_HEIGHT/2, color=arcade.color.RED, font_size=64, anchor_x='center')

        # 5. Draw game stat
        arcade.draw_text(text=f'Win: {self.stats.win}, Draw: {self.stats.draw}, Loose: {self.stats.loose}', start_x=constants.GAME_FIELD_WIDTH / 2, start_y=14, color=arcade.color.RED, font_size=14, anchor_x='center')

        # 6. Draw "New game" button
        self.manager.draw()

        # 7. Draw "Whose turn" text
        arcade.draw_text(text=self.whose_turn_text, start_x=30, start_y=constants.HEIGHT-27, color=arcade.color.RED, font_size=14)

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """ Called whenever the mouse moves """

        # Get mouse position
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button """

        # 1. Handle mouse press when it's a Player's turn
        if self.state == constants.STATE_PLAYER_MAKES_TURN:

            # Handle click on cells
            for cell in self.cells:
                if button == arcade.MOUSE_BUTTON_LEFT and cell.on_hover:
                    cell.text = 'X'  # Player set "X"
                    cell.on_hover = False

                    # Check for player's victory
                    if helpers.check_for_victory(self.cells, 'X'):
                        self.game_over_text = 'You win!'
                        self.stats.player_win()
                        self.state = constants.STATE_WAITING_FOR_GAME_OVER
                        break

                    # Check for draw
                    if helpers.check_for_draw(self.cells):
                        self.game_over_text = 'It\'s a draw'
                        self.stats.its_a_draw()
                        self.state = constants.STATE_WAITING_FOR_GAME_OVER
                        break

                    # Change games state to "Waiting for Bot to turn"
                    self.state = constants.STATE_WAITING_FOR_BOT_TO_TURN
                    self.whose_turn_text = 'Bot`s turn [O]...'

                    break


App()
arcade.run()

import random

import constants


def check_for_victory(cells, char):
    """ Check for victory
    :param cells: list of cells
    :param char: "X" or "O"
    :return: "Winning line" coordinates - if win
             None - not win
    """

    # 1. Get list of cells that are occupied by this char
    turns = [c.id for c in cells if c.text == char]

    # 2. Check if horizontal / vertical / diagonal lines filled
    if all([1 in turns, 2 in turns, 3 in turns]):
        x = constants.WIDTH/6
        return {'start_x': x, 'start_y': constants.GAME_FIELD_Y_START, 'end_x': x, 'end_y': constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT}
    elif all([4 in turns, 5 in turns, 6 in turns]):
        x = constants.WIDTH/6
        return {'start_x': x, 'start_y': constants.GAME_FIELD_Y_START, 'end_x': x, 'end_y': constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT}
    elif all([7 in turns, 8 in turns, 9 in turns]):
        x = constants.WIDTH*5/6
        return {'start_x': x, 'start_y': constants.GAME_FIELD_Y_START, 'end_x': x, 'end_y': constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT}
    elif all([1 in turns, 4 in turns, 7 in turns]):
        y = constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT/6
        return {'start_x': 0, 'start_y': y, 'end_x': constants.WIDTH, 'end_y': y}
    elif all([2 in turns, 5 in turns, 8 in turns]):
        y = constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT/2
        return {'start_x': 0, 'start_y': y, 'end_x': constants.WIDTH, 'end_y': y}
    elif all([3 in turns, 6 in turns, 9 in turns]):
        y = constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT-constants.GAME_FIELD_HEIGHT/6
        return {'start_x': 0, 'start_y': y, 'end_x': constants.WIDTH, 'end_y': y}
    elif all([1 in turns, 5 in turns, 9 in turns]):
        return {'start_x': 0, 'start_y': constants.GAME_FIELD_Y_START, 'end_x': constants.WIDTH, 'end_y': constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT}
    elif all([3 in turns, 5 in turns, 7 in turns]):
        return {'start_x': 0, 'start_y': constants.GAME_FIELD_Y_START+constants.GAME_FIELD_HEIGHT, 'end_x': constants.WIDTH, 'end_y': constants.GAME_FIELD_Y_START}


def check_for_draw(cells):
    """ Check for draw
    :param cells: list of cells
    :return True - it's a draw
            False - it's not a draw
    """

    # It's not a draw if there are some "empty" cells
    return not bool([c for c in cells if not c.text])


def bot_makes_turn(cells, level='normal'):
    """ Bot makes turn
    :param cells: list of cells
    :param level: AI level, can be easy|normal|hard
    """

    # 1. Get list of available cells
    available_cell_ids = [c.id for c in cells if not c.text]
    bot_turns = [c.id for c in cells if c.text == 'O']

    # 2. "Easy" level
    if level == 'easy':
        # Bot makes stupid random turns
        cell_id = random.choice(available_cell_ids)
        for cell in cells:
            if cell.id == cell_id:
                cell.text = 'O'
                return

    # 3. "Hard" level
    elif level == 'hard':
        # No chance to win
        return  # TODO: Add AI logic

    # 4. "Normal" level
    # If Bot didn't make turns yet - make turn into the center of game field or in the corners (if center is already occupied)
    if not bot_turns:
        if 5 in available_cell_ids:
            cells[4].text = 'O'  # Bot makes turn in the center of the screen
            return
        elif 1 in available_cell_ids:
            cells[0].text = 'O'  # Bot makes turn in left upper corner
            return
        elif 3 in available_cell_ids:
            cells[2].text = 'O'  # Bot makes turn in right upper corner
            return
        elif 7 in available_cell_ids:
            cells[6].text = 'O'  # Bot makes turn in left lower corner
            return
        elif 9 in available_cell_ids:
            cells[8].text = 'O'  # Bot makes turn in right lower corner
            return

    # Check what turn Bot should do in order to win
    for i in range(len(cells)):
        if not cells[i].text:
            cells[i].text = 'O'  # make bot's turn
            if check_for_victory(cells, 'O'):
                cells[i].text = 'O'
                return
            cells[i].text = None  # revert bot's turn

    # If Bot can't win - he'll check what turn to make to prevent Player's win
    for i in range(len(cells)):
        if not cells[i].text:
            cells[i].text = 'X'  # make bot's turn
            if check_for_victory(cells, 'X'):
                cells[i].text = 'O'
                return
            cells[i].text = None  # revert bot's turn

    # If player if far from win, then Bot makes turn into one of preferable cells
    if 5 in available_cell_ids:
        cells[4].text = 'O'  # Bot makes turn in the center of the screen
        return
    elif 1 in available_cell_ids:
        cells[0].text = 'O'  # Bot makes turn in left upper corner
        return
    elif 3 in available_cell_ids:
        cells[2].text = 'O'  # Bot makes turn in right upper corner
        return
    elif 7 in available_cell_ids:
        cells[6].text = 'O'  # Bot makes turn in left lower corner
        return
    elif 9 in available_cell_ids:
        cells[8].text = 'O'  # Bot makes turn in right lower corner
        return

    # If all preferable cells are occupied, make turn in any available cell
    for cell in cells:
        if not cell.text:
            cell.text = 'O'
            return

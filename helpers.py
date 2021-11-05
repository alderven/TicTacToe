def check_for_victory(cells, char):
    """ Check for victory
    :param cells: list of cells
    :param char: "X" or "O"
    :return: True - if win
             None - not win
    """

    # 1. Get list of cells that are occupied by this char
    turns = [c.id for c in cells if c.text == char]

    # 2. Check for horizontal / vertical / diagonal lines
    if all([1 in turns, 2 in turns, 3 in turns]) or\
       all([4 in turns, 5 in turns, 6 in turns]) or \
       all([7 in turns, 8 in turns, 9 in turns]) or \
       all([1 in turns, 4 in turns, 7 in turns]) or \
       all([2 in turns, 5 in turns, 8 in turns]) or \
       all([3 in turns, 6 in turns, 9 in turns]) or \
       all([1 in turns, 5 in turns, 9 in turns]) or \
       all([3 in turns, 5 in turns, 7 in turns]):
        return True


def check_for_draw(cells):
    """ Check for draw
    :param cells: list of cells
    :return True - it's a draw
            False - it's not a draw
    """

    # It's not a draw if there are some "empty" cells
    return not bool([c for c in cells if not c.text])


def bot_makes_turn(cells):
    """ Bot makes turn
    :param cells: list of cells
    """

    # 1. Get list of available cells
    available_cells = [c.id for c in cells if not c.text]
    bot_turns = [c.id for c in cells if c.text == 'O']

    # 2. If Bot didn't make turns yet - make turn into the center of game field or in the corners (if center is already occupied)
    if not bot_turns:
        if 5 in available_cells:
            cells[4].text = 'O'  # Bot makes turn in the center of the screen
            return
        elif 1 in available_cells:
            cells[0].text = 'O'  # Bot makes turn in left upper corner
            return
        elif 3 in available_cells:
            cells[2].text = 'O'  # Bot makes turn in right upper corner
            return
        elif 7 in available_cells:
            cells[6].text = 'O'  # Bot makes turn in left lower corner
            return
        elif 9 in available_cells:
            cells[8].text = 'O'  # Bot makes turn in right lower corner
            return

    # 3. Check what turn Bot should do in order to win
    for i in range(len(cells)):
        if not cells[i].text:
            cells[i].text = 'O'  # make bot's turn
            if check_for_victory(cells, 'O'):
                cells[i].text = 'O'
                return
            cells[i].text = None  # revert bot's turn

    # 4. If Bot can't win - he'll check what turn to make to prevent Player's win
    for i in range(len(cells)):
        if not cells[i].text:
            cells[i].text = 'X'  # make bot's turn
            if check_for_victory(cells, 'X'):
                cells[i].text = 'O'
                return
            cells[i].text = None  # revert bot's turn

    # 5. If player if far from win, then Bot makes turn into one of preferable cells
    if 5 in available_cells:
        cells[4].text = 'O'  # Bot makes turn in the center of the screen
        return
    elif 1 in available_cells:
        cells[0].text = 'O'  # Bot makes turn in left upper corner
        return
    elif 3 in available_cells:
        cells[2].text = 'O'  # Bot makes turn in right upper corner
        return
    elif 7 in available_cells:
        cells[6].text = 'O'  # Bot makes turn in left lower corner
        return
    elif 9 in available_cells:
        cells[8].text = 'O'  # Bot makes turn in right lower corner
        return

    # 6. If all preferable cells are occupied, make turn in any available cell
    for cell in cells:
        if not cell.text:
            cell.text = 'O'
            return

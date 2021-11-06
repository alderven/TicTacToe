import os
import sys
import json


class Stats(object):
    def __init__(self):
        """ Keep game statistics in file """

        # 1. Get path to file
        if getattr(sys, 'frozen', False):
            root_path = sys._MEIPASS
        else:
            root_path = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(root_path, 'stats.json')

        # 2. Read stat from file
        try:
            with open(self.file_path, encoding='utf-8') as f:
                data = json.load(f)
                self.win = data['win']
                self.loose = data['loose']
                self.draw = data['draw']
        except FileNotFoundError:
            self.win = 0
            self.draw = 0
            self.loose = 0

    def save_to_file(self):
        """ Save stat to file """

        with open('stats.json', 'w') as f:
            json.dump({'win': self.win, 'loose': self.loose, 'draw': self.draw}, f)

    def player_win(self):
        """ Called when Player wins """

        # 1. Increase number of wins
        self.win += 1

        # 2. Save stat to file
        self.save_to_file()

    def bot_win(self):
        """ Called when Bot wins """

        # 1. Increase number of looses
        self.loose += 1

        # 2. Save stat to file
        self.save_to_file()

    def its_a_draw(self):
        """ Called when it's a draw """

        # 1. Increase number of draws
        self.draw += 1

        # 2. Save stat to file
        self.save_to_file()

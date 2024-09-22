import random
from RPS.utils import file_to_dict, file_path


class Logic:
    def __init__(self):
        self.logic_dict = file_to_dict(file_path)
        self.level = 2
        self.data = self.logic_dict[f'lvl{self.level}']
        self.choices = self.data['choices']
        self.characters = self.data['characters']
        self.logic = self.data['logic']
        self.legends = self.data['legends']
        self.score = [0, 0]
        self.player_choice = 1
        self.computer_choice = 1
        self.locked = False
        self.round_winner = None
        self.winner = None
        self.max_rounds = 5
        self.rounds = 0
        self.table = {index: choice for (index, choice) in zip(list(range(1, self.choices+1)), self.characters)}
        self.game_end = False

    def rng(self):
        choice = random.randint(1, self.choices)
        return choice

    def winner_logic(self):
        if self.rounds <= self.max_rounds:
            if self.player_choice != self.computer_choice:
                if f'{self.legends[self.table[self.player_choice]]}/{self.legends[self.table[self.computer_choice]]}' in self.logic:
                    self.round_winner = 'Player'
                    self.score[0] += 1
                else:
                    self.round_winner = 'Computer'
                    self.score[1] += 1
            else:
                self.round_winner = 'Tied'
        else:
            if self.score[0] > self.score[1]:
                self.winner = 'Player'
            elif self.score[1] < self.score[0]:
                self.winner = 'Computer'
            else:
                self.winner = 'Tied'
            self.game_end = True
            self.rounds = 0
            self.score = [0, 0]




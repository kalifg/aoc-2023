labels = 'J23456789TQKA'


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid
        self.rank = self._compute_rank()

    def _compute_rank(self):
        runs = {}

        for card in self.cards:
            runs[card.label] = runs.get(card.label, 0) + 1

        run_pairs = sorted(
            [(label, count) for label, count in runs.items() if label != 'J'],
            key=lambda p: (p[1], p[0]),
            reverse=True
        )

        if 'J' in runs:
            if runs['J'] == 5:
                run_pairs = [('A', 5)]
            else:
                run_pairs[0] = (run_pairs[0][0], run_pairs[0][1] + runs['J'])

        if run_pairs[0][1] in [1, 4, 5]:
            return run_pairs[0][1]

        if run_pairs[0][1] == 3 and run_pairs[1][1] == 2:
            return 3.5

        if run_pairs[0][1] == 3:
            return 3

        if run_pairs[0][1] == run_pairs[1][1] == 2:
            return 2.5

        return 2

    def __eq__(self, other):
        if self.rank != other.rank:
            return False

        for i in range(len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return False

        return True

    def __lt__(self, other):
        if self.rank < other.rank:
            return True

        if self.rank > other.rank:
            return False

        for i in range(len(self.cards)):
            if self.cards[i] < other.cards[i]:
                return True
            
            if self.cards[i] > other.cards[i]:
                return False
            
        return False

    def __repr__(self):
        return f'<{self.cards}({self.rank}): {self.bid}>'
        

class Card:
    def __init__(self, label):
        if label not in labels:
            raise Exception(f'{label} is an invalid Card')
            
        self.label = label

    def __eq__(self, other):
        return self.label == other.label

    def __lt__(self, other):
        return labels.index(self.label) < labels.index(other.label)

    def __repr__(self):
        return self.label
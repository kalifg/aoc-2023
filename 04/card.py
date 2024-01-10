def format_numbers(numbers):
    return ' '.join([str(num) for num in numbers])


class Card:
    def __init__(self, id, winning_numbers, numbers):
        self.id = id
        self.winning_numbers = winning_numbers
        self.numbers = numbers

    def __repr__(self):
        return f'<Card {self.id}: {format_numbers(self.winning_numbers)} | {format_numbers(self.numbers)}>'

    def score(self):
        count = self.count_wins()

        return 0 if count < 1 else 2 ** (count - 1)

    def count_wins(self):
        return len([num for num in self.numbers if num in self.winning_numbers])

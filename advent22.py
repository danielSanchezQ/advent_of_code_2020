import itertools
from collections import deque
from enum import Enum, auto


def parse_deck(f):
    # skip player x
    next(f)
    return list(map(int, itertools.takewhile(lambda x: x not in [""], f)))


def parse_data(f):
    f = map(str.rstrip, f)
    return [parse_deck(f) for _ in range(2)]


def combat_one(deck1, deck2):
    card1, card2 = map(deque.pop, (deck1, deck2))
    if card1 > card2:
        deck1.appendleft(card1)
        deck1.appendleft(card2)
    else:
        deck2.appendleft(card2)
        deck2.appendleft(card1)


def deque_decks(decks):
    decks = map(reversed, decks)
    return tuple(map(deque, decks))


def calc_points(deck):
    return sum(x * y for x, y in enumerate(deck, 1))


def combat(decks):
    decks = deck1, deck2 = deque_decks(decks)
    while all(len(deck) != 0 for deck in decks):
        combat_one(deck1, deck2)
    return max(zip(Winner, decks), key=lambda x: len(x[1]))


class Winner(Enum):
    Player1 = auto()
    Player2 = auto()


def copy_decks(decks):
    return [list(reversed(d)) for d in decks]


def round(decks):
    deck1, deck2 = decks
    card1, card2 = map(deque.pop, (deck1, deck2))
    deck1_size = len(deck1)
    deck2_size = len(deck2)

    if deck1_size >= card1 and deck2_size >= card2:
        new_decks = copy_decks(decks)
        new_decks = tuple(
            d[:c] for c, d in zip((card1, card2), new_decks)
        )
        winner, _ = recursive_combat(new_decks)
    else:
        winner = Winner.Player1 if card1 > card2 else Winner.Player2

    if winner == Winner.Player1:
        deck1.appendleft(card1)
        deck1.appendleft(card2)
    else:
        deck2.appendleft(card2)
        deck2.appendleft(card1)


def recursive_combat(decks):
    states = set()
    deck1, deck2 = decks = deque_decks(decks)
    cache_state = lambda x: tuple(tuple(d.copy()) for d in x)
    while all(len(deck) != 0 for deck in decks):
        if cache_state(decks) in states:
            return Winner.Player1, deck1
        states.add(cache_state(decks))
        round(decks)
    return max(zip(Winner, decks), key=lambda x: len(x[1]))


if __name__ == "__main__":
    with open("./input/advent22.txt") as f:
        decks = parse_data(f)
        winner, winner_deck = combat(decks)
        print(winner, calc_points(winner_deck))
        winner, winner_deck = recursive_combat(decks)
        print(winner, calc_points(winner_deck))
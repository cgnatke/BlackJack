# There are 5 steps in the TDD flow:
# Read, understand, and process the feature or bug request.
# Translate the requirement by writing a unit test. ...
# Write and implement the code that fulfills the requirement. ...
# Clean up your code by refactoring.
# Rinse, lather and repeat.

from collections import namedtuple
import blackjack
import pytest


# @pytest.mark.parameterize('x, result', [(2, 2), (3, 3), 4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])
# @pytest.mark.parameterize("test_input,expected", [(2, 2)])
# @pytest.mark.parametrize("test_input,expected", [(5, 5), (6, 6), (8, 9)])
# @pytest.mark.parametrize("test_input,expected", [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)])
@pytest.mark.parametrize("test_input,expected", [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
                                                 (10, 10), (11, 10), (12,
                                                                      10), (13, 10), (14, 11),
                                                 (0, ValueError), (-10, ValueError), (15, ValueError)])
def test_getcardvalue(test_input, expected):
    if type(expected) == type and issubclass(expected, Exception):
        with pytest.raises(expected):
            blackjack.get_card_value(test_input)
    else:
        assert blackjack.get_card_value(test_input) == expected


@pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 54)])
def test_eval(test_input, expected):
    assert eval(test_input) == expected


def test_get_hand_value_17():
    Card = namedtuple('Card', ['value', 'suit'])
    # queen and 7 = 17
    x = [Card(value=12, suit='clubs'), Card(value=7, suit='diamonds')]
    assert blackjack.get_hand_value(x) == 17


def test_get_hand_value_23():
    card = namedtuple("card", ["value", "suit"])
    # queen, 7 and 6 = 23
    x = [card(value="q", suit="clubs"), card(value="7", suit="diamonds"),
         card(value=6, suit='diamonds')]

    assert blackjack.get_hand_value(x) == 23


def test_get_hand_value_20():
    card = namedtuple('Card', ['value', 'suit'])
    card[0]
    # king and jack = 20
    x = [card(value="k", suit='clubs'), card(value="j", suit='diamonds')]

    assert blackjack.get_hand_value(x) == 20


def test_get_hand_value_blackjack():
    card = namedtuple("card", ["value", "suit"])
    card[0]
    # king and ace = 21
    x = [card(value="k", suit="clubs"), card(value="a", suit='diamonds')]

    assert blackjack.get_hand_value(x) == 21

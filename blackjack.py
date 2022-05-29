# https://edge.twinspires.com/blackjack-terms-explained-blackjack-glossary-and-terminology/
# https://bicyclecards.com/how-to-play/blackjack/

from collections import namedtuple
import random


minimum_bet = 10


def add_to_bankroll(bankroll: int):
    print(f"Your bankroll currently is {bankroll}.")
    return int(input("How much would you like to add to your bankroll? "))


def get_bet_amount(bankroll: int):
    while(True):
        amt = int(
            input(f"How much do you want to bet? Table minimum is {minimum_bet}: "))
        if amt >= minimum_bet:
            print(f"You are betting {amt}!")
            if amt == bankroll:
                print("Holy $^$#@#@! you went all in!!!")
            return amt  # exit
        elif amt > bankroll:
            print(
                "Try again- You cannot bet more than your current bankroll of {bankroll}")
        else:
            print("Try again- You need to bet at least the table minimum...")


def get_card_value(card_val: str):
    if not card_val.isdigit():
        if (card_val.lower() in ("j", "q", "k")):
            return 10
        elif card_val.lower() == "a":
            return 11
        else:
            raise ValueError(
                "card_val provided out of the range of Jack-Ace")
    card_num = int(card_val)
    print(card_num)  # todo remove
    if(card_num < 2 or card_num > 10):
        raise ValueError(
            "card_val provided out of the range of 2-10, inclusive")
    elif(card_num <= 10):  # cards less than 10
        return card_num

# todo this function should accept a list of cards and add them up


def check_for_natural(card1: tuple, card2: tuple):
    if get_card_value(card1[0]) + get_card_value(card2[0]) == 21:
        return True
    else:
        return False

# todo is an ace considered an 11 or 1???
# def get_hand_value(cards: list[namedtuple('card', ['value', 'suit'])]):


def get_hand_value(cards):
    sum = 0
    for card in cards:
        # get each card's "value"  #todo why can't I access using .value() from the named tuple?
        sum += get_card_value(card[0])
    return sum

# https://stackoverflow.com/questions/41970795/what-is-the-best-way-to-create-a-deck-of-cards


def create_deck():
    card = namedtuple('card', ['value', 'suit'])
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    print("--------------------------------------------------------")
    cards = [card(value, suit) for value in range(2, 15) for suit in suits]
    print(cards)  # todo remove
    print("--------------------------------------------------------")
    deck = random.sample(cards, k=len(cards))  # shuffle the deck
    print(deck)
    print("--------------------------------------------------------")

    return deck


def main():

    # todo create init deck function

    deck = create_deck()
    # todo what to do when deck is about to run out?

    bankroll = 0
    bankroll += add_to_bankroll(bankroll)
    print(bankroll)

    while (bankroll > 0):
        print(f"Bankroll: {bankroll}")
        bet = get_bet_amount(bankroll)
        bankroll -= bet
        player_cards = []
        dealer_cards = []
        # if deck has more than x cards left, else shuffle or end games?
        player_cards.append(deck.pop())
        dealer_cards.append(deck.pop())
        print(
            f"The dealer has the card {dealer_cards[0]} and another card face down")
        player_cards.append(deck.pop())
        dealer_cards.append(deck.pop())

        print("Player cards: ", end="")
        print(player_cards)
        print("Dealer's cards: ", end="")
        # todo change to  only print  one card (the face up card)
        print(dealer_cards)

        # todo get rid of check_for_natural function- it's not needed
        if check_for_natural(player_cards[0], player_cards[1]):
            print("Congratulations! You hit blackjack!")
            if check_for_natural(dealer_cards[0], dealer_cards[1]):
                print("The dealer also got blackjack! It's a push...")
                bankroll += bet  # player gets their bet back
            else:
                print(f"You win 1.5x your bet which is: {bet*1.5}")
                bankroll += bet*1.5
        elif check_for_natural(dealer_cards[0], dealer_cards[1]):
            print("The dealer hit blackjack!")

        else:  # no one hit blackjack, continue...
            # player gameplay
            while (get_hand_value(player_cards) < 21):
                print(f"Player's hand: {player_cards}")
                # todo print gameplay options:
                player_decision = input("What is your next move? ").lower()
                if player_decision == "s":  # stand
                    break  # exit, go on to dealer play
                elif player_decision == "h":  # hit
                    card = deck.pop()
                    print(f"Your next card is {card}")
                    player_cards.append(card)
                else:
                    print("Invalid input, try again...")
            player_hand_value = get_hand_value(player_cards)  # store the value
            if (player_hand_value > 21):
                print("You went bust, dealer wins!")
                bet = 0  # todo do I need this?
                continue  # todo should I break out of this iteration differently?
            elif (player_hand_value < 22):
                print(
                    f"Congrats! You hit {player_hand_value}, let's see how the dealer fairs...")

            # dealer gameplay
            print(f"The dealer's second card is: {dealer_cards[1]}")

            # if dealer has a hand less than 17, they must hit
            while get_hand_value(dealer_cards) < 17:
                # If the dealer has an ace, and counting it as 11 would bring the total to 17 or more (but not over 21), the dealer must count the ace as 11 and stand.
                card = deck.pop()
                print(f"The dealer's next card is {card}")
                dealer_cards.append(card)
                print(dealer_cards)
                print(
                    f"The dealer's hand adds up to: {get_hand_value(dealer_cards)}")
            if get_hand_value(dealer_cards) > 21:
                print("The dealer went bust! You win!!!")
                bankroll += bet * 1.5  # 3:2 payout
                continue
            # dealer check if they have 21
            # todo create print function for human readable hand
            print(dealer_cards)

            if (get_hand_value(dealer_cards) > player_hand_value):
                print("Dealer wins!")
            elif (get_hand_value(dealer_cards) < player_hand_value):
                print("Player wins")
                bankroll += bet * 1.5  # 3:2 payout
            else:  # push
                bankroll += bet  # player get their bet back

        bet = 0  # reset the player's bet... todo why do we need this code?
        print(f"Player's bankroll is currently: {bankroll}")
    print("Looks like you ran out of money... Maybe apply for a home equity or 401k loan?")


if __name__ == "__main__":
    # PythonApplication1.pymain()
    main()

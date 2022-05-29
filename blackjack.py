# https://edge.twinspires.com/blackjack-terms-explained-blackjack-glossary-and-terminology/
# https://bicyclecards.com/how-to-play/blackjack/

# Note as of 5/19/2022 this is a very basic version of single player BlackJack: There are many features left
# out of this game. One example is a hand cannot be split.


# todo possible bug: if player wins 1.5 times bet and amount awarded is a decimal. Should this be allowed? Should be rounded to nearest integer?
# todo bug: Player can get stuck in while loop if their bankroll is less than the minimum bet.
from collections import namedtuple
import random
import time

minimum_bet = 10


def add_to_bankroll(bankroll: int):
    print(f"Your bankroll currently is {bankroll}.")
    while(True):
        bankroll_amt = input(
            "How much would you like to add to your bankroll? ")
        if not bankroll_amt.isdigit():
            print("Invalid input: Input must be an integer value. Try again...")
            continue
        break  # input is integer value, we can proceed.
    print(f"Adding {bankroll_amt} to the player's bankroll...")
    return int(bankroll_amt)


def get_bet_amount(bankroll: int):
    while(True):
        amt = input(
            f"How much do you want to bet? Table minimum is {minimum_bet}. Press enter without a value to bet table minimum. ")

        if amt == "":
            amt = minimum_bet
        elif not amt.isdigit():
            print("Invalid input: Input must be an integer value. Try again...")
            continue

        # assumption: at this point amt.isdigit() will always equal True
        amt = int(amt)
        if amt > bankroll:
            print(
                f"Try again- You cannot bet more than your current bankroll of {bankroll}")
        elif amt >= minimum_bet:
            print(f"You are betting {amt}!")
            if amt == bankroll:
                print("Holy $^$#@#@! you went all in!!!")
            return amt  # exit

        else:
            print("Try again- You need to bet at least the table minimum...")


def get_card_value(card_val: str):
    if not card_val.isdigit():
        if (card_val[0].lower() in ("j", "q", "k")):
            return 10
        elif card_val[0].lower() == "a":
            return 11
        else:
            raise ValueError(
                "card_val provided out of the range of Jack-Ace")
    card_num = int(card_val)
    if(card_num < 2 or card_num > 10):
        raise ValueError(
            "card_val provided out of the range of 2-10, inclusive")
    elif(card_num <= 10):  # cards less than 10
        return card_num


def check_for_natural(card1: tuple, card2: tuple):
    if get_card_value(card1[0]) + get_card_value(card2[0]) == 21:
        return True
    else:
        return False


# note only one Ace per hand can be played with value of 1


def get_hand_value(cards):
    sum = 0
    containsAce = False
    for card in cards:
        sum += get_card_value(card[0])
        if card[0] == "Ace":
            containsAce = True
    if sum > 21 and containsAce:
        sum = sum - 10  # one ace is being used as a 1, instead of 11
    return sum

# https://stackoverflow.com/questions/41970795/what-is-the-best-way-to-create-a-deck-of-cards


def create_deck():
    card = namedtuple('card', ['value', 'suit'])
    suits = ['hearts', 'diamonds', 'spades', 'clubs']
    card_values = ("2", "3", "4", "5", "6", "7", "8",
                   "9", "10", "Jack", "Queen", "King", "Ace")
    cards = [card(value, suit) for value in card_values for suit in suits]
    # print(cards)  # debugging only
    # print("--------------------------------------------------------") # debugging only
    deck = random.sample(cards, k=len(cards))  # shuffle the deck
    # print(deck) # debugging only
    # print("--------------------------------------------------------") # debugging only

    return deck


def main():

    deck = create_deck()

    bankroll = 0
    bankroll += add_to_bankroll(bankroll)

    while (bankroll > 0):
        print(f"Bankroll: {bankroll}")
        bet = get_bet_amount(bankroll)
        bankroll -= bet
        player_cards = []
        dealer_cards = []

        if (len(deck) < 22):
            msg = """
            The dealer needs to add another deck to the shoe.
            Please enjoy a drink while we wait for the dealer to add another deck and shuffle"""
            print(msg)
            time.sleep(5)
            print("Sorry this is taking so long...")
            new_deck = create_deck()
            deck = deck + new_deck  # add the new deck to the existing cards
            print("Finally have the new deck, just need to shuffle")
            time.sleep(5)
            random.shuffle(deck)  # shuffle the deck
            print("All done- Back to business...\n")

            # print(deck)  # debugging only...
            # print(f"Deck length: {len(deck)}") # debugging only...

        player_cards.append(deck.pop())
        dealer_cards.append(deck.pop())
        print(
            f"The dealer has the card {dealer_cards[0]} and another card face down")
        player_cards.append(deck.pop())
        dealer_cards.append(deck.pop())

        print(f"Player's hand: {player_cards}")
        # for debugging only
        # print("Dealer's cards: ", end="")
        # print(dealer_cards)

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
                player_decision = input(
                    "What is your next move? (S)tand or (H)it: ").lower()
                if player_decision == "s":  # stand
                    break  # exit, go on to dealer play
                elif player_decision == "h":  # hit
                    card = deck.pop()
                    print(f"Your next card is {card}")
                    player_cards.append(card)
                else:
                    print("Invalid input, try again...")
                print(f"Player's hand: {player_cards}")
                print(
                    f"Player's hand adds up to: {get_hand_value(player_cards)}")

            player_hand_value = get_hand_value(player_cards)  # store the value

            if (player_hand_value > 21):
                print("You went bust, dealer wins!")
                bet = 0  # just in case...
                continue
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
                print(f"Dealer's cards: {dealer_cards}")
                print(
                    f"The dealer's hand adds up to: {get_hand_value(dealer_cards)}")
            if get_hand_value(dealer_cards) > 21:
                print("The dealer went bust! You win!!!")
                bankroll += bet * 1.5  # 3:2 payout
                continue
            # dealer check if they have 21
            # todo create print function for human readable hand- maybe another time it's good enough to play for now...?

            if (get_hand_value(dealer_cards) > player_hand_value):
                print("Dealer wins!")
            elif (get_hand_value(dealer_cards) < player_hand_value):
                print("Player wins")
                bankroll += bet * 1.5  # 3:2 payout
            else:  # push
                print("Push! Player and the dealer tied.")
                bankroll += bet  # player get their bet back

        bet = 0  # reset the player's bet just in case it doesn't get cleared during prompt
        print(f"Player's bankroll is currently: {bankroll}")
    print("Looks like you ran out of money... Maybe apply for a home equity or 401k loan?")


if __name__ == "__main__":
    # PythonApplication1.pymain()
    main()

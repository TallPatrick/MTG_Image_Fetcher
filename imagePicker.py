#!/usr/bin/env python3.7

import scrython
import shutil
import time
from urllib.request import urlopen
from scrython.cards import Named
from scrython.cards import Autocomplete
from scrython.cards import Search


def main():
    # support for transforming cards
    transformable = False
    # start the loop of looking for card names to search
    while True:
        Card_Query = str(
            input('Enter name of card to fetch or <ENTER> to reset image: '))
        if Card_Query.lower() == 'flip' or Card_Query.lower() == 'transform':
            if transformable:
                if showing_front:
                    downloadCard(back)
                    print("Flipped!")
                    showing_front = False
                else:
                    downloadCard(front)
                    print("Flipped!")
                    showing_front = True
            else:
                print("Transform card not loaded")
            continue
        if Card_Query.lower() == 'clear' or Card_Query.lower() == '':
            # clear the image and loop
            print('Resetting image...')
            shutil.copy2('blank.png', 'card.png')
            continue
        if Card_Query.lower() == 'exit please':
            # Exit the program
            print('Bye bye!  Thanks for being polite!')
            shutil.copy2('blank.png', 'card.png')
            exit()
        # Exact Search checking
        if Card_Query[len(Card_Query) - 1] == '.':
            print("Force search for exact")
            Card_Query = Card_Query[:-1]
            try:
                time.sleep(0.05)
                card = Named(exact=Card_Query.lower())

            except Exception:
                print("No Exact match.  Trying partial match")
                card = RobustSearch(Card_Query)
                if not card:
                    continue
        else:
            # Regular Searching
            card = (Card_Query)
            if not card:
                continue
        # the meat and potatoes of copying down the image to the right spot
        ###################################################################
        # Find printings of the card
        card = findPrintingsOfCard(card)
        showing_front = True
        # check for Transform
        if card['layout'] == 'transform':
            transformable = True
            front = card['card_faces'][0]
            back = card['card_faces'][1]
        else:
            transformable = False
            front = card
            back = card
        # Pull down the image!
        downloadCard(front)
        # Communicate success!
        print('Downloaded ' + card["name"] +
              '.  Type "Clear" or a new card to clear the image')
        if transformable:
            print("Type 'Flip' or 'Transform' to see the back side")

# Reused functions


def findPrintingsOfCard(card):
    Card_Name = GetName(card)
    printings = Search(q="++{}".format(Card_Name))
    i = 1
    if len(printings.data()) != 1:
        print("Card: " + Card_Name)
        for card in printings.data():
            print(i, ":", card['set'].upper(), ":", card['set_name'])
            i = i + 1
        # Select a printing
        set_select = selectPrintingPrompt(i)
    else:
        set_select = 1
    return printings.data(int(set_select) - 1)


def selectPrintingPrompt(total_options):
    while True:
        set_select = input("Select a printing: ")
        if isinstance(set_select, int):
            print('Please try again, and type a number next time.\n')
            continue
        if int(set_select) > total_options or int(set_select) < 1:
            print('Please pick a printing from the list!\n')
            continue
        return set_select


def downloadCard(cardSide):
    Card_uri = cardSide['image_uris']['png']
    file = urlopen(Card_uri)
    with open('card.png', 'wb') as cardFile:
        cardFile.write(file.read())


def GetName(AutoOrCard):
    if isinstance(AutoOrCard, Named):
        return AutoOrCard.name()
    if isinstance(AutoOrCard, Autocomplete):
        return AutoOrCard.data()[0]
    print("ERROR!!!  Not sure how to handle this type!!!")
    return None


def getCardWithAutocomplete(CardQuery):
    try:
        return Autocomplete(q=CardQuery.lower(),
                            query=CardQuery.lower())
    except Exception as e:
        print("Something went wrong. Returning to prompt.")
        print(f"error details: {e}")
        print("\n\n")
        shutil.copy2('blank.png', 'card.png')
        return None


def getCardWithFuzzySearch(CardQuery):
    CardQuery = Named(fuzzy=CardQuery).name()
    return getCardWithAutocomplete(CardQuery)


def RobustSearch(CardQuery):
    auto = ""
    try:
        time.sleep(0.05)
        card = Named(exact=CardQuery.lower())
        auto = Autocomplete(q=CardQuery.lower(), query=CardQuery.lower())
    except Exception:
        time.sleep(0.05)
        auto = Autocomplete(q=CardQuery.lower(), query=CardQuery.lower())
    if auto:
        if len(auto.data()) == 1:
            try:
                card = Autocomplete(q=CardQuery.lower(),
                                    query=CardQuery.lower())
            except Exception as e:
                print(
                    "Something went wrong.  Clearing the image and returning to prompt.\nError details:")
                print(e)
                print("\n\n")
                shutil.copy2('blank.png', 'card.png')
                return False
        else:
            if len(auto.data()) == 0:
                print("No Cards found.  Trying fuzzy search...")
                try:
                    card = Named(fuzzy=CardQuery)
                    CardQuery = card.name()
                    card = Autocomplete(q=CardQuery.lower(),
                                        query=CardQuery.lower())
                except Exception as e:
                    print("still nothing, or some other error")
                    return False
            else:
                print("Did you mean?  Please search again!")
                for item in auto.data():
                    print(item)
                return False
    return card


if __name__ == '__main__':
    main()

#!/usr/bin/env python3.7

import scrython
import sys
import shutil
import time
from urllib.request import urlopen


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
                    Card_uri = back['image_uris']['png']
                    file = urlopen(Card_uri)
                    local = open('card.png', 'wb')
                    local.write(file.read())
                    local.close()
                    showing_front = False
                    print("Flipped!")
                else:
                    Card_uri = front['image_uris']['png']
                    file = urlopen(Card_uri)
                    local = open('card.png', 'wb')
                    local.write(file.read())
                    local.close()
                    showing_front = True
                    print("Flipped!")
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
                card = scrython.cards.Named(exact=Card_Query.lower())

            except Exception:
                print("No Exact match.  Trying partial match")
                card = RobustSearch(Card_Query)
                if not card:
                    card = None
                    continue
        else:
            # Regular Searching
            card = RobustSearch(Card_Query)
            if not card:
                card = None
                continue
        # the meat and potatoes of copying down the image to the right spot
        ###################################################################
        # Find printings of the card
        Card_Name = GetName(card)
        printings = scrython.cards.Search(q="++{}".format(Card_Name))
        i = 1
        if len(printings.data()) != 1:
            print("Card: " + Card_Name)
            for card in printings.data():
                print(i, ":", card['set'].upper(), ":", card['set_name'])
                i = i + 1
            # Select a printing
            set_select = input("Select a printing: ")
            if isinstance(set_select, int):
                print('Please try again, and type a number next time.\n')
                continue
            if int(set_select) > i or int(set_select) < 1:
                print('Please pick a printing from the list!\n')
                continue
        else:
            set_select = 1
        card = printings.data(int(set_select) - 1)
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
        Card_uri = front['image_uris']['png']
        file = urlopen(Card_uri)
        local = open('card.png', 'wb')
        local.write(file.read())
        local.close()
        # Communicate success!
        print('Downloaded ' + card["name"] +
              '.  Type "Clear" or a new card to clear the image')
        if transformable:
            print("Type 'Flip' or 'Transform' to see the back side")

# Reused functions


def GetName(AutoOrCard):
    if str(type(AutoOrCard)) == "<class 'scrython.cards.named.Named'>":
        return AutoOrCard.name()
    if str(type(AutoOrCard)) == "<class 'scrython.cards.autocomplete.Autocomplete'>":
        return AutoOrCard.data()[0]
    print("ERROR!!!  Not sure how to handle this type!!!")
    return None


def RobustSearch(CardQuery):
    auto = ""
    try:
        time.sleep(0.05)
        card = scrython.cards.Named(exact=CardQuery.lower())
        auto = scrython.cards.Autocomplete(
            q=CardQuery.lower(), query=CardQuery.lower())
    except Exception:
        time.sleep(0.05)
        auto = scrython.cards.Autocomplete(
            q=CardQuery.lower(), query=CardQuery.lower())
    if auto:
        if len(auto.data()) == 1:
            try:
                card = scrython.cards.Autocomplete(
                    q=CardQuery.lower(), query=CardQuery.lower())
            except:
                e = sys.exc_info()
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
                    card = scrython.cards.Named(fuzzy=CardQuery)
                    CardQuery = card.name()
                    card = scrython.cards.Autocomplete(
                        q=CardQuery.lower(), query=CardQuery.lower())
                except:
                    e = sys.exc_info()
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

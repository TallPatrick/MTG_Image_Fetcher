# MTG_Image_Fetcher
A Simple Script for pulling down images from Scryfall for display on a stream overlay.


###########################################
SETUP:
This script needs python 3.7 or newer.  Get it from here: https://www.python.org/downloads/
you'll also need these libraries: scrython
Get them by opening command prompt and typing: pip install <library_name>
Remember, it is case sensitive

###########################################
New Features in V1.0:
*Flip Cards can flip!
*Selecting printings!
*Adventure cards don't crash the script anymore!

###########################################
INSTRUCTIONS:
Once setup is complete, you can start the script.  
The script will download card images and replace card.png with the image of the card you selected.
Typing in "clear", or just hitting enter without typing anything will clear the image
You can type "exit please" to close the script gracefully and clear the image.
Details on how it works:
	The Script first tries to find exact matches to what you typed.
	  If that fails, it tries to auto-complete what you typed and look for cards that match there.  
	  If there are multiple auto-completes that are cards, it will show you a list of them and send you back to re-enter cards.  
	  If after trying to auto-complete it still can't find any matching cards, it will try to fuzzy search. 
	  If that fails, it will send you back to enter a card name again.
	If you successfully get a card and that card has only one printing, it will display.
	If the card you found has multiple printings it will ask you to select one numerically from a list.
Extra special features:
If the card can transform, you can then type 'flip' or 'transform' to transform the card and show the other side.
If there is a card you want to search for where the name is fully contained in the name of another card (ie Forest and Forest Bear), you can end your search with "." (Search for "Forest.") and it will try to force searching for exact matches.

###########################################
ADDITIONAL INFO:
For this to work on stream, the stream needs to be pulling the "card.png" to put on stream.  The old script pulled "card.jpg" so some updating may be needed here.
Don't mess with the blank.png picture, unless you know what you're doing and you're sure it looks good on stream.
If this ever breaks, it's probably because Scryfall (or the dude that built Scrython, https://github.com/NandaScott/Scrython) made some changes, and it threw everything out of whack.
	If this happens, let someone who knows python know, and they can probably fix it while cringing at my terrible code.
Lastly, I highly doubt anyone will actually read this file.  Kudos to you if you did.

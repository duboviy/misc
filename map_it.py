#!/usr/bin/env python
# Launches a map in the browser using an address from the command line or clipboard.

import webbrowser
import sys

import pyperclip    # pip install pyperclip


def map_it():
    if len(sys.argv) > 1:
        # get address from command line
        address = ' '.join(sys.argv[1:])
    else:
        # get address from clipboard
        address = pyperclip.paste()

    webbrowser.open('https://www.google.com/maps/place/' + address)

if __name__ == '__main__':
    map_it()

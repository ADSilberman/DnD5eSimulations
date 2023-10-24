#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "ADSilberman"
__version__ = "0.1.0"
__license__ = "MIT"

import RollClass

def main():
    """ Main entry point of the app """
    print("hello world")
    r = Roll("1d4")
    print (r)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
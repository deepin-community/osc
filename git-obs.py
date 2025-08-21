#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK


"""
This wrapper allows git-obs to be called from the source directory during development.
"""


import osc.commandline_git


if __name__ == "__main__":
    osc.commandline_git.main()

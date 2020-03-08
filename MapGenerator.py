#!/usr/bin/env python
#-----------------------------------
# This program part of Binary Land |
#-----------------------------------
# Author: Micro Robot              |
# Desc: generate Binary Map        |
#-----------------------------------

import sys
import random
import argparse

# --- generate Binary Map
def generateMap(cols, rows):
    return ( "\n".join( [ "".join( [ str(int(random.random()*2-0.2))  for _ in range(cols) ] ) for _ in range(rows) ]) )

# --- start program
def main():
    # ---------------------- #
    #     parse arguments    #
    # ---------------------- #
    parser = argparse.ArgumentParser(prog="Map generator", description="Binary Land Map generator")
    parser.add_argument("-f", help="File Name Map")
    parser.add_argument("-c", help="columns Map for generate", type=int)
    parser.add_argument("-r", help="rows Map for generate"   , type=int)
    args = parser.parse_args()
    # ---------------------- #
    #       Save Values      #
    # ---------------------- #
    # -- file name
    if args.f:
        FileName=args.f
    else:
    	FileName="MapGeneratorDef"
    # -- cols
    if args.c:
        Cols=args.c
    else:
    	Cols=10
    # -- rows
    if args.c:
        Rows=args.r
    else:
    	Rows=10

    # ---------------------- #
    #      Generate Map      #
    # ---------------------- #
    MAP = generateMap(Cols, Rows)
    #print(MAP)

    # ---------------------- #
    #        Save Map        #
    # ---------------------- #
    with open(FileName , 'w') as file:
    	file.write(MAP)


# --- start
if __name__ == "__main__":
    main()

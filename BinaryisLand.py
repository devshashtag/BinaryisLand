#!/usr/bin/env python
#-----------------------------------
#  Binary Land Solver              |
#-----------------------------------
# Author: Unprogramable            |
# Desc: Find Big Land On Map       |
#-----------------------------------

import sys
from random import random
import argparse

# Global Variables
# Char in File
LAND_F_CH  = '1'
WATER_F_CH = '0'

# print options
P="\33["
C_WATER    = P + "0;7;34m" #  water color
C_BIG_LAND = P + "0;7;32m" # big land color
C_OTH_LAND = P + "0;7;31m" # other lands color
C_NORM_W   = P + "0;34m"   # normal color for waters
C_NORM_L   = P + "0;1;31m" # normal color for lands
C_NORM_T   = P + "0;1;33m"   # normal color for text

DIS_CH_WATER    = C_WATER    + " " # print char water
DIS_CH_BIG_LAND = C_BIG_LAND + " " # print char big land
DIS_CH_OTH_LAND = C_OTH_LAND + " " # print char other land

# generate binary random Map
def generateRandomMap(cols, rows):
    return [ "".join( [ str(int(random()*2-0.2)) for _ in range(cols) ] )  for _ in range(rows) ]

# Functions
# duplicate group exist ?
def need_to_join_groups(group_lands):
    len_lands = 0
    uniq_len_lands = 0
    lands=[]
    # uniq length all lands
    for row in group_lands:
        lands += row

    len_lands = len( lands )
    uniq_len_lands = len( set(lands) )
    # print(uniq_len_lands , len_lands)
    # duplicate exist if uniq_len_lands not equals to len_lands
    if uniq_len_lands < len_lands:
        return True
    else:
        return False


# remove duplicate and join groups
def join_groups(group_lands):
    # [ [(1, 2), (1,0)], [(2,3), (1,0)], [(3,3), (1,3)]]
    #   |________####____ _______####_|
    # joined :           v
    # [ [(1,0), (1, 2), (2,3)], [(3,3), (1,3)]]

    new_group_lands = []

    #print("before:" , len(group_lands))

    # 2 group needed for check and join ?
    if(len(group_lands) > 1):
        # iterate all item in group_lands for join two group duplicated
    	for row in group_lands:
            # for check need to create a new group or not
            new_group = True
            for column in row:
                # for first time create a new group
                if len(new_group_lands) <= 0:
                    new_group_lands.append(row)
                    # no need to create a new group
                    new_group = False
                    break
                else:
                    # iterate all items in new_group_lands for find duplicate
                    for i,item in enumerate(new_group_lands):
                        if column in item:
                                # add into this group
                        	new_group_lands[i] += row
                                # no need to create a new group
                        	new_group = False
                        	break
                    # leave this group if no need to create a new group
                    if not new_group:
                        break
            # create a new group
            if new_group:
                 new_group_lands.append( row )

    # remove duplicates in groups
    group_lands = [ [ column for column in set(item) ] for item in new_group_lands ]

    # print("after:" , len(group_lands))
    # if duplicate finded  need to join groups
    if need_to_join_groups(group_lands):
        group_lands = join_groups(group_lands)

    return group_lands


# make positions in area for check in map
def AreaItem(Land):
    # return in Area positions (pos-x,pos-y)
    # (x-1, y-1) (x,  y-1) (x+1, y-1)
    # (x-1, y  )  LandPos  (x+1, y  )
    # (x-1, y+1) (x,  y+1) (x+1, y+1)
    #------------------------------
    x = Land[0]
    y = Land[1]

    # Make list area
    Area = [
      (x-1, y-1), (x, y-1), (x+1, y-1),
      (x-1, y  )          , (x+1, y  ),
      (x-1, y+1), (x, y+1), (x+1, y+1)
    ]

    # return
    return Area


# find location lands and create group lands
def FindLands(MAP):
    lands = []       # location pixels LANDS
    waters = []      # location pixels WATERS
    group_lands = [] # location pixels LANDS by group

    # positions (1, 0) in lands and waters
    for y, row in enumerate(MAP):
        for x, column in enumerate(row):
            if   column == LAND_F_CH :    lands.append((x, y))
            elif column == WATER_F_CH:    waters.append((x, y))

    # detect relationships between positions in lands
    for item in lands:
        # for first time create a new group 'land' with first position in 'lands'
        if len(group_lands) <= 0:
            # added  item = [(x, y)]
            group_lands.append( [ item ] )
        else:
            # create positions in area for check in map
            area_item = AreaItem(item)
            # for check need to create new group or not
            new_group = True
            # iterate all group_lands for check items in area_item
            for y,row in enumerate(group_lands):
                for x,column in enumerate(row):
                    # [check item in area ?]
                    if column in area_item:
                        # Add into group
                        group_lands[y].append(item)
                        # no need to create a new group
                        new_group = False
                        # leave this group
                        break
            # create a new group if new_group is true
            if new_group:
                group_lands.append( [item] )

    # remove duplicate
    group_lands = join_groups(group_lands)

    return waters, group_lands


# show map by MAP array
def ShowMap(MAP):
    print(f"{C_NORM_T}Before find big land : ")
    for row in MAP:
        for ch in row:
            if ch == LAND_F_CH:
                print(f"{C_NORM_L}{ch}",end='')
            elif ch == WATER_F_CH:
                print(f"{C_NORM_W}{ch}",end='')
        print(f"{P}m")

# show map by Options
def ShowMapByOptions(Lands, Waters, MAP):
    BigLandLen    = max([ len(row) for row in Lands ]) # max length lands
    OtherLandsLen = set( len(item) for item in Lands if len(item) < BigLandLen )
    WatersLen     = len(Waters)

    print(f"\n{C_NORM_T}After find big land : ")

    # print map with Color and more details
    for y,row in enumerate(MAP):
        for x,column in enumerate(row):
            # map in waters
            if (x,y) in Waters:
                print(f"{DIS_CH_WATER}",end='')
            # map in Lands
            else:
                for item in Lands:
                    if (x,y) in item:
                        # big map
                        if len(item) == BigLandLen:
                            print(f"{DIS_CH_BIG_LAND}",end='')
                        else:
                            print(f"{DIS_CH_OTH_LAND}",end='')
        # new line
        print("")
    # print options
    print("")
    print(f"{C_NORM_T}All    Land \t-> { len(Lands) }")
    print(f"{C_NORM_T}big    Land \t-> CH: {DIS_CH_BIG_LAND + C_NORM_T} -> size : {BigLandLen}")
    print(f"{C_NORM_T}Other  Lands\t-> CH: {DIS_CH_OTH_LAND + C_NORM_T} -> sizes: {OtherLandsLen}")
    print(f"{C_NORM_T}Waters\t\t-> CH: {DIS_CH_WATER    + C_NORM_T} -> size : {WatersLen}\n")


# start program
def main():

    # parse arguments
    parser = argparse.ArgumentParser(prog="BinaryLand Solver", description="Binary Land Algorithms")
    parser.add_argument("-c", help="columns Map", type=int)
    parser.add_argument("-r", help="rows Map"   , type=int)
    args = parser.parse_args()

    # Save Values
    # cols
    if args.c:
        Cols=args.c
    else:
    	Cols=20
    # rows
    if args.r:
        Rows=args.r
    else:
    	Rows=10

    # Map
    MAP = generateRandomMap(Cols, Rows)

    # Print Map
    ShowMap(MAP)

    # Find Lands
    Waters, group_lands = FindLands(MAP)

    # show map with bigger land and other lands
    ShowMapByOptions(group_lands, Waters , MAP)

# start
if __name__ == "__main__":
    main()

# dnd_fightsimulator
!! This program is not optimised. Im very new to this. Suggestions to improve welcomed !!
Written in python using pandas.
Simple fight simulator for two opposing groups of fighters in DND.
Fill in the fighterstats.csv file with your players' names and stats and the monsters' names and stats. Just add and delete rows to suit the fight you want to simulate.
In the py file you will need to change the path file to the csv file 
When you hit run it will ask how many fights you want to simulate. I suggest maybe 20 or so, or 1. It will give you a probability of winning vs losing (ie all players being knocked out).
Good for DMs wanting to get a solid feel for whether a group of monsters is appropriate challenge for a specific group of players/characters.
This is simple and assumes only one type of attack per fighter, which is way off for spell casters and fighters with special abilities etc - but it helps me as DM.
Please be kind - Ive been programming for no longer than one month.
csv column explanations:
name: name
dex: dexterity bonus for initiative
ac: armour class
hp: hit points
resistance: 0 for none; 1 for yes (assumes 50% cut to all incoming damage)
initiative: set to 0. This is filled in by the program. This is a bit arbitrary - i dont know why i did it like this but it works.
numattacks: The number of attacks the fighter has per turn
tohit1: to hit bonus
damdie1: The die used for damage (for 2d6 this is 6)
damrolls: The number of rolls for damdie1 (for 2d6 this is 2)
dambonus1: damage bonus
type: player or monster. No other input will work.

This project is licensed under the terms of the MIT license.

import numpy as np
import pandas as pd
import random

n=int(input('How many fight simulations are we running?'))
reruns=0
wins=0
for reruns in range(0,n):
    csv_loc = 'C:/Users/dream/iCloudDrive/iCloud~com~omz-software~Pythonista3/DND/fighterstats.csv'
    alls = pd.read_csv(csv_loc, sep=',', header=0) 
    ps = alls[alls['type'] == 'player']
    ms = alls[alls['type'] == 'monster']

    def setfightgroups(playernames,monsternames):
        pnames = list(playernames)
        mnames = list(monsternames)
        random.shuffle(mnames)
        random.shuffle(pnames)
        fightgroups = {}
        if len(pnames) != len(mnames):
            if len(pnames) > len(mnames):
                biggergroup = pnames
                smallergroup = mnames
            else:
                biggergroup = mnames
                smallergroup = pnames
            fightgroups = dict(zip(biggergroup[0:len(smallergroup)], smallergroup))
            for bgfighter in biggergroup[len(smallergroup):]:
                fightgroups[bgfighter] = random.choice(smallergroup)
                for sgfighter in smallergroup:
                    if sum(map((sgfighter).__eq__, fightgroups.values())) >= len(biggergroup)/len(smallergroup):
                        smallergroup.remove(sgfighter)
            return fightgroups
        else: 
            fightgroups = dict(zip(pnames, mnames))
            return fightgroups

    def invert(a):
        inverted_dict = dict()
        for key, value in a.items():
            inverted_dict.setdefault(value, list()).append(key)
        return inverted_dict

    fightgroups = setfightgroups(ps["name"],ms["name"])
    inverted_fgroups = invert(fightgroups)
    print(f'The INVERTED fightgroups are as follows:\n {inverted_fgroups}\n')  #               PRINT INVERTED_FG

    def rollinitiative():
        for i in range(0,len(alls["name"])):
            alls.iat[i,5] = random.randint(1,20) + alls.iloc[i,1]
        initiative_dict = {}
        for fighter in alls["name"]:
            initiative_dict[fighter] = alls.iat[alls[alls['name'] == fighter].index[0],5]
        return initiative_dict

    initiative_dict = rollinitiative()
    initiative_sorted = dict(sorted(initiative_dict.items(), key=lambda item: item[1], reverse=True))
    order_of_play = list(initiative_sorted)
    print(f'Order of play is \n {order_of_play}\n')

    def select_target(attackingfighter):
        izPresent = attackingfighter in fightgroups
        izPresent2 = attackingfighter in inverted_fgroups
        if izPresent == True:
            if type(fightgroups[attackingfighter]) == str:
                ttarget = fightgroups[attackingfighter]
                return ttarget
            else:
                ttarget = random.choice(fightgroups[attackingfighter])
                return ttarget
        elif izPresent2 == True:
            if type(inverted_fgroups[attackingfighter]) == str:
                ttarget = inverted_fgroups[attackingfighter]
                return ttarget
            else:
                ttarget = random.choice(inverted_fgroups[attackingfighter])
                return ttarget
        else:
            pass
        
    def rolltohit(attackertohit, targetac):
        attackdieroll = random.randint(1,20)
        attackroll = attackdieroll + attackertohit
        if attackroll == 20 + attackertohit:
            print('Critical hit!')
            return 2
        elif attackroll > targetac:
            print(f'Rolled {attackdieroll} plus {attackertohit}: Hit!')
            return 1
        else: 
            print(f'Rolled {attackdieroll} plus {attackertohit}: Miss!')
            return 0

    def damageroll(damdie, dierolls, dambonus):
        return random.randint(1, damdie) * dierolls + dambonus 

    PIA = list(ps['name'])
    MIA = list(ms['name'])
    deathcount = 0
    roundcount=1

    while True:
        print(f'\nROUND {roundcount}!')
        roundcount += 1
        print(f'Fight is now \n{PIA} \nvs\n{MIA}\nAnd inv_fg is:\n{inverted_fgroups}')
        print(f'Death count is now {deathcount}')
        for attacker in order_of_play:
            if MIA == [] or PIA == []: break
            print(f'\n{attacker}\'s turn')
            for eachattack in range(0,alls.iat[alls[alls['name'] == attacker].index[0],6]):
                if MIA == [] or PIA == []: break
                target = select_target(attacker)
                print(f'{attacker} attacks {target} (attack no {eachattack + 1})')
                hit = rolltohit(alls.iat[alls[alls['name'] == attacker].index[0],7], alls.iat[alls[alls['name'] == target].index[0],2])
                if hit > 0:
                    damage = hit * damageroll(alls.iat[alls[alls['name'] == attacker].index[0],8], alls.iat[alls[alls['name'] == attacker].index[0],9], alls.iat[alls[alls['name'] == attacker].index[0],10])
                    if alls.iat[alls[alls['name'] == target].index[0],4] == 1:
                        print('Damage resistance!')
                        damage *= 0.5
                    alls.iat[alls[alls['name'] == target].index[0],3] -= damage
                    hp = alls.iat[alls[alls['name'] == target].index[0],3]
                    print(f'{damage} damage! {target} has {hp} hp remaining.')
                    if alls.iat[alls[alls['name'] == target].index[0],3] <= 0: # <========================== DEADFIGHTER ========================*
                        deathcount += 1
                        deadfighter = target
                        order_of_play.remove(deadfighter)
                        gselect1 = deadfighter in fightgroups
                        if gselect1 == True:
                            for listofplayers in list(inverted_fgroups.values()):
                                if deadfighter in listofplayers:
                                    if len(listofplayers) == 1: 
                                        listofplayers.remove(deadfighter)
                                        if deadfighter in PIA:
                                            PIA.remove(deadfighter)
                                            if PIA == []: break
                                        else:
                                            MIA.remove(deadfighter)
                                            if MIA == []: break
                                        fightgroups = setfightgroups(PIA,MIA)     
                                        inverted_fgroups = invert(fightgroups)
                                    else:
                                        listofplayers.remove(deadfighter)
                                        if deadfighter in PIA:
                                            PIA.remove(deadfighter)
                                            if PIA == []: break
                                        else:
                                            MIA.remove(deadfighter)
                            print(f'{deadfighter} is unconscious and out of the fight')
                            print(f'Death count is now: {deathcount}')
                        else:
                            if deadfighter in PIA:
                                PIA.remove(deadfighter)
                                if PIA == []: break
                                fightgroups = setfightgroups(PIA,MIA) 
                                inverted_fgroups = invert(fightgroups)
                            else:
                                MIA.remove(deadfighter)
                                if MIA == []: break
                                fightgroups = setfightgroups(PIA,MIA) 
                                inverted_fgroups = invert(fightgroups)
                            print(f'{deadfighter} is unconscious and out of the fight')
                            print(f'Death count is now: {deathcount}')
                        break
        if MIA == []:
            print(f'The fight is over after {roundcount} rounds of blood, bravery and fear. You were victorious! Bask in the glory of the kill!')
            print(f'The survivors are:\n{PIA}')
            wins += 1
            break
        elif PIA == []:
            print(f'The fight is over after {roundcount} rounds of blood, bravery and fear. You were defeated! You fought bravely! Your names will be remembered through the ages!')
            break
    reruns += 1
print('\n********************************************************\n')
print(f'You won {wins*100/n:.1f}% of the time, or {wins} wins out of {n} fights')
print('\n********************************************************\n')
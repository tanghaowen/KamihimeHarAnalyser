import json
import csv
import ijson
import codecs
import re

from haralyzer import HarPage, HarParser
from sys import argv
def dealWithHar():
    battleData = BattleData()
    with open(harFileName, 'r', encoding='UTF-8') as f:
        objects = ijson.items(f, 'log.entries.item')
        entries = []
        print('Analysing HAR file......')

        jindu = 1
        pattern = re.compile("/ability$|/attack$|/ability$|/start$")
        for o in objects:
            match = pattern.search( o['request']['url'] )
            if match:
                entries.append(o)
            print("Analysing Completed, count:"+str(jindu))
            jindu+=1
        print('Analysing end')
    party_names = None
    before_party_names = None
    round = 1;

    print( 'Analysing BattleData......')
    iiiii = -1
    for entry in entries:
        iiiii += 1
        print(iiiii)
        if "/attack" in entry['request']['url']:
            attack_turn_json = json.loads(entry['response']['content']['text'])
            scenario = attack_turn_json['scenario']
            turn_mode = 0

            if party_names == None:
                party_names = []
                party_members = attack_turn_json['status']['party_members']
                print( attack_turn_json)
                for party in party_members:
                    party_names.append( party['name'])
                before_party_names = party_names
            else:
                party_names = before_party_names
                party_members = attack_turn_json['status']['party_members']
                before_party_names = []
                for party in party_members:
                    before_party_names.append( party['name'])



            inBurst = False
            burstCharacterName = ''
            burstFromPos = 0
            burstTarget = 0
            burstFrom = ''
            for li in scenario:
                burstDamage = 0;
                cmd = li['cmd']

                if cmd == 'attack':
                    fromWhere = li['from']
                    fromPos = li['pos']

                    damages = li['damage']

                    multiAttack = 1
                    iii=0
                    for damageLi in damages:
                        for damage2nd in damageLi:
                            damage = damage2nd['value']
                            toWhere = damage2nd['pos']
                            if fromWhere == 'player':
                                if iiiii == 65:
                                    print()
                                    print(li)
                                    print(round)
                                    print(fromWhere)
                                    print(fromPos)
                                    print(party_names[int(fromPos)])
                                    print(toWhere)
                                    print(damage)
                                    print(len(damages))
                                battleData.addOneTurn( round, fromWhere, fromPos, party_names[int(fromPos)], toWhere,"enemy", damage , len(damages))
                            elif fromWhere == 'enemy':
                                battleData.addOneTurn( round, fromWhere, fromPos, "enemy", toWhere,party_names[int(toWhere)], damage , len(damages))


                elif cmd == 'burst':
                    inBurst = True;
                    burstFromPos = li['pos']
                    burstCharacterName = party_names[ burstFromPos ]
                    if li['from'] == 'enemy':
                        burstFrom = 'enemy'
                    elif li['from'] == 'player':
                        burstFrom = 'player'

                elif cmd == 'damage' and inBurst:
                    burstTarget = li['damage'][0][0]['pos']
                    for fbDamage in  li['damage']:
                        for fbDamage2nd in fbDamage:
                            burstDamage += fbDamage2nd['value']
                    if burstFrom == 'player':
                        battleData.addOneTurn(round, 'player', burstFromPos, burstCharacterName, burstTarget, "enemy",
                                      burstDamage,
                                      1, 'burst')
                    elif burstFrom == 'enemy':
                        battleData.addOneTurn(round, 'enemy', burstFromPos, 'enemy', burstTarget, "player",
                                      burstDamage,
                                      1, 'burst')
                    inBurst = False

                elif cmd == 'burst_streak':
                    fullBurstDamage = 0
                    for d1 in li['damage']:
                        for d2 in d1:
                            fullBurstDamage += d2['value']
                    if burstFrom == 'player':
                        battleData.addOneTurn(round, 'player', -1, "Characters Full Burst", burstTarget, "enemy",
                                              fullBurstDamage,
                                              1, 'fullBurst')
            round += 1





        if "/ability" in entry['request']['url']:
            ability_turn_json = json.loads(entry['response']['content']['text'])

            party_names=[]
            party_members = ability_turn_json['status']['party_members']
            for party in party_members:
                party_names.append( party['name'])
            before_party_names = party_names


            scenarios = ability_turn_json['scenario']
            abilityName = ''
            fromWhere = ''
            fromPos = 0
            fromCharacterName = ''
            abilitySummary = ''
            allDamage = 0
            toWhere = 0
            for scenario in scenarios:
                cmd = scenario['cmd']
                if cmd == 'ability':
                    abilityName = scenario['name']
                    fromWhere = scenario['from']
                    if fromWhere == 'player':
                        fromPos = scenario['pos']
                        fromCharacterName = party_names[ fromPos ]
                        toWhere = 'enemy'
                    abilitySummary = scenario['comment']
                elif cmd == 'damage':
                    for damage in scenario['damage']:
                        for damage2nd in damage:
                            allDamage += damage2nd['value']
            battleData.addOneTurn(round,fromWhere ,fromPos , fromCharacterName , -1 , 'enemy' , allDamage,0 , 'ability',abilityName , abilitySummary )

        if "/start" in  entry['request']['url']:
            print('Starting a battle')
            party_names = None;
            before_party_names = None
            round =1;
    print( 'Analysing end, generating damage data')

    damageList = {}
    iiii = 0
    for turn in battleData.turns:
        iiii+=1
        characterName = turn['fromCharacterName']
        if not characterName in damageList:
            damageList.update({turn['fromCharacterName']:
                {'attackDamage':0 , 'burstDamage':0 ,'fullBurstDamage':0, 'abilityDamage':0 ,'doubleAttack':0 , 'tripleAttack':0 , 'attackCount':0}
                               })

        if turn['damageType'] == 'attack':
            damageList[characterName]['attackDamage'] += turn['damage']
            damageList[characterName]['attackCount'] += 1
            if turn['attackTimes'] == 2:
                damageList[characterName]['doubleAttack']+=1
            elif turn['attackTimes'] == 3:
                damageList[characterName]['tripleAttack']+=1

        elif turn['damageType'] == 'burst':
            damageList[characterName]['burstDamage'] += turn['damage']
        elif turn['damageType'] == 'ability':
            damageList[characterName]['abilityDamage'] += turn['damage']
        elif turn['damageType'] == 'fullBurst':
            damageList[characterName]['fullBurstDamage'] += turn['damage']


    for char,damageType in damageList.items():
        damageType["doubleAttack"] /=2
        damageType["tripleAttack"] /= 3
        damageType["attackCount"] -= ( damageType["doubleAttack"] + damageType["tripleAttack"] *2 )

        '''for type, damage in damageType.items():
            if  type == 'doubleAttack':
                damage/=2
                damageType["attackCount"] = damageType["attackCount"] - damage
            elif type == 'tripleAttack':
                damageType = damage / 3'''

    for char,damageType in damageList.items():
        print( char + " :")
        for type,damage in damageType.items():
            print( "\t"+type+" : \t" + str(damage))

        if damageType["attackCount"]*100 != 0:
            print("\t"+"doubleAttackProbability"+" : \t" + str(damageType["doubleAttack"]/damageType["attackCount"]*100)+"%"  )
            print("\t"+"tripleAttackProbability"+" : \t" + str(damageType["tripleAttack"]/damageType["attackCount"]*100)+"%"  )


    print( 'Importing battle detail to '+harFileName + ' ' + 'battaleDetail.csv' + '......')
    with open(harFileName + ' ' + 'battaleDetail.csv','w' , newline="" , encoding='UTF-8') as csvFile:
        csvFile.write('\ufeff')
        csvWriter = csv.writer( csvFile , dialect='excel')
        csvWriter.writerow(['round', 'damageType' , 'damage' , 'from' , 'fromCharacterName' , 'to' , 'toTargetName' ,'attackTimes', 'abilityName','abilitySummary'])
        '''csvWriter.writerow(['第几轮' , '伤害类型，平a，技能，burt，FB','具体伤害数值','伤害的来源，玩家或者敌人','伤害来源自玩家的话，来源神姬的名字','伤害给那个位置，暂时不用','如果玩家受到伤害，受到伤害的神姬名字','这是连击次数，2表示本次和下一次是同一个二连伤害，3表示本次和接下来两次是同一次三连伤害打出来的','伤害如果是技能类型的话，技能名','技能介绍'])'''
        for turn in battleData.turns:
            csvWriter.writerow([str(turn['round']),turn['damageType'],str(turn['damage']),turn['from'],turn['fromCharacterName'] , str(turn['to']) , turn['toTargetName'],str(turn['attackTimes']) ,turn['abilityName'],turn['abilitySummary']] )
        print('importing end')
class BattleData:
    def __init__(self):
        self.turns = []

    def addOneTurn(self , round , fromWhere, fromPos,fromCharacterName, toWhere, toTargetName, damage,attackTimes , damageType = 'attack' , abilityName='' , abilitySummary=''):
        self.turns.append({'round':round , 'from': fromWhere, 'fromPos': fromPos , 'fromCharacterName':fromCharacterName, 'to': toWhere, 'toTargetName':toTargetName,'damage': damage ,'attackTimes':attackTimes,'damageType':damageType,'abilityName':abilityName,'abilitySummary':abilitySummary })


harFileName = ''
if len(argv)>=2:
    for filename in argv[1:]:
        harFileName = filename
        dealWithHar()



input()
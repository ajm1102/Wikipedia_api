from qwikidata.sparql import return_sparql_query_results
import pandas as pd
import wikipedia
import numpy as np
import requests
import cProfile

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def CreateTextFile(battles, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        for item in battles:
            f.write(f"{item}\n")
    return


def BattlesTextFile():
    filename = "battleslist.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            battles = f.read().splitlines()
    except FileNotFoundError:
        battles = ListOfBattles()
        CreateTextFile(battles, filename)
    return battles


def ListOfBattles():
    query_string = """
    SELECT
      ?itemLabel
    WHERE {
          ?item wdt:P31 wd:Q178561 
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    res = return_sparql_query_results(query_string)
    battles = []
    for row in res["results"]["bindings"]:
        battle = row["itemLabel"]["value"]
        if "Battle" in battle:
            battles.append(row["itemLabel"]["value"])
    return battles


def CheckDuplicateBattles(battle):
    battleS = []
    for i in wikipedia.search(battle.strip()):
        if battle in i and i != battle and has_numbers(i) == True:
            battleS.append(i)
    if len(battleS) == 1:
        battleS = battleS[0]
    if not battleS:
        battleS = battle
    return battleS, battle


def GetTable(battle):
    NotFound = 'Casualties and losses not found'

    url = f"https://en.wikipedia.org/wiki/{battle.strip().replace(' ', '_')}"
    r = requests.get(url)
    website = r.text
    try:
        dfs = pd.read_html(website, encoding="UTF-8")
    except:
        return NotFound

    for table in dfs:
        a = pd.Series(str(table.iloc[:, 0]))
        b = a.str.contains('Casualties and losses')

        if b[0]:
            Castable = table
            u = Castable.head(0).iloc[:, 0]
            b = Castable.index[Castable[u.name].str.contains("Casualties and losses", case=False, na=False)]
            Cas = Castable.loc[b[0] + 1]
            return Cas

    return NotFound


def ParseCasualties(battle):
    battle, battle_without_date = CheckDuplicateBattles(battle)
    table = []

    if type(battle) is list:
        for i in battle:
            table.append(GetTable(i))
    else:
        table = GetTable(battle)
    return table


def ScrapeNumbers():
    return


def main():
    battles = BattlesTextFile()

    Casualties = []
    battles = battles[0:20]
    for i in battles:
        print(i)
        Casualties.append(ParseCasualties(i))
    print(Casualties)
    return


if __name__ == "__main__":
    main()

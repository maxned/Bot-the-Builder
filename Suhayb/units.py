# Vertual Environment Setup
# cd to file dir
# python3 -m venv $(pwd)
# source $(pwd)/bin/activate

# pip install tqdm
# pip install sc2reader

# To run:
# python3 units.py replayFilePath

# Input: paths to star craft 2 replay files
# Output file Structure:
#    units
#      replay.csv
#      ...

import sc2reader, csv, sys, os, glob

import tqdm
import concurrent.futures

# Removed non Terran units
# https://github.com/GraylinKim/sc2reader/blob/d69feb4e0be597581040588193579d29e8241431/sc2reader/data/unit_lookup.csv
statsHead = [
    'winner', 'opponent', 'seconds', 'BarracksTechLab', 'AutoTurretReleaseWeapon', 'Hellion', 'ExtendingBridgeNEWide10Out', 'ATSLaserBatteryLMWeapon', 'MULE', 'WidowMineWeapon', 'VikingFighter', 'Barracks', 'SiegeTankSieged', 'TornadoMissileDummyWeapon', 'Ghost', 'SupplyDepot', 'Factory', 'AutoTurret', 'TechLab', 'EMP2Weapon', 'ReaperPlaceholder', 'OrbitalCommandFlying', 'Reactor', 'SeekerMissile', 'FusionCore', 'ExtendingBridgeNEWide10', 'Raven', 'ExtendingBridgeNEWide8', 'Bunker', 'FactoryTechLab', 'CommandCenterFlying', 'AutoTestAttacker', 'VikingAssault', 'EngineeringBay', 'WidowMineAirWeapon', 'SiegeTank', 'StarportFlying', 'ThorAALance', 'Battlecruiser', 'ExtendingBridgeNWWide12', 'Armory', 'Refinery', 'Marine', 'ExtendingBridgeNWWide12Out', 'CommandCenter', 'PlanetaryFortress', 'VikingFighterWeapon', 'ExtendingBridgeNWWide10', 'PointDefenseDroneReleaseWeapon', 'GhostAcademy', 'Thor', 'HellionTank', 'Banshee', 'SCV', 'WidowMine', 'BacklashRocketsLMWeapon', 'ATALaserBatteryLMWeapon', 'LongboltMissileWeapon', 'FactoryReactor', 'TornadoMissileWeapon', 'ExtendingBridgeNWWide10Out', 'D8ChargeWeapon', 'Medivac', 'WarHound', 'Reaper', 'ExtendingBridgeNEWide12Out', 'FactoryFlying', 'OrbitalCommand', 'BarracksFlying', 'WidowMineBurrowed', 'ExtendingBridgeNWWide8Out', 'SupplyDepotLowered', 'MissileTurret', 'Starport', 'Nuke', 'WarHoundWeapon', 'ThorAAWeapon', 'AutoTestAttackTargetAir', 'ExtendingBridgeNWWide8', 'StarportTechLab', 'TowerMine', 'StarportReactor', 'HunterSeekerWeapon', 'AutoTestAttackTargetGround', 'SensorTower', 'ExtendingBridgeNEWide8Out', 'Marauder', 'BarracksReactor', 'YamatoWeapon', 'PunisherGrenadesLMWeapon', 'ExtendingBridgeNEWide12', 'PointDefenseDrone'
]

def parseFileSafe(file):
    try:
        parseFile(file)
    except:
        print("failed: " + file)
        return

def parseFile(file):
    #create output files
    fileName = os.path.splitext(os.path.basename(file))[0]

    #Check if file already exsists if so skip
    path = 'output/units/' + fileName + '.csv'
    if os.path.exists(path):
        return True

    replay = sc2reader.load_replay(file, load_level=3)

    #one vs one. Terran vs Terran
    if len(replay.players) != 2 or replay.type != '1v1' or (replay.players[0].play_race != "Terran" and replay.players[1].play_race != "Terran") or not replay.competitive:
        # raise Exception('Players not equal to two or player race not Terran!')
        return True

    #Collect Stats of Game
    winner = replay.winner.players[0].pid
    loser = 1 + (winner) % 2
    #only track Terran
    trackp = [False, replay.players[0].play_race == "Terran", replay.players[1].play_race == "Terran"]

    statsFile = open(path, 'w', newline='')
    statsCSV = csv.writer(statsFile)
    statsCSV.writerow(statsHead)

    # Parse unit stats
    unitCount = [{'BarracksTechLab':0, 'AutoTurretReleaseWeapon':0, 'Hellion':0, 'ExtendingBridgeNEWide10Out':0, 'ATSLaserBatteryLMWeapon':0, 'MULE':0, 'WidowMineWeapon':0, 'VikingFighter':0, 'Barracks':0, 'SiegeTankSieged':0, 'TornadoMissileDummyWeapon':0, 'Ghost':0, 'SupplyDepot':0, 'Factory':0, 'AutoTurret':0, 'TechLab':0, 'EMP2Weapon':0, 'ReaperPlaceholder':0, 'OrbitalCommandFlying':0, 'Reactor':0, 'SeekerMissile':0, 'FusionCore':0, 'ExtendingBridgeNEWide10':0, 'Raven':0, 'ExtendingBridgeNEWide8':0, 'Bunker':0, 'FactoryTechLab':0, 'CommandCenterFlying':0, 'AutoTestAttacker':0, 'VikingAssault':0, 'EngineeringBay':0, 'WidowMineAirWeapon':0, 'SiegeTank':0, 'StarportFlying':0, 'ThorAALance':0, 'Battlecruiser':0, 'ExtendingBridgeNWWide12':0, 'Armory':0, 'Refinery':0, 'Marine':0, 'ExtendingBridgeNWWide12Out':0, 'CommandCenter':0, 'PlanetaryFortress':0, 'VikingFighterWeapon':0, 'ExtendingBridgeNWWide10':0, 'PointDefenseDroneReleaseWeapon':0, 'GhostAcademy':0, 'Thor':0, 'HellionTank':0, 'Banshee':0, 'SCV':0, 'WidowMine':0, 'BacklashRocketsLMWeapon':0, 'ATALaserBatteryLMWeapon':0, 'LongboltMissileWeapon':0, 'FactoryReactor':0, 'TornadoMissileWeapon':0, 'ExtendingBridgeNWWide10Out':0, 'D8ChargeWeapon':0, 'Medivac':0, 'WarHound':0, 'Reaper':0, 'ExtendingBridgeNEWide12Out':0, 'FactoryFlying':0, 'OrbitalCommand':0, 'BarracksFlying':0, 'WidowMineBurrowed':0, 'ExtendingBridgeNWWide8Out':0, 'SupplyDepotLowered':0, 'MissileTurret':0, 'Starport':0, 'Nuke':0, 'WarHoundWeapon':0, 'ThorAAWeapon':0, 'AutoTestAttackTargetAir':0, 'ExtendingBridgeNWWide8':0, 'StarportTechLab':0, 'TowerMine':0, 'StarportReactor':0, 'HunterSeekerWeapon':0, 'AutoTestAttackTargetGround':0, 'SensorTower':0, 'ExtendingBridgeNEWide8Out':0, 'Marauder':0, 'BarracksReactor':0, 'YamatoWeapon':0, 'PunisherGrenadesLMWeapon':0, 'ExtendingBridgeNEWide12':0, 'PointDefenseDrone':0}] * 3

    for event in replay.tracker_events:
        if (event.name == 'UnitBornEvent' or event.name == 'UnitDoneEvent' or event.name == 'UnitDiedEvent') and event.unit.owner and trackp[event.unit.owner.pid] and event.unit.name in unitCount[event.unit.owner.pid]:
            unitCount[event.unit.owner.pid][event.unit.name] += -1 if event.name == 'UnitDiedEvent' else 1
        elif event.name == 'UnitTypeChangeEvent' and event.unit.owner and trackp[event.unit.owner.pid] and event.unit_type_name in unitCount[event.unit.owner.pid]:
            unitCount[event.unit.owner.pid][event.unit_type_name] += 1
        else:
            continue
        if event.unit.owner:
            oponent = replay.players[(event.unit.owner.pid) % 2].play_race[0]
            statsCSV.writerow([1 if event.unit.owner.pid == winner else 0, oponent, event.second] + list(unitCount[event.unit.owner.pid].values()))

    statsFile.close()
    return True

#inital setup
os.makedirs('output/units', exist_ok=True)
filePaths = sys.argv[1]

#Concurrent Parser
with concurrent.futures.ProcessPoolExecutor() as executor:
    files = glob.glob(filePaths + "/*.SC2Replay")

    #progress bar
    results = executor.map(parseFileSafe, files)
    list(tqdm.tqdm(results, desc='Processing', total=len(files), bar_format=' {desc}: {bar}  {percentage:3.0f}% '))
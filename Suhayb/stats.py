# Vertual Environment Setup
# cd to file dir
# python3 -m venv $(pwd)
# source $(pwd)/bin/activate

# pip install tqdm
# pip install sc2reader

# To run:
# python3 stats.py file1.SC2Replay file2.SC2Replay ...

# Input: paths to star craft 2 replay files
# Output file Structure:
#  wins
#    stats
#      replay.csv
#      ...
#  losses
#    stats
#      replay.csv
#      ...

import sc2reader, csv, sys, os
from tqdm import trange

#inital setup
os.makedirs('output/wins/stats', exist_ok=True)
os.makedirs('output/losses/stats', exist_ok=True)

files = sys.argv[1:]

#progress bar
pbar = trange(
    len(files),
    desc='Processing',
    bar_format=' {desc}: {bar}  {percentage:3.0f}% ')

#parser
for num, parseFile in enumerate(files, start=1):
    replay = sc2reader.load_replay(parseFile, load_map=1)

    #one vs one
    if len(replay.players) != 2 or replay.type != '1v1' or not replay.competitive:
        raise Exception('Players not equal to two!')

    #Collect Stats of Game
    map_hash = replay.map_hash
    winner = replay.winner.players[0].pid
    loser = 1 + (winner) % 2

    #create output files
    fileName = os.path.splitext(os.path.basename(parseFile))[0]

    # TODO: Check if file already exsists if so skip
    winnerStatsFile = open(
        'output/wins/stats/' + fileName + '.csv', 'w', newline='')
    winnerstatsCSV = csv.writer(winnerStatsFile)

    looserStatsfile = open(
        'output/losses/stats/' + fileName + '.csv', 'w', newline='')
    looserStatsCSV = csv.writer(looserStatsfile)

    statsHead = [
        'seconds', 'minerals_current', 'vespene_current',
        'minerals_collection_rate', 'vespene_collection_rate',
        'workers_active_count', 'minerals_used_in_progress_army',
        'minerals_used_in_progress_economy',
        'minerals_used_in_progress_technology',
        'vespene_used_in_progress_army', 'vespene_used_in_progress_economy',
        'vespene_used_in_progress_technology', 'minerals_used_current_army',
        'minerals_used_current_economy', 'minerals_used_current_technology',
        'vespene_used_current_army', 'vespene_used_current_economy',
        'vespene_used_current_technology', 'minerals_lost_army',
        'minerals_lost_economy', 'minerals_lost_technology',
        'vespene_lost_army', 'vespene_lost_economy', 'vespene_lost_technology',
        'minerals_killed_army', 'minerals_killed_economy',
        'minerals_killed_technology', 'vespene_killed_army',
        'vespene_killed_economy', 'vespene_killed_technology', 'food_used',
        'food_made', 'minerals_used_active_forces',
        'vespene_used_active_forces', 'ff_minerals_lost_army',
        'ff_minerals_lost_economy', 'ff_minerals_lost_technology',
        'ff_vespene_lost_army', 'ff_vespene_lost_economy',
        'ff_vespene_lost_technology'
    ]

    winnerstatsCSV.writerow(statsHead)
    looserStatsCSV.writerow(statsHead)

    # Parse
    for event in replay.tracker_events:
        if event.name == 'PlayerStatsEvent':
            if event.pid == winner:
                winnerstatsCSV.writerow([event.second] +
                                        list(event.stats.values()))
            else:
                looserStatsCSV.writerow([event.second] +
                                        list(event.stats.values()))

    winnerStatsFile.close()
    looserStatsfile.close()

    #update progress bar
    pbar.update(num)

pbar.close()
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
#    stats
#      replay.csv
#      ...

import sc2reader, csv, sys, os
from tqdm import trange

#inital setup
os.makedirs('output/stats', exist_ok=True)

files = sys.argv[1:]

#progress bar
pbar = trange(
    len(files),
    desc='Processing',
    bar_format=' {desc}: {bar}  {percentage:3.0f}% ')

statsHead = [
    'winner', 'seconds', 'minerals_current', 'vespene_current',
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


#parser
for num, parseFile in enumerate(files, start=1):
    replay = sc2reader.load_replay(parseFile, load_map=1)

    #one vs one. Terran vs Terran
    if len(replay.players) != 2 or replay.type != '1v1' or (replay.players[0].play_race != "Terran" and replay.players[1].play_race != "Terran") or not replay.competitive:
        return

    #Collect Stats of Game
    winner = replay.winner.players[0].pid
    loser = 1 + (winner) % 2

    #create output files
    fileName = os.path.splitext(os.path.basename(parseFile))[0]
    statsFile = open(
        'output/stats/' + fileName + '.csv', 'w', newline='')
    statsCSV = csv.writer(statsFile)
    
    statsCSV.writerow(statsHead)
    # Parse
    for event in replay.tracker_events:
        if event.name == 'PlayerStatsEvent':
            statsCSV.writerow([1 if event.pid == winner else 0, event.second] +
                                        list(event.stats.values()))

    statsFile.close()

    #update progress bar
    pbar.update(num)

pbar.close()
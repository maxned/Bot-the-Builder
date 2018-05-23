from pprint import pprint
import sc2reader, csv, sys, os

replay = sc2reader.load_replay(
    sys.argv[1], load_level=4)

if len(replay.players) != 2:
    raise  Exception('Players not equal to two!')

# for player in replay.players:
#     assertTrue(player.is_human)

# pprint(dir(person))

for person in replay.people:
    print(person.pid, person.play_race)

print(replay.map_hash)
print(replay.game_length)
print(replay.frames)
print(replay.game_fps)
print(replay.category)
print(replay.type)
print(replay.competitive)
print(replay.cooperative)
print("Winner #:", replay.winner.players[0].pid)
winner = replay.winner.players[0].pid
loser = 1 + (winner) % 2

print(replay.winner.players[0].play_race)

# 0: PlayerStatsEvent,
# 1: UnitBornEvent,
# 2: UnitDiedEvent,
# 3: UnitOwnerChangeEvent,
# 4: UnitTypeChangeEvent,
# 5: UpgradeCompleteEvent,
# 6: UnitInitEvent,
# 7: UnitDoneEvent,

#  event.unit._type_class.id = unique unit ID
#  event.unit.owner.pid = owner player ID

for event in replay.tracker_events:
    if event.name == 'UnitBornEvent':
        if event.unit.owner:
            print("Born:", event.unit.name, event.unit.owner.pid, event.second,
                event.unit._type_class.id)
    elif event.name == 'UnitDiedEvent':
        if event.unit.owner:
            print("Died:", event.unit.name, event.unit.owner.pid, event.second,
                  event.unit._type_class.id)
    elif event.name == 'UnitTypeChangeEvent':
        print("TypeChange:", event.unit_type_name, event.unit.owner.pid,
            event.unit._type_class.id, event.second)
    elif event.name == 'UpgradeCompleteEvent':
        print("Upgrade:", event.upgrade_type_name, event.pid, event.second, event.count)
    elif event.name == 'UnitDoneEvent':
        print("Built:", event.unit.name, event.unit.owner.pid, event.unit._type_class.id, event.second)


# print(vars(replay.game_events))

# print(sc2reader)
# pprint(vars(replay))

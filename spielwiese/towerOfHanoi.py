def move(disc, towerFrom, towerIntermediate, towerTo):
    if disc > 0:
        move(disc-1, towerFrom, towerTo, towerIntermediate)
        print(f"Move a Disc from {towerFrom} to {towerTo}")
        move(disc-1, towerIntermediate, towerFrom, towerTo)


move(3,1,2,3)

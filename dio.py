packages = (6,9,20)
totSol = list()
sort = list()

def find():
    ##Find all possible combinations of 6, 9, 20 packs of McNuggets and save
    ##the possible combination in list.
    for n in range(1, 150):
        for a in range(0, 26):
            for b in range(0, 18):
                for c in range(0, 8):
                    tot = (a*packages[0]) + (b*packages[1]) + (c*packages[2])
                    if tot == n:
                        totSol.append(n)
    ##Find the largest impossible to get number of McNuggets
    for x in range(1, 150):
        if x not in totSol:
            sort.append(x)
    print(max(sort))
    print(sort)

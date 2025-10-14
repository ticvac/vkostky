from environment import Environment
from random import randint

nuly = 0
soucet = 0

env = Environment()

iteraci = 100000

for kostek in range(1,6):
    graf = [0 for i in range(0,int(8050/50))]

    for i in range(iteraci):
        vs = [randint(1,6) for x in range(1,kostek + 1)]
        
        graf[int(env.calculate_score(vs)/50)] += 1

        """
        if env.calculate_score(vs) >= 350:
            soucet += env.calculate_score(vs)
        elif 0 < env.calculate_score(vs) and env.calculate_score(vs) < 350:
            nuly += 1
        """
    graf_dict = {}
    for i in range(len(graf)):
        if graf[i] != 0:
            graf_dict[i*50] = graf[i]/iteraci
    print(graf_dict, end="\n\n")

    #print(graf)
    """
    print(kostek)
    print(soucet/iteraci)
    print(nuly/iteraci)
    """



from environment import Environment
from random import randint

nuly = 0
soucet = 0

env = Environment()

kostek = 1
iteraci = 100000

for i in range(iteraci):
    vs = [randint(1,6) for x in range(1,kostek + 1)]
    #print(vs)
    soucet += env.calculate_score(vs)
    if env.calculate_score(vs) == 0:
        nuly += 1

print(kostek)
print(soucet/iteraci)
print(nuly/iteraci)



from numpy import inf
from JobShop import *
import networkx as nx

def get_start_times(t: list, order: list) -> list:
    out = [-1 for i in range(len(t))]
    current_t = 0
    for job in order:
        out[job] = current_t
        current_t += t[job]
    return out

def EDD(t: list,d: list) -> list:
    out = [-1 for i in range(len(t))]
    te = t[:]
    de = d[:]

    current_t = 0

    while -1 in out:
        current_job = de.index(min(de))

        out[current_job] = current_t
        current_t+=te[current_job]
        te[current_job] = de[current_job] = inf
    return out

def SPT(t: list,d: list) -> list:
    out = [-1 for i in range(len(t))]
    te = t[:]
    de = d[:]

    current_t = 0

    while -1 in out:
        current_job = te.index(min(te))

        out[current_job] = current_t
        current_t+=te[current_job]
        te[current_job] = de[current_job] = inf

    return out

def Moore(t: list,d: list) -> list:
    times = t[:]
    A = list()
    edd = EDD(t, d)
    B = [edd.index(i) for i in sorted(edd)]
    late = True
    while late:
        done = []
        late = False
        current_time = 0
        for current_job in B:
            done.append(t[current_job])
            if current_time+t[current_job] > d[current_job]:
                late = True
                longest = t.index(max(done))
                t[longest] = inf
                B.remove(longest)
                A.append(longest)
                break
            current_time+=times[current_job]
    print(times)
    out = get_start_times(times, B+A)
       
    return out




task = input('Odaberite zadatak a) ili b): ')

if 'a' in task.lower():

    time = eval(input('Unesite vremena trajanja u obliku liste: '))
    deadline = eval(input('Unesite rokove poslova u obliku liste: '))

    mode = input('Unesite nacin rasporedivanja (Moore, EDD ili SPT): ')

    if mode.upper() == 'EDD':
        out = EDD(time,deadline)
    elif mode.upper() == 'SPT':
        out = SPT(time,deadline)
    elif mode.upper() == 'MOORE':
        out = Moore(time,deadline)

    print(out)

elif 'b' in task.lower():
    J = eval(input('Unesite definiciju sustava u obliku liste listi uredenih parova: '))
    js = JobShop(J)
        
    print(js.shifting_bottleneck())
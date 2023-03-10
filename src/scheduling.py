from numpy import inf
from JobShop import *

def calculate_CTi(out: list, time: list) -> list:
    CTi = []
    for i, j in zip(out, time):
        CTi.append(i + j)
    return CTi

def calculate_CT(CTi: list) -> float:
    return sum(CTi)/len(CTi)

def calculate_CTku(CTi: list, deadline: list) -> list:
    CTku = []
    for i, j in zip(CTi, deadline):
        CTku.append(i - j)
    return CTku

def calculate_CTu(CTku: list) -> float:
    m = max(CTku)
    return max(m, 0)

def calculate_TH(CTi: list) -> float:
    M = max(CTi)
    return len(CTi)/M

def calculate_WIP(CT: float, TH: float) -> float:
    return  CT * TH

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

    t = eval(input('Unesite vremena trajanja u obliku liste: '))
    d = eval(input('Unesite rokove poslova u obliku liste: '))

    mode = input('Unesite nacin rasporedivanja (Moore, EDD ili SPT): ')

    time = t[:]
    deadline = d[:]
    if mode.upper() == 'EDD':
        out = EDD(time,deadline)
    elif mode.upper() == 'SPT':
        out = SPT(time,deadline)
    elif mode.upper() == 'MOORE':
        out = Moore(time,deadline)

    CTi = calculate_CTi(out, t)
    CT = calculate_CT(CTi)
    CTku = calculate_CTku(CTi, d)
    CTu = calculate_CTu(CTku)
    TH = calculate_TH(CTi)
    WIP = calculate_WIP(CT, TH)

    print(f's: {out}')
    print(f'CTi: {CTi}')
    print(f'CT: {CT}')
    print(f'CTku: {CTku}')
    print(f'CTu: {CTu}')
    print(f'TH: {TH}')
    print(f'WIP: {WIP}')

elif 'b' in task.lower():
    J = eval(input('Unesite definiciju sustava u obliku liste listi uredenih parova: '))
    js = JobShop(J)

    out = js.shifting_bottleneck()
        
    for machine in sorted(out.keys()):
        print(f"stroj {machine}:")
        print(f"m1j: {out[machine][0]}")
        print(f"m2j: {out[machine][1]}")

    print(f"M={max([interval[1] for machine in out for interval in out[machine][1]])}")
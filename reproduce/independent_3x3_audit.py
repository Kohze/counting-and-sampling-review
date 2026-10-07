import itertools,json,random
rng=random.Random(20261007)
def compositions(total,slots):
    if slots==1:
        yield (total,)
        return
    for first in range(total+1):
        for tail in compositions(total-first,slots-1):
            yield (first,)+tail
def check(rows,cols,caps):
    total=sum(rows)
    ranks=[]
    for mask in range(512):
        rr=sum(min(rows[i],sum(caps[3*i+j] for j in range(3) if mask>>(3*i+j)&1)) for i in range(3))
        cr=sum(min(cols[j],sum(caps[3*i+j] for i in range(3) if mask>>(3*i+j)&1)) for j in range(3))
        ranks.append(min(rr,cr))
    direct=set()
    bases=set()
    for vector in compositions(total,9):
        if all(vector[k]<=caps[k] for k in range(9)) and all(sum(vector[3*i+j] for j in range(3))==rows[i] for i in range(3)) and all(sum(vector[3*i+j] for i in range(3))==cols[j] for j in range(3)):
            direct.add(vector)
        if ranks[-1]==total and all(sum(vector[k] for k in range(9) if mask>>k&1)<=rank for mask,rank in enumerate(ranks)):
            bases.add(vector)
    if direct!=bases:
        raise AssertionError((rows,cols,caps,direct,bases))
    return len(direct)
counts=[]
for trial in range(100):
    total=rng.randrange(4)
    margins=list(compositions(total,3))
    rows=rng.choice(margins)
    cols=rng.choice(margins)
    caps=tuple(rng.choice((0,1,2,2**30+1)) for _ in range(9))
    counts.append(check(rows,cols,caps))
controls={'binary_permutations':check((1,1,1),(1,1,1),(1,)*9),'six_cycle':check((1,1,1),(1,1,1),(1,1,0,0,1,1,1,0,1))}
assert controls=={'binary_permutations':6,'six_cycle':2}
print(json.dumps({'independent_cases':100,'additional_controls':controls,'dimension':'3 by 3','total_values':'0..3','cap_values':[0,1,2,2**30+1],'seed':20261007,'nonempty':sum(c>0 for c in counts),'max_count':max(counts),'status':'all direct sets equal all-subset common-base sets','vector_enumeration':'all weak compositions of total; no cell-cap pruning'},sort_keys=True))

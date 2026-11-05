"""Descriptive aggregation of repeated passes; not independent resampling."""
from collections import defaultdict
import numpy as np

def collapse_by_phase(records):
    groups=defaultdict(list);keys=['experiment','method','seed','class','phase_sample']
    for row in records:groups[tuple(row[k] for k in keys)].append(row)
    result=[]
    for values,rows in groups.items():
        result.append(dict(zip(keys,values))|{'aw_true':float(np.mean([float(r['aw_true']) for r in rows])),'aw_pred':float(np.mean([float(r['aw_pred']) for r in rows])),'passes':len({r['repetition'] for r in rows})})
    return result

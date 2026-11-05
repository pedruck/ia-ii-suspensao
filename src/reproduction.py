"""Compare scientific outputs, independently of runtime and checkpoint metadata."""
import math

def compare_evaluations(original,repeated):
    fields=['experiment','method','seed','class']
    old={tuple(r[k] for k in fields):r for r in original}
    new={tuple(r[k] for k in fields):r for r in repeated}
    mismatches=[];max_deltas={k:0. for k in ['body_rmse_m','aw_mae','accuracy']}
    for key in old.keys()&new.keys():
        for metric in max_deltas:
            a,b=old[key][metric],new[key][metric];delta=abs(a-b)
            max_deltas[metric]=max(max_deltas[metric],delta)
            close=math.isclose(a,b,rel_tol=0 if metric=='accuracy' else 1e-4,abs_tol=1e-12 if metric=='accuracy' else 1e-7)
            if not close:mismatches.append({'key':list(key),'metric':metric,'original':a,'reproduced':b})
    return {'matches_within_tolerance':set(old)==set(new) and not mismatches,'missing_runs':[list(k) for k in old.keys()-new.keys()],'extra_runs':[list(k) for k in new.keys()-old.keys()],'max_absolute_differences':max_deltas,'mismatches':mismatches,'tolerance':'accuracy 1e-12 absolute; physical errors 1e-7 absolute + 1e-4 relative'}

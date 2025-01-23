


import paneltime as pt
import pandas as pd
import numpy as np
import pickle
import time
from paneltime.output import stat_functions as sf
import cProfile
import pstats
from pstats import SortKey
import os



pt.options.pqdkm.set([2,2,0,2,2])
#pt.options.fixed_random_group_eff.set(0)
#pt.options.fixed_random_time_eff.set(0)
#pt.options.fixed_random_variance_eff.set(0)
#pt.options.fixed_random_variance_eff.set(0)
pt.options.supress_output.set(False)
pt.options.multicoll_threshold_max.set(100000)
pt.options.include_initvar.set(False)
pt.options.use_analytical.set(2)


#pt.options.constraints_engine.set(False)
#pt.options.user_constraints.set({'beta': np.array([[-13.13315683],
#       [ -2.69371823],
#       [ -0.8612572 ]])})


#pt.enable_parallel()
a=[]


def estimate(betaconstr, analhess):
	pt.options.betaconstraint.set(betaconstr)
	pt.options.use_analytical.set(analhess)
	fname = f'paneltimeres_{betaconstr}_{analhess}.csv'
	a = None
	if os.path.exists(fname):# and False:
		a = np.loadtxt(fname, dtype = str, delimiter=';')
		a = [i for i in a]
	if a is None:
		i = 0
	else:
		i = len(a)-1
	
	while True:
		s = estimate_sample(i)
		if s is None:
			break
		if a is None:
			a=[['sample'] + s.coef_names + ['SE '+ j for j in s.coef_names] + ['LL', 'time', 'its']]
		a.append([i] + list(s.coef_params)+list(s.coef_se_robust)+[s.log_likelihood, s.time, s.its])
		np.savetxt(fname, a, fmt='%s', delimiter=';')
		i += 1

def estimate_sample(i):
	print(f"Sample {i}")
	try:
		df=pd.read_pickle(f"simulations/data{i}.df")
	except Exception as e:
		print(e)
		return None
	
	t = time.time()

	if False:
		cProfile.run("pt.execute('Y~X0+X1',df,T='dates',ID='IDs', console_output=True)", 'profile_results')
		stats = pstats.Stats('profile_results')
		stats.sort_stats(SortKey.CUMULATIVE).print_stats(40)
	else:
		s = pt.execute("Y~X0+X1",df,T='dates',ID="IDs", console_output=True)
	
	print(f"Executed in {time.time()-t} seconds")
	print(s.results())
	print(s.ll.LL)

	return s


pt.options.betaconstraint.set(False)
pt.options.use_analytical.set(2)
estimate_sample(487)
estimate(False, 2)

a=0



import paneltime as pt
import pandas as pd
import numpy as np
import pickle
import time
from paneltime.output import stat_functions as sf


pt.options.pqdkm.set([2,2,0,2,2])
#pt.options.fixed_random_group_eff.set(0)
#pt.options.fixed_random_time_eff.set(0)
#pt.options.fixed_random_variance_eff.set(0)
#pt.options.fixed_random_variance_eff.set(0)
pt.options.supress_output.set(False)
pt.options.multicoll_threshold_max.set(1000)
pt.options.include_initvar.set(True)


#pt.options.constraints_engine.set(False)
#pt.options.user_constraints.set({'beta': np.array([[-13.13315683],
#       [ -2.69371823],
#       [ -0.8612572 ]])})


#pt.enable_parallel()
a=[]
if False:
	a = np.loadtxt('paneltimeres.csv', dtype = str, delimiter=';')
	a = [i for i in a]

i = 0
while True:
	try:
		df=pd.read_pickle(f"paneltime_test/simulations/data{i}.df")
		i += 1
	except Exception as e:
		print(e)
		break
	print(f"Sample {i-1}")
	t = time.time()
	s = pt.execute("Y~X0+X1",df,T='dates',ID="IDs", console_output=True)
	print(f"Executed in {time.time()-t} seconds")
	print(s.results())
	print(s.ll.LL)
	if i == 1:
		a=[s.coef_names + ['SE '+ i for i in s.coef_names] + ['LL', 'time', 'its']]
	a.append(list(s.coef_params)+list(s.coef_se_robust)+[s.log_likelihood, s.time, s.its])
	np.savetxt('paneltimeres.csv', a, fmt='%s', delimiter=';')



a=0
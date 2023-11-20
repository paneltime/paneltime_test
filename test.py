
import paneltime as pt
import pandas as pd
import numpy as np
import pickle
import time




pt.options.pqdkm.set([2,2,0,2,2])
pt.options.fixed_random_group_eff.set(2)
pt.options.fixed_random_time_eff.set(2)
pt.options.supress_output.set(False)
pt.options.parallel.set(True)
pt.options.debug_mode.set(False)

df=pd.read_pickle(f"simulations/data0.df")





import cProfile
profiler = cProfile.Profile()
profiler.enable()

t = time.time()

s = pt.execute("Y~X0+X1",df,T='dates',ID="IDs", console_output=True)

profiler.disable()
profiler.print_stats(sort='cumulative')


print(f"time was {time.time()-t}")
print(s)
print(s.ll.args.args_v)

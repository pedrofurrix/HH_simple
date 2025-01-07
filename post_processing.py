import numpy as np
import os
import time
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import functions.csv_max_minshift as csv_max_minshift
import functions.numpy_max_shift as npmaxshift
import functions.low_pass as low_pass

start=time.time()

# # CF=[100,500,1000,2000,3000,5000,10000,20000,30000,40000,50000]
# E=[10,20,30,50,100,150,200,300,400,500,700,1000]
# CF=[100]
# E=[90]
cell_id=1
# for freq in CF:
#     for e in E:
#         top_dir,bot_dir=csv_max_minshift.get_folder(freq,e,cell_id)
#         max_shift, max_v, min_v, results=csv_max_minshift.cmax_shift(bot_dir,top_dir, cell=None)
#         # # max_shift, max_v, min_v,results=npmaxshift.cmax_shift_numpy(bot_dir,top_dir)
#         csv_max_minshift.plot_voltage(bot_dir,results)
    
# import functions.spike_detector as spike_detector
# spike_detector.spike_detector(bot_dir)


# CF=100
# E=[80]
# cell_id=1
# cutoff=20
# order=3

# for e in E:
#     low_pass.filter_data(CF,e,cell_id,cutoff,order=order)

# # low_pass.test_fake_data()

import functions.process_results as pr
summary_dfp,summary_dfn,top_dir=pr.load_results(cell_id)
pr.plot_results(summary_dfp,title="Max Shiftp",top_dir=top_dir)
pr.plot_results(summary_dfn,title="Max Shiftn",top_dir=top_dir)

end=time.time()
print(f"Time passed:{end-start} seconds")
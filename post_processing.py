import numpy as np
import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import functions.csv_max_minshift as csv_max_minshift
import functions.numpy_max_shift as npmaxshift

CF=100
E=10
cell_id=1

top_dir,bot_dir=csv_max_minshift.get_folder(CF,E,cell_id)

max_shift, max_v, min_v, results=csv_max_minshift.cmax_shift(bot_dir,top_dir, cell=None)
# max_shift, max_v, min_v,results=npmaxshift.cmax_shift_numpy(bot_dir,top_dir)
csv_max_minshift.plot_voltage(bot_dir,results)
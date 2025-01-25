import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Change the working directory to the script's directory
os.chdir(script_dir)
import functions.csv_max_minshift as max
from functions.filter_allvoltages import filter_and_save_voltages

cell_id=1
# CF=[100,500,1000,2000,3000,5000,10000,20000,30000,40000,50000]
# E=[10,20,30,50,100,150,200,300,400,500,700,1000]
MF=[0,5,10,20,30,40,50,100]
E=[10,20,30,50,100,150,200,300,400,500,700,1000]
var="modfreq"
cutoff_freq=100
order=3
filter=True
for cfreq in MF:
     for e in E:
        top_dir, bot_dir,param_dir=max.get_folder(cfreq,e,cell_id,var,filtered=filter)
        filter_and_save_voltages(param_dir,cutoff_freq,order)
        max_shift, max_v, min_v, results=max.cmax_shift(bot_dir,top_dir, param_dir,var=var,filtered=filter)
        max.plot_voltage(bot_dir,results,filtered=filter)

        
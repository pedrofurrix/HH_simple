from neuron import h
from . import stim
def thresh_excited(cell,simtime,apc,simparams,stimparams,amp):
    t,stim1=stim.ampmodulation_wiki(stimparams[1],amp,stimparams[5],simparams[0],stimparams[3],simparams[1],stimparams[4],stimparams[6])
    h.finitialize(cell.v_init)
    h.run(simtime)
    return apc.n>0

def threshold(cell,simtime,apc,simparams,stimparams):
    low=0
    high=1e5
    amp=stimparams[2]

    if amp==0: amp=1

    while low==0 or high==1e5:
        if thresh_excited(cell,simtime,apc,simparams,stimparams,amp):
            high=amp
            amp/=2
        else:
            low=amp
            amp*=2
        # Stop the loop if stoprun_flag is True
        if h.stoprun==1: 
            return amp
        
        if low > high:
            return high
        
        epsilon = 1e-8 + 1e-4 * high
        amp=(high+low)/2
        while (high - low) > epsilon:
            if thresh_excited(cell,simtime,apc,simparams,stimparams,amp): 
                high = amp
            else:
                low = amp
            amp = (high + low)/2
        if h.stoprun==1: 
            break
            
        return amp
    

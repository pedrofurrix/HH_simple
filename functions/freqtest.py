from neuron import h
import stim
import matplotlib.pyplot as plt


def freqtest(fmin,fmax,step,amp,simtime,dt,cell,v_init):
    t=h.Vector().record(h._ref_t)
    fig, ax = plt.subplots()
    for freq in range(fmin,fmax,step):
        #simpleplaysin
        #amp,dt,tstop,freq
        amp=amp
        tstop=simtime
        freq=freq
        times,stim1=stim.simpleplaysin(amp,dt,tstop,freq)
        voltage=h.Vector().record(cell.soma(0.5)._ref_v)
        run(v_init,simtime,dt,times,stim1)
        plot(ax,voltage,t,freq)
    ax.legend(title="Frequency")
    ax.set_xlabel("time(ms)")
    ax.set_ylabel("Voltage (mV)")
    ax.set_title("Membrane Voltage Soma")
    plt.show()
    

def run(v_init,simtime,dt,times,stim1):
    h.dt=dt
    h.tstop=simtime
    h.finitialize(v_init)
    h.continuerun(simtime)

def plot(ax,voltage,t,freq):
    label1=f"{freq} Hz"
    ax.plot(t,voltage,label=label1)
    
    
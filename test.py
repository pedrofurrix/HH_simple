from Extracellular_test.HH_simple.functions.HH_minimal_cells import Fast_Spiking,Intrinsic_Bursting
from neuron import h,gui
import matplotlib.pyplot as plt
h.load_file("stdrun.hoc")

cell=Fast_Spiking(0,0,0,0,0,1)
h.topology()


# Insert electrode
#T
CURR_AMP = 0.5
stim = h.IClamp(cell.soma(0.5))  # Insert IClamp in the center of each cell's soma
stim.delay = 300  # Delay before the current starts
stim.dur = 400    # Duration of the current pulse
stim.amp = CURR_AMP  # Amplitude of the injected current

# Transient Time
trans = 0000


# setup simulation parameters
Dt = 0.1			# macroscopic time step <<>>
npoints = 10000

h.dt = 0.1			# must be submultiple of Dt
#tstart = trans
h.tstop = trans + npoints * Dt
h.steps_per_ms = 5
h.celsius = 36
h.v_init = cell.v_init


# Record v membrane
v=h.Vector().record(cell.soma(0.5)._ref_v)
t=h.Vector().record(h._ref_t)

h.finitialize()
h.fcurrent()
h.continuerun()


plt.Figure()
plt.plot(t,v)
plt.xlabel("time(ms)")
plt.ylabel("Membrane voltage(mV)")
plt.title("Testing simple HH models")
plt.show()
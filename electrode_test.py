from neuron import h
def stim_test(cell):
    if cell.name=="Fast Spiking":    
        CURR_AMP = 0.5
        stim = h.IClamp(cell.soma(0.5))  # Insert IClamp in the center of each cell's soma
        stim.delay = 300  # Delay before the current starts
        stim.dur = 400    # Duration of the current pulse
        stim.amp = CURR_AMP  # Amplitude of the injected current
        simtime=1000
    elif cell.name=="Intrinsically Bursting":
        CURR_AMP = 0.15
        stim = h.IClamp(cell.soma(0.5))  # Insert IClamp in the center of each cell's soma
        stim.delay = 500 # Delay before the current starts
        stim.dur = 2000   # Duration of the current pulse
        stim.amp = CURR_AMP  # Amplitude of the injected current
        simtime=3000
    elif cell.name=="Repetitive Bursting":
        CURR_AMP = 0.15
        stim = h.IClamp(cell.soma(0.5))  # Insert IClamp in the center of each cell's soma
        stim.delay = 500 # Delay before the current starts
        stim.dur = 2000   # Duration of the current pulse
        stim.amp = CURR_AMP  # Amplitude of the injected current
        simtime=3000
    elif cell.name=="Low Threshold":
        CURR_AMP = 0.15
        stim = h.IClamp(cell.soma(0.5))  # Insert IClamp in the center of each cell's soma
        stim.delay = 400 # Delay before the current starts
        stim.dur = 400   # Duration of the current pulse
        stim.amp = CURR_AMP  # Amplitude of the injected current
        simtime=1000
    elif cell.name=="Regular Spiking":
        CURR_AMP = 0.75
        stim = h.IClamp(cell.soma(0.5))  # Insert IClamp in the center of each cell's soma
        stim.delay = 300 # Delay before the current starts
        stim.dur = 400   # Duration of the current pulse
        stim.amp = CURR_AMP  # Amplitude of the injected current
        simtime=1000
    return stim,simtime
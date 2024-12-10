from neuron import h
from neuron.units import um,mV,ms
class Cell:
    def __init__(self, gid, x, y, z, theta,nseg=0): 
        self._gid = gid
        self._setup_morphology()
        self.all = self.soma.wholetree()
        self._discretize(nseg)
        self._setup_biophysics()
        self.x = self.y = self.z = 0
        self._setup_apcs()
        self._rotate_z(theta) 
        self._set_position(x, y, z) #x,y,z are in um
        # Spike detector - register the spikes associated with the cell
        # can look to plot them in a scatter plot.
        self._spike_detector = h.NetCon(self.soma(0.5)._ref_v, None, sec=self.soma)
        self.spike_times = h.Vector()
        self._spike_detector.record(self.spike_times)

        self._ncs = []

        self.soma_v = h.Vector().record(self.soma(0.5)._ref_v)
    
    def _setup_morphology(self):
        self.soma = h.Section(name="soma", cell=self)
        self.dend = h.Section(name="dend", cell=self)
        self.dend.connect(self.soma)

    def _discretize(self,nseg):
        if nseg==0:
            from . import dlambda
            for sec in self.all:
                dlambda.geom_nseg(self)
             
        else:
            for sec in self.all:
                sec.nseg=nseg
            h.define_shape()

    def __repr__(self):
        return "{}[{}]".format(self.name, self._gid)

    def _set_position(self, x, y, z): #this was basically already done before #can try it with this specification of coordinates
        for sec in self.all:
            for i in range(sec.n3d()):
                sec.pt3dchange(
                    i,
                    x - self.x + sec.x3d(i),
                    y - self.y + sec.y3d(i),
                    z - self.z + sec.z3d(i),
                    sec.diam3d(i),
                )
        self.x, self.y, self.z = x, y, z

    def _rotate_z(self, theta):
        """Rotate the cell about the Z axis."""
        for sec in self.all:
            for i in range(sec.n3d()):
                x = sec.x3d(i)
                y = sec.y3d(i)
                c = h.cos(theta)
                s = h.sin(theta)
                xprime = x * c - y * s
                yprime = x * s + y * c
                sec.pt3dchange(i, xprime, yprime, sec.z3d(i), sec.diam3d(i))
    def _setup_apcs(self): # Set up APCs with standard time and threshold
        self.apc_soma=h.APCount(self.soma(0.5)) 
        self.apc_dend=h.APCount(self.dend(0.5))
        self.recAp_soma=h.Vector()
        self.apc_soma.record(self.recAp_soma)
        self.recAp_dend=h.Vector()
        self.apc_dend.record(self.recAp_dend)
        



class Fast_Spiking(Cell):
   
    # Single-compartment model of "fast-spiking" cortical neurons,
    #     which is the most commonly encountered electrophysiological type
    #     of inhibitory (interneuron) cell in cortex.  The model is based
	# on the presence of two voltage-dependent currents: 
    #     - INa, IK: action potentials
	# (no spike-frequency adaptation in this model)
    '''
        #  Model described in:

        #    Pospischil, M., Toledo-Rodriguez, M., Monier, C., Piwkowska, Z., 
        #    Bal, T., Fregnac, Y., Markram, H. and Destexhe, A.
        #    Minimal Hodgkin-Huxley type models for different classes of
        #    cortical and thalamic neurons.
        #    Biological Cybernetics 99: 427-441, 2008.

        #   The model was taken from a thalamocortical model, described in:

        #    Destexhe, A., Contreras, D. and Steriade, M.
        #    Mechanisms underlying the synchronizing action of corticothalamic
        #    feedback through inhibition of thalamic relay cells.
        #    J. Neurophysiol. 79: 999-1016, 1998.


        #         Alain Destexhe, CNRS, 2009
        # 	http://cns.iaf.cnrs-gif.fr
    '''
    # Paper has more detail on different parameters and on which were chosen for each test/figure
    
    name= "Fast Spiking"

    def _setup_morphology(self):
        super()._setup_morphology()
        # self.soma = h.Section(name="soma", cell=self)
        # self.dend = h.Section(name="dend", cell=self)
        # self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 67*um #so area is about 14000 um2
        self.dend.L = 900*um # similar area 
        self.dend.diam = 5*um
        #self.name = "Fast Spiking"

    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1  # Membrane capacitance in micro Farads / cm^2
            sec.insert("pas")
            sec.insert("extracellular")
            sec.insert('xtra')
            sec.insert('hh2')

            for seg in sec: 
                seg.pas.g = 0.00015	  # Passive conductance in S/cm2 #Rin = 48Meg
                # // conversion with McC units: 
                # // g(S/cm2) = g(nS)*1e-9/29000e-8
                # //	    = g(nS) * 3.45e-
                seg.pas.e = -70  # Leak reversal potential mV
                # HH parameters
                seg.hh2.vtraub= -55  # resting Vm, BJ was -55
                seg.hh2.gnabar= 0.05 # McCormick=15 muS, thal was 0.09
                # gkbar_hh2 = 0.007	# McCormick=2 muS, thal was 0.01
                # gkbar_hh2 = 0.004
                seg.hh2.gkbar = 0.01	# spike duration of interneurons
                seg.ek=-100*mV
                seg.ena=50*mV

         # NEW: the synapse - definimos a localização da sinapse em cada célula da classe ball and stick
        self.syn = h.ExpSyn(self.soma(0.5))
        self.syn.tau = 2 * ms
        self.v_init=-70

class Intrinsic_Bursting(Cell):
   
    # Simplified model of bursting cortical neuron
	# ============================================

    #     Single-compartment model of "rebound bursts" in pyramidal
    #     neurons (type of cell very common in association areas of
	# cortex).  The model is based on the presence of four
    #     voltage-dependent currents: 
    #     - INa, IK: action potentials
    #     - IM: slow K+ current for spike-frequency adaptation
    #     - IL: L-type calcium currents for burst generation
    '''
    Model described in:

    Pospischil, M., Toledo-Rodriguez, M., Monier, C., Piwkowska, Z., 
    Bal, T., Fregnac, Y., Markram, H. and Destexhe, A.
    Minimal Hodgkin-Huxley type models for different classes of
    cortical and thalamic neurons.
    Biological Cybernetics 99: 427-441, 2008.


            Alain Destexhe, CNRS, 2009
        http://cns.iaf.cnrs-gif.fr'''
    # Paper has more detail on different parameters and on which were chosen for each test/figure
    
    name= "Intrinsically Bursting"

    
    def _setup_morphology(self):
        super()._setup_morphology()
        # self.soma = h.Section(name="soma", cell=self)
        # self.dend = h.Section(name="dend", cell=self)
        # self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 96*um #so area is about 29000 um2
        self.dend.L = 1843*um #so area is similar...
        self.dend.diam = 5*um
    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1  # Membrane capacitance in micro Farads / cm^2
            sec.insert("pas")
            sec.insert("extracellular")
            sec.insert('xtra')
            sec.insert('hh2')   # Hodgin-Huxley INa and IK 
            sec.insert("im")    # M current  
            sec.insert("cad")   # calcium decay
            sec.insert("ical")  # IL current
            h.im.taumax=1000
            sec.ek=-100*mV
            sec.ena=50*mV 
            sec.cai=2.4e-4
            sec.cao=2
            sec.eca=120
            for seg in sec: 
                seg.pas.g = 1e-5    # Passive conductance in S/cm2 #idem TC cell
                # // conversion with McC units: 
	            # // g(S/cm2) = g(nS)*1e-9/29000e-8
	            # //	    = g(nS) * 3.45e-6
                seg.pas.e = -85  # Leak reversal potential mV

                # HH parameters
                seg.hh2.vtraub= -55  # resting Vm, BJ was -55
                seg.hh2.gnabar= 0.05 # McCormick=15 muS, thal was 0.09
                # gkbar_hh2 = 0.007	# McCormick=2 muS, thal was 0.01
                # gkbar_hh2 = 0.004
                seg.hh2.gkbar = 0.005	# spike duration of pyramidal cells
                  

                #IM parameters
                seg.im.gkbar=3e-5   # specific to LTS pyr cell
                
                #cad parameters
                seg.cad.depth=1 #McCormick=0.1 um
                seg.cad.taur=5  #McCormick=1 ms
                seg.cad.cainf=2.4e-4 #McCormick=0
                seg.cad.kt=0         # no pump  

                #ical parameters 
                # // L-current density:
                # // 0.0001 -> RS behavior
                # // 0.00017 -> one burst, then RS
                # // 0.0002 -> two bursts, then RS
                # // 0.00022 -> repetitive bursting
                seg.ical.gcabar=1.7e-4
                

         # NEW: the synapse - definimos a localização da sinapse em cada célula da classe ball and stick
        self.syn = h.ExpSyn(self.soma(0.5))
        self.syn.tau = 2 * ms
        self.v_init=-84

class Repetitive_Bursting(Cell):
   
    # Simplified model of repetitive bursting cortical neuron
	# ============================================

    #     Single-compartment model of "rebound bursts" in pyramidal
    #     neurons (type of cell very common in association areas of
	# cortex).  The model is based on the presence of four
    #     voltage-dependent currents: 
    #     - INa, IK: action potentials
    #     - IM: slow K+ current for spike-frequency adaptation
    #     - IL: L-type calcium currents for burst generation
    #       Repetitive bursting with stronger IL
    '''
    Model described in:

    Pospischil, M., Toledo-Rodriguez, M., Monier, C., Piwkowska, Z., 
    Bal, T., Fregnac, Y., Markram, H. and Destexhe, A.
    Minimal Hodgkin-Huxley type models for different classes of
    cortical and thalamic neurons.
    Biological Cybernetics 99: 427-441, 2008.


            Alain Destexhe, CNRS, 2009
        http://cns.iaf.cnrs-gif.fr'''
    
    # Paper has more detail on different parameters and on which were chosen for each test/figure
    # Not much of a point in having this one, only changes one thing comparing top 1
    name= "Repetitive Bursting"

    
    def _setup_morphology(self):
        super()._setup_morphology()
        # self.soma = h.Section(name="soma", cell=self)
        # self.dend = h.Section(name="dend", cell=self)
        # self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 96*um #so area is about 29000 um2
        self.dend.L = 1843*um #so area is similar...
        self.dend.diam = 5*um
    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1  # Membrane capacitance in micro Farads / cm^2
            sec.insert("pas")
            sec.insert("extracellular")
            sec.insert('xtra')
            sec.insert('hh2')   # Hodgin-Huxley INa and IK 
            sec.insert("im")    # M current  
            sec.insert("cad")   # calcium decay
            sec.insert("ical")  # IL current
            h.im.taumax=1000
            sec.ek=-100*mV
            sec.ena=50*mV 
            sec.cai=2.4e-4
            sec.cao=2
            sec.eca=120

            for seg in sec: 
                seg.pas.g = 1e-5    # Passive conductance in S/cm2 #idem TC cell
                # // conversion with McC units: 
	            # // g(S/cm2) = g(nS)*1e-9/29000e-8
	            # //	    = g(nS) * 3.45e-6
                seg.pas.e = -85  # Leak reversal potential mV

                # HH parameters
                seg.hh2.vtraub= -55  # resting Vm, BJ was -55
                seg.hh2.gnabar= 0.05 # McCormick=15 muS, thal was 0.09
                # gkbar_hh2 = 0.007	# McCormick=2 muS, thal was 0.01
                # gkbar_hh2 = 0.004
                seg.hh2.gkbar = 0.005	# spike duration of pyramidal cells
                  

                #IM parameters
                seg.im.gkbar=3e-5   # specific to LTS pyr cell
                
                #cad parameters
                seg.cad.depth=1 #McCormick=0.1 um
                seg.cad.taur=5  #McCormick=1 ms
                seg.cad.cainf=2.4e-4 #McCormick=0
                seg.cad.kt=0         # no pump  

                #ical parameters 
                # // L-current density:
                # // 0.0001 -> RS behavior
                # // 0.00017 -> one burst, then RS
                # // 0.0002 -> two bursts, then RS
                # // 0.00022 -> repetitive bursting
                seg.ical.gcabar=2.2e-4
                

         # NEW: the synapse - definimos a localização da sinapse em cada célula da classe ball and stick
        self.syn = h.ExpSyn(self.soma(0.5))
        self.syn.tau = 2 * ms
        self.v_init=-84

class Low_Threshold(Cell):
   
    # Simplified model of bursting cortical neuron
	# ============================================
	# LTS CORTICAL PYRAMIDAL CELL

    #     Single-compartment model of "rebound bursts" in pyramidal
    #     neurons (type of cell very common in association areas of
	# cortex).  The model is based on the presence of four
    #     voltage-dependent currents: 
    #     - INa, IK: action potentials
    #     - IM: slow K+ current for spike-frequency adaptation
    #     - IT: T-type calcium currents for burst generation
    '''
    Model described in:

    Pospischil, M., Toledo-Rodriguez, M., Monier, C., Piwkowska, Z., 
    Bal, T., Fregnac, Y., Markram, H. and Destexhe, A.
    Minimal Hodgkin-Huxley type models for different classes of
    cortical and thalamic neurons.
    Biological Cybernetics 99: 427-441, 2008.

    The model was originally published in the following reference:

    Destexhe, A. Contreras, D. and Steriade, M.
    LTS cells in cerebral cortex and their role in generating
    spike-and-wave oscillations.   
    Neurocomputing 38: 555-563 (2001).


            Alain Destexhe, CNRS, 2009
        http://cns.iaf.cnrs-gif.fr'''
    
    # Paper has more detail on different parameters and on which were chosen for each test/figure
    # Not much of a point in having this one, only changes one thing comparing top 1
    name= "Low Threshold"

    
    def _setup_morphology(self):
        super()._setup_morphology()
        # self.soma = h.Section(name="soma", cell=self)
        # self.dend = h.Section(name="dend", cell=self)
        # self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 89.2*um #so area is about 29000 um2
        self.dend.L = 1591*um #so area is similar...
        self.dend.diam = 5*um

    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1  # Membrane capacitance in micro Farads / cm^2
            sec.insert("pas")
            sec.insert("extracellular")
            sec.insert('xtra')
            sec.insert('hh2')   # Hodgin-Huxley INa and IK 
            sec.insert("im")    # M current  
            sec.insert("cad")   # calcium decay
            sec.insert("it")  # IT current
            h.im.taumax=1000
            sec.ek=-100*mV
            sec.ena=50*mV 
            sec.cai=2.4e-4
            sec.cao=2
            sec.eca=120

            for seg in sec: 
                seg.pas.g = 1e-5    # Passive conductance in S/cm2 #idem TC cell
                # // conversion with McC units: 
	            # // g(S/cm2) = g(nS)*1e-9/29000e-8
	            # //	    = g(nS) * 3.45e-6
                seg.pas.e = -85  # Leak reversal potential mV

                # HH parameters
                seg.hh2.vtraub= -55  # resting Vm, BJ was -55
                seg.hh2.gnabar= 0.05 # McCormick=15 muS, thal was 0.09
                # gkbar_hh2 = 0.007	# McCormick=2 muS, thal was 0.01
                # gkbar_hh2 = 0.004
                seg.hh2.gkbar = 0.005	# spike duration of pyramidal cells
                  

                #IM parameters
                seg.im.gkbar=3e-5   # specific to LTS pyr cell
                
                #cad parameters
                seg.cad.depth=1 #McCormick=0.1 um
                seg.cad.taur=5  #McCormick=1 ms
                seg.cad.cainf=2.4e-4 #McCormick=0
                seg.cad.kt=0         # no pump  

                #it parameters 
                #T-current density adjusted to delaPena & Geigo-Barrientos
                seg.it.gcabar=4e-4 # specific to LTS pyr cell
                # // this parameter set (above) is for bursting behavior; for 
                # // regular spiking:
                # //   e_pas = -75
                # //   El[0].stim.amp = 0.12
                # // LTS:
                # //   e_pas = -60
                # //   El[0].stim.amp = -0.075
                # // bursting:
                # //   e_pas = -85
                # //   El[0].stim.amp = 0.15
                # // classic RS and FS behavior are obtained by blocking IT and IM successively

         # NEW: the synapse - definimos a localização da sinapse em cada célula da classe ball and stick
        self.syn = h.ExpSyn(self.soma(0.5))
        self.syn.tau = 2 * ms
        self.v_init=-84

class Regular_Spiking(Cell):
   
    # Simplified model of regular-spiking cortical neuron
	# ===================================================
    # REGULAR-SPIKING CORTICAL PYRAMIDAL CELL
    #     Single-compartment model of "regular-spiking" pyramidal neurons,
    #     which is the most commonly encountered electrophysiological type
    #     of excitatory cell in cortex.  The model is based on the presence
	# of three voltage-dependent currents: 
    #     - INa, IK: action potentials
    #     - IM: slow K+ current for spike-frequency adaptation
    #     (no ICa/IK[Ca] in this model)

    ''' Model described in:

   Pospischil, M., Toledo-Rodriguez, M., Monier, C., Piwkowska, Z., 
   Bal, T., Fregnac, Y., Markram, H. and Destexhe, A.
   Minimal Hodgkin-Huxley type models for different classes of
   cortical and thalamic neurons.
   Biological Cybernetics 99: 427-441, 2008.

    The model was taken from a thalamocortical model, described in:

   Destexhe, A., Contreras, D. and Steriade, M.
   Mechanisms underlying the synchronizing action of corticothalamic
   feedback through inhibition of thalamic relay cells.
   J. Neurophysiol. 79: 999-1016, 1998.



        Alain Destexhe, CNRS, 2009
	http://cns.iaf.cnrs-gif.fr
    '''
    
    # Paper has more detail on different parameters and on which were chosen for each test/figure
    # Not much of a point in having this one, only changes one thing comparing top 1
    name= "Regular Spiking"

    
    def _setup_morphology(self):
        super()._setup_morphology()
        # self.soma = h.Section(name="soma", cell=self)
        # self.dend = h.Section(name="dend", cell=self)
        # self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 61.8*um #so area is about 1200 um2
        self.dend.L = 764*um #so area is similar...
        self.dend.diam = 5*um
    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1  # Membrane capacitance in micro Farads / cm^2
            sec.insert("pas")
            sec.insert("extracellular")
            sec.insert('xtra')
            sec.insert('hh2')   # Hodgin-Huxley INa and IK 
            sec.insert("im")    # M current  
            sec.insert("cad")   # calcium decay
            sec.insert("it")  # IT current
            h.im.taumax=1000
            sec.ek=-100*mV
            sec.ena=50*mV 
            sec.cai=2.4e-4
            sec.cao=2
            sec.eca=120

            for seg in sec: 
                seg.pas.g = 1e-4    # Passive conductance in S/cm2 #Rin = 34 Meg
                seg.pas.e = -70  # Leak reversal potential mV
                # // conversion with McC units: 
                # // g(S/cm2) = g(nS)*1e-9/29000e-8
                # //	    = g(nS) * 3.45e-6

                # HH parameters
                seg.hh2.vtraub= -55  # resting Vm, BJ was -55
                seg.hh2.gnabar= 0.05 # McCormick=15 muS, thal was 0.09
                # gkbar_hh2 = 0.007	# McCormick=2 muS, thal was 0.01
                # gkbar_hh2 = 0.004
                seg.hh2.gkbar = 0.005	# spike duration of pyramidal cells
                  

                #IM parameters
                seg.im.gkbar=7e-5   # Diego's IM (copyrighted)
                
                #cad parameters
                seg.cad.depth=1 #McCormick=0.1 um
                seg.cad.taur=5  #McCormick=1 ms
                seg.cad.cainf=2.4e-4 #McCormick=0
                seg.cad.kt=0         # no pump  

                #it parameters 
                #T-current density adjusted to delaPena & Geigo-Barrientos
                seg.it.gcabar=4e-4 # specific to LTS pyr cell
                # // this parameter set (above) is for bursting behavior; for 
                # // regular spiking:
                # //   e_pas = -75
                # //   El[0].stim.amp = 0.12
                # // LTS:
                # //   e_pas = -60
                # //   El[0].stim.amp = -0.075
                # // bursting:
                # //   e_pas = -85
                # //   El[0].stim.amp = 0.15
                # // classic RS and FS behavior are obtained by blocking IT and IM successively
                
         # NEW: the synapse - definimos a localização da sinapse em cada célula da classe ball and stick
        self.syn = h.ExpSyn(self.soma(0.5))
        self.syn.tau = 2 * ms
        self.v_init=-70
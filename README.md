# Minimal Hodgkin–Huxley type models for different classes of cortical and thalamic neurons

- Fast Spiking 
- Regular Spiking 
- Intrinsically Bursting
- Low-Threshold Spike

Models described in:
[Pospischil, M., Toledo-Rodriguez, M., Monier, C., Piwkowska, Z., Bal, T., Fregnac, Y., Markram, H. and Destexhe, A. "Minimal Hodgkin-Huxley type models for different classes of cortical and thalamic neurons." Biological Cybernetics 99: 427-441, 2008.](https://link.springer.com/article/10.1007/s00422-008-0263-8)

Adapted into different python classes, flexibility introduced with variable number of compartments, extracellular mechanism and possibility of stimulation.

## Usage
Clone the repository, go into mechanisms and compile, by writing "mknrndll" on the console.
**test_EC.ipynb** - for extracellular stimulation, run , choosing between the rx and stim methods.
**test_electrode.ipynb** - with a current clamp similar to the paper - can recreate the obtained results.
Change the cell class as you see fit.



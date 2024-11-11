from neuron import h

# Define the frequency and d_lambda (used to calculate nseg)
freq = 1000  # Hz, frequency at which AC length constant will be computed
d_lambda = 0.1

# Define the function to compute the AC length constant
def lambda_f(sec, freq):
    """Calculate the AC length constant for a section."""
    if sec.n3d() < 2:
        # If there are fewer than 2 3D points, use a simpler approximation
        return 1e5 * (sec.diam / (4 * h.PI * freq * sec.Ra * sec.cm)) ** 0.5
    # Use the 3D coordinates to get a more accurate estimate
    x1 = sec.arc3d(0)
    d1 = sec.diam3d(0)
    lam = 0
    for i in range(1, int(sec.n3d())):
        x2 = sec.arc3d(i)
        d2 = sec.diam3d(i)
        lam += (x2 - x1) / ((d1 + d2) / 2) ** 0.5
        x1 = x2
        d1 = d2
    # Length of the section in units of lambda
    lam *= (2 ** 0.5) * 1e-5 * ((4 * h.PI * freq * sec.Ra * sec.cm) ** 0.5)
    return sec.L / lam

# Define the procedure to set nseg in each section
def geom_nseg(self):
    """Adjust nseg for all sections to ensure proper spatial discretization."""
    h.define_shape()  # Update geometry for all sections # Ensure that diam reflects 3D points
    for sec in self.all:
        # Set nseg based on L, d_lambda, and lambda_f
        nseg = int((sec.L / (d_lambda * lambda_f(sec, freq)) + 0.9) / 2) * 2 + 1
        sec.nseg = nseg
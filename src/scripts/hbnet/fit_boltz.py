#!/usr/bin/env python
import pylab
import numpy as np
from scipy.optimize import curve_fit

'''Fit the distribution of energies of the intermediate states.
'''

def fitfu(x, a, b):
    return a * np.exp(-b*x)

def main():
    energies = [float(ener) for ener in open("energytraject.txt")]
    N = len(energies)
    (n, bins, patches) = pylab.hist(energies, color="green")
    print n
    print bins
    print patches
    p = n/float(N)
    print p
    e = []
    for i in range(len(bins)-1):
        e.append((bins[i] + bins[i+1])/2)
    e = np.array(e)
    print e
#     print e
#     print p
#     popt, pcov = curve_fit(fitfu, e, n)
    pylab.plot(e, n, color="yellow")
#     pylab.plot(e, popt[0] * np.exp(-1 * popt[1] * e), color="red")
#     pylab.title("a=%.3f b=%.3f astd=%.3f bstd=%.3f" % (popt[0], popt[1], pcov[0][0], pcov[1][1]))
#     x = pylab.linspace(0, 50, 100)
#     yn = fitfu(x, 2.5, 1.3) + 0.2*np.random.normal(size=len(x))
#     popt, pcov = curve_fit(fitfu, x, yn)
#     print popt
#     print pcov
    pylab.show()
    
if __name__ == "__main__":
    main()
    
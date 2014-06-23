#!/usr/bin/env python
import matplotlib.pylab as plt
import os

def plot_e_dist():
    baseDir = "/Users/xzhu/sibyl"
    paths = [os.path.join(baseDir, "BR2/1C3W/hydro/def/raw_O/pathStatistics.txt"),\
             os.path.join(baseDir, "BR2/1C8R/hydro/def/raw_O/pathStatistics.txt"),\
             os.path.join(baseDir, "BR2/1CKG9/hydro/def/raw_O/pathStatistics.txt")]

    energies = []
    allPahts = "pathStatistics.txt"
    for i in range(len(paths)):
        for eachLine in open(paths[i]):
            energies.append(float(eachLine.split()[-1]))
        
        x = [i+1] * len(energies)
        plt.plot(x, energies, 'r_', markersize=30)
        energies = []
        
    plt.xticks([1,2,3], ["1C3W", "1C8R", "1KG9"])
    plt.ylabel("energy barrier(kcal/mol)")
    plt.title("distribution of energy barriers of pathways")
    plt.xlim(0, 10)
    plt.show()
    
if __name__ == "__main__":
    plot_e_dist()
    
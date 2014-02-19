from pymol import cmd
from os import listdir
def loadMultiConf():
    keyRes = ["ASPA0085", "HOHA0402", "HOHA0406", "ARGA0082", "HOHA0403", "GLUA0194"]

    for res in keyRes:
        for f in os.listdir("."):
	    if res[3:] in f:
	    	cmd.load(f)

cmd.extend("loadMultiConf", loadMultiConf)

from pymol import cmd

def loadAllPdb(removeAll=True):

    if removeAll:
    	cmd.delete("all")
    allPdbs = ["1C3W", "1C8R", "1KG9", "1DZE", "1KG8", "1C8S"]
    homeDir = "/Users/xzhu/sibyl/BR_ipe_mem/"

    for pdb in allPdbs:
        cmd.load(homeDir + pdb + "/qu/step2_out.pdb", pdb)

    cmd.hide("everything", "resn hoh")
    cmd.hide("lines")
    cmd.show("cartoon")

cmd.extend("loadAllPdb", loadAllPdb)

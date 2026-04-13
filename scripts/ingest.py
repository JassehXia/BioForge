from Bio.PDB import PDBList, PDBParser, PDBIO, Select

class CleanSelect(Select):
    """
    This class acts as a filter. For every residue and atom in 
    the structure, the IO writer will call these methods.
    """
    def accept_residue(self, residue):
        res_name = residue.get_resname() # get the residue name

        if res_name == "HOH": # don't accept if it is H2O (Water)
            return False
        return True

    def accept_atom(self, atom):
        alt_loc = atom.get_altloc() # get the alternate location of an atom

        if alt_loc in [' ', 'A']: # Keep if atom is in priamry location
            return True

        return False # otherwise, if an alt location present, discard

def bootstrap():
    pdbl = PDBList() # initialized the PDB database connection
    
    # 1. Fetch
    print("--- Fetching 1OPJ ---")
    raw_path = pdbl.retrieve_pdb_file("1OPJ", pdir="data/raw", file_format="pdb")

    parser = PDBParser(QUIET=True) # translates raw text to a python structure object
    io = PDBIO() # saves results to file 
    structure = parser.get_structure("1OPJ", raw_path)
    

    io.set_structure(structure) # tells the IO writer which structure to save
    output_path = "data/processed/1OPJ_clean.pdb"

    print("--- Saving Cleaned PDB ---")
    io.save(output_path, CleanSelect())

if __name__ == "__main__":
    bootstrap()

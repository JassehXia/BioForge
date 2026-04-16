from Bio.PDB import PDBList, PDBParser, PDBIO, Select, Selection, NeighborSearch
from Bio.PDB.Polypeptide import is_aa
import os

class CleanSelect(Select):
    """
    Bio.PDB selection filter for structural standardization.
    Identifies protein residues and the target ligand.
    """
    def accept_residue(self, residue):
        # strip away impurities like H2O, etc.

        residue_name = residue.get_resname()

        if is_aa(residue):
            return True

        if residue_name == "STI":
            return True
        return False

    def accept_atom(self, atom):
        # only accepts the primary location

        alt_loc = atom.get_altloc()

        if alt_loc in [' ', 'A']:
            return True
        return False

class IngestionManager:
    """
    Orchestration layer for target acquisition, cleaning, and pocket extraction.
    """
    def __init__(self, raw_dir="data/raw", processed_dir="data/processed"):
        self.raw_dir = raw_dir
        self.processed_dir = processed_dir
        self.parser = PDBParser(QUIET=True)
        self.pdbl = PDBList()

    def fetch_target(self, pdb_id):
        """
        Retrieves a target PDB from RCSB.
        :return: String path to the raw file.
        """

        raw_path = self.pdbl.retrieve_pdb_file(
            pdb_id,
            pdir=self.raw_dir,
            file_format = "pdb",
            overwrite=True
        )

        return raw_path
        pass

    def clean_structure(self, pdb_id, raw_path):
        """
        Applies CleanSelect and saves a sanitized version of the protein.
        :return: String path to the cleaned file.
        """

        structure = self.parser.get_structure(pdb_id, raw_path)
        io = PDBIO()
        io.set_structure(structure)

        output_path = os.path.join(self.processed_dir, f"{pdb_id}_clean.pdb")

        io.save(output_path, CleanSelect())
        return output_path
        pass

    def extract_active_site(self, structure, pivot_residue="STI", radius=5.0):
        """
        Identifies all residues within a physical distance of a target ligand.
        :return: List of Residue objects.
        """
        

        # finding the center
        target_atoms = [atom for atom in structure.get_atoms() if atom.get_parent().get_resname() == pivot_residue]

        # flattens to an array to go through
        all_atoms = Selection.unfold_entities(structure, "A")

        # instantiate the NeighborSearch to look near at a radius of the center
        ns = NeighborSearch(all_atoms)

        pocket_residues = set()

        # search at a radius around the center atom
        for atom in target_atoms:
            results = ns.search(atom.coord, radius, level='R')
            pocket_residues.update(results)

        return list(pocket_residues)
        pass

# Mentorship: Example Usage
if __name__ == "__main__":
    # This block allows you to test the manager as you build it.
    manager = IngestionManager()
    
    target_id = "1OPJ"
    path = manager.fetch_target(target_id)
    clean_path = manager.clean_structure(target_id, path)
    
    print(f"Cleaned PDB ready at: {clean_path}")

import numpy as np
from Bio.PDB import PDBParser

class DockingEngine:
  """
  Orchestrates the AutoDock Vina simulation via Docker.
  """
  def calculate_grid(self, pocket_residues):
    """
    Calculates the 3D center and dimensions of the docking box.
    :param pocket_residues: List of Bio.PDB.Residue objects from Iteration 1.
    :return: (center_coords, box_size)
    """

    # 1. Collect all atom coordinates from every residue in the pocket
    atom_coords = []
    for res in pocket_residues:
      for atom in res.get_atoms():
        atom_coords.append(atom.get_coord())
    

    coords_array = np.array(atom_coords)

    # Find the center of mass of the pocket
    center = np.mean(coords_array, axis=0)

    #Find the box size
    # add a buffer of 5-10Aof buffer to ensure rotation is free
    min_coords = np.min(coords_array, axis=0)
    max_coords = np.max(coords_array, axis=0)
    size = max_coords - min_coords + 10

    return center, size 

  def run_vina(self, protein_path, ligand_path, config):
    # TODO: Subprocess call to Docker container 'vina' command
    pass

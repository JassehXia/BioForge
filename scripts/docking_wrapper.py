import numpy as np
from Bio.PDB import PDBParser
import subprocess
import os

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

  def run_vina(self, protein_path, ligand_path, center, size):
    """
    Executes the docking simulation by calling the Docker container.
    """

    output_path = ligand_path.replace(".pdbqt", "_out.pdbqt")

    # Construct the Docker command
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{os.getcwd()}:/app",
        "bioforge-vina",
        "vina",
        "--receptor", f"/app/{protein_path}",
        "--ligand", f"/app/{ligand_path}",
        "--center_x", str(center[0]),
        "--center_y", str(center[1]),
        "--center_z", str(center[2]),
        "--size_x", str(size[0]),
        "--size_y", str(size[1]),
        "--size_z", str(size[2]),
        "--out", f"/app/{output_path}"
    ]

    print(f"--- Running Simulation inside of Docker ---")

    # use a subprocess to run the command and wait for completion
    result = subprocess.run(docker_cmd, capture_output = True, text=True)

    if result.returncode == 0:
      print("Simulation complete!")
      return result.stdout 

    else:
      print("Simulation failed")
      return None
    

if __name__ == "__main__":
    engine = DockingEngine()
    parser = PDBParser(QUIET=True)
    
    # 1. Load the protein to identify the pocket coordinates
    protein_pdb = "data/processed/1OPJ_clean.pdb"
    structure = parser.get_structure("1OPJ", protein_pdb)
    
    # 2. Extract residues to define the 'Search Box'
    # For this test, we'll just use all residues in Chain A
    # (In a real run, you'd use your specific Active Site list)
    all_residues = []
    for model in structure:
        for chain in model:
            if chain.id == "A":
                all_residues.extend(list(chain.get_residues()))
    
    print(f"Calculating grid for {len(all_residues)} residues...")
    center, size = engine.calculate_grid(all_residues)
    print(f"Grid Center: {center}")
    print(f"Grid Size: {size}")

    # 3. Run the Docking simulation
    # We'll use the files we prepared in the last step
    protein_pdbqt = "data/processed/1OPJ_clean.pdbqt"
    ligand_pdbqt = "test_ligand.pdbqt" # The Benzene we made earlier
    
    output = engine.run_vina(protein_pdbqt, ligand_pdbqt, center, size)
    
    if output:
        print("\n--- Simulation Output ---")
        print(output)

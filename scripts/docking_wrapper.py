import numpy as np
from Bio.PDB import PDBParser
import subprocess
import os
import re

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
    
    # 1. Extract just the filename (e.g., 'imatinib.pdbqt')
    ligand_filename = os.path.basename(ligand_path)
    
    # 2. Create the output path in the results folder
    # Result: 'data/results/imatinib_out.pdbqt'
    output_filename = ligand_filename.replace(".pdbqt", "_out.pdbqt")
    output_path = f"data/results/{output_filename}"

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

  def parse_score(self, vina_output):
    """
    Extracts the best affinity score from the Vina output text
    """

    # We look for '1' (the mode) followed by the score (e.g., -4.652)
    # Pattern: find the first number in the 'affinity' column
    match = re.search(r"^\s+1\s+(-?\d+\.\d+)", vina_output, re.MULTILINE)

    if match:
      affinity = float(match.group(1))
      return affinity

    return None

if __name__ == "__main__":
    engine = DockingEngine()
    parser = PDBParser(QUIET=True)
    
    # 1. Load protein for grid calculation
    protein_pdb = "data/processed/1OPJ_clean.pdb"
    structure = parser.get_structure("1OPJ", protein_pdb)
    
    # 2. Extract Active Site (Chain A)
    all_residues = [r for m in structure for c in m if c.id == "A" for r in c]
    center, size = engine.calculate_grid(all_residues)

    # 3. Define our Benchmark files
    # (Note: Make sure you prepared imatinib.pdbqt using preparation.py!)
    protein_pdbqt = "data/processed/1OPJ_clean.pdbqt"
    ligand_pdbqt = "data/processed/imatinib.pdbqt" 
    
    # 4. Run & Parse
    raw_output = engine.run_vina(protein_pdbqt, ligand_pdbqt, center, size)
    
    if raw_output:
        best_score = engine.parse_score(raw_output)
        print(f"\n✅ VALIDATION COMPLETE")
        print(f"Target: BCR-ABL (1OPJ)")
        print(f"Ligand: Imatinib")
        print(f"Calculated Affinity: {best_score} kcal/mol")
        
        if best_score and best_score < -8.0:
            print("🚀 PIPELINE VALIDATED: Replicated high-affinity bind!")
    else:
        print("Docking simulation did not return a valid output.")
        

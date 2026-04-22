from meeko import MoleculePreparation, PDBQTWriterLegacy
from rdkit import Chem
from rdkit.Chem import AllChem
import subprocess
import os

class MolecularPreparer:
  def embed_3d(self, mol):
    mol = Chem.AddHs(mol) # Returns a new molecule with hydrogens
    AllChem.EmbedMolecule(mol) # Generate a 3D conformer
    AllChem.MMFFOptimizeMolecule(mol) # Optimize the molecule's internal strain
    return mol 
    
  def convert_to_pdbqt(self, mol, output_path):
    prepper = MoleculePreparation()
    meeko_setups = prepper.prepare(mol) # Returns a list

    # Instantiating the Legacy writer
    writer = PDBQTWriterLegacy()
    
    # We take the first setup from the list
    pdbqt_string, is_ok, error_msg = writer.write_string(meeko_setups[0])

    if is_ok:
        with open(output_path, "w") as f:
            f.write(pdbqt_string)
        return True
    return False
  def prepare_receptor(self, cleaned_pdb_path):
    """
    Converts a cleaned PDB protein into a PDBQT receptor.
    Required for AutoDock Vina simulation.
    """

    output_path = cleaned_pdb_path.replace(".pdb", ".pdbqt")
     # 1. We use the 'mk_prepare_receptor' tool that came with Meeko
    # -i: Input path
    # -o: Output path
    # --add_hydrogens: Ensures polar hydrogens are present
    command = [
        "mk_prepare_receptor", 
        "--read_pdb", cleaned_pdb_path, 
        "-p", output_path
    ]

    try:
      print(f"Preparing receptor: {cleaned_pdb_path}")
      # Run the command and await for finish
      subprocess.run(command, check=True, capture_output=True, text=True)
      print(f"Success! {output_path} created.")
      return output_path

    except subprocess.CalledProcessError as e:
      print(f"Error preparing receptor: {e}")
      return None

# Mentorship: Example Usage
if __name__ == "__main__":
    preparer = MolecularPreparer()
    
    # 1. This is the Imatinib SMILES
    imatinib_smiles = "Cc1ccc(cc1Nc2nccc(n2)c3cccnc3)Nc4ccc(cc4C(=O)Nc5ccc(cc5)CN6CCN(CC6)C)"
    mol = Chem.MolFromSmiles(imatinib_smiles)
    
    # 2. Embed 3D
    mol = preparer.embed_3d(mol) 
    
    # 3. Save it as imatinib.pdbqt (NOT test_ligand.pdbqt)
    output_file = "data/processed/imatinib.pdbqt"
    if preparer.convert_to_pdbqt(mol, output_file):
        print(f"Success! {output_file} created.")




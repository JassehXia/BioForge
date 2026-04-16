from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
import logging

class HeuristicFilter:
    """
    Biological filter applying Lipinski's Rule of Five to assess oral bioavailability.
    """
    def __init__(self, max_mw=500, max_logp=5, max_hbd=5, max_hba=10):
        self.max_mw = max_mw
        self.max_logp = max_logp
        self.max_hbd = max_hbd
        self.max_hba = max_hba

    def evaluate(self, mol):
        """
        Calculates Lipinski properties and returns a violation count.
        """
        # Always add hydrogens for accurate property calculation
        mol = Chem.AddHs(mol)
        
        mw = Descriptors.MolWt(mol) # Molecular Weight
        logp = Descriptors.MolLogP(mol) # Lipophilicity
        num_h_donors = Descriptors.NumHDonors(mol) # Hydrogen Bond Donors
        num_h_acceptors = Descriptors.NumHAcceptors(mol) # Hydrogen Bond Acceptors

        # Calculate violation count. Rule of Five states a molecule is 
        # 'drug-like' if it violates NO MORE than one of the criteria.
        violations = 0
        if mw > self.max_mw:
            violations += 1
        if logp > self.max_logp:
            violations += 1
        if num_h_donors > self.max_hbd:
            violations += 1
        if num_h_acceptors > self.max_hba:
            violations += 1
        
        # Return a dictionary containing the calculated properties and violation count
        return {
            "MW": mw,
            "LogP": logp,
            "HBD": num_h_donors,
            "HBA": num_h_acceptors,
            "Violations": violations,
            "Pass": violations <= 1
        }

class MoleculeGenerator:
    """
    Interface for converting raw generative output (SMILES) into 
    sanitized molecular objects.
    """
    def __init__(self):
        self.filter = HeuristicFilter()

    def sanitize_smiles(self, smiles):
        """
        Converts SMILES to a Mol object and performs valence/aromaticity checks.
        """
        # 1. Convert SMILES to Mol object
        mol = Chem.MolFromSmiles(smiles)
        
        if mol is None:
            logging.error(f"Invalid SMILES string: {smiles}")
            return None
            
        # 2. Sanitize (Valence and aromaticity perception)
        try:
            Chem.SanitizeMol(mol)
            return mol
        except Exception as e:
            logging.error(f"Sanitization failed for {smiles}: {e}")
            return None

# Mentorship: Example Usage
if __name__ == "__main__":
    generator = MoleculeGenerator()
    
    # Example: Imatinib (Gleevec) SMILES
    sti_smiles = "CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5"
    
    mol = generator.sanitize_smiles(sti_smiles)
    if mol:
        print(f"SMILES sanitized successfully!")
        properties = generator.filter.evaluate(mol)
        print(f"Properties: {properties}")

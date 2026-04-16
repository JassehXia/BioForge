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

    def validate_lipinski(self, mol):
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

    def is_sanitized(self, mol):
        """
        Checks if the molecule survives RDKit's Chem.SanitizeMol().
        """
        # TODO: Implement Sanitization check
        return mol is not None and Chem.SanitizeMol(mol) == 0

class MoleculeGenerator:
    """
    Interface for converting raw generative output (SMILES) into 
    sanitized molecular objects.
    """
    def __init__(self):
        self.filter = HeuristicFilter()

    def generate_candidate(self, template_smiles):
        """
        Generates a SMILES string (initially from a template).
        """
        # 1. Generate SMILES
        # Placeholder for actual generation logic: adding a Methyl group
        raw_smiles = template_smiles + "C"

        # 2. Sanitize SMILES
        # Convert and sanitize
        mol = Chem.MolFromSmiles(raw_smiles)
        if not self.filter.is_sanitized(mol):
            print(f"Candidate {raw_smiles} failed sanitization")
            return None

        # 3. Validate Lipinski
        metrics = self.filter.validate_lipinski(mol)
        if not metrics["Pass"]:
            print(f"Candidate {raw_smiles} failed Lipinski validation")
            return None
        
        # Return the valid molecule
        return {
            "smiles": raw_smiles,
            "mol": mol,
            "metrics": metrics
        }


# Mentorship: Example Usage
if __name__ == "__main__":
    generator = MoleculeGenerator()
    
    # Example 1: Imatinib (Gleevec) SMILES - Positive Control
    sti_smiles = "CC1=C(C=C(C=C1)NC(=O)C2=CC=C(C=C2)CN3CCN(CC3)C)NC4=NC=CC(=N4)C5=CN=CC=C5"
    
    print("--- Testing Positive Control (Imatinib) ---")
    mol = Chem.MolFromSmiles(sti_smiles)
    if generator.filter.is_sanitized(mol):
        print(f"SMILES sanitized successfully!")
        properties = generator.filter.validate_lipinski(mol)
        print(f"Properties: {properties}")

    # Example 2: Generative Candidate
    print("\n--- Testing Generative Candidate ---")
    benzene = "c1ccccc1"
    candidate = generator.generate_candidate(benzene)
    if candidate:
        print(f"Generated valid candidate: {candidate['smiles']}")
        print(f"Metrics: {candidate['metrics']}")

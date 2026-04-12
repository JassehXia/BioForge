# Iteration 1: Structural Foundation & Ingestion

## Overview

The first iteration of BioForge focuses on **Target Ingestion & Structural Preprocessing**. In the context of drug discovery, the reliability of a physical simulation depends entirely on the quality of the starting coordinates. This phase transforms raw, noisy biological data into a standardized, "simulation-ready" format.

### Primary Objective
Establish a robust pipeline to programmatically fetch, clean, and refine 3D protein structures from the Protein Data Bank (PDB).

---

## Technical Deep-Dive

### 1. PDB Ingestion
We utilize the `Bio.PDB` module to interact with the Protein Data Bank. The ingestion layer must be capable of handling network-level fetching and local parsing of various file formats (.pdb, .cif).

- **Library**: `Biopython`
- **Component**: `PDBList` for retrieval, `PDBParser` for object-oriented structural manipulation.

### 2. Structural Cleaning (The "Select" Logic)
Raw PDB files often contains "chatter" that interferes with physics-based docking:
- **Solvent Molecules**: Water molecules (HOH) can artificially fill a pocket and block a ligand from identifying the true binding site.
- **Header Residues**: Non-standard residues or crystallization aids that are not part of the biological system.
- **Alternate Locations (Altlocs)**: Some atoms in high-resolution structures occupy multiple positions. We must select the primary position (usually location 'A') to avoid "clashing" with the physics engine.

### 3. Active Site Identification
The "active site" or "pocket" defines where the simulation grid will be placed. We use a **Coordinate-Based Search** via `NeighborSearch` to identify residues within a specific radius of a focal point (e.g., a known ligand or a catalytic triad).

---

## Architectural Scaffolding

> [!NOTE]
> As per the Operating Rules in `ai.md`, you are responsible for fulfilling the logic inside these methods. These stubs define the interface and architectural requirements for the `IngestionManager`.

```python
from Bio.PDB import PDBList, PDBParser, PDBIO, Select, NeighborSearch

class StructuralCleaningSelect(Select):
    """
    Bio.PDB selection filter for structural standardization.
    """
    def accept_residue(self, residue):
        # TODO: Implement logic to discard water/HOH residues
        # TIP: Check residue.get_resname()
        return True

    def accept_atom(self, atom):
        # TODO: Implement logic to handle altlocs
        # TIP: Only accept atom.get_altloc() if it is ' ' or 'A'
        return True

class IngestionManager:
    """
    Orchestration layer for target acquisition and cleaning.
    """
    def __init__(self, workspace_path: str):
        self.workspace = workspace_path
        self.parser = PDBParser(QUIET=True)
        self.pdbl = PDBList()

    def fetch_target(self, pdb_id: str) -> str:
        """
        Retrieves a target PDB from RCSB.
        :return: Local path to the fetched file.
        """
        # TODO: Use PDBList.retrieve_pdb_file()
        pass

    def clean_structure(self, input_path: str, output_path: str):
        """
        Applies StructuralCleaningSelect to remove solvents and altlocs.
        """
        # TODO: Parse structure -> Setup PDBIO -> Save with Selection class
        pass

    def extract_active_site(self, structure_path: str, radius: float = 5.0):
        """
        Identifies 3D coordinates of the target pocket for docking grid definition.
        """
        # TODO: Implement NeighborSearch logic to find residues near a pivot point.
        pass
```

---

## Testing & Validation Protocols

### The "Known-Truth" Rediscovery Benchmark (Iteration 1)

To validate your ingestion pipeline, we will use **Imatinib (Gleevec)** as a positive control against its primary target: **BCR-ABL** (PDB ID: `1OPJ`).

1.  **Ingestion**: Fetch `1OPJ`.
2.  **Cleaning**: Remove water molecules. In the raw file, verify that water molecules exist; in the cleaned file, verify they are gone.
3.  **Active Site Validation**: Use the co-crystallized Imatinib ligand as the center for your `extract_active_site` call. 
4.  **Success Metric**: The system should identify the known binding residues (e.g., MET318, THR315) within the extracted site coordinates.

---

## Guidance: The "Why" behind Protonation

At this stage, structures often lack hydrogen atoms (Protonation). While Biopython identifies coordinates, software like **AutoDock Vina** requires explicit polar hydrogens to calculate hydrogen bonding strength. 

> [!TIP]
> In later iterations, we will integrate `OpenBabel` or `RDKit` to add hydrogens to our cleaned structures before simulation. For now, focus on the **purity** of the heavy-atom coordinates.

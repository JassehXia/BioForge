# Testing Protocol: Iteration 1

This document outlines the validation strategy for the **Structural Foundation & Ingestion** phase. The goal is to ensure that our ingestion pipeline produces high-fidelity, clean coordinates for downstream simulations.

---

## 1. Unit Testing: IngestionManager

We will use `pytest` to validate the core logic of the `IngestionManager`. These tests ensure that the individual components of the cleaning pipeline are working as expected.

### Test Case: PDB Retrieval
- **Objective**: Verify that `fetch_target` correctly downloads and saves a PDB file.
- **Input**: PDB ID `1OPJ`.
- **Assertion**: File exists at the target path and is not empty.

### Test Case: Water Molecule Removal
- **Objective**: Ensure `StructuralCleaningSelect` correctly identifies and removes solvent molecules.
- **Input**: A parsed structure containing `HOH` residues.
- **Assertion**: The saved structure must have zero residues with the name `HOH`.

### Test Case: Alternate Location Selection
- **Objective**: Verify that only the primary atom position (Altloc 'A' or ' ') is retained.
- **Input**: Atom with multiple occupancy positions.
- **Assertion**: `atom.get_altloc()` in the final file must always be ' ' or 'A'.

---

## 2. Integration Test: The "Gleevec" Rediscovery

This "Known-Truth" benchmark is the final proof of Iteration 1 success. We will attempt to rediscover the known binding site of Imatinib (Gleevec).

### Workflow
1.  **Download**: Use the manager to fetch `1OPJ`.
2.  **Process**: Run the structural cleaning algorithm.
3.  **Inspect**: Manually or programmatically confirm the removal of ligands (Imatinib is co-crystallized as residue `STI`).
4.  **Extract Site**: Call `extract_active_site()` using the known coordinates of the `STI` ligand as the pivot point.
5.  **Verify**: Compare the list of residues in the extracted site against the literature-standard binding residues for BCR-ABL.

### Success Criteria
| Metric | Passing Threshold |
| :--- | :--- |
| **Purity** | 0.0% water molecules remaining. |
| **Integrity** | RMSD of heavy atoms < 0.1Å compared to raw (excluding removed atoms). |
| **Site Accuracy** | > 90% overlap with known binding site residues (MET318, THR315, GLU286, etc.). |

---

## 3. Visual Verification

While automated tests are critical, visual inspection provides an immediate "sanity check."

1.  **Open in PyMOL/ChimeraX**: Load both the raw and cleaned PDB files.
2.  **Toggle Water**: Verify that the "cloud" of water molecules around the protein has disappeared in the cleaned version.
3.  **Active Site Mesh**: Visualize the extracted active site residues as a surface or mesh to ensure the "pocket" is correctly isolated.

---

## 4. Automation Command

Once implemented, run the following to execute the test suite:

```bash
# Run unit tests
pytest tests/test_ingestion.py

# Run integration benchmark
python scripts/benchmark_iteration_one.py --pdb 1OPJ
```

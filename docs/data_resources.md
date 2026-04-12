# Data Resources for BioForge

This document centralizes the primary biological and chemical data repositories used for the development, testing, and validation of the BioForge pipeline.

---

## 1. Structural Data (Proteins)

### [RCSB Protein Data Bank (PDB)](https://www.rcsb.org/)
The global repository for 3D atomic coordinates of proteins, nucleic acids, and complex assemblies.
- **Usage**: Primary input for the ingestion pipeline.
- **Access**: Programmatic via Biopython's `PDBList` or REST API.

---

## 2. Validation and Benchmarking

### [PDBbind-CN](http://www.pdbbind.org.cn/)
A comprehensive collection of experimentally determined binding affinity data ($K_i, K_d, IC_{50}$) for all protein-ligand complexes in the PDB.
- **Usage**: Gold standard for validating docking accuracy and scoring functions.
- **Reference Sets**: Use the "Refined Set" for high-fidelity validation.

### [DUD-E (Database of Useful Decoys: Enhanced)](http://dude.docking.org/)
A widely used benchmarking set for virtual screening performance.
- **Usage**: Evaluate "Enrichment Power"—the ability to find true binders within a pool of chemically similar decoys.

### [CASF (Comparative Assessment of Scoring Functions)](http://www.pdbbind.org.cn/casf.php)
A curated benchmark specifically for evaluating the scoring, ranking, docking, and screening power of docking programs.

---

## 3. Chemical Data (Ligands and Molecules)

### [ZINC20 / ZINC22](https://zinc20.docking.org/)
A curated collection of commercially available chemical compounds for virtual screening.
- **Usage**: Library source for large-scale virtual screening or generative candidate generation.
- **Formats**: Available in "ready-to-dock" 3D formats (.pdbqt).

### [ChEMBL](https://www.ebi.ac.uk/chembl/)
A manually curated database of bioactive molecules with drug-like properties.
- **Usage**: Extracting large bioactivity datasets for specific protein targets to train or validate generative models.

### [BindingDB](https://www.bindingdb.org/)
A public database of measured binding affinities, focusing on the interactions of protein targets with drug-like small molecules.

---

## 4. Clinical and Genomic Context

### [MSK-MET Dataset](https://www.cbioportal.org/study/summary?id=msk_met_2021)
A large-scale dataset of patient-matched primary and metastatic tumors.
- **Usage**: (Planned for Phase 6) Correlating molecular leads with specific organ-level metastatic risks.

---

## 🧪 Summary Table

| Resource | Data Type | Primary Role |
| :--- | :--- | :--- |
| **RCSB PDB** | 3D Coordinates | Structural Target Ingestion |
| **PDBbind** | Complexes + Affinities | Scoring/Docking Validation |
| **ZINC** | SMILES/3D Molecules | Screening Libraries |
| **DUD-E** | Actives + Decoys | Enrichment Power Benchmarking |
| **ChEMBL** | Bioactivity | Generative Model Training |
| **BindingDB** | Measured Affinities | Independent Affinity Validation |

# BioForge: Project Master Document

> **Automated Drug-Discovery Pipeline**
> *Bridging the gap between genomic identification and physical simulation.*

---

## Project Overview

**BioForge** is an automated drug-discovery pipeline that bridges the gap between genomic identification and physical simulation. While current tools can predict protein shapes, BioForge focuses on the **application layer**: taking a target protein and "architecting" a validated molecule to bind with it. By integrating **generative AI** with **physics-based docking simulations**, it transforms drug design from a high-cost laboratory experiment into a rapid, iterative software engineering process.

---

## Technical Breakdown

The pipeline is divided into five distinct stages, moving from raw data to validated leads.

### Stage 1: Target Ingestion & Structural Preprocessing
*The foundation of structural accuracy.*
- **PDB Retrieval**: The system fetches 3D atomic coordinates from the Protein Data Bank (PDB) using established bioinformatics libraries such as **Biopython**.
- **Structural Refinement**: Raw PDB files undergo automated preprocessing to remove water molecules, non-standard residues, and co-crystallized ligands.
- **Protonation and Pocket Identification**: The pipeline calculates the optimal placement of hydrogen atoms and identifies the 3D coordinates of the active site (the target "pocket") to define the simulation grid for molecular docking.

### Stage 2: Generative Molecular Synthesis
*Architecting novel chemical structures.*
- **SMILES Generation**: The generative engine outputs **SMILES** (Simplified Molecular Input Line Entry System) strings, which represent complex 3D chemical structures as linear text sequences.
- **Constrained Architecture**: The model is prompted with specific structural constraints derived from the target protein's geometry, ensuring that the generated molecules are physically complementary to the target active site.

### Stage 3: Cheminformatics Heuristics & Filtering
*The "Sanity Filter" for computational efficiency.*
- **Lipinski’s Rule of Five**: Each candidate is evaluated against pharmacological standards for molecular weight, hydrogen bond donors/acceptors, and lipophilicity to assess oral bioavailability.
- **Valence and Stability Check**: Using the **RDKit** library, the system verifies chemical stability, discarding any "hallucinated" structures that violate the fundamental laws of valence.
- **Synthesizeability Scoring**: Candidates are ranked based on their **Synthetic Accessibility (SA)** score to prioritize molecules that can be feasibly manufactured in a laboratory setting.

### Stage 4: Asynchronous Physics-Based Docking
*Validation through physical simulation.*
- **Simulation Orchestration**: The system wraps **AutoDock Vina** within a **FastAPI** environment, leveraging an asynchronous architecture similar to high-performance pipelines used for multimodal data processing.
- **Binding Affinity Calculation**: The simulator calculates the **Gibbs Free Energy** of binding ($\Delta G$). A lower energy score (measured in kcal/mol) indicates a stronger, more stable bond.
- **Task Management**: Heavy computational loads are offloaded to background workers, ensuring the system can process large pools of candidates concurrently without performance degradation.

### Stage 5: Result Persistence & Lead Ranking
*Data intelligence and prioritization.*
- **Relational State Management**: The system utilizes **Prisma** to manage the relational mapping between different protein targets, generated molecules, and their corresponding simulation scores.
- **Database Integration**: All molecular metadata and affinity scores are persisted in **PostgreSQL** via the **Supabase** platform.
- **Lead Prioritization**: An analytical layer identifies the **top-k candidates** (the "leads") based on the lowest binding energy scores and highest chemical stability for final human review.

---

## Tech Stack

### Core Languages
- **Python**: Utilized as the primary language for the backend, scientific logic, and data processing due to its extensive ecosystem of bioinformatics and machine learning libraries.
- **TypeScript**: Employed for the frontend and API client layers to ensure type safety and maintainability across the complex biological data structures.

### Backend & Orchestration
- **FastAPI**: Serves as the high-performance web framework for the API layer, chosen for its native asynchronous support and Pydantic-based data validation.
- **Aiohttp**: Integrated for handling asynchronous HTTP requests, particularly for fetching remote biological data from the Protein Data Bank (PDB).
- **Celery / Redis**: Orchestrates the distributed task queue required for offloading long-running molecular docking simulations from the main API thread.

### Scientific & Cheminformatics Core
- **AutoDock Vina**: The primary physics-based simulation engine for calculating protein-ligand binding affinities.
- **RDKit**: An industry-standard cheminformatics library used for molecular sanitization, descriptor calculation, and SMILES-to-3D structure conversion.
- **Biopython**: Utilized for parsing, manipulating, and cleaning complex PDB and genomic data files.

### Database & Persistence
- **Supabase (PostgreSQL)**: Provides a robust relational database environment for storing molecular leads, simulation scores, and target metadata.
- **Prisma ORM**: Manages the relational state and database migrations, providing a type-safe interface for the PostgreSQL backend.
- **Cloudflare R2**: Integrated as a S3-compatible object storage solution for persisting large 3D coordinate files (.pdb, .pdbqt) with zero egress fees.

### Frontend & Visualization
- **Next.js 15 (App Router)**: Powers the research dashboard, utilizing server components for efficient data fetching and SEO-friendly rendering.
- **Tailwind CSS**: Employed for a responsive, modular UI design.
- **Three.js / React Three Fiber**: Provides the 3D rendering engine for visualizing molecular docking poses and protein surfaces directly in the browser.

### DevOps & Infrastructure
- **Docker**: Containerizes the scientific environment to ensure that complex C++ dependencies (like AutoDock Vina) remain consistent across development and production environments.
- **GitHub Actions**: Automates the CI/CD pipeline, executing the "Sanitization Benchmark" tests on every commit to maintain chemical logic integrity.
- **Vercel**: Handles the deployment and scaling of the Next.js frontend and serverless API functions.

---

## Implementation Roadmap

| Phase | Title | Primary Objective | Key Technologies |
| :--- | :--- | :--- | :--- |
| **P1** | **Structural Foundation** | Acquire and refine biological target data. | Biopython, PDB |
| **P2** | **Simulation Benchmarks** | Validate physics-based simulation core. | AutoDock Vina, Docker |
| **P3** | **Scalable Orchestration** | High-performance FastAPI backend. | FastAPI, Celery, Redis |
| **P4** | **Generative Design** | Integrate AI-driven chemical synthesis. | SMILES, RDKit |
| **P5** | **Result Intelligence** | Distributed persistence & ranking. | Supabase, Prisma, PostgreSQL, R2 |
| **P6** | **Clinical Visualization** | 3D visualizer & clinician dashboard. | Next.js, Three.js, R3F |

---

## Testing Methodology

> [!NOTE]
> The testing and validation methodology for BioForge is structured to ensure that computational predictions are scientifically sound, reproducible, and chemically feasible. Industry standards emphasize a shift from simple virtual screening to a multi-layered verification process that combines heuristic rules, physics-based simulations, and benchmarking against established pharmaceutical data.

### 1. Cheminformatics & Generative Validation
*Focuses on the "chemical grammar" of the molecules generated by the pipeline.*
- **Heuristic Compliance (RDKit)**: Every candidate molecule undergoes automated sanitization via the RDKit library to verify valence laws and chemical semantics.
- **Drug-Likeness Benchmarking**: Candidates are evaluated against the Lipinski’s Rule of Five to assess potential oral bioavailability, ensuring they fall within acceptable ranges for molecular weight and lipophilicity.
- **Synthetic Feasibility Scoring**: The pipeline calculates an **SA (Synthetic Accessibility)** score, which estimates the difficulty of manufacturing a "constructed" drug in a laboratory environment, prioritizing candidates with realistic synthesis routes.

### 2. The "Known-Truth" Rediscovery Benchmark
*Validating architectural logic against retrospective testing.*
- **Positive Control Testing**: The system is tasked with designing a binder for a target with an existing therapy, such as **Imatinib** for the BCR-ABL protein.
- **Validation Metric**: Success is defined by the system independently generating a molecule that achieves a binding affinity score ($\Delta G$) comparable to or better than the established benchmark drug.
- **Structural Precision**: The predicted binding "pose" (the 3D orientation of the drug in the protein pocket) is compared to co-crystallized structures from the Protein Data Bank (PDB) to measure root-mean-square deviation (**RMSD**).

### 3. Comparative Docking & Scoring Calibration
*Benchmarking against high-fidelity scoring models.*
- **Cross-Model Benchmarking**: Simulation results are periodically compared against advanced engines like **GNINA** (which uses convolutional neural networks for scoring) or **ArtiDock** to verify that the system can accurately distinguish between true positives and false positives.
- **Statistical Performance**: Testing includes the calculation of **ROC** (Receiver Operating Characteristic) curves and **Enrichment Factors (EF)** to quantify the pipeline’s ability to pull viable "hits" out of a large pool of generative candidates.

### 4. Infrastructure & Pipeline Reliability
*Technical stress tests for high-performance discovery.*
- **Concurrency & Load Testing**: The FastAPI orchestration layer is tested for its ability to manage hundreds of simultaneous docking simulations across distributed workers without data corruption or memory leaks.
- **Latency Benchmarking**: The system tracks the time elapsed from the initial target ingestion to the final lead ranking, aiming for a "months-to-days" reduction in the early-discovery timeline.
- **Data Integrity Audit**: Utilizing the **Prisma ORM**, the system performs consistency checks to ensure that molecular strings, affinity scores, and 3D coordinate files remain correctly linked within the PostgreSQL database.

### 5. Regulatory & Compliance Readiness
*Alignment with 2026 regulatory frameworks (e.g., FDA AI guidance, EU AI Act).*
- **Credibility Assessment Plans**: The pipeline generates detailed logs of the model architectures, training data, and decision-making logic used during the generation and ranking of molecules.
- **Human-in-the-Loop Validation**: The system is designed to provide "**Confidence Scores**" for its top candidates, flagging high-risk predictions for final review by qualified medicinal chemists.
mists.




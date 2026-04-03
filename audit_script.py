#!/usr/bin/env python3
"""Script to extract evaluate functions from notebooks."""

import json
import os
from pathlib import Path

# Mapping of notebooks to problems
NOTEBOOK_TO_PROBLEMS = {
    "autocorrelation_problems.ipynb": [
        ("analysis/first_autocorr_ineq", "evaluate_sequence", 4),
        ("analysis/second_autocorr_ineq", "evaluate_sequence_1", 11),
        ("analysis/third_autocorr_ineq", "evaluate_sequence_2", 17),
        ("analysis/first_autocorrelation_inequality", "final_robust", 21),
    ],
    "classical_inequalities.ipynb": [
        ("analysis/hausdorff_young_inequality", None, None),
        ("analysis/young_convolution_inequality", None, None),
        ("analysis/gagliardo_nirenberg_inequality", None, None),
    ],
    "difference_bases.ipynb": [("number_theory/difference_bases", None, None)],
    "edges_vs_triangles.ipynb": [("combinatorics/edges_vs_triangles", None, None)],
    "flat_polynomials.ipynb": [("analysis/flat_polynomials", None, None)],
    "imo_2025_p6.ipynb": [("combinatorics/imo_2025_p6", None, None)],
    "kakeya_needle_2d.ipynb": [("geometry/kakeya_needle_2d", None, None)],
    "kakeya_needle_3d.ipynb": [("geometry/kakeya_needle_3d", None, None)],
    "kissing_cylinders.ipynb": [("geometry/kissing_cylinders", None, None)],
    "no_5_on_a_sphere.ipynb": [("geometry/no_5_on_sphere", None, None)],
    "ovals_problem.ipynb": [("geometry/ovals_problem", None, None)],
    "packing_unit_cubes.ipynb": [("geometry/packing_unit_cubes", None, None)],
    "prime_number_theorem.ipynb": [("number_theory/prime_number_theorem", None, None)],
    "ring_loading_problem.ipynb": [("combinatorics/ring_loading_problem", None, None)],
    "sphere_packing_uncertainty_principles.ipynb": [("analysis/sphere_packing_uncertainty", None, None)],
    "spherical_t_designs.ipynb": [("geometry/spherical_t_design_n24_t7", None, None)],
    "sums_differences_problems.ipynb": [
        ("combinatorics/sums_differences", None, None),
        ("combinatorics/cap_set", None, None),
    ],
    "tammes_problem.ipynb": [
        ("geometry/tammes_n14", None, None),
        ("geometry/tammes_n24", None, None),
    ],
    "the_2d_moving_sofa.ipynb": [("geometry/moving_sofa_2d", None, None)],
    "the_3d_moving_sofa.ipynb": [("geometry/moving_sofa_3d", None, None)],
    "thomson_problem.ipynb": [("geometry/thomson_n32", None, None)],
}

def extract_code_cells(notebook_path):
    """Extract all code cells from a notebook."""
    with open(notebook_path, 'r') as f:
        nb = json.load(f)
    
    code_cells = []
    for i, cell in enumerate(nb.get('cells', [])):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            code_cells.append((i, source))
    
    return code_cells

def main():
    notebooks_dir = Path("notebooks")
    
    for notebook_name, problems in NOTEBOOK_TO_PROBLEMS.items():
        notebook_path = notebooks_dir / notebook_name
        
        if not notebook_path.exists():
            print(f"❌ Notebook not found: {notebook_name}")
            continue
        
        print(f"\n{'='*80}")
        print(f"📓 {notebook_name}")
        print(f"{'='*80}")
        
        try:
            code_cells = extract_code_cells(notebook_path)
            print(f"Found {len(code_cells)} code cells")
            
            # Print each code cell with its index
            for idx, source in code_cells:
                print(f"\n--- Cell {idx} ---")
                # Print first few lines
                lines = source.split('\n')[:5]
                for line in lines:
                    print(line)
                if len(source.split('\n')) > 5:
                    print("...")
                    
        except Exception as e:
            print(f"❌ Error processing: {e}")

if __name__ == "__main__":
    main()

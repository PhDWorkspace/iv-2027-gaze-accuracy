# IEEE IV 2027: Towards Reliable Gaze Supervision for Autonomous Driving

Double-blind submission draft (IEEE conference template, 6 pages expected, max. 8 with page charges;
deadline 2026-11-15 23:59 AWST).

- `main.tex`: entry point (pdfLaTeX + BibTeX; Overleaf default). Red `\todo{}` notes mark open items.
- `sections/`: one file per section.
- `figures/`: generated figure PDFs plus the plotted values (`*_data.csv`).
- `scripts/make_section6.py`: regenerates the four-driver offset figure and recording/day-transfer table from the frozen, audited evaluation snapshot: `python scripts/make_section6.py` (pandas, matplotlib). See `evals/06_transfer_to_driving.md` for the preserved benchmark definitions and audit. The detailed linear/velocity table uses the same expanded four-driver benchmark; historical runs remain available for provenance.
- `scripts/make_section4.py /home/william/data`: refreshes raw scene and participant summaries; `make_dataset_composition.py` refreshes coverage. Both read the dataset without changing it.
- `scripts/make_figures.py` and `scripts/make_tables.py`: earlier figure/table generators; the current manuscript uses the section-specific generators and the controlled-distance illustration described in `data/illustration/distance_baseline/METHODS.md` under the dataset root.
- `literature/`: git submodule of `phd-literature`, the only source of the bibliography. `references.bib` and `bib_short.def` in the root are generated copies for Overleaf (`scripts/sync_bib.sh`; see `LITERATURE.md`).
- `planning/STORYBOARD.md`: storyboard, outline, RQ-to-evidence map, figure plan and open items.

Participants are pseudonymised P1–P11 (mapping in `scripts/make_section5.py`). The four drivers retain P1, P2, P6 and P8 throughout.

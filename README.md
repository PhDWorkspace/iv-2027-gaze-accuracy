# IEEE IV 2027: Towards Reliable Gaze Supervision for Autonomous Driving

Double-blind submission draft (IEEE conference template, 6 pages expected, max. 8 with page charges;
deadline 2026-11-15 23:59 AWST).

- `main.tex`: entry point (pdfLaTeX + BibTeX; Overleaf default). Red `\todo{}` notes mark open items.
- `sections/`: one file per section.
- `figures/`: generated figure PDFs plus the plotted values (`*_data.csv`).
- `scripts/make_figures.py`: regenerates Figs. 3 and 4 from the saved evaluation outputs:
  `python scripts/make_figures.py /home/william/data` (needs pandas, matplotlib).
- `scripts/make_tables.py`: regenerates Tables I and II (`figures/tab_*.tex`) from the same outputs:
  `python scripts/make_tables.py /home/william/data` (standard library only).
- `literature/`: git submodule of `phd-literature`, the only source of the bibliography. `references.bib` and `bib_short.def` in the root are generated copies for Overleaf (`scripts/sync_bib.sh`; see `LITERATURE.md`).
- `planning/STORYBOARD.md`: storyboard, outline, RQ-to-evidence map, figure plan and open items.

Participants are pseudonymised (P1–P6); the mapping is in `scripts/make_figures.py` only.

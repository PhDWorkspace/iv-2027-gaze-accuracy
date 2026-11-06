# Bibliography: the `literature/` submodule and its synced copies

The single source of the paper's bibliography is the shared literature repository
[`PhDWorkspace/phd-literature`](https://github.com/PhDWorkspace/phd-literature). It is included as a git submodule at
`literature/`.

Overleaf's GitHub sync does not include submodules, so the paper compiles from two **generated copies** in the repo
root:

| File | Generated from | Used in `main.tex` |
|---|---|---|
| `references.bib` | `literature/bib/references.bib` | `\bibliography{references}` |
| `bib_short.def` | `literature/bib/bib_short.def` | `\input{bib_short.def}` |

Both copies start with a `% GENERATED … do not edit` line. **Never edit them by hand.** They are overwritten by
`scripts/sync_bib.sh`.

## Clone

```bash
git clone --recurse-submodules git@github.com:PhDWorkspace/iv-2027-gaze-accuracy.git
git submodule update --init          # for an existing clone without literature/
```

## Adding or fixing a reference

1. **Edit only in `phd-literature`.** The `literature/` folder is a full clone of it, or use a separate clone.
2. **Follow the BibTeX skill**, `literature/skills/bibtex_skill_venue_macros.md`:
   - verify against official publisher or proceedings metadata, not Google Scholar;
   - use the citation-key format `firstauthorYearKeyword`;
   - reuse a venue macro `{\macro{}}` that exists in **both** `bib_long.def` and `bib_short.def`, or add it to both;
   - invent no metadata (omit unverifiable fields);
   - keep existing keys unchanged.
3. **Log the addition** in `literature/bib/bibtex_verification.md`: key, status, sources and version decisions.
4. **Commit and push** the literature repo.
5. **In the paper repo**, update the submodule and regenerate the copies:

   ```bash
   git submodule update --remote literature
   scripts/sync_bib.sh
   git add literature references.bib bib_short.def
   git commit -m "Update bibliography from phd-literature"
   ```

6. **Compile** and check that no citation is undefined.

## Checking for drift

```bash
scripts/sync_bib.sh --check    # exit 1 and "OUT OF SYNC" if a root copy differs from literature/
```

Run it before committing paper changes that touch citations. If it reports drift, someone edited a root copy or
forgot to sync. Fix the reference in `phd-literature`, then sync again.

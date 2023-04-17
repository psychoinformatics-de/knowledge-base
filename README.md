# The PsyInf Knowledge Base

[![Documentation Status](https://readthedocs.org/projects/psyinf-knowledge-base/badge/?version=latest&style=for-the-badge)](https://knowledge-base.psychoinformatics.de/?badge=latest)

The actual knowledge is in the `kbi/` directory. The knowledge base can be
rendered in HTML format by running `make html` in the root of the repository
(requires Sphinx).

## Adding a knowledge base item (KBI)

- Create a new subdirectory in `kbi/` with a zero-padded integer name
  (length-4) that matches the successor of the "highest" present directory
  (check active PRs for possible conflicts)
- Pick the best matching template from the `protoypes/` directory, and copy it
  into the new subdirectory as `index.rst`
- Edit as necessary and propose a PR


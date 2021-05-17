# EOSC-PERF Frontend

## Instructions
To generate the documentation:
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Go to `docs/`
1. (Optional) Run `make clean`
1. Run `make html`

Steps to regenerate documentation:
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Go to `docs/`
1. (Optional) Run `make clean`
1. Run `sphinx-apidoc -fo source ../eosc_perf`
1. Move 'Module contents' to the top of the .rst files, under title and main description   
1. Run `make html`

To run tests (requires virtual environment):
1. Enable the virtual environment: `. ./venv/bin/activate`
1. Run `pip install tox`
1. Run `tox` (it should install test requirements automatically)

Tips:
- To enable debug mode, set `EOSC_PERF_DEBUG=true` in the `.env`


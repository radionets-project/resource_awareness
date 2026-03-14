# AKPIK Workshop | Resource-Aware Deep Learning: Tracking Energy Consumption in Scientific AI Applications

This repository contains all files for the DPG Spring Meeting 2026 AKPIK Workshop
*Resource-Aware Deep Learning: Tracking Energy Consumption in Scientific AI Applications*.


## Slides

You can find the slides for the presentation inside the slides directory. Before building the slides
with the provided `Makefile`, make sure to install the pygments style located in `slides/pygments_style`
using pip. Then call `make` inside the slides directory.


## Hands-on Session

To participate in the hands-on session, make sure to install the virtual environment we provide
in this repository, e.g. using `uv` or `conda/mamba`:
```
$ uv pip install -r requirements.txt
$ mamba env create --file=environment.yml
```

The repository contains two notebooks for the hands-on session. `resource_awareness.ipynb` contains a template
for the tasks during the session, `resource_awareness_solution.ipynb` contains the solution to the tasks.
The notebooks will teach you *one* way to track the emissions of your code/deep-learning models.

Additionally, we provide a small script `visualise.py` which will allow you to visualise your results
using [STREP](https://github.com/raphischer/strep).

# continuity

/!\ This project is being re-written. It is not functionnal at the moment, but will be soon. The objective is to make clear the different important parts of the code, and highlight the results and the different ways of testing the algorithm for spatiotemporal continuity.

## What is this repository for?

All that surrounds my internship at IMT-Atlantic. 

See my [internship report.](https://perso.ens-lyon.fr/guillaume.duboc/files/Rapport%20de%20Stage%20L3.pdf)

## Build

`pip install -r requirements.txt` should install all the needed dependencies.

## Architecture

- cache: Preprocessed datasets that don’t need to be re-generated every time you perform an analysis.
- config: Configuration settings for the project
- data: Raw data files.
- munge: Preprocessing data munging code, the outputs of which are put in cache.
- src: Statistical analysis scripts.
- doc: Documentation written about the analysis.
- graphs: Graphs created from analysis.
- logs: Output of scripts and any automatic logging.
- profiling: Scripts to benchmark the timing of the code.
- reports: Output reports and content that might go into reports such as tables.
- tests: Unit tests and regression suite for the code.


## Dependencies

- tensorflow
- keras
- pygame, Pillow for creating and processing animation dataset
- bokeh for data visualisation

# Long-term field experiment Westerfeld

[![code style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

Accompanying [Python](https://www.python.org) source code repository for the data set
"Long-term field experiment Westerfeld". This source code repository contains basic usage instructions, validation
source code for quality assurance of the data set, and some examples for the actual use of the data set.

## Getting started

The following few steps are necessary to get started.

### Get the source code repository

Clone the source code repository with [Git](https://www.git-scm.com):
```
git clone https://github.com/laschuet/long-term_field_experiment_westerfeld.git
```

Alternatively, [download](https://github.com/laschuet/long-term_field_experiment_westerfeld/archive/refs/heads/main.zip)
and unzip the source code repository as a file.

### Install Python dependencies

An installation of Python 3 is required.

All Python dependencies for this source code repository are listed in the file [`requirements.txt`](requirements.txt).

Create a new virtual environment in the root directory of this source code repository:
```
python3 -m venv .venv
```

Activate the new environment:
```
source .venv/bin/activate
```

Install requirements:
```
python3 -m pip install -r requirements.txt
```

Alternatively, your favorite IDE might also handle the previous steps.

### Get the data set

Get the data set from the BonaRes Repository for Soil and Agricultural Research Data.

Move the data set into the root of this source code repository, i.e., the data set should be located next to this
README.

## Examples

There are (TODO: specify number) examples.

```
python3 examples/main.py
```

## Validation

There a some source code files in the [`validation`](validation) directory.
We have used these source code files to compare the raw data set with the final data set created after the
transformation for database storage purposes. We only provide these source code files for documentation purposes and to
ensure traceability and transparency. It is not possible to run these source code files on your end because we cannot
supply the raw data.

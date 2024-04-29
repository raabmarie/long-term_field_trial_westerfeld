# Long-term field experiment Westerfeld

[![code style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

Usage notes for the data set "Long-term field experiment Westerfeld".

## Getting started

### Configuration

Copy the example configuration file [`config.sample.toml`](config.sample.toml) to the new main configuration file `config.toml`:
```
cp config.sample.toml config.toml
```
Adjust the settings within the main configuration file `config.toml` according to your needs.

By default, it is assumed that the data set is placed in the root directory of this source code repository.
However, you can change its location via the main configuration file `config.toml` that you created previously.

### Installation

All dependencies are listed in the file [`requirements.txt`](requirements.txt).
Create a new virtual environment in the root directory of this repository:
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

### Run

```
python3 main.py
```


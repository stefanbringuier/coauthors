<!-- These are examples of badges you might want to add to your README:
     please update the URLs accordingly

[![Built Status](https://api.cirrus-ci.com/github/<USER>/coauthors.svg?branch=main)](https://cirrus-ci.com/github/<USER>/coauthors)
[![Coveralls](https://img.shields.io/coveralls/github/<USER>/coauthors/main.svg)](https://coveralls.io/r/<USER>/coauthors)
[![PyPI-Server](https://img.shields.io/pypi/v/coauthors.svg)](https://pypi.org/project/coauthors/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/coauthors.svg)](https://anaconda.org/conda-forge/coauthors)
[![Twitter](https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter)](https://twitter.com/coauthors)
-->

[![ReadTheDocs](https://readthedocs.org/projects/coauthors/badge/?version=latest)](https://coauthors.readthedocs.io/en/stable/) [![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/) [![Monthly Downloads](https://pepy.tech/badge/coauthors/month)](https://pepy.tech/project/coauthors)

# coauthors

> Generate a DataFrame or file of coauthors for proposals.

This is a very small package that uses [scholarly](https://github.com/scholarly-python-package/scholarly) to grab coauthors of papers who have google scholar profiles. It is probably most useful when putting together a list of collaborators for proposal writing.


## Usage

The intend way to use this package is via the command line. For example:

```shell
python -m coauthors.grab -n "Stefan Bringuier" -o "my_coauthors.csv"
```
<!-- pyscaffold-notes -->

## Note

This project has been set up using PyScaffold 4.4. For details and usage
information on PyScaffold see https://pyscaffold.org/.

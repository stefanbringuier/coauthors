from pathlib import Path
from tempfile import NamedTemporaryFile

from coauthors.grab import main, query_author_by_id, query_author_by_name

# import pytest


__author__ = "Stefan Bringuier"
__copyright__ = "Stefan Bringuier"
__license__ = "MIT"


def test_query_author_by_name():
    """API Tests"""
    name = "Stefan Bringuier"
    author = query_author_by_name(name)
    assert author["name"] == name


def test_query_author_by_id():
    name = "Stefan Bringuier"
    gid = "MhJTimgAAAAJ"
    author = query_author_by_id(gid)
    assert author["name"] == name
    assert author["scholar_id"] == gid


def test_main():
    """CLI Tests"""
    f = NamedTemporaryFile()
    main(["-n", "Stefan Bringuier", "-o", f.name])
    path = Path(f.name)
    assert path.is_file() is True

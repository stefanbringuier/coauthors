import argparse
import logging
import sys
from pathlib import Path

import pandas as pd
from scholarly import ProxyGenerator, scholarly

from coauthors import __version__

__author__ = "Stefan Bringuier"
__copyright__ = "Stefan Bringuier"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from coauthors.grab import ...`,
# when using this Python module as a library.

# TODO: Determine if needed
pg = ProxyGenerator()
success = pg.FreeProxies()
scholarly.use_proxy(pg)


def author_names(query_result):
    """Iterate over author(s) from scholarly query."""
    author_options = {}
    i = 1
    while True:
        try:
            item = next(query_result)
            author_options[i] = item
            i += 1
        except StopIteration:
            break
    return author_options


def confirm_author_name(author_options) -> int:
    """Provides option to check if query by name is correct.

    Args:
      author_options (list): list of authors with the queried names.

    Returns:
      selected (int)
    """
    if len(author_options.items()) == 1:
        selected = 1
    else:
        print("Confirm author name")
        for k, v in author_options.items():
            name = v["name"]
            affiliation = v["affiliation"]
            gid = v["scholar_id"]
            edomain = v["email_domain"]
            print(f"{k}: {name}, {affiliation}, {edomain}, scholar id: {gid}")
        selected = int(input("Entry number id: "))

    return selected


def query_author_by_name(name, institute=None):
    """Use author name and/or intitute to query."""
    if institute:
        query = ", ".join(name, institute)
    else:
        query = name
    names = author_names(scholarly.search_author(query))
    idkey = confirm_author_name(names)
    return names[idkey]


def query_author_by_id(scholar_id):
    """Use google scholar id to query."""
    return scholarly.search_author_id(scholar_id)


def get_coauthors(author) -> pd.DataFrame:
    """Grab the coauthors for a scholarly returned author."""
    list_of_coauthors = scholarly.fill(author, sections=["coauthors"])

    dfs = []
    for coauth in list_of_coauthors["coauthors"]:
        name = coauth["name"]
        affiliation = coauth["affiliation"]
        df = pd.DataFrame(data={"Name": [name], "Affiliation": [affiliation]})
        dfs.append(df)

    return pd.concat(dfs)


def save_csv(outfile, author):
    """Save coauthor list to csv file

    Args:
      outfile (str): path to output file.
      author (dict): scholarly result for author.
    """
    df: pd.DataFrame = get_coauthors(author)
    filepath = Path(outfile)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Generate DataFrame of file of coauthors for proposals."
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        help="Author name",
    )
    parser.add_argument(
        "-inst",
        "--institution",
        dest="institute",
        default=None,
        type=str,
        help="Authors institution.",
    )
    parser.add_argument(
        "-id",
        "--google-scholar-id",
        dest="gid",
        default=None,
        type=str,
        help="Google scholar id. See squence\
              after scholar.google.com/citations?user=... for id.",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        dest="outfile",
        default="coauthors.csv",
        type=str,
        help="Path and name of file for saving coauthors.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"coauthors {__version__}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing :func:`query_author_by_id` or :func:`query_author_by_name` to
    be called with string arguments in a CLI fashion.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)

    setup_logging(args.loglevel)
    _logger.debug("Querying google scholar...")

    if args.gid:
        author = query_author_by_id(args.gid)
    else:
        author = query_author_by_name(args.name, institute=args.institute)

    save_csv(args.outfile, author)

    _logger.info("Finished.")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m coauthors.grab
    #
    run()

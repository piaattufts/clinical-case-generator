"""Rebuild the canonical bibliographic table from import batches."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["normalize", *sys.argv[1:]])

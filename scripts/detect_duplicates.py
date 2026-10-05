"""Flag duplicate candidates without merging records."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["duplicates", *sys.argv[1:]])

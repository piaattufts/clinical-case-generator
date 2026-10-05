"""Queue INCLUDE and MAYBE records for full-text screening."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["prepare-fulltext", *sys.argv[1:]])

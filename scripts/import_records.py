"""Import one bibliographic export into an interim batch."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["import-records", *sys.argv[1:]])

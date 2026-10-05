"""Calculate calibration agreement without editing reviewer files."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["agreement", *sys.argv[1:]])

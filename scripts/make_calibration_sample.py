"""Draw the stratified calibration sample."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["calibration", *sys.argv[1:]])

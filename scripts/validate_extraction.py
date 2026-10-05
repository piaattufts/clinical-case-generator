"""Validate screening and extraction integrity."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["validate", *sys.argv[1:]])

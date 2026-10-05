"""Derive PRISMA counts from the current data files."""

import sys

import review_bootstrap  # noqa: F401
from inthewild_review.cli import main

if __name__ == "__main__":
    main(["prisma", *sys.argv[1:]])

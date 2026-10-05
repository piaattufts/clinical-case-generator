"""Cohen's kappa, including collapsed INCLUDE/MAYBE and zero-cell cases."""

from __future__ import annotations

import pytest

from inthewild_review.agreement import (
    COLLAPSED_CATEGORIES,
    cohens_kappa,
    collapse_decision,
    confusion_matrix,
    percentage_agreement,
)
from inthewild_review.schemas import SCREENING_DECISIONS


def test_cohens_kappa_matches_a_hand_calculated_two_by_two() -> None:
    pairs = [("YES", "YES")] * 20 + [("YES", "NO")] * 5 + [("NO", "YES")] * 10 + [("NO", "NO")] * 15
    result = cohens_kappa(pairs, ("YES", "NO"))
    assert result["n"] == 50
    assert result["po"] == 0.7
    assert result["pe"] == 0.5
    assert result["kappa"] == pytest.approx(0.4)


def test_three_category_kappa_keeps_maybe_separate_from_collapsed_agreement() -> None:
    three_way = [("INCLUDE", "MAYBE"), ("MAYBE", "INCLUDE"), ("EXCLUDE", "EXCLUDE")]
    result = cohens_kappa(three_way, SCREENING_DECISIONS)
    assert result["po"] == 1 / 3
    assert result["kappa"] == 0
    matrix = confusion_matrix(three_way, SCREENING_DECISIONS)
    assert matrix["MAYBE"]["INCLUDE"] == 1
    assert matrix["INCLUDE"]["MAYBE"] == 1
    assert matrix["EXCLUDE"]["EXCLUDE"] == 1
    collapsed_pairs = [(collapse_decision(left), collapse_decision(right)) for left, right in three_way]
    collapsed = cohens_kappa(collapsed_pairs, COLLAPSED_CATEGORIES)
    assert collapsed["po"] == 1
    assert collapsed["kappa"] == 1
    assert percentage_agreement(three_way) == 1 / 3
    assert percentage_agreement(collapsed_pairs) == 1


def test_zero_cells_and_undefined_kappa_do_not_raise() -> None:
    pairs = [("INCLUDE", "INCLUDE"), ("INCLUDE", "EXCLUDE")]
    result = cohens_kappa(pairs, SCREENING_DECISIONS)
    assert result["n"] == 2
    assert result["kappa"] == 0
    matrix = confusion_matrix(pairs, SCREENING_DECISIONS)
    assert matrix["MAYBE"]["MAYBE"] == 0
    perfect = [("INCLUDE", "INCLUDE"), ("INCLUDE", "INCLUDE")]
    undefined = cohens_kappa(perfect, SCREENING_DECISIONS)
    assert undefined["kappa"] is None
    assert "undefined" in str(undefined["note"])
    empty = cohens_kappa([], SCREENING_DECISIONS)
    assert empty["kappa"] is None
    assert empty["n"] == 0

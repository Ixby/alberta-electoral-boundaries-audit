"""Tests for submission_search.py — keyword detection and position classification.

Covers build_patterns() (7 configurations, fire/no-fire), classify_position()
(all 6 branches), and search_submissions() (end-to-end with fixture files).

These directly guard the audit's counter-claim against "no public support"
for the minority configurations.

Run from the repo root:
    python -m pytest tests/test_submission_search.py -v
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

import submission_search
from submission_search import build_patterns, classify_position, search_submissions


# ============================================================
# build_patterns — structure
# ============================================================


def test_build_patterns_returns_all_seven_keys():
    pats = build_patterns()
    assert set(pats.keys()) == {
        "airdrie_4way_split",
        "nolan_hill_cochrane",
        "rmh_banff_park",
        "olds_three_hills_didsbury",
        "chestermere_split",
        "red_deer_hybrids",
        "st_albert_sturgeon",
    }


def test_build_patterns_each_key_has_at_least_one_regex():
    for key, regs in build_patterns().items():
        assert len(regs) >= 1, f"{key} has no regex patterns"


# ============================================================
# build_patterns — fire / no-fire per configuration
# ============================================================


def _hits(key: str, text: str) -> bool:
    return any(r.search(text) for r in build_patterns()[key])


class TestAirdrie4waySplit:
    def test_fires_on_four_ridings(self):
        assert _hits("airdrie_4way_split", "The proposal splits the city of Airdrie into four ridings")

    def test_fires_on_dividing_airdrie(self):
        assert _hits("airdrie_4way_split", "Dividing Airdrie into four districts is harmful")

    def test_no_fire_benign_mention(self):
        assert not _hits("airdrie_4way_split", "Airdrie is a rapidly growing community")

    def test_no_fire_different_city(self):
        assert not _hits("airdrie_4way_split", "The proposal splits Calgary into four ridings")


class TestNolanHillCochrane:
    def test_fires_on_linked(self):
        assert _hits("nolan_hill_cochrane", "Nolan Hill should not be linked with Cochrane in one riding")

    def test_fires_on_reverse_order(self):
        assert _hits("nolan_hill_cochrane", "Cochrane and Nolan Hill make poor riding partners")

    def test_no_fire_cochrane_alone(self):
        assert not _hits("nolan_hill_cochrane", "Cochrane is a thriving foothills town")

    def test_no_fire_nolan_hill_alone(self):
        assert not _hits("nolan_hill_cochrane", "Nolan Hill is a Calgary neighbourhood")


class TestRmhBanffPark:
    def test_fires_rmh_then_banff(self):
        assert _hits("rmh_banff_park", "Rocky Mountain House and Banff should not be joined")

    def test_fires_banff_then_rmh(self):
        assert _hits("rmh_banff_park", "Banff National Park is far from Rocky Mountain House")

    def test_no_fire_rmh_alone(self):
        assert not _hits("rmh_banff_park", "Rocky Mountain House is a rural service centre")


class TestOldsThreeHillsDidsbury:
    def test_fires_olds_three_hills(self):
        assert _hits("olds_three_hills_didsbury", "Olds and Three Hills should not share a riding")

    def test_fires_three_hills_didsbury(self):
        assert _hits("olds_three_hills_didsbury", "Three Hills and Didsbury have very different communities")

    def test_fires_olds_didsbury(self):
        assert _hits("olds_three_hills_didsbury", "Olds is far from Didsbury and should not be combined")

    def test_no_fire_olds_alone(self):
        assert not _hits("olds_three_hills_didsbury", "Olds is a small agricultural service town")

    def test_no_fire_three_hills_alone(self):
        assert not _hits("olds_three_hills_didsbury", "Three Hills is located in Kneehill County")

    def test_no_fire_didsbury_alone(self):
        assert not _hits("olds_three_hills_didsbury", "Didsbury is a community in Mountain View County")


class TestChesteremereSplit:
    def test_fires_chestermere_split(self):
        assert _hits("chestermere_split", "splitting Chestermere with Calgary makes no sense")

    def test_fires_chestermere_calgary(self):
        assert _hits("chestermere_split", "merging Chestermere into Calgary is wrong")

    def test_no_fire_chestermere_alone(self):
        assert not _hits("chestermere_split", "Chestermere is a thriving lakeside municipality")


class TestRedDeerHybrids:
    def test_fires_red_deer_blackfalds(self):
        assert _hits("red_deer_hybrids", "Red Deer should not include Blackfalds")

    def test_fires_innisfail_red_deer(self):
        assert _hits("red_deer_hybrids", "Innisfail has nothing in common with Red Deer urban areas")

    def test_no_fire_red_deer_alone(self):
        assert not _hits("red_deer_hybrids", "Red Deer is Alberta's third-largest city")


class TestStAlbertSturgeon:
    def test_fires_st_albert_sturgeon(self):
        assert _hits("st_albert_sturgeon", "St. Albert and Sturgeon County are proposed together")

    def test_fires_sturgeon_st_albert(self):
        assert _hits("st_albert_sturgeon", "Sturgeon County and St. Albert have very different interests")

    def test_no_fire_st_albert_alone(self):
        assert not _hits("st_albert_sturgeon", "St. Albert is a small city north of Edmonton")


# ============================================================
# classify_position — all branches
# ============================================================


def test_classify_support_only():
    assert classify_position("I support and endorse this proposal") == "supporting"


def test_classify_oppose_only():
    assert classify_position("I oppose this and strongly disagree with the plan") == "opposing"


def test_classify_neutral():
    assert classify_position("The boundary runs along Highway 2 north of the river") == "neutral"


def test_classify_cannot_support_is_opposing():
    assert classify_position("I cannot support this proposal") == "opposing"


def test_classify_wont_support_is_opposing():
    assert classify_position("We won't support this boundary change") == "opposing"


def test_classify_will_not_support_is_opposing():
    assert classify_position("The community will not support this configuration") == "opposing"


def test_classify_problematic_terrain_is_neutral():
    # "problematic" no longer fires OPPOSE_WORDS (removed to prevent false positives)
    assert classify_position("The problematic terrain makes access difficult") == "neutral"


def test_classify_ambiguous_leaning_oppose():
    # Two oppose words, one support word
    result = classify_position(
        "I oppose this proposal and object to it, though I accept one aspect"
    )
    assert result == "ambiguous-leaning-oppose"


def test_classify_ambiguous_leaning_support():
    # Three support words, one oppose word
    result = classify_position(
        "I support and endorse and recommend this boundary, but I have concerns"
    )
    assert result == "ambiguous-leaning-support"


def test_classify_ambiguous_equal():
    # Equal support and oppose
    result = classify_position("I support this but I oppose it too")
    assert result == "ambiguous"


# ============================================================
# search_submissions — end-to-end integration
# ============================================================


def test_search_submissions_finds_hits(tmp_path, monkeypatch):
    """search_submissions() locates keyword hits in fixture .txt files."""
    (tmp_path / "EBC-2025-2-0001.txt").write_text(
        "The commission should not split the city of Airdrie into four ridings. "
        "Dividing Airdrie this way is wrong.",
        encoding="utf-8",
    )
    (tmp_path / "EBC-2025-2-0002.txt").write_text(
        "Nolan Hill should remain separate from Cochrane.",
        encoding="utf-8",
    )
    (tmp_path / "EBC-2025-2-0003.txt").write_text(
        "Thank you for the opportunity to comment on the boundaries.",
        encoding="utf-8",
    )

    monkeypatch.setattr(submission_search, "TEXT", tmp_path)

    log = []
    rows, totals, pos_counts, n_searched = search_submissions(log)

    assert n_searched == 3
    assert len(rows) == 2, f"Expected 2 hit rows, got {len(rows)}"

    hit_ids = {r["submission_id"] for r in rows}
    assert "EBC-2025-2-0001" in hit_ids
    assert "EBC-2025-2-0002" in hit_ids
    assert "EBC-2025-2-0003" not in hit_ids

    assert totals.get("airdrie_4way_split", 0) >= 1
    assert totals.get("nolan_hill_cochrane", 0) >= 1


def test_search_submissions_no_hits_when_empty(tmp_path, monkeypatch):
    """Empty text directory → zero rows, zero totals."""
    monkeypatch.setattr(submission_search, "TEXT", tmp_path)

    log = []
    rows, totals, pos_counts, n_searched = search_submissions(log)

    assert n_searched == 0
    assert rows == []
    assert all(v == 0 for v in totals.values())


def test_search_submissions_position_recorded(tmp_path, monkeypatch):
    """position_on_mentioned is populated for hit rows."""
    (tmp_path / "EBC-2025-1-0010.txt").write_text(
        "I oppose splitting Chestermere with Calgary.",
        encoding="utf-8",
    )
    monkeypatch.setattr(submission_search, "TEXT", tmp_path)

    log = []
    rows, _, _, _ = search_submissions(log)

    assert len(rows) == 1
    assert rows[0]["position_on_mentioned"] in {
        "supporting", "opposing", "neutral",
        "ambiguous", "ambiguous-leaning-support", "ambiguous-leaning-oppose",
    }

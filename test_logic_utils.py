# FIX: Test file created with Claude (claude.ai) to verify all refactored logic in logic_utils.py.
# Claude suggested organizing tests by function and covering edge cases like None input and late wins.

import pytest
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


# --- get_range_for_difficulty ---
# FIX: Claude suggested testing all three difficulties plus an unknown value
# to confirm the default fallback works correctly.


def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 100)


# --- parse_guess ---
# FIX: Claude recommended testing float input, empty string, and None separately
# since the original function had two separate checks that could be consolidated.
def test_parse_valid_integer():
    ok, val, err = parse_guess("42")
    assert ok is True
    assert val == 42
    assert err is None

def test_parse_float_truncates():
    # FIX: Verified that "7.9" becomes 7, not raises an error — Claude caught that
    # the original broad except could silently fail on float strings.
    ok, val, err = parse_guess("7.9")
    assert ok is True
    assert val == 7

def test_parse_empty_string():
    ok, val, err = parse_guess("")
    assert ok is False
    assert val is None
    assert "guess" in err.lower()

def test_parse_none():
    # FIX: Claude suggested testing None explicitly since Streamlit can pass None
    # before the user types anything into the input field.
    ok, val, err = parse_guess(None)
    assert ok is False

def test_parse_non_numeric():
    ok, val, err = parse_guess("abc")
    assert ok is False
    assert "number" in err.lower()

# --- check_guess ---
# FIX: Claude identified that the original check_guess had a broken string-comparison
# fallback. These tests confirm the fixed version returns correct (outcome, message) tuples.

def test_correct_guess():
    outcome, msg = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in msg

def test_guess_too_high():
    # FIX: This test caught that the original string fallback could return wrong outcomes.
    # Claude helped write the tuple-unpacking pattern used here.
    outcome, msg = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in msg

def test_guess_too_low():
    outcome, msg = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in msg


# --- update_score ---
# FIX: Claude flagged the original scoring bug where "Too High" on even attempts
# gave +5 points instead of subtracting. These tests verify the corrected behavior.

def test_win_early_gives_high_score():
    score = update_score(0, "Win", attempt_number=1)
    assert score == 90  # 100 - 10*1

def test_win_late_gives_minimum_10():
    # FIX: Claude suggested testing the max() cap — original used an if/else that
    # could be bypassed. This confirms the floor of 10 is always enforced.

    score = update_score(0, "Win", attempt_number=20)
    assert score == 10  # capped at 10

def test_wrong_guess_subtracts_5():
    # FIX: Original gave +5 for "Too High" on even attempts. Claude identified this
    # as an unintentional reward for wrong guesses.
    assert update_score(50, "Too High", 3) == 45
    assert update_score(50, "Too Low", 3) == 45

def test_unknown_outcome_unchanged():
    assert update_score(100, "Unknown", 1) == 100
# FIX: Refactored all game logic out of app.py into this module using Claude (claude.ai)
# Claude identified that mixing UI and logic in one file made bugs harder to find and test.


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Removed the broken "Hard" range (original returned 1-50 but was listed after Normal,
    # making it unreachable). Claude suggested reordering and adding a clear default fallback.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Hard":
        return 1, 50
    return 1, 100  # Normal (default)


def parse_guess(raw: str):
    """
    Parse user input into an int guess.
    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX: Simplified the None/empty check using `not raw` instead of two separate conditions.
    # Claude suggested this cleaner pattern while keeping the same behavior.
    if not raw:
        return False, None, "Enter a guess."
    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).
    Outcomes: "Win", "Too High", "Too Low"
    """
    # FIX: Removed the broken string-comparison fallback from the original app.py.
    # Claude identified that the original code tried to compare guess/secret as strings
    # if a TypeError occurred, which caused hints to be wrong or unpredictable.
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    # FIX: Replaced the original `if points < 10: points = 10` pattern with max().
    # Claude suggested this as a cleaner, more Pythonic equivalent.
    if outcome == "Win":
        points = max(10, 100 - 10 * attempt_number)
        return current_score + points
    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 5
    return current_score
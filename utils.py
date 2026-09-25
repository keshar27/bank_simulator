"""
utils.py
Shared input validation and formatting helpers used across the app.
"""


def get_float(prompt, allow_negative=False, allow_zero=True):
    """Repeatedly asks for a valid float (used for money amounts)."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  Invalid input. Please enter a numeric amount.")
            continue

        if not allow_negative and value < 0:
            print("  Negative amounts are not allowed.")
            continue
        if not allow_zero and value == 0:
            print("  Amount must be greater than zero.")
            continue

        return round(value, 2)


def get_nonempty_str(prompt):
    """Repeatedly asks for a non-empty string (used for names, account IDs)."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty.")


def get_choice(prompt, valid_choices):
    """Asks for input restricted to a fixed set of valid choices (case-insensitive)."""
    valid_lower = [c.lower() for c in valid_choices]
    while True:
        value = input(prompt).strip().lower()
        if value in valid_lower:
            return value
        print(f"  Please enter one of: {', '.join(valid_choices)}")


def format_currency(amount):
    """Formats a number as a currency string, e.g. 1234.5 -> '$1,234.50'."""
    return f"${amount:,.2f}"


def pause():
    input("\nPress Enter to return to the menu...")


def print_header(title):
    print("\n" + "=" * 55)
    print(title.center(55))
    print("=" * 55)

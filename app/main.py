# Entry point for the CS 480 Final terminal application.

from app import queries

# Not a set design, just something that can get us started
MENU = """
=== CS 480 Final ===
1. Test database connection
0. Quit
"""


def test_connection_action():
    try:
        version = queries.ping()
        print(f"\nConnected. {version}")
    except Exception as e:
        print(f"\nConnection failed: {e}")



ACTIONS = {
    "1": test_connection_action,
}

# Not a set program flow, just a example flow
def main():
    while True:
        print(MENU)
        choice = input("> ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid choice.")
            continue
        action()


if __name__ == "__main__":
    main()
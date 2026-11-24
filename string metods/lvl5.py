from text_utils import normalize_text


def run():
    print("\nwelcome to level 5")
    print("normalizes a string:")
    print("1) removes junk chars like @, #, *")
    print("2) keeps letters, digits and . , ! ? : ; -")
    print("3) removes extra spaces")
    print("4) removes spaces before . , ! ? : ;")
    print("5) removes repeated punctuation")
    print("6) first letter upper, rest lower")

    t = "  ***hELLO   ,,,   wORLD!!!###  "

    print(
        "tests:"
        f"\ntest string: {t!r}"
        f"\nresult: {normalize_text(t)!r}"
    )

    s = input("\nstring: ")
    print(f"result: {normalize_text(s)}")

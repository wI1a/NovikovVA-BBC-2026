def normalize_text(text):
    s = ""

    for c in text:
        if c.isalnum() or c.isspace() or c in ".,!?:;-":
            s += c
        else:
            s += " "

    s = " ".join(s.split())

    for p in ".,!?:;":
        s = s.replace(" " + p, p)

    r = ""

    for c in s:
        if c in ".,!?:;" and r.endswith(c):
            continue
        r += c

    return r.strip().capitalize()


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

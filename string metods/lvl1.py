def run():
    t = "hElLo WoRlD"

    print("\nwelcome to level 1")
    print("methods: upper(), lower(), capitalize()")
    print("1) upper() - uppercase")
    print("2) lower() - lowercase")
    print("3) capitalize() - first letter upper, rest lower")

    print(
        "tests:"
        f"\ntest string: {t}"
        f"\n1) {t.upper()}"
        f"\n2) {t.lower()}"
        f"\n3) {t.capitalize()}"
    )

    print("\nenter string and method number separated by ', '")
    print("example: hello world, 1")
    p = input().rsplit(", ", 1)

    if len(p) != 2:
        print("error: incorrect input")
        return

    v, m = p

    if m == "1":
        print(f"result: {v.upper()}")
    elif m == "2":
        print(f"result: {v.lower()}")
    elif m == "3":
        print(f"result: {v.capitalize()}")
    else:
        print("error: no such method")

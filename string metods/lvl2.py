def run():
    t = "Very cool"

    print("\nwelcome to level 2")
    print("methods: find(), replace(), count()")
    print("1) find() - index of first match, -1 if not found")
    print("2) replace() - replaces all matches")
    print("3) count() - counts non-overlapping matches")

    print(
        "tests:"
        f"\ntest string: {t}"
        f"\n1) find 'cool': {t.find('cool')}"
        f"\n2) replace 'cool' with 'p': {t.replace('cool', 'p')}"
        f"\n3) count 'o': {t.count('o')}"
    )

    print("\nenter args separated by '; '")
    print("find: string; find; sub")
    print("replace: string; replace; old; new")
    print("count: string; count; sub")
    p = input().split("; ")

    if len(p) < 3:
        print("error: not enough args")
        return

    v, a = p[0], p[1]

    if a == "find":
        print(f"result: {v.find(p[2])}")

    elif a == "replace":
        if len(p) != 4:
            print("error: need old and new substrings")
            return
        print(f"result: {v.replace(p[2], p[3])}")

    elif a == "count":
        print(f"result: {v.count(p[2])}")

    else:
        print("error: no such method")

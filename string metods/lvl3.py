def run():
    t = "I study Python"
    w = ["I", "study", "Python"]

    print("\nwelcome to level 3")
    print("methods: split(), join()")
    print("1) split() - splits string into list")
    print("2) join() - joins list items with separator")

    print(
        "tests:"
        f"\ntest string: {t}"
        f"\n1) split(): {t.split()}"
        f"\ntest list: {w}"
        f"\n2) join() with '-': {'-'.join(w)}"
    )

    m = input("\nmethod num (1-2): ").strip()

    if m == "1":
        t = input("string: ")
        s = input("separator (enter - whitespace): ")
        r = t.split() if s == "" else t.split(s)
        print(f"result: {r}")

    elif m == "2":
        print("enter items separated by '; '")
        print("example: I; study; Python")
        i = input().split("; ")
        s = input("separator (enter - none): ")
        print(f"result: {s.join(i)}")

    else:
        print("error: no such method")

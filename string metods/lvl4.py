def run():
    d = "12345"
    a = "Hello"
    s = "   Hello world   "
    f = "Hello, {}! You are {} years old."

    print("\nwelcome to level 4")
    print("methods: isdigit(), isalpha(), strip(), format()")
    print("1) isdigit() - non-empty string of digits")
    print("2) isalpha() - non-empty string of letters")
    print("3) strip() - removes chars from both ends, whitespace by default")
    print("4) format() - fills values into template")

    print(
        "tests:"
        f"\n1) {d!r}.isdigit(): {d.isdigit()}"
        f"\n2) {a!r}.isalpha(): {a.isalpha()}"
        f"\n3) {s!r}.strip(): {s.strip()!r}"
        f"\n4) format(): {f.format('Anna', 20)}"
    )

    m = input("\nmethod num (1-4): ").strip()

    if m == "1":
        t = input("string: ")
        print(f"result: {t.isdigit()}")

    elif m == "2":
        t = input("string: ")
        print(f"result: {t.isalpha()}")

    elif m == "3":
        t = input("string: ")
        c = input("chars to strip (enter - whitespace): ")
        r = t.strip() if c == "" else t.strip(c)
        print(f"result: {r!r}")

    elif m == "4":
        print("enter template with {} or {0}, {1} etc")
        print("example: Hello, {}! You are {} years old.")
        t = input("template: ")

        print("enter values separated by '; '")
        print("example: Anna; 20")
        v = input().split("; ")

        try:
            print(f"result: {t.format(*v)}")
        except (IndexError, KeyError, ValueError) as e:
            print(f"error: {e}")
            print("check template and number of values")

    else:
        print("error: no such method")

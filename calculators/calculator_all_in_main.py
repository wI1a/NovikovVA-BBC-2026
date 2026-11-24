print("q to quit, = to start over")
a = None
while True:
    try:
        if a is None:
            s = input("\nfirst num: ")
            if s.lower() == 'q':
                break
            a = float(s)

        o = input("operator(+, -, *, /): ")
        if o.lower() == 'q':
            break
        if o == '=':
            a = None
            continue

        s = input("next num: ")
        if s.lower() == 'q':
            break
        b = float(s)

        if o == '+':
            a += b
        elif o == '-':
            a -= b
        elif o == '*':
            a *= b
        elif o == '/':
            if b == 0:
                print("error: division by zero")
                continue
            a /= b
        else:
            print("error: incorrect input")
            continue

        print(f"result: {a}")

    except ValueError:
        print("error: incorrect input")

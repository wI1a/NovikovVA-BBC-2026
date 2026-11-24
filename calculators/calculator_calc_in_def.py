def start_calculator():
    print("q to quit")
    while True:
        try:
            s = input("\nfirst num: ")
            if s.lower() == 'q':
                break
            a = float(s)

            o = input("operator(+, -, *, /): ")

            s = input("second num: ")
            b = float(s)

            if o == '+':
                print(f"result: {a + b}")
            elif o == '-':
                print(f"result: {a - b}")
            elif o == '*':
                print(f"result: {a * b}")
            elif o == '/':
                if b == 0:
                    print("error: division by zero")
                else:
                    print(f"result: {a / b}")
            else:
                print("error: incorrect input")

        except ValueError:
            print("error: incorrect input")

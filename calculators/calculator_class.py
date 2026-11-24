class Calculator:
    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b

    def run(self):
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
                    a = self.add(a, b)
                elif o == '-':
                    a = self.sub(a, b)
                elif o == '*':
                    a = self.mul(a, b)
                elif o == '/':
                    a = self.div(a, b)
                else:
                    print("error: incorrect input")
                    continue

                print(f"result: {a}")

            except ZeroDivisionError as e:
                print(f"error: {e}")
            except ValueError:
                print("error: incorrect input")


if __name__ == "__main__":
    calc = Calculator()
    calc.run()

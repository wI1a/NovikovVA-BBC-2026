import level1
import level2
import level3
import level4
import level5


L = {
    1: level1.run,
    2: level2.run,
    3: level3.run,
    4: level4.run,
    5: level5.run,
}


def main():
    print("hello! string methods program")

    try:
        c = int(input("level (1-5): "))
    except ValueError:
        print("error: incorrect input")
        return

    h = L.get(c)
    if h is None:
        print("error: no such level")
        return

    h()


if __name__ == "__main__":
    main()

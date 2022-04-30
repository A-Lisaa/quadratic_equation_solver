from solver import Equation


def file_test():
    with open("equations.txt", encoding="utf-8") as file:
        for line in file:
            eq = line.split("; ")
            equation = Equation(eq[0])
            answer = eq[1].split(" ")
            print(equation)
            print(*answer)


if __name__ == "__main__":
    file_test()

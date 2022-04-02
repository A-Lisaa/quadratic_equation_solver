from solver import print_solution, get_equation


def file_test():
    with open("equations.txt", encoding="utf-8") as file:
        for line in file:
            equation = line.split("; ")
            answer = equation[1].split(" ")
            print_solution(equation[0])
            print(*answer)


def input_test():
    equation = get_equation()
    print_solution(equation)


if __name__ == "__main__":
    file_test()

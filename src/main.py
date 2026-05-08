import determinant

def main():
    # Input
    matrix: list = []
    term = int(input("What level term is the system of equations you are planning to solve: "))

    for i in range(term):
        matrix.append(list(map(float, input(f"Enter the {i+1}st term equation's constants with each constant seperated by a space (A1 A2 A3...): ").split())))
            
    print(determinant.det(term, matrix))

if __name__ == "__main__":
    main()
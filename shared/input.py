def readfile(filename):
    print(f'Opening {filename}')

    with open(filename) as fin:
        return [line.strip() for line in fin.readlines()]

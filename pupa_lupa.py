import argparse


class Matrix:
    def __init__(self, file):
        """
        Reads matrix from a given file

        :param file: file variable to read from
        :return: returns a read matrix
        """
        line = file.readline()
        self.matrix = []
        while line != '':
            self.matrix.append([int(x) for x in line.split()])
            line = file.readline()

    def __len__(self):
        return len(self.matrix)


class DataScientist:
    def __init__(self):
        self._cash = 0
        self._hours = 0

    def do_works(self, filename1, filename2, func, worker):
        """
        Method describing a work process of a data-scientist

        :param filename1: name of matrix to calculate
        :param filename2: name of matrix to calculate
        :param func: type of calculation
        :param worker: who is doing the calculation
        """
        f1 = open(filename1, 'r')
        f2 = open(filename2, 'r')

        a = Matrix(f1)
        b = Matrix(f2)

        res = []
        for i in range(len(a)):
            res.append([])
            for j in range(len(a.matrix[0])):
                try:
                    res[i].append(func(a.matrix[i][j], b.matrix[i][j]))
                except IndexError:
                    res[i].append([])
                    print('Error! Matrices have different sizes.')

        print('Result of {name}\'s work:'.format(name=worker))
        for i in range(len(res)):
            print(' '.join(map(str, res[i])))

        self._hours += 1

        f1.close()
        f2.close()

    def take_salary(self, profit):
        """
        Method to request a data-scientist's salary

        :param profit: amount of salary
        """
        self._cash += profit

    @property
    def cash(self):
        return self._cash

    @property
    def hours(self):
        return self._hours


class Pupa(DataScientist):
    def do_work(self, filename1, filename2):
        """
        Method, specifying a work of Pupa data-scientist

        :param filename1: name of a matrix to calculate
        :param filename2: name of a matrix to calculate
        """
        super().do_works(filename1, filename2, lambda x, y: x+y, 'Pupa')


class Lupa(DataScientist):
    def do_work(self, filename1, filename2):
        """
        Method, specifying a work of Lupa data-scientist

        :param filename1: name of a matrix to calculate
        :param filename2: name of a matrix to calculate
        """
        super().do_works(filename1, filename2, lambda x, y: x-y, 'Lupa')


class Accountant:
    def __init__(self):
        self.pupa_payment = 100
        self.lupa_payment = 150

    def give_salary(self, worker):
        """
        Charges a salary of a given worker considering his payment

        :param worker: name of a worker
        """
        if isinstance(worker, Pupa):
            Pupa.take_salary(worker, self.lupa_payment * worker.hours)
        else:
            Lupa.take_salary(worker, self.pupa_payment * worker.hours)


def main():
    parser = argparse.ArgumentParser(description='Calculates a convolution of matrices')
    # here to add matrices to calculate
    parser.add_argument('matrix1', type=str, help='matrix 1')
    parser.add_argument('matrix2', type=str, help='matrix 2')
    parser.add_argument('matrix3', type=str, help='matrix 3')
    #
    args = parser.parse_args()

    pupa = Pupa()
    lupa = Lupa()
    accountant = Accountant()

    # here to write workers' day:
    pupa.do_work(args.matrix1, args.matrix2)
    pupa.do_work(args.matrix2, args.matrix3)
    lupa.do_work(args.matrix1, args.matrix2)
    lupa.do_work(args.matrix1, args.matrix3)
    accountant.give_salary(pupa)
    accountant.give_salary(lupa)
    # end of a day, checking for the workers' profit:
    print('Money earned by Pupa: {cash1}$\nMoney earned by Lupa: {cash2}$'.format(cash1=pupa.cash, cash2=lupa.cash))


if __name__ == '__main__':
    main()

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt


def conv(x, y):
    """
    Вычисляет свертку двух матриц

    :param x: оригинал
    :param y: ядро свертки, не должно быть больше оригинала

    :return: возвращает матрицу-карту признаков
    """
    c = []
    for i in range(len(x)-len(y)+1):
        c.append([])
        for j in range(len(x[0])-len(y[0])+1):
            c[i].append(calc(x[i:(i+len(y))], y, j))
    return c


def calc(subx, y, s_col):
    """
    Вычисляет "наложение" 2 двух матриц одного размера (элементы с одинаковыми индексами перемножаются и добавляются к
    результату)

    :param subx: "подматрица" Х того же размера, что и ядро
    :param y: матрица-ядро свертки
    :param s_col: index-number of column in matrix 'x'

    :return: возвращает сумму произведений элементов матриц
    """
    summ = 0
    for i in range(len(y)):
        for j in range(len(y[0])):
            summ += subx[i][s_col + j] * y[i][j]
    return summ


def read_matrix(file):
    """
    Читает матрицу из заданного файла

    :param file: файл, из которого нужно читать

    :return: возвращает матрицу
    """
    line = file.readline()
    matrix = []
    while line != '\n' and line != '':
        matrix.append([int(x) for x in line.split()])
        line = file.readline()
    return matrix


def write_matrix(file, matrix):
    """
    Записывает матрицу в заданный файл

    :param file: файл, в который нужно записать матрицу

    :param matrix: матрица
    """
    for i in range(len(matrix)):
        file.writelines(' '.join(map(str, matrix[i])) + '\n')


def is_correct(matrix):
    """
    Проверка матрицы на корректность

    :param matrix: матрица

    :return: результат (корректна матрица или нет)
    """
    count = len(matrix[0])
    for i in range(1, len(matrix)):
        if len(matrix[i]) != count:
            return False
    return True


def visualize(orig, core, result):
    """
    Визуализирует результат операции свертки

    :param orig: оригинал
    :param core: ядро
    :param result: карта признаков
    """
    fig = plt.figure(figsize=(10, 7))
    rows = 1
    cols = 3

    a = np.array(orig)
    b = np.array(core)
    res = np.array(result)

    fig.add_subplot(rows, cols, 1)
    plt.matshow(a, fignum=False)
    plt.axis('off')
    plt.title("Оригинал")

    fig.add_subplot(rows, cols, 2)
    plt.matshow(b, fignum=False)
    plt.axis('off')
    plt.title("Ядро")

    fig.add_subplot(rows, cols, 3)
    plt.matshow(res, fignum=False)
    plt.axis('off')
    plt.title("Карта признаков")

    plt.colorbar()
    plt.show()


def main():
    parser = argparse.ArgumentParser(description='Вычисляет свертку матриц')
    parser.add_argument('in_name', type=str, help='название входного файла')
    parser.add_argument('out_name', type=str, help='название выходного файла')
    parser.add_argument('show_res', type=bool, help='визуализировать результат?')
    args = parser.parse_args()

    f_in = open(args.in_name, 'r')
    f_out = open(args.out_name, 'w')

    a = read_matrix(f_in)
    b = read_matrix(f_in)

    err_stream = sys.stderr

    if not (is_correct(a) and is_correct(b)):
        err_stream.write('Матрица некорректна, измените ее')
        exit(-1)

    if len(b) > len(a) or len(b[0]) > len(a[0]):
        err_stream.write('ядро свертки больше оригинала. попробуйте изменить размер')
        exit(-2)

    res = conv(a, b)
    write_matrix(f_out, res)

    f_in.close()
    f_out.close()

    if args.show_res:
        visualize(a, b, res)


if __name__ == '__main__':
    main()

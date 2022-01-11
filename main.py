from cell import Cell
from copy import deepcopy
from field import Field
from random import randint
from tkinter import Tk, Canvas


WIDTH = 1600
HEIGHT = 900


def check_size(x, y):
    """
        Это процедура, которая проверяет введённые данные размера игрового поля
        На вход поступает 2 числовые переменные
    """

    if x > 100 or y > 100 or x < 8 or y < 8:
        print("Размеры данных переменных не могут быть меньше 8 и больше 100")
        exit()


def create_new_game(root, canvas, platform, x_size, y_size):
    """
            Это процедура, которая запускает основной игровой цикл
    """

    while True:
        canvas.delete("all")
        current_array_of_cells = deepcopy(platform.get_collection())
        check_platform_and_draw_cells(root, canvas, platform, x_size, y_size, current_array_of_cells)


def create_new_platform(x_size, y_size):
    """
            Это функция, которая создаёт основной массив всех клеток для игрового поля
            Возвращает массив всех клеток
    """

    array_of_all_cells = []  # массив всех клеток
    for i in range(x_size):
        array_of_cells = []  # одна из строк массива клеток
        for j in range(y_size):
            new_cell = Cell(randint(0, 1))
            array_of_cells.append(new_cell)

        array_of_all_cells.append(array_of_cells)

    return array_of_all_cells


def check_platform_and_draw_cells(root, canvas, platform, x_size, y_size, array):
    """
                Это процедура, которая проверяет вложенным циклом все клетки исходя из правил игры, вносит изменения
                в массив всех клеток, а также выводит на экран каждую живую клетку
    """

    for i in range(x_size):
        prev_y = i * (HEIGHT / y_size)
        for j in range(y_size):
            if array[i][j].get_condition():
                prev_x = j * (WIDTH / x_size)

                canvas.create_rectangle(prev_x, prev_y,
                                        prev_x + WIDTH / x_size, prev_y + HEIGHT / y_size,
                                        outline="black", fill="green"
                                        )  # прорисовка прямоугольников x1 y1 x2 y2

            count = 0  # количество соседей

            if i > 0:
                count += array[i - 1][j].get_condition()
                if j > 0:
                    count += array[i - 1][j - 1].get_condition()
                if j < y_size - 1:
                    count += array[i - 1][j + 1].get_condition()

            if i < x_size - 1:
                count += array[i + 1][j].get_condition()
                if j < y_size - 1:
                    count += array[i + 1][j + 1].get_condition()
                if j > 0:
                    count += array[i + 1][j - 1].get_condition()

            if 0 < j <= y_size - 1:
                count += array[i][j - 1].get_condition()
            if j <= y_size - 2:
                count += array[i][j + 1].get_condition()

            if count not in (2, 3):
                platform.get_collection()[i][j].set_condition(0)
            else:
                if count == 3:
                    platform.get_collection()[i][j].set_condition(1)

    root.update()  # обновление окна


def main():
    try:
        x_size = int(input("Write x:"))
        y_size = int(input("Write y:"))
    except ValueError:
        print("Похоже вы ввели не числа...")
        exit()

    check_size(x_size, y_size)

    root = Tk()
    root.geometry("1600x900+100+100")
    canvas = Canvas(root, width=1600, height=900, bg='black')
    canvas.pack()

    platform = Field(create_new_platform(x_size, y_size))  # инициализация нового игрового поля
    create_new_game(root, canvas, platform, x_size, y_size)  # запуск основого процесса игры


if __name__ == "__main__":
    main()
